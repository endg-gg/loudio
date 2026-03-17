#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(cmd: str, quiet: bool = False) -> bool:
    try:
        if quiet:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def main() -> None:
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)

    print("Installing loudio...")

    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ required")
        sys.exit(1)

    venv_dir = script_dir / ".venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv .venv"):
            print("Error: Failed to create virtual environment")
            sys.exit(1)

    is_windows = platform.system() == "Windows"
    venv_python = venv_dir / ("Scripts" if is_windows else "bin") / ("python.exe" if is_windows else "python")
    venv_pip = venv_dir / ("Scripts" if is_windows else "bin") / ("pip.exe" if is_windows else "pip")

    print("Upgrading pip...")
    run_command(f'"{venv_python}" -m pip install --upgrade pip', quiet=True)

    print("Installing dependencies...")
    run_command(f'"{venv_pip}" install -r requirements.txt', quiet=True)

    if is_windows:
        install_dir = Path.home() / "AppData" / "Local" / "Programs" / "loudio"
        install_dir.mkdir(parents=True, exist_ok=True)

        launcher = install_dir / "loudio.bat"
        launcher.write_text(
            f'@echo off\n"{venv_python}" "{script_dir / "main.py"}" %*\n',
            encoding='utf-8'
        )

        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
            current_path, _ = winreg.QueryValueEx(key, "Path")

            if isinstance(current_path, str) and str(install_dir) not in current_path:
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, f"{current_path};{install_dir}")
                print(f"Added to PATH: {install_dir}")
                print("Restart terminal to use: loudio")
            else:
                print("Already in PATH")

            winreg.CloseKey(key)
        except Exception as e:
            print(f"Could not add to PATH automatically: {e}")
            print(f"Add manually: {install_dir}")

    else:
        install_dir = Path.home() / ".local" / "bin"
        install_dir.mkdir(parents=True, exist_ok=True)

        launcher = install_dir / "loudio"
        launcher.write_text(
            f'#!/usr/bin/bash\nsource "{venv_dir / "bin" / "activate"}"\nexec python3 "{script_dir / "main.py"}" "$@"\n',
            encoding='utf-8'
        )
        launcher.chmod(0o755)

        path_export = 'export PATH="$HOME/.local/bin:$PATH"'
        for rc in [Path.home() / ".zshrc", Path.home() / ".bashrc"]:
            if rc.exists():
                content = rc.read_text(encoding='utf-8')
                if ".local/bin" not in content:
                    rc.open("a").write(f"\n{path_export}\n")
                    print(f"Added to PATH in {rc}")
                    print(f"Run: source {rc}")

    print("\nloudio installed successfully!")
    print("Run with: loudio --help")


if __name__ == "__main__":
    main()
