import argparse
import sys
from .server import run_server
from .client import run_client
from .utils import list_devices, find_loopback_device


def main():
    parser = argparse.ArgumentParser(
        prog="loudio",
        description="Cross-platform audio streaming over UDP with Opus encoding"
    )
    parser.add_argument("mode", choices=["server", "client"], nargs="?", help="Run as server (receiver) or client (transmitter)")
    parser.add_argument("--host", default="0.0.0.0", help="Server IP to bind (server) or connect to (client)")
    parser.add_argument("--port", type=int, default=4455, help="UDP port (default: 4455)")
    parser.add_argument("--device", type=int, default=None, help="Audio device index")
    parser.add_argument("--list-devices", action="store_true", help="List available audio devices and exit")
    parser.add_argument("--auto-loopback", action="store_true", help="Auto-detect loopback device (client mode)")

    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    if not args.mode:
        parser.print_help()
        sys.exit(1)

    if args.mode == "server":
        run_server(host=args.host, port=args.port, output_device=args.device)
    elif args.mode == "client":
        device = args.device
        if args.auto_loopback and device is None:
            device = find_loopback_device()
            if device is not None:
                print(f"[loudio] Auto-detected loopback device: {device}")
            else:
                print("[loudio] No loopback device found, using default input.")
        run_client(server_ip=args.host, port=args.port, input_device=device)
