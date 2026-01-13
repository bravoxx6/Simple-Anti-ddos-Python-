import time
import redis
from flask import request, abort
from config import * # ADD .app if needed
from logger import log_attack # ADD .app if needed
from fingerprint import get_fingerprint     # ADD .app if needed
from firewall import block_ip # ADD .app if needed
import fingerprint as fingerprint # ADD .app if needed
from unblock import unblock_ip # ADD .app if needed
import threading
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def reset_state():
    r.flushdb()

def ddos_protection():
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "unknown")
    fingerprint = get_fingerprint(ip, ua)

    now = int(time.time())

    # check block
    blocked_until = r.get(f"block:{fingerprint}")
    if blocked_until and now < int(blocked_until):
        #
        abort(403)

    # log request
    key = f"req:{fingerprint}"
    r.lpush(key, now)
    r.ltrim(key, 0, REQUEST_LIMIT)
    r.expire(key, TIME_WINDOW)

    requests = r.llen(key)

    if requests > REQUEST_LIMIT:
        blocked_until = now + BLOCK_TIME
        r.setex(f"block:{fingerprint}", BLOCK_TIME, now + BLOCK_TIME)
        block_ip(ip)
        log_attack(f"DDoS detected | IP: {ip} | UA: {ua}")
        print(f"DDoS detected from {ip} with UA: {ua}. Blocking for {BLOCK_TIME} seconds.")
        threading.Thread(target=unblock_ip, args=(ip, BLOCK_TIME), daemon=True).start()
        abort(429)
        
    
           
