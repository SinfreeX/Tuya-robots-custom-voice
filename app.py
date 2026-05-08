from __future__ import annotations

import base64
import concurrent.futures
import datetime as dt
import hashlib
import ipaddress
import json
import mimetypes
import os
import posixpath
import socket
import tarfile
import threading
import time
import traceback
import urllib.parse
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import tinytuya


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
STATE_PATH = ROOT / "state.json"
PACKAGES_DIR = ROOT / "packages"
LOGS_DIR = ROOT / "logs"
STATIC_DIR = ROOT / "static"

DEFAULT_CONFIG: dict[str, Any] = {
    "robot": {
        "device_id": "",
        "ip": "",
        "local_key": "",
        "protocol_version": 3.3,
        "voice_dp": 35,
        "language_dp": 36,
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8780,
        "public_ip": "auto",
    },
    "voice": {
        "default_source_folder": "",
        "language_id_min": 8,
        "language_id_max": 250,
        "listen_seconds": 150,
    },
}


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: Path, data: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    tmp.replace(path)


CONFIG = load_json(CONFIG_PATH, json.loads(json.dumps(DEFAULT_CONFIG)))
CONFIG_LOCK = threading.Lock()
STATE_LOCK = threading.Lock()
JOB_LOCK = threading.Lock()
CURRENT_JOB: dict[str, Any] | None = None
ACTIVE_PACKAGE: Path | None = None
ACTIVE_PACKAGE_LOCK = threading.Lock()


class MemoryLog:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._lines: list[str] = []
        LOGS_DIR.mkdir(exist_ok=True)
        self.file = LOGS_DIR / f"robot_voice_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    def add(self, message: str) -> None:
        stamp = dt.datetime.now().strftime("%H:%M:%S")
        line = f"[{stamp}] {message}"
        with self._lock:
            self._lines.append(line)
            self._lines = self._lines[-500:]
            with self.file.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        print(line, flush=True)

    def lines(self) -> list[str]:
        with self._lock:
            return list(self._lines)


LOG = MemoryLog()


def save_config() -> None:
    with CONFIG_LOCK:
        save_json(CONFIG_PATH, CONFIG)


def public_config() -> dict[str, Any]:
    cfg = json.loads(json.dumps(CONFIG))
    key = cfg.get("robot", {}).get("local_key", "")
    if key:
        cfg["robot"]["local_key_masked"] = "*" * max(0, len(key) - 4) + key[-4:]
    cfg.get("robot", {}).pop("local_key", None)
    return cfg


def ensure_robot_configured(require_ip: bool = True) -> None:
    robot = CONFIG.get("robot", {})
    missing = []
    if not robot.get("device_id"):
        missing.append("Device ID")
    if not robot.get("local_key"):
        missing.append("Local Key")
    if require_ip and not robot.get("ip"):
        missing.append("Robot IP")
    if missing:
        raise ValueError("Fill robot settings: " + ", ".join(missing))


def checksum(data: bytes) -> int:
    return sum(data) & 0xFF


def encode_voice_0x34(language_id: int, md5: str, url: str) -> bytes:
    md5_b = md5.encode("utf-8")
    url_b = url.encode("utf-8")
    payload = (
        int(language_id).to_bytes(4, "big")
        + bytes([len(md5_b)])
        + md5_b
        + len(url_b).to_bytes(4, "big")
        + url_b
    )
    body = bytes([0x34]) + payload
    return b"\xab\x00" + len(body).to_bytes(4, "big") + body + bytes([checksum(body)])


def decode_voice_report_b64(raw: str) -> dict[str, Any]:
    try:
        packet = base64.b64decode(raw)
    except Exception as exc:
        return {"valid": False, "error": f"base64: {exc}"}
    if len(packet) < 13 or packet[:2] != b"\xab\x00":
        return {"valid": False, "hex": packet.hex(), "error": "bad packet"}
    declared_len = int.from_bytes(packet[2:6], "big")
    if packet[6] != 0x35:
        return {"valid": False, "hex": packet.hex(), "cmd": packet[6]}
    payload = packet[7:]
    if len(payload) < 6:
        return {"valid": False, "hex": packet.hex(), "error": "short payload"}
    return {
        "valid": True,
        "hex": packet.hex(),
        "declared_len": declared_len,
        "languageId": int.from_bytes(payload[0:4], "big"),
        "status": payload[4],
        "progress": payload[5],
        "extra": payload[6:].hex(),
    }


def get_local_ip(robot_ip: str) -> str:
    configured = CONFIG.get("server", {}).get("public_ip", "auto")
    if configured and configured != "auto":
        return configured
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((robot_ip, 6668))
        return sock.getsockname()[0]
    finally:
        sock.close()


def tcp_port_open(ip: str, port: int = 6668, timeout: float = 0.35) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except OSError:
        return False


def summarize_robot_status(status: dict[str, Any]) -> dict[str, Any]:
    dps = status.get("dps") or {}
    info: dict[str, Any] = {}
    raw_info = dps.get("34") or dps.get(34)
    if raw_info:
        try:
            decoded = base64.b64decode(raw_info).decode("utf-8", errors="replace")
            info = json.loads(decoded)
        except Exception:
            info = {}
    return {
        "languageId": dps.get(str(CONFIG["robot"].get("language_dp", 36))),
        "state": dps.get("5") or dps.get(5),
        "battery": dps.get("8") or dps.get(8),
        "mac": info.get("Mac") or info.get("MAC") or info.get("mac"),
        "firmware": info.get("Firmware_Version") or info.get("MCU_Version"),
        "moduleUuid": info.get("Module_UUID"),
    }


def verify_robot_at_ip(ip: str) -> tuple[bool, dict[str, Any] | None, str | None]:
    robot = CONFIG["robot"]
    try:
        dev = tinytuya.OutletDevice(
            robot["device_id"],
            ip,
            robot["local_key"],
            version=float(robot.get("protocol_version", 3.3)),
        )
        dev.set_socketTimeout(2)
        status = dev.status()
        if isinstance(status, dict) and status.get("dps"):
            return True, summarize_robot_status(status), None
        return False, None, str(status)[:300]
    except Exception as exc:
        return False, None, str(exc)[:300]


def scan_local_network(subnet: str | None = None) -> dict[str, Any]:
    ensure_robot_configured(require_ip=False)
    robot_ip = CONFIG["robot"].get("ip") or "8.8.8.8"
    local_ip = get_local_ip(robot_ip)
    network = ipaddress.ip_network(subnet or f"{local_ip}/24", strict=False)
    hosts = [str(ip) for ip in network.hosts()]

    LOG.add(f"Scanning subnet {network} for Tuya LAN port 6668...")
    open_ips: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as pool:
        future_map = {pool.submit(tcp_port_open, ip): ip for ip in hosts}
        for future in concurrent.futures.as_completed(future_map):
            ip = future_map[future]
            try:
                if future.result():
                    open_ips.append(ip)
            except Exception:
                pass

    open_ips = sorted(open_ips, key=lambda value: tuple(int(part) for part in value.split(".")))
    LOG.add(f"Devices with open 6668 found: {len(open_ips)}")

    candidates: list[dict[str, Any]] = []
    for ip in open_ips:
        confirmed, info, error = verify_robot_at_ip(ip)
        candidate = {
            "ip": ip,
            "port": 6668,
            "confirmed": confirmed,
            "current": ip == CONFIG["robot"]["ip"],
            "info": info or {},
            "error": error,
        }
        candidates.append(candidate)
        if confirmed:
            LOG.add(f"Robot confirmed at {ip}: {json.dumps(info, ensure_ascii=False)}")
        else:
            LOG.add(f"Tuya port found at {ip}, but key/ID did not confirm this robot")

    return {
        "localIp": local_ip,
        "subnet": str(network),
        "candidates": candidates,
        "currentIp": CONFIG["robot"]["ip"],
    }


def robot_device() -> tinytuya.OutletDevice:
    ensure_robot_configured(require_ip=True)
    robot = CONFIG["robot"]
    dev = tinytuya.OutletDevice(
        robot["device_id"],
        robot["ip"],
        robot["local_key"],
        version=float(robot.get("protocol_version", 3.3)),
    )
    dev.set_socketPersistent(True)
    dev.set_socketTimeout(8)
    return dev


def read_current_language_id() -> int | None:
    try:
        status = robot_device().status()
        dps = status.get("dps") or {}
        raw = dps.get(str(CONFIG["robot"].get("language_dp", 36)))
        return int(raw) if raw is not None else None
    except Exception as exc:
        LOG.add(f"Could not read current languageId: {exc}")
        return None


def choose_next_language_id() -> int:
    voice = CONFIG.get("voice", {})
    low = int(voice.get("language_id_min", 8))
    high = int(voice.get("language_id_max", 250))
    current = read_current_language_id()
    with STATE_LOCK:
        state = load_json(STATE_PATH, {"last_language_id": low - 1})
        last = int(state.get("last_language_id", low - 1))
        base = current if current is not None else last
        next_id = base + 1
        if next_id > high or next_id < low:
            next_id = low
        if current is not None and next_id == current:
            next_id += 1
            if next_id > high:
                next_id = low
        state["last_language_id"] = next_id
        state["last_used_at"] = dt.datetime.now().isoformat(timespec="seconds")
        save_json(STATE_PATH, state)
        return next_id


def list_mp3s(folder: Path) -> list[Path]:
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".mp3"]
    return sorted(files, key=lambda p: p.name.lower())


def build_package(source_folder: Path) -> tuple[Path, str, int, int]:
    if not source_folder.exists() or not source_folder.is_dir():
        raise ValueError(f"Folder not found: {source_folder}")
    mp3s = list_mp3s(source_folder)
    if not mp3s:
        raise ValueError("No MP3 files found in the folder")

    PACKAGES_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = PACKAGES_DIR / f"voice_pack_{stamp}.tar.gz"
    with tarfile.open(out, "w:gz") as tar:
        for mp3 in mp3s:
            info = tar.gettarinfo(str(mp3), arcname=mp3.name)
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            with mp3.open("rb") as fh:
                tar.addfile(info, fh)

    data = out.read_bytes()
    return out, hashlib.md5(data).hexdigest(), len(data), len(mp3s)


@dataclass
class SendResult:
    package: str
    md5: str
    size: int
    file_count: int
    language_id: int
    url: str
    set_value_result: Any
    reports: list[dict[str, Any]]


def send_voice_package(source_folder: Path) -> SendResult:
    global ACTIVE_PACKAGE
    ensure_robot_configured(require_ip=True)
    package, md5, size, file_count = build_package(source_folder)
    with ACTIVE_PACKAGE_LOCK:
        ACTIVE_PACKAGE = package

    robot_ip = CONFIG["robot"]["ip"]
    port = int(CONFIG["server"]["port"])
    public_ip = get_local_ip(robot_ip)
    url = f"http://{public_ip}:{port}/smart/product/voice/custom.tar.gz?"
    language_id = choose_next_language_id()
    LOG.add(f"Built package: {package.name}, files: {file_count}, size: {size}, md5: {md5}")
    LOG.add(f"Selected languageId={language_id}, URL={url}")

    packet = encode_voice_0x34(language_id, md5, url)
    b64 = base64.b64encode(packet).decode("ascii")
    dev = robot_device()
    LOG.add("Sending DP35 voice_data to robot...")
    result = dev.set_value(int(CONFIG["robot"].get("voice_dp", 35)), b64, nowait=False)
    LOG.add(f"set_value response: {json.dumps(result, ensure_ascii=False)[:800]}")

    reports: list[dict[str, Any]] = []
    dps = (result or {}).get("dps") or {}
    first_raw = dps.get(str(CONFIG["robot"].get("voice_dp", 35)))
    if first_raw:
        report = decode_voice_report_b64(first_raw)
        reports.append(report)
        LOG.add(f"DP35: {json.dumps(report, ensure_ascii=False)}")

    listen_seconds = int(CONFIG.get("voice", {}).get("listen_seconds", 150))
    end = time.time() + listen_seconds
    last = first_raw
    while time.time() < end:
        try:
            resp = dev.receive()
            if not resp:
                continue
            dps = resp.get("dps") or {}
            raw = dps.get(str(CONFIG["robot"].get("voice_dp", 35))) or dps.get(int(CONFIG["robot"].get("voice_dp", 35)))
            if raw and raw != last:
                last = raw
                report = decode_voice_report_b64(raw)
                reports.append(report)
                LOG.add(f"DP35: {json.dumps(report, ensure_ascii=False)}")
                if report.get("languageId") == language_id and report.get("progress") == 100:
                    break
        except Exception:
            try:
                dev.heartbeat()
            except Exception:
                pass
            time.sleep(1)

    return SendResult(
        package=str(package),
        md5=md5,
        size=size,
        file_count=file_count,
        language_id=language_id,
        url=url,
        set_value_result=result,
        reports=reports,
    )


def run_job(folder: str) -> None:
    global CURRENT_JOB
    try:
        source = Path(folder).expanduser().resolve()
        LOG.add(f"Start: source={source}")
        result = send_voice_package(source)
        with JOB_LOCK:
            if CURRENT_JOB:
                CURRENT_JOB["status"] = "done"
                CURRENT_JOB["result"] = asdict(result)
        LOG.add("Done: package sent.")
    except Exception as exc:
        err = "".join(traceback.format_exception_only(type(exc), exc)).strip()
        LOG.add(f"Error: {err}")
        LOG.add(traceback.format_exc())
        with JOB_LOCK:
            if CURRENT_JOB:
                CURRENT_JOB["status"] = "error"
                CURRENT_JOB["error"] = err


class Handler(BaseHTTPRequestHandler):
    server_version = "RobotVoice/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        LOG.add(f"HTTP {self.client_address[0]} {fmt % args}")

    def send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path == "/":
            self.serve_file(STATIC_DIR / "index.html")
        elif path == "/app.css":
            self.serve_file(STATIC_DIR / "app.css")
        elif path == "/app.js":
            self.serve_file(STATIC_DIR / "app.js")
        elif path == "/api/config":
            state = load_json(STATE_PATH, {})
            self.send_json({"config": public_config(), "state": state, "logs": LOG.lines()})
        elif path == "/api/job":
            with JOB_LOCK:
                job = dict(CURRENT_JOB or {"status": "idle"})
            job["logs"] = LOG.lines()
            self.send_json(job)
        elif path == "/smart/product/voice/custom.tar.gz":
            self.serve_active_package()
        else:
            self.send_error(404, "Not found")

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/start":
            data = self.read_json()
            folder = str(data.get("folder", "")).strip().strip('"')
            if not folder:
                self.send_json({"error": "Enter the MP3 folder"}, 400)
                return
            with JOB_LOCK:
                global CURRENT_JOB
                if CURRENT_JOB and CURRENT_JOB.get("status") == "running":
                    self.send_json({"error": "A job is already running"}, 409)
                    return
                CURRENT_JOB = {
                    "status": "running",
                    "folder": folder,
                    "started_at": dt.datetime.now().isoformat(timespec="seconds"),
                }
            threading.Thread(target=run_job, args=(folder,), daemon=True).start()
            self.send_json({"ok": True, "status": "running"})
        elif parsed.path == "/api/status":
            try:
                current = read_current_language_id()
                self.send_json({"languageId": current, "logs": LOG.lines()})
            except Exception as exc:
                self.send_json({"error": str(exc), "logs": LOG.lines()}, 400)
        elif parsed.path == "/api/scan":
            data = self.read_json()
            subnet = str(data.get("subnet", "")).strip() or None
            try:
                result = scan_local_network(subnet)
                result["logs"] = LOG.lines()
                self.send_json(result)
            except Exception as exc:
                LOG.add(f"Scan error: {exc}")
                self.send_json({"error": str(exc), "logs": LOG.lines()}, 500)
        elif parsed.path == "/api/select_robot":
            data = self.read_json()
            ip = str(data.get("ip", "")).strip()
            try:
                ipaddress.ip_address(ip)
            except ValueError:
                self.send_json({"error": "Invalid IP"}, 400)
                return
            CONFIG["robot"]["ip"] = ip
            save_config()
            LOG.add(f"Robot IP saved: {ip}")
            self.send_json({"ok": True, "ip": ip, "config": public_config(), "logs": LOG.lines()})
        elif parsed.path == "/api/settings":
            data = self.read_json()
            robot = CONFIG.setdefault("robot", {})
            for key in ("device_id", "local_key", "ip"):
                if key in data:
                    robot[key] = str(data.get(key, "")).strip()
            if "protocol_version" in data:
                robot["protocol_version"] = float(data.get("protocol_version") or 3.3)
            if "voice_dp" in data:
                robot["voice_dp"] = int(data.get("voice_dp") or 35)
            if "language_dp" in data:
                robot["language_dp"] = int(data.get("language_dp") or 36)
            save_config()
            LOG.add("Robot settings saved.")
            self.send_json({"ok": True, "config": public_config(), "logs": LOG.lines()})
        else:
            self.send_error(404, "Not found")

    def serve_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(404, "Not found")
            return
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_active_package(self) -> None:
        with ACTIVE_PACKAGE_LOCK:
            package = ACTIVE_PACKAGE
        if not package or not package.exists():
            self.send_error(404, "Package not ready")
            return
        LOG.add(f"Robot is downloading package: {package.name}")
        self.send_response(200)
        self.send_header("Content-Type", "application/gzip")
        self.send_header("Content-Length", str(package.stat().st_size))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        with package.open("rb") as fh:
            while True:
                chunk = fh.read(1024 * 128)
                if not chunk:
                    break
                self.wfile.write(chunk)
        LOG.add(f"Package served to client {self.client_address[0]}")


def main() -> None:
    host = CONFIG.get("server", {}).get("host", "0.0.0.0")
    port = int(CONFIG.get("server", {}).get("port", 8780))
    LOG.add(f"RobotVoice UI: http://127.0.0.1:{port}/")
    if CONFIG.get("robot", {}).get("ip"):
        LOG.add(f"Robot HTTP package URL: http://{get_local_ip(CONFIG['robot']['ip'])}:{port}/smart/product/voice/custom.tar.gz?")
    else:
        LOG.add("Robot IP is not set. Fill settings and run the scanner in the Web UI.")
    httpd = ThreadingHTTPServer((host, port), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        LOG.add("Stopped.")


if __name__ == "__main__":
    main()
