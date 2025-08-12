#!/usr/bin/env python3
"""
Simple Python ping sweep scanner for discovering live hosts in a subnet.
It pings each IP in the specified network range to check if hosts are up.
"""

import argparse
import ipaddress
import subprocess
import platform
import concurrent.futures


def ping_host(ip: ipaddress.IPv4Address) -> bool:
    """Ping a single host. Returns True if host responds."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    # On Linux/Unix, we can specify timeout with -W 1 (1 second)
    command = ["ping", param, "1", "-W", "1", str(ip)]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0


def scan_network(network: ipaddress.IPv4Network) -> list[str]:
    """Scan all hosts in the network using threads and return list of live hosts."""
    live_hosts: list[str] = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_ip = {executor.submit(ping_host, ip): ip for ip in network.hosts()}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    live_hosts.append(str(ip))
                    print(f"[+] {ip} is up")
            except Exception:
                pass
    return live_hosts


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple ping sweep scanner")
    parser.add_argument("network", help="Network in CIDR notation, e.g., 192.168.1.0/24")
    args = parser.parse_args()
    try:
        net = ipaddress.ip_network(args.network, strict=False)
    except ValueError as exc:
        print(f"Invalid network: {exc}")
        return
    print(f"Scanning network {net} for live hosts...")
    live_hosts = scan_network(net)
    print(f"\nScan complete. {len(live_hosts)} hosts found up.")
    for ip in live_hosts:
        print(ip)


if __name__ == "__main__":
    main()
