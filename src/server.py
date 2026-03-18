import socket
import sounddevice as sd
import opuslib

RATE = 48000
CHANNELS = 2
CHUNK = 960  # 20ms frame at 48kHz
PORT = 4455


def run_server(host="0.0.0.0", port=PORT, output_device=None):
    decoder = opuslib.Decoder(RATE, CHANNELS)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"[loudio server] Listening on {host}:{port}")

    stream = sd.RawOutputStream(samplerate=RATE, channels=CHANNELS, dtype='int16', device=output_device)
    stream.start()
    print(f"[loudio server] Output stream started: {RATE}Hz {CHANNELS}ch device={output_device}")

    known_clients = set()
    packet_count = 0

    try:
        while True:
            data, addr = sock.recvfrom(4096)
            if addr not in known_clients:
                known_clients.add(addr)
                print(f"[loudio server] Client connected: {addr[0]}:{addr[1]}")
            packet_count += 1
            try:
                pcm = decoder.decode(data, CHUNK)
                stream.write(pcm)
                if packet_count % 500 == 0:
                    print(f"[loudio server] {packet_count} packets received, pcm_len={len(pcm)}")
            except Exception as e:
                print(f"[loudio server] Decode/write error: {e} (packet_size={len(data)})")
    except KeyboardInterrupt:
        print(f"\n[loudio server] Stopped. Total packets: {packet_count}")
    finally:
        stream.stop()
        sock.close()
