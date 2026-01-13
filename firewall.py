import subprocess
import logging

logging.basicConfig(level=logging.WARNING)

WHITELIST = {"127.0.0.1"}

def block_ip(ip):
    if ip in WHITELIST:
        logging.warning(f"Skip blocking whitelisted IP: {ip}")
        return

    try:
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            check=True
        )
        logging.warning(f"IP blocked via iptables: {ip}")
    except subprocess.CalledProcessError as e:
        logging.error(f"iptables error: {e}")

def block_subnet(subnet):
    try:
        subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-s", subnet, "-j", "DROP"],
            check=True
        )
        logging.warning(f"Subnet blocked: {subnet}")
    except subprocess.CalledProcessError as e:
        logging.error(f"iptables error: {e}")
