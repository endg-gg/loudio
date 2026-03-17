# loudio

Cross-platform audio streaming over UDP with Opus encoding. Stream system audio from any client (Linux/Windows) to a server receiver.

## Requirements

```bash
pip install -r requirements.txt
```

**Linux** also needs:
```bash
# Debian/Ubuntu
sudo apt install libopus-dev portaudio19-dev

# Arch
sudo pacman -S opus portaudio
```

**Windows** needs the Opus DLL - download from [opus-codec.org](https://opus-codec.org/downloads/) and place `opus.dll` in the project root or system PATH.

## Usage

### List audio devices
```bash
python main.py --list-devices
```

### Server (receiver)
```bash
python main.py server --host 0.0.0.0 --port 4455
```

### Client (transmitter)
```bash
# Stream default mic/input
python main.py client --host <server-ip> --port 4455

# Stream specific device by index
python main.py client --host <server-ip> --device 3

# Auto-detect loopback/monitor device (capture system audio)
python main.py client --host <server-ip> --auto-loopback
```

### Capture system audio (loopback)

**Linux (PulseAudio/Pipewire):** Use `--list-devices` to find your monitor sink (e.g. `Monitor of ...`), then pass its index with `--device`.

**Windows:** Use `--list-devices` to find `Stereo Mix` or `WASAPI loopback` device, then pass with `--device`.

## License

MIT
