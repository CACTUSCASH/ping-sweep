# Ping Sweep

A simple Python ping sweep scanner that discovers live hosts within a given subnet using ICMP echo requests (ping).

## Features

- Scans any IPv4 subnet specified in CIDR notation and lists hosts that respond to ICMP requests.
- Utilizes threading for faster scanning of large networks.
- Prints live hosts as they are discovered and provides a summary at the end.
- Cross‑platform support (Linux/Windows) with automatic detection of ping command options.

## Usage

```bash
python3 ping_sweep.py 192.168.1.0/24
```

Replace `192.168.1.0/24` with the subnet you want to scan. The script will ping each host in the network and output those that respond. Use a prefix like `sudo` if your environment requires elevated privileges to send ICMP packets.

## Disclaimer

This tool is provided for educational purposes only. Ensure you have permission to scan any network before using this script.
