#!/usr/bin/env python3
"""
Strix Recon Agent launcher (WSL / Docker friendly)

Usage examples:
  python strix.py 10.10.11.58
  python strix.py dog.htb
  python strix.py https://example.com

Advanced:
  python strix.py --layer 4 example.com
  python strix.py --interactive --timeout 1.5 https://target.edu
  python strix.py --layer 4 --ovpn vpn.ovpn --hosts hosts.txt target.com
  python strix.py --force-build 10.10.11.58
"""

from __future__ import annotations
import argparse
import os
import subprocess
import sys
from pathlib import Path
import hashlib
import textwrap

# Config
IMAGE_NAME = "strix-agent"
PROJECT_ROOT = Path(__file__).resolve().parent


def print_banner() -> None:
    print(
        textwrap.dedent(
            r"""
       _____ __        __    
      / ___// /_____ _/ /____
      \__ \/ __/ __ `/ / ___/
     ___/ / /_/ /_/ / (__  ) 
    /____/\__/\__,_/_/____/  
    STRIX | LLM Recon Agent
    """
        )
    )


def compute_config_hash(project_root: Path) -> str:
    """Hash .env + configs/ content to detect changes and force rebuild."""
    md5 = hashlib.md5()
    env = project_root / ".env"
    if env.exists():
        md5.update(env.read_bytes())
    configs = project_root / "configs"
    if configs.is_dir():
        for root, _, files in os.walk(configs):
            for fname in sorted(files):
                p = Path(root) / fname
                if p.is_file():
                    md5.update(p.read_bytes())
    return md5.hexdigest()


def docker_image_exists(image_name: str) -> bool:
    try:
        out = subprocess.check_output(["docker", "images", "-q", image_name], stderr=subprocess.DEVNULL)
        return bool(out.strip())
    except subprocess.CalledProcessError:
        return False


def build_image(image_name: str, project_root: Path) -> None:
    print(f"[*] Building Docker image '{image_name}' (may take several minutes)...")
    subprocess.check_call(["docker", "build", "--platform=linux/amd64", "-t", image_name, str(project_root)])


def make_docker_cmd(
    image_name: str,
    project_root: Path,
    target: str,
    layer: int,
    interactive: bool,
    ovpn: str | None,
    hosts: str | None,
    timeout: float,
    test: bool,
) -> list[str]:
    """Construct docker run command array."""
    docker_cmd: list[str] = [
        "docker",
        "run",
        "--rm",
        "-it",  # keep interactive so output shows; can be changed if needed
        "--cap-add=NET_ADMIN",
        "--device",
        "/dev/net/tun",
        "-v",
        f"{project_root}:/opt/agent",  # mount repository
        "-e",
        f"PYTHONPATH=/opt/agent",
        "-e",
        f"LLM_BACKEND={os.environ.get('LLM_BACKEND', 'ollama')}",
        "-e",
        f"OLLAMA_URL={os.environ.get('OLLAMA_URL', 'http://host.docker.internal:11434')}",
    ]

    # On Linux hosts (including WSL2), ensure host.docker.internal resolves
    if sys.platform.startswith("linux"):
        # host-gateway is supported in modern Docker: maps host.docker.internal -> host gateway IP
        docker_cmd += ["--add-host", "host.docker.internal:host-gateway"]

    # Target environment
    # Decide if host or website is used; inside container main.py decides but pass TARGET appropriately
    docker_cmd += ["-e", f"TARGET_HOST={target}"]

    # Optional mounts/environment vars
    if ovpn:
        abs_ovpn = str(Path(ovpn).resolve())
        docker_cmd += ["-v", f"{abs_ovpn}:/opt/agent/ovpn_config.ovpn", "-e", "OVPN_FILE=/opt/agent/ovpn_config.ovpn"]

    if hosts:
        abs_hosts = str(Path(hosts).resolve())
        docker_cmd += ["-v", f"{abs_hosts}:/opt/agent/custom_hosts", "-e", "CUSTOM_HOSTS_FILE=/opt/agent/custom_hosts"]

    if interactive:
        docker_cmd += ["-e", "INTERACTIVE=true"]
    if test:
        docker_cmd += ["-e", "TEST_MODE=true"]

    # Steps and timeout: container expects STEPS and TIMEOUT (seconds or multiplier)
    docker_cmd += ["-e", f"STEPS={layer}", "-e", f"TIMEOUT={int(timeout * 180)}"]

    # Provide a harmless dummy key only to satisfy legacy checks inside container (harmless for Ollama).
    # With the LLMClient changes we made, this is no longer required for Ollama, but harmless to keep.
    if "LLM_API_KEY" in os.environ:
        docker_cmd += ["-e", f"LLM_API_KEY={os.environ['LLM_API_KEY']}"]
    else:
        # only set a dummy to avoid startup aborts in older code - optional
        docker_cmd += ["-e", "LLM_API_KEY=dummy_for_local_ollama"]

    # Final: image + command to run main.py directly (avoid python -m agent.main issues)
    docker_cmd += [
        image_name,
        "python3",
        "/opt/agent/main.py",
        target,
        str(layer),
        str(int(bool(interactive))),
        "host",
    ]

    return docker_cmd


def run_target(
    target: str,
    layer: int = 3,
    ovpn: str | None = None,
    hosts: str | None = None,
    interactive: bool = False,
    timeout: float = 1.0,
    test: bool = False,
    force_build: bool = False,
) -> int:
    # Auto-detect rebuild need by hashing config
    last_hash_file = PROJECT_ROOT / ".last_build_hash"
    current_hash = compute_config_hash(PROJECT_ROOT)
    need_build = force_build

    if last_hash_file.exists():
        last_hash = last_hash_file.read_text().strip()
        if last_hash != current_hash:
            need_build = True
    else:
        need_build = True

    if need_build:
        # write current hash for future runs
        last_hash_file.write_text(current_hash)

    if need_build or not docker_image_exists(IMAGE_NAME):
        build_image(IMAGE_NAME, PROJECT_ROOT)

    docker_cmd = make_docker_cmd(
        IMAGE_NAME, PROJECT_ROOT, target, layer, interactive, ovpn, hosts, timeout, test
    )

    print("[*] Running container with command:")
    print(" ".join(docker_cmd))
    try:
        subprocess.run(docker_cmd, check=True)
        print("[*] Container finished successfully.")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"[!] Docker run failed with exit code {e.returncode}")
        return e.returncode


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="strix.py",
        description="Launch Strix Recon Agent (build+run inside Docker).",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("target", help="Target IP, domain, or website URL")
    parser.add_argument("--layer", type=int, default=3, choices=range(1, 6), metavar="[1-5]", help="Number of layers to execute (default: 3)")
    parser.add_argument("--ovpn", help="OpenVPN .ovpn file to mount into container")
    parser.add_argument("--hosts", help="Custom hosts file to mount into container")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive LLM-assisted mode")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout multiplier (default 1.0)")
    parser.add_argument("--config", help="Custom layer0.yaml config path (unused by launcher; forwarded to container if needed)")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    parser.add_argument("--force-build", action="store_true", help="Force rebuild of the Docker image")
    return parser.parse_args()


def main():
    print_banner()
    args = parse_cli()
    rc = run_target(
        target=args.target,
        layer=args.layer,
        ovpn=args.ovpn,
        hosts=args.hosts,
        interactive=args.interactive,
        timeout=args.timeout,
        test=args.test,
        force_build=args.force_build,
    )
    sys.exit(rc)


if __name__ == "__main__":
    main()
