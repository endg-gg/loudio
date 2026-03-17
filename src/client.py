import socket
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

    def callback(indata, frames, time, status):
        encoded = encoder.encode(bytes(indata), CHUNK)
        sock.sendto(encoded, (server_ip, port))

    try:
        with sd.RawInputStream(samplerate=RATE, channels=CHANNELS, dtype='int16',
                               blocksize=CHUNK, callback=callback, device=input_device):
            print("[loudio client] Streaming... Ctrl+C to stop")
            while True:
                pass
    except KeyboardInterrupt:
        print("\n[loudio client] Stopped.")
    finally:
        sock.close()
