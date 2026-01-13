import subprocess
import time

def unblock_ip(ip, delay):
    time.sleep(delay)
    subprocess.run(
        ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"]
    )
    print(f"Unblocked IP: {ip}")
    
