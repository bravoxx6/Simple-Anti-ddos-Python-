# Anti-DDoS Protection System

Python-based system for detecting and mitigating DDoS attacks at the application layer. 
Includes:
- Flask middleware
- Rate-limiting
- Redis for request tracking
- Auto-unblocking
- Unit tests

# How to execute
# Install
pip install -r requirements.txt

# Flask
python app/app.py

# How to test
pytest -v

Request → Flask middleware → Redis check → Block/Allow → Logging

iptables only works on Linux

TTL and auto-unlock via threading

In WSL, iptables rules are visible, but they do not filter Windows traffic.

```bash
git init
git add .
git commit -m "Initial commit: Flask Anti-DDoS with Redis and unit tests"
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
