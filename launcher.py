"""
Widget launcher - uses a local HTTP API server + Microsoft Edge in app mode.
No third-party Python packages required. Works with Python 3.8 and later.
"""

import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')
CACHE_FILE  = os.path.join(BASE_DIR, 'weather_cache.json')
HTML_FILE   = os.path.join(BASE_DIR, 'widget.html')
API_PORT    = 27632

DEFAULT_CONFIG = {
    "cities": [
        {"name": "New York", "timezone": "America/New_York", "country": "USA"},
        {"name": "London",   "timezone": "Europe/London",    "country": "UK"},
        {"name": "Tokyo",    "timezone": "Asia/Tokyo",       "country": "Japan"}
    ],
    "weather": {"city": "", "lat": None, "lon": None},
    "window":  {"x": 80, "y": 80}
}

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def find_browser():
    for path in EDGE_PATHS + CHROME_PATHS:
        if os.path.exists(path):
            return path
    return None


def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return default


def save_json(path, data):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


class ApiHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass

    def send_json(self, status, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length:
            return json.loads(self.rfile.read(length).decode('utf-8'))
        return None

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path == '/api/config':
            self.send_json(200, load_json(CONFIG_FILE, DEFAULT_CONFIG))

        elif path == '/api/weather-cache':
            cache = load_json(CACHE_FILE, None)
            self.send_json(200, cache if cache is not None else {})

        elif path == '/api/sysinfo':
            try:
                cpu_out = subprocess.check_output("wmic cpu get loadpercentage", shell=True, text=True)
                cpu = int(cpu_out.strip().split('\n')[-1].strip())
            except Exception:
                cpu = 0
            
            try:
                ram_out = subprocess.check_output("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize", shell=True, text=True)
                lines = ram_out.strip().split('\n')
                if len(lines) >= 2:
                    parts = lines[-1].strip().split()
                    free = int(parts[0])
                    total = int(parts[1])
                    ram = int(((total - free) / total) * 100)
                else:
                    ram = 0
            except Exception:
                ram = 0
            self.send_json(200, {"cpu": cpu, "ram": ram})

        elif path == '/widget':
            with open(HTML_FILE, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        body = self.read_body()

        if path == '/api/config':
            ok = save_json(CONFIG_FILE, body)
            self.send_json(200, {"ok": ok})

        elif path == '/api/weather-cache':
            ok = save_json(CACHE_FILE, body)
            self.send_json(200, {"ok": ok})

        elif path == '/api/quit':
            self.send_json(200, {"ok": True})
            threading.Thread(target=lambda: (time.sleep(0.3), os._exit(0))).start()

        else:
            self.send_json(404, {"error": "not found"})


def start_api_server():
    server = HTTPServer(('127.0.0.1', API_PORT), ApiHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def launch_browser(browser_path):
    cfg = load_json(CONFIG_FILE, DEFAULT_CONFIG)
    wx = cfg.get("window", {}).get("x", 80)
    wy = cfg.get("window", {}).get("y", 80)

    url = f'http://127.0.0.1:{API_PORT}/widget'
    args = [
        browser_path,
        f'--app={url}',
        '--window-size=700,380',
        f'--window-position={wx},{wy}',
        '--disable-extensions',
        '--disable-background-networking',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-sync',
        '--disable-translate',
    ]
    return subprocess.Popen(args)


def main():
    browser = find_browser()
    if not browser:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            'Microsoft Edge or Google Chrome is required to run this widget.\n'
            'Please install either browser and try again.',
            'Widget - Browser Not Found',
            0x10
        )
        sys.exit(1)

    start_api_server()
    time.sleep(0.5)

    proc = launch_browser(browser)
    proc.wait()


if __name__ == '__main__':
    main()
