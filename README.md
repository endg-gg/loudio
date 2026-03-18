# Loudio

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

**Linux:** If no loopback device is found, set the monitor source manually then run with the `pulse` device:
```bash
pactl set-default-source alsa_output.<your-card>.analog-stereo.monitor
loudio client --host <server-ip> --device <pulse-device-index>
```
Check your card name with `pactl list sources short`.

**Windows:** Enable `Stereo Mix` in Sound settings → Recording devices.

## Firewall

The server listens on UDP port 4455 by default. Make sure to allow it on the server's firewall:

**Linux (ufw):**
```bash
sudo ufw allow 4455/udp
```

**Linux (iptables):**
```bash
sudo iptables -A INPUT -p udp --dport 4455 -j ACCEPT
```

**Windows:** Allow the port in Windows Defender Firewall → Inbound Rules → New Rule → Port → UDP 4455.

Use `--port` to change the default port on both server and client.

## License

MIT
