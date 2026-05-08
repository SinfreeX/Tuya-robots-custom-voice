const i18n = {
  en: {
    "hero.subtitle": "Build a custom voice pack and send it to your robot over the local network.",
    "settings.title": "Robot settings",
    "settings.hint": "Device ID and Local Key are unique for each robot and are required for the local Tuya LAN protocol.",
    "settings.save": "Save",
    "folder.label": "MP3 folder",
    "folder.start": "Build and send",
    "folder.hint": "Files are read from the folder root and added to the archive root. Use the original names: C001.mp3, D001.mp3, E001.mp3...",
    "scan.title": "Find robot on LAN",
    "scan.hint": "Scans the local /24 subnet, then verifies discovered Tuya devices using this robot's key.",
    "scan.button": "Scan network",
    "scan.scanning": "Scanning...",
    "scan.subnet": "Subnet",
    "scan.found": "found",
    "scan.empty": "No devices with the Tuya LAN port were found. Check that the robot and PC are on the same Wi-Fi/LAN network.",
    "scan.current": "current",
    "scan.confirmed": "Robot confirmed",
    "scan.unconfirmed": "Port 6668 is open, but this was not confirmed as this robot",
    "scan.select": "Select",
    "log.title": "Log",
    "log.status": "Check status",
    "placeholder.localKey": "16 characters",
    "placeholder.robotIp": "Can be found with scanner",
    "placeholder.folder": "Example: C:\\Users\\Name\\Documents\\voicePack",
    "notSet": "not set",
    "alert.folder": "Enter the folder containing MP3 files",
    "alert.save": "Could not save settings",
    "alert.status": "Could not read status",
    "alert.scan": "Scan failed",
    "alert.selectIp": "Could not save IP",
    "alert.start": "Start failed"
  },
  ru: {
    "hero.subtitle": "\u0421\u0431\u043e\u0440\u043a\u0430 \u043a\u0430\u0441\u0442\u043e\u043c\u043d\u043e\u0433\u043e \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u043e\u0433\u043e \u043f\u0430\u043a\u0435\u0442\u0430 \u0438 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0440\u043e\u0431\u043e\u0442\u0443 \u043f\u043e \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e\u0439 \u0441\u0435\u0442\u0438.",
    "settings.title": "\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0440\u043e\u0431\u043e\u0442\u0430",
    "settings.hint": "Device ID \u0438 Local Key \u0438\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u044c\u043d\u044b \u0434\u043b\u044f \u043a\u0430\u0436\u0434\u043e\u0433\u043e \u0440\u043e\u0431\u043e\u0442\u0430 \u0438 \u043d\u0443\u0436\u043d\u044b \u0434\u043b\u044f \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u043e\u0433\u043e Tuya LAN-\u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b\u0430.",
    "settings.save": "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c",
    "folder.label": "\u041f\u0430\u043f\u043a\u0430 \u0441 MP3",
    "folder.start": "\u0421\u043e\u0431\u0440\u0430\u0442\u044c \u0438 \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c",
    "folder.hint": "\u0424\u0430\u0439\u043b\u044b \u0431\u0435\u0440\u0443\u0442\u0441\u044f \u0438\u0437 \u043a\u043e\u0440\u043d\u044f \u043f\u0430\u043f\u043a\u0438 \u0438 \u043a\u043b\u0430\u0434\u0443\u0442\u0441\u044f \u0432 \u043a\u043e\u0440\u0435\u043d\u044c \u0430\u0440\u0445\u0438\u0432\u0430. \u0418\u043c\u0435\u043d\u0430 \u0434\u043e\u043b\u0436\u043d\u044b \u0431\u044b\u0442\u044c \u0448\u0442\u0430\u0442\u043d\u044b\u043c\u0438: C001.mp3, D001.mp3, E001.mp3...",
    "scan.title": "\u041f\u043e\u0438\u0441\u043a \u0440\u043e\u0431\u043e\u0442\u0430 \u0432 \u0441\u0435\u0442\u0438",
    "scan.hint": "\u0421\u043a\u0430\u043d\u0438\u0440\u0443\u0435\u0442\u0441\u044f \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u0430\u044f /24 \u043f\u043e\u0434\u0441\u0435\u0442\u044c, \u0437\u0430\u0442\u0435\u043c \u043d\u0430\u0439\u0434\u0435\u043d\u043d\u044b\u0435 Tuya-\u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430 \u043f\u0440\u043e\u0432\u0435\u0440\u044f\u044e\u0442\u0441\u044f \u043f\u043e \u043a\u043b\u044e\u0447\u0443 \u044d\u0442\u043e\u0433\u043e \u0440\u043e\u0431\u043e\u0442\u0430.",
    "scan.button": "\u0421\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0441\u0435\u0442\u044c",
    "scan.scanning": "\u0421\u043a\u0430\u043d\u0438\u0440\u0443\u044e...",
    "scan.subnet": "\u041f\u043e\u0434\u0441\u0435\u0442\u044c",
    "scan.found": "\u043d\u0430\u0439\u0434\u0435\u043d\u043e",
    "scan.empty": "\u0423\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432 \u0441 Tuya LAN-\u043f\u043e\u0440\u0442\u043e\u043c \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u043e. \u041f\u0440\u043e\u0432\u0435\u0440\u044c, \u0447\u0442\u043e \u0440\u043e\u0431\u043e\u0442 \u0438 \u041f\u041a \u0432 \u043e\u0434\u043d\u043e\u0439 Wi-Fi/LAN \u0441\u0435\u0442\u0438.",
    "scan.current": "\u0442\u0435\u043a\u0443\u0449\u0438\u0439",
    "scan.confirmed": "\u0420\u043e\u0431\u043e\u0442 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d",
    "scan.unconfirmed": "\u041f\u043e\u0440\u0442 6668 \u043e\u0442\u043a\u0440\u044b\u0442, \u043d\u043e \u044d\u0442\u043e \u043d\u0435 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u043b\u043e\u0441\u044c \u043a\u0430\u043a \u044d\u0442\u043e\u0442 \u0440\u043e\u0431\u043e\u0442",
    "scan.select": "\u0412\u044b\u0431\u0440\u0430\u0442\u044c",
    "log.title": "\u041b\u043e\u0433",
    "log.status": "\u041f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c \u0441\u0442\u0430\u0442\u0443\u0441",
    "placeholder.localKey": "16 \u0441\u0438\u043c\u0432\u043e\u043b\u043e\u0432",
    "placeholder.robotIp": "\u041c\u043e\u0436\u043d\u043e \u043d\u0430\u0439\u0442\u0438 \u0441\u043a\u0430\u043d\u0435\u0440\u043e\u043c",
    "placeholder.folder": "\u041d\u0430\u043f\u0440\u0438\u043c\u0435\u0440: C:\\Users\\Name\\Documents\\voicePack",
    "notSet": "\u043d\u0435 \u0437\u0430\u0434\u0430\u043d",
    "alert.folder": "\u0423\u043a\u0430\u0436\u0438\u0442\u0435 \u043f\u0430\u043f\u043a\u0443 \u0441 MP3-\u0444\u0430\u0439\u043b\u0430\u043c\u0438",
    "alert.save": "\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0441\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438",
    "alert.status": "\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043f\u0440\u043e\u0447\u0438\u0442\u0430\u0442\u044c \u0441\u0442\u0430\u0442\u0443\u0441",
    "alert.scan": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f",
    "alert.selectIp": "\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0441\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c IP",
    "alert.start": "\u041e\u0448\u0438\u0431\u043a\u0430 \u0437\u0430\u043f\u0443\u0441\u043a\u0430"
  }
};

const folderInput = document.querySelector("#folder");
const startBtn = document.querySelector("#startBtn");
const statusBtn = document.querySelector("#statusBtn");
const scanBtn = document.querySelector("#scanBtn");
const scanResults = document.querySelector("#scanResults");
const saveSettingsBtn = document.querySelector("#saveSettingsBtn");
const deviceIdInput = document.querySelector("#deviceId");
const localKeyInput = document.querySelector("#localKey");
const robotIpInput = document.querySelector("#robotIpInput");
const langEn = document.querySelector("#langEn");
const langRu = document.querySelector("#langRu");
const logEl = document.querySelector("#log");
const jobBadge = document.querySelector("#jobBadge");
const languageId = document.querySelector("#languageId");
const robotIp = document.querySelector("#robotIp");
const serverPort = document.querySelector("#serverPort");
const lastId = document.querySelector("#lastId");

let timer = null;
let lang = localStorage.getItem("robotVoiceLang") || "en";
let lastScanData = null;

function t(key) {
  return i18n[lang][key] || i18n.en[key] || key;
}

function setLanguage(nextLang) {
  lang = nextLang;
  localStorage.setItem("robotVoiceLang", lang);
  document.documentElement.lang = lang;
  langEn.classList.toggle("active", lang === "en");
  langRu.classList.toggle("active", lang === "ru");
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  localKeyInput.placeholder = localKeyInput.dataset.masked || t("placeholder.localKey");
  robotIpInput.placeholder = t("placeholder.robotIp");
  folderInput.placeholder = t("placeholder.folder");
  if (robotIp.textContent === i18n.en.notSet || robotIp.textContent === i18n.ru.notSet) {
    robotIp.textContent = t("notSet");
  }
  if (lastScanData) renderScanResults(lastScanData);
}

function renderLogs(lines) {
  logEl.textContent = (lines || []).join("\n");
  logEl.scrollTop = logEl.scrollHeight;
}

function applyConfig(config, state) {
  const robot = config.robot || {};
  const voice = config.voice || {};
  folderInput.value = voice.default_source_folder || "";
  deviceIdInput.value = robot.device_id || "";
  robotIpInput.value = robot.ip || "";
  localKeyInput.value = "";
  localKeyInput.dataset.masked = robot.local_key_masked || "";
  localKeyInput.placeholder = robot.local_key_masked || t("placeholder.localKey");
  robotIp.textContent = robot.ip || t("notSet");
  serverPort.textContent = config.server?.port || "...";
  lastId.textContent = state?.last_language_id ?? "...";
}

async function loadConfig() {
  setLanguage(lang);
  const res = await fetch("/api/config");
  const data = await res.json();
  applyConfig(data.config || {}, data.state || {});
  renderLogs(data.logs);
  await refreshJob();
}

async function refreshJob() {
  const res = await fetch("/api/job");
  const data = await res.json();
  jobBadge.textContent = data.status || "idle";
  startBtn.disabled = data.status === "running";
  if (data.result) {
    lastId.textContent = data.result.language_id;
    languageId.textContent = `languageId: ${data.result.language_id}`;
  }
  if (data.logs) renderLogs(data.logs);
  if (data.status !== "running" && timer) {
    clearInterval(timer);
    timer = null;
  }
}

async function saveSettings() {
  const payload = {
    device_id: deviceIdInput.value.trim(),
    ip: robotIpInput.value.trim()
  };
  const localKey = localKeyInput.value.trim();
  if (localKey) payload.local_key = localKey;

  saveSettingsBtn.disabled = true;
  try {
    const res = await fetch("/api/settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) {
      alert(data.error || t("alert.save"));
      return;
    }
    applyConfig(data.config || {}, {});
    renderLogs(data.logs);
  } finally {
    saveSettingsBtn.disabled = false;
  }
}

async function checkStatus() {
  const res = await fetch("/api/status", { method: "POST" });
  const data = await res.json();
  if (!res.ok) {
    alert(data.error || t("alert.status"));
  } else {
    languageId.textContent = `languageId: ${data.languageId ?? "..."}`;
  }
  renderLogs(data.logs);
}

function renderScanResults(data) {
  lastScanData = data;
  scanResults.textContent = "";
  const title = document.createElement("p");
  title.className = "hint";
  title.textContent = `${t("scan.subnet")}: ${data.subnet || "..."}; ${t("scan.found")}: ${(data.candidates || []).length}`;
  scanResults.appendChild(title);

  if (!data.candidates || data.candidates.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty";
    empty.textContent = t("scan.empty");
    scanResults.appendChild(empty);
    return;
  }

  for (const candidate of data.candidates) {
    const row = document.createElement("div");
    row.className = `scanRow ${candidate.confirmed ? "confirmed" : ""}`;

    const body = document.createElement("div");
    const name = document.createElement("strong");
    name.textContent = `${candidate.ip}${candidate.current ? ` (${t("scan.current")})` : ""}`;
    const meta = document.createElement("span");
    const info = candidate.info || {};
    meta.textContent = candidate.confirmed
      ? `${t("scan.confirmed")}; languageId ${info.languageId ?? "?"}; battery ${info.battery ?? "?"}; ${info.mac || ""}`
      : t("scan.unconfirmed");
    body.appendChild(name);
    body.appendChild(meta);

    const button = document.createElement("button");
    button.type = "button";
    button.className = candidate.confirmed ? "" : "secondary";
    button.textContent = t("scan.select");
    button.addEventListener("click", () => selectRobot(candidate.ip));

    row.appendChild(body);
    row.appendChild(button);
    scanResults.appendChild(row);
  }
}

async function scanNetwork() {
  scanBtn.disabled = true;
  scanBtn.textContent = t("scan.scanning");
  try {
    const res = await fetch("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({})
    });
    const data = await res.json();
    if (!res.ok) {
      alert(data.error || t("alert.scan"));
      renderLogs(data.logs);
      return;
    }
    renderScanResults(data);
    renderLogs(data.logs);
  } finally {
    scanBtn.disabled = false;
    scanBtn.textContent = t("scan.button");
  }
}

async function selectRobot(ip) {
  const res = await fetch("/api/select_robot", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ip })
  });
  const data = await res.json();
  if (!res.ok) {
    alert(data.error || t("alert.selectIp"));
    return;
  }
  robotIp.textContent = ip;
  robotIpInput.value = ip;
  renderLogs(data.logs);
  await checkStatus();
}

startBtn.addEventListener("click", async () => {
  const folder = folderInput.value.trim();
  if (!folder) {
    alert(t("alert.folder"));
    return;
  }
  startBtn.disabled = true;
  const res = await fetch("/api/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ folder })
  });
  const data = await res.json();
  if (!res.ok) {
    alert(data.error || t("alert.start"));
    startBtn.disabled = false;
    return;
  }
  await refreshJob();
  timer = setInterval(refreshJob, 1200);
});

statusBtn.addEventListener("click", checkStatus);
scanBtn.addEventListener("click", scanNetwork);
saveSettingsBtn.addEventListener("click", saveSettings);
langEn.addEventListener("click", () => setLanguage("en"));
langRu.addEventListener("click", () => setLanguage("ru"));

loadConfig().catch(err => {
  logEl.textContent = String(err.stack || err);
});
