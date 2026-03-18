import socket
import numpy as np
import sounddevice as sd
import opuslib

RATE = 48000
CHANNELS = 2
CHUNK = 960  # 20ms frame at 48kHz
PORT = 4455


def run_client(server_ip, port=PORT, input_device=None):
    encoder = opuslib.Encoder(RATE, CHANNELS, opuslib.APPLICATION_AUDIO)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[loudio client] Streaming to {server_ip}:{port}")

    packet_count = 0

    def callback(indata, frames, time, status):
        nonlocal packet_count
        if status:
            print(f"[loudio client] Stream status: {status}")
        raw = bytes(indata)
        amplitude = int(np.abs(np.frombuffer(raw, dtype='int16')).max())
        encoded = encoder.encode(raw, CHUNK)
        sock.sendto(encoded, (server_ip, port))
        packet_count += 1
        if packet_count % 500 == 0:
            print(f"[loudio client] {packet_count} packets sent, amplitude={amplitude}, encoded={len(encoded)}b")



    try:
        with sd.RawInputStream(samplerate=RATE, channels=CHANNELS, dtype='int16',
                               blocksize=CHUNK, callback=callback, device=input_device):
            print(f"[loudio client] Streaming... device={input_device} {RATE}Hz {CHANNELS}ch. Ctrl+C to stop")
            while True:
                pass
    except KeyboardInterrupt:
        print(f"\n[loudio client] Stopped. Total packets sent: {packet_count}")
    finally:
        sock.close()
