# Vibe coded utility class
# to detect the OS and ARCH
import os
import platform
import subprocess
from typing import Dict

# Mappings used to normalize detected OS/arch tokens
_OS_MAP = {
    "darwin": "darwin", "mac": "darwin", "macos": "darwin",
    "linux": "linux",
    "windows": "windows", "win": "windows", "cygwin": "windows"
}

_ARCH_MAP = {
    # common names -> canonical artifact names
    "x86_64": "amd64",
    "amd64": "amd64",
    "i386": "386",
    "i686": "386",
    "x86": "386",
    "arm64": "arm64",
    "aarch64": "arm64",
    "armv8": "arm64",
    "armv7l": "armv7",
    "armv7": "armv7",
    "arm": "armv7",
    # add more mappings if upstream uses different tokens
}


def _maybe_rosetta_on_macos() -> bool:
    """
    Return True if running under Rosetta translation on macOS.
    Uses `sysctl -in sysctl.proc_translated` which returns '1' when translated.
    If the check fails (permission/tool missing), returns False.
    """
    try:
        # Only macOS has sysctl.proc_translated
        out = subprocess.run(
            ["sysctl", "-in", "sysctl.proc_translated"],
            check=False,
            capture_output=True,
            text=True,
            timeout=0.5,
        )
        return out.stdout.strip() == "1"
    except Exception:
        return False


def detect_os_arch(
    honor_env: bool = True,
) -> Dict[str, str]:
    """
    Detect and return normalized 'os' and 'arch' tokens.

    Returns a dict with keys:
      - os: one of 'darwin', 'linux', 'windows'
      - arch: one of 'amd64', 'arm64', '386', 'armv7' (or best effort)
      - raw_machine: platform.machine() (for debugging)
      - notes: optional notes (e.g., 'rosetta detected')
    """
    notes = []
    # 1) Allow environment overrides if requested
    if honor_env:
        env_os = os.environ.get("OS")
        env_arch = os.environ.get("ARCH")
    else:
        env_os = env_arch = None

    # 2) prefer explicit function args, then env, then autodetect
    if env_os:
        os_token_raw = env_os.strip().lower()
    else:
        os_token_raw = platform.system().lower()

    os_token = _OS_MAP.get(os_token_raw, os_token_raw)

    # 3) detect machine/arch
    if env_arch:
        arch_raw = env_arch.strip().lower()
    else:
        arch_raw = platform.machine().lower()

    raw_machine = arch_raw

    # Special-case: macOS + Rosetta (Python sees x86_64 but host CPU is arm64)
    if os_token == "darwin" and raw_machine in ("x86_64", "amd64"):
        if _maybe_rosetta_on_macos():
            notes.append("rosetta_translation: true (host is arm64, process is x86_64)")
            # treat host CPU as arm64 for download selection
            arch_raw = "arm64"

    # Windows process can be 32-bit on 64-bit machine; inspect env vars for a better hint
    if os_token == "windows":
        # PROCESSOR_ARCHITECTURE or PROCESSOR_ARCHITEW6432 can indicate native arch
        pa = os.environ.get("PROCESSOR_ARCHITECTURE", "").lower()
        pa_w6432 = os.environ.get("PROCESSOR_ARCHITEW6432", "").lower()
        if pa_w6432:
            # When a 32-bit process runs on 64-bit Windows, PROCESSOR_ARCHITEW6432 contains the native arch
            arch_raw = pa_w6432
        elif pa:
            arch_raw = pa

    # Normalize arch token using mapping; fall back to the raw machine string if unknown
    arch_token = _ARCH_MAP.get(arch_raw, arch_raw)

    # Normalize a few common oddities (strip spaces)
    arch_token = arch_token.strip()
    os_token = os_token.strip()

    return {
        "os": os_token,
        "arch": arch_token,
        "raw_machine": raw_machine,
        "notes": "; ".join(notes) if notes else "",
    }