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

    stream = sd.OutputStream(samplerate=RATE, channels=CHANNELS, dtype='int16', device=output_device)
    stream.start()

    try:
        while True:
            data, addr = sock.recvfrom(4096)
            pcm = decoder.decode(data, CHUNK)
            stream.write(pcm)
    except KeyboardInterrupt:
        print("\n[loudio server] Stopped.")
    finally:
        stream.stop()
        sock.close()
