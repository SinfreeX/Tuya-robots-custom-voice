# Robot Voice Tool

A local web tool for building and installing custom voice packs on Tuya/Ray-based robot vacuums such as RP38.

The tool runs on your PC, builds a `.tar.gz` archive from MP3 files, serves it over local HTTP, rotates `languageId`, and sends the Tuya LAN `voice_data` command to the robot.

## Requirements

- Windows with Python 3 installed.
- Your PC and robot must be on the same local network.
- A Tuya/Ray robot vacuum that supports the DP35 voice package command.
- The robot's `Device ID`.
- The robot's `Local Key`.

`Device ID` and `Local Key` are unique per device. You usually get them by linking your Smart Life/Tuya account to a project in the Tuya IoT Platform, or by using a compatible helper such as TinyTuya wizard.

After you have the `Local Key`, normal package installation is local-only. The tool does not need to keep using Tuya Cloud to send the voice pack.

## Quick Start

Run:

```bat
start_robot_voice.bat
```

The script starts the local web UI:

```text
http://127.0.0.1:8780/
```

It also installs `tinytuya` automatically if it is missing.
The web UI opens in English by default and has an `EN/RU` switch in the header.

## Usage

1. Enter your robot's `Device ID` and `Local Key`.
2. Click `Save`.
3. Click `Scan network` and select the confirmed robot IP.
4. Enter the folder path containing your modified MP3 files.
5. Click `Build and send`.

MP3 files are added to the root of the archive. Use the original voice-pack filenames, for example:

```text
C001.mp3
C002.mp3
D001.mp3
E001.mp3
S001.mp3
```

Generated packages are saved in `packages/`. Logs are saved in `logs/`.

## languageId Rotation

The tool automatically rotates `languageId`.

This matters because some robots will report success without downloading the file if you send the same already-installed `languageId` again.

## Configuration

Local configuration is stored in:

```text
config.json
```

Use `config.example.json` as a template for a fresh setup.

Do not publish your real `config.json`. It contains your robot's `Local Key`.

The included `.gitignore` excludes:

```text
config.json
state.json
packages/
logs/
```

## Notes

- Default voice DP: `35`.
- Default language/status DP: `36`.
- Default web UI port: `8780`.
- The local HTTP download URL is generated automatically from your PC LAN IP.

If the scanner finds several Tuya devices, select the one marked as confirmed. Confirmation is done using your `Device ID` and `Local Key`.
