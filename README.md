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
# Stream default input
loudio client --host <server-ip>

# Stream specific device by index
loudio client --host <server-ip> --device 3

# Auto-detect loopback/monitor device (capture system audio)
loudio client --host <server-ip> --auto-loopback
```

## Capturing System Audio (Loopback)

**Linux:** Run `loudio --list-devices` and find the `Monitor of ...` device, pass its index with `--device`.

**Windows:** Find `Stereo Mix` or WASAPI loopback device via `--list-devices`, pass with `--device`.

## License

MIT
