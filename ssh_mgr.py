#!/usr/bin/env python3
"""SSH Key Manager CLI."""
import argparse
import os
import json
from pathlib import Path
from datetime import datetime

SSH_DIR = Path.home() / ".ssh"
CONFIG_FILE = SSH_DIR / "ssh_mgr.json"

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"hosts": {}, "keys": {}}

def save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

def cmd_generate(args):
    key_path = SSH_DIR / args.name
    key_type = args.type or "ed25519"
    print(f"Generating {key_type} key: {key_path}")
    os.system(f'ssh-keygen -t {key_type} -f {key_path} -N "" -q')
    config = load_config()
    config["keys"][args.name] = {
        "path": str(key_path),
        "type": key_type,
        "created": datetime.now().isoformat(),
    }
    save_config(config)
    print(f"Key generated: {key_path}")

def cmd_add_host(args):
    config = load_config()
    config["hosts"][args.name] = {
        "ip": args.ip, "user": args.user,
        "key": args.key, "port": args.port or 22,
    }
    save_config(config)
    print(f"Host {args.name} added")

def cmd_list(args):
    config = load_config()
    print(f"Keys: {len(config.get('keys', {}))}")
    for name, info in config.get("keys", {}).items():
        print(f"  {name}: {info['type']} ({info['created'][:10]})")
    print(f"Hosts: {len(config.get('hosts', {}))}")
    for name, info in config.get("hosts", {}).items():
        print(f"  {name}: {info['user']}@{info['ip']}:{info['port']}")

def main():
    parser = argparse.ArgumentParser(description="SSH Key Manager")
    sub = parser.add_subparsers(dest="command")
    
    gen = sub.add_parser("generate")
    gen.add_argument("--name", required=True)
    gen.add_argument("--type", default="ed25519")
    
    add = sub.add_parser("add-host")
    add.add_argument("name")
    add.add_argument("--ip", required=True)
    add.add_argument("--user", default="root")
    add.add_argument("--key")
    add.add_argument("--port", type=int, default=22)
    
    sub.add_parser("list")
    
    args = parser.parse_args()
    cmds = {"generate": cmd_generate, "add-host": cmd_add_host, "list": cmd_list}
    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
