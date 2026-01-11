import time
import redis
from flask import request, abort
from config import *
from logger import log_attack
from fingerprint import get_fingerprint

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def ddos_protection():
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "unknown")
    fingerprint = get_fingerprint(ip, ua)

    now = int(time.time())

    # Проверка блокировки
    blocked_until = r.get(f"block:{fingerprint}")
    if blocked_until and now < int(blocked_until):
        abort(403)

    # Учёт запросов
    key = f"req:{fingerprint}"
    r.lpush(key, now)
    r.ltrim(key, 0, REQUEST_LIMIT)
    r.expire(key, TIME_WINDOW)

    requests = r.llen(key)

    if requests > REQUEST_LIMIT:
        r.setex(f"block:{fingerprint}", BLOCK_TIME, now + BLOCK_TIME)
        log_attack(f"DDoS detected | IP: {ip} | UA: {ua}")
        abort(429)
