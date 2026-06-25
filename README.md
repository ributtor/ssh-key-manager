# ssh-key-manager

CLI tool to manage SSH keys, configs, and known_hosts across servers.

## Features
- Generate and rotate SSH keys
- Manage `~/.ssh/config` entries
- Batch deploy keys to servers
- Audit known_hosts
- Key expiry tracking

## Usage
```bash
# Generate a new key pair
ssh-mgr generate --name myserver --type ed25519

# Add server config
ssh-mgr add-host myserver --ip 192.168.1.10 --user admin --key ~/.ssh/myserver

# Deploy key to server
ssh-mgr deploy myserver

# List all managed keys
ssh-mgr list
```

## License
MIT
