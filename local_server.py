"""
SwiftVPN Local Python Test Server
Zero external dependencies - runs directly on Python 3.x
Serves the exact same API endpoints as the Node.js Render backend:
  - GET  /health
  - GET  /api/health
  - GET  /api/ip
  - GET  /api/servers
  - POST /api/license/verify
  - POST /api/license/generate
  - GET  /
"""

import http.server
import socketserver
import json
import time
import urllib.parse
import uuid

PORT = 3000

LICENSE_STORE = {
    "SWIFT-VIP-2026-PRO": {
        "plan": "premium",
        "planLabel": "VIP Ultra Lifetime",
        "expiresAt": "2030-12-31T23:59:59Z",
        "maxDevices": 10,
        "features": ["all_servers", "turbo_speed", "adblock_shield", "webrtc_guard", "unlimited_data"]
    },
    "SWIFT-PREMIUM-LIFETIME": {
        "plan": "premium",
        "planLabel": "VIP Lifetime Pass",
        "expiresAt": "2030-12-31T23:59:59Z",
        "maxDevices": 5,
        "features": ["all_servers", "turbo_speed", "adblock_shield", "webrtc_guard", "unlimited_data"]
    },
    "SWIFT-TURBO-PASS": {
        "plan": "premium",
        "planLabel": "VIP Turbo Annual",
        "expiresAt": "2028-12-31T23:59:59Z",
        "maxDevices": 5,
        "features": ["all_servers", "turbo_speed", "adblock_shield", "webrtc_guard", "unlimited_data"]
    }
}

START_TIME = time.time()

class SwiftVPNHandler(http.server.BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Admin-Key')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ['/health', '/api/health']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors()
            self.end_headers()
            data = {
                "status": "healthy",
                "uptime": int(time.time() - START_TIME),
                "nodeRegion": "local-development",
                "version": "2.0.0"
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))

        elif path == '/api/ip':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors()
            self.end_headers()
            client_ip = self.client_address[0]
            data = {
                "ip": client_ip,
                "country": "Local Dev / US",
                "isProxied": False,
                "timestamp": int(time.time() * 1000)
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))

        elif path == '/api/servers':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors()
            self.end_headers()
            servers = [
                {
                    "id": "render-cloud-primary",
                    "name": "⚡ Render Cloud Gateway",
                    "country": "US",
                    "city": "Oregon / Cloud",
                    "flag": "🇺🇸",
                    "host": "localhost",
                    "port": 3000,
                    "protocol": "http",
                    "free": True,
                    "category": "cloud",
                    "pingMs": 14,
                    "loadPercent": 25,
                    "description": "Local test / Render cloud proxy node"
                },
                {
                    "id": "us-east-free",
                    "name": "United States (New York)",
                    "country": "US",
                    "city": "New York",
                    "flag": "🇺🇸",
                    "host": "198.199.86.11",
                    "port": 3128,
                    "protocol": "http",
                    "free": True,
                    "category": "standard",
                    "pingMs": 35,
                    "loadPercent": 42,
                    "description": "Standard fast web proxy"
                },
                {
                    "id": "de-frankfurt-free",
                    "name": "Germany (Frankfurt)",
                    "country": "DE",
                    "city": "Frankfurt",
                    "flag": "🇩🇪",
                    "host": "159.65.120.106",
                    "port": 8080,
                    "protocol": "http",
                    "free": True,
                    "category": "standard",
                    "pingMs": 42,
                    "loadPercent": 38,
                    "description": "European low-latency gateway"
                },
                {
                    "id": "sg-singapore-free",
                    "name": "Singapore #1 (Asia Central)",
                    "country": "SG",
                    "city": "Singapore",
                    "flag": "🇸🇬",
                    "host": "128.199.202.124",
                    "port": 3128,
                    "protocol": "http",
                    "free": True,
                    "category": "standard",
                    "pingMs": 50,
                    "loadPercent": 48,
                    "description": "High-speed Asia Pacific hub"
                },
                {
                    "id": "uk-london-vip",
                    "name": "👑 UK (London VIP Turbo)",
                    "country": "GB",
                    "city": "London",
                    "flag": "🇬🇧",
                    "host": "178.62.83.189",
                    "port": 3128,
                    "protocol": "http",
                    "free": False,
                    "category": "streaming",
                    "pingMs": 28,
                    "loadPercent": 22,
                    "description": "VIP Streaming & BBC iPlayer optimized"
                },
                {
                    "id": "jp-tokyo-vip",
                    "name": "👑 Japan (Tokyo VIP Ultra)",
                    "country": "JP",
                    "city": "Tokyo",
                    "flag": "🇯🇵",
                    "host": "139.180.208.152",
                    "port": 8080,
                    "protocol": "http",
                    "free": False,
                    "category": "gaming",
                    "pingMs": 32,
                    "loadPercent": 18,
                    "description": "Low-ping VIP Gaming & Anime hub"
                }
            ]
            self.wfile.write(json.dumps({"ok": True, "servers": servers}).encode('utf-8'))

        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self._send_cors()
            self.end_headers()
            html = f"""
            <html><body style="font-family:sans-serif;background:#0b1220;color:#e2e8f0;padding:40px;text-align:center;">
              <h1 style="color:#10b981;">⚡ SwiftVPN Local Test Server</h1>
              <p>Status: <b>ONLINE & RUNNING</b> on port {PORT}</p>
              <p>Uptime: {int(time.time() - START_TIME)}s</p>
              <p>Endpoints: <code>/api/health</code> | <code>/api/servers</code> | <code>/api/ip</code></p>
            </body></html>
            """
            self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length > 0 else b'{}'
        try:
            payload = json.loads(body.decode('utf-8'))
        except:
            payload = {}

        if path == '/api/license/verify':
            key = str(payload.get('key', '')).strip().upper()
            if key in LICENSE_STORE:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._send_cors()
                self.end_headers()
                res = {"valid": True, "key": key, **LICENSE_STORE[key]}
                self.wfile.write(json.dumps(res).encode('utf-8'))
            elif key.startswith('SWIFT-VIP-') and len(key) >= 16:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._send_cors()
                self.end_headers()
                res = {
                    "valid": True,
                    "key": key,
                    "plan": "premium",
                    "planLabel": "VIP Pro Active",
                    "expiresAt": "2029-12-31T23:59:59Z",
                    "features": ["all_servers", "turbo_speed", "adblock_shield", "webrtc_guard", "unlimited_data"]
                }
                self.wfile.write(json.dumps(res).encode('utf-8'))
            else:
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self._send_cors()
                self.end_headers()
                res = {"valid": False, "error": "Invalid or expired key. Demo key: SWIFT-VIP-2026-PRO"}
                self.wfile.write(json.dumps(res).encode('utf-8'))
        else:
            self.send_response(404)
            self._send_cors()
            self.end_headers()

if __name__ == '__main__':
    print(f"==================================================")
    print(f"⚡ SwiftVPN Python Local Backend running on port {PORT}")
    print(f"👉 Health URL: http://localhost:{PORT}/api/health")
    print(f"👉 Servers URL: http://localhost:{PORT}/api/servers")
    print(f"👉 VIP Key: SWIFT-VIP-2026-PRO")
    print(f"==================================================")
    with socketserver.TCPServer(("", PORT), SwiftVPNHandler) as httpd:
        httpd.serve_forever()
