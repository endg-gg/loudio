import sounddevice as sd


def list_devices():
    devices = sd.query_devices()
    print(f"{'ID':<4} {'Name':<45} {'In':<4} {'Out':<4} {'Rate'}")
    print("-" * 70)
    for i, d in enumerate(devices):
        print(f"{i:<4} {d['name'][:44]:<45} {int(d['max_input_channels']):<4} {int(d['max_output_channels']):<4} {int(d['default_samplerate'])}")


def find_loopback_device():
    """Try to auto-detect loopback/monitor device."""
    devices = sd.query_devices()
    keywords = ["monitor", "loopback", "stereo mix", "what u hear"]
    for i, d in enumerate(devices):
        if any(k in d['name'].lower() for k in keywords) and d['max_input_channels'] > 0:
            return i
    return None
