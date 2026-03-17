# loudio

Cross-platform audio streaming over UDP with Opus encoding. Stream system audio from any client (Linux/Windows) to a server receiver.

## Installation

**Linux/Mac:**
```bash
git clone git@github.com:endg-gg/loudio.git
cd loudio
chmod +x install.sh && ./install.sh
```

**Windows:**
```bash
git clone git@github.com:endg-gg/loudio.git
cd loudio
python setup.py
```

After install, restart terminal or source your shell config, then run `loudio --help`.

## Usage

### List audio devices
```bash
loudio --list-devices
```

### Server (receiver)
```bash
loudio server --host 0.0.0.0 --port 4455
```

### Client (transmitter)
```bash
# Auto-detects loopback/monitor device by default (system audio, not mic)
loudio client --host <server-ip>

# Override with specific device index
loudio --list-devices
loudio client --host <server-ip> --device 3
```

## Capturing System Audio (Loopback)

By default, loudio auto-detects the loopback/monitor device to capture system audio (browser, music, etc.) instead of the microphone.

**Linux:** If no loopback device is found, enable the monitor sink via `pavucontrol` → Recording tab.

**Windows:** Enable `Stereo Mix` in Sound settings → Recording devices.

## License

MIT
