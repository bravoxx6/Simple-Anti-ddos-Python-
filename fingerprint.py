import hashlib

def get_fingerprint(ip, user_agent):
    raw = f"{ip}:{user_agent}"
    return hashlib.sha256(raw.encode()).hexdigest()
