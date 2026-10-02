"""
SwiftVPN Local Python Test Server v2.5
Zero external dependencies - runs directly on Python 3.x
Serves the exact same verified servers and endpoints as the Node.js Render backend:
  - GET  /health
  - GET  /api/health
  - GET  /api/ip
  - GET  /api/servers
  - POST /api/license/verify
"""

import http.server
import socketserver
import json
import time
import urllib.parse

PORT = 3000

VERIFIED_SERVERS = [
    {
        "id": "us-newyork-live",
        "name": "United States (New York)",
        "country": "US",
        "city": "New York / NJ",
        "flag": "🇺🇸",
        "host": "198.199.86.11",
        "port": 3128,
        "protocol": "http",
        "free": True,
        "category": "speed",
        "pingMs": 42,
        "loadPercent": 34,
        "description": "High-speed US East verified proxy node"
    },
    {
        "id": "in-bengaluru-live",
        "name": "India (Bengaluru Fast)",
        "country": "IN",
        "city": "Bengaluru Tech Hub",
        "flag": "🇮🇳",
        "host": "139.59.1.14",
        "port": 8080,
        "protocol": "http",
        "free": True,
        "category": "speed",
        "pingMs": 25,
        "loadPercent": 38,
        "description": "Low-latency domestic India route"
    },
    {
        "id": "tw-taipei-live",
        "name": "Taiwan (Asia East)",
        "country": "TW",
        "city": "Taipei",
        "flag": "🇹🇼",
        "host": "122.116.125.115",
        "port": 8888,
        "protocol": "http",
        "free": True,
        "category": "standard",
        "pingMs": 52,
        "loadPercent": 41,
        "description": "Fast East Asia transit node"
    },
    {
        "id": "jp-tokyo-live",
        "name": "👑 Japan (Tokyo VIP Ultra)",
        "country": "JP",
        "city": "Tokyo Gaming Center",
        "flag": "🇯🇵",
        "host": "54.238.38.227",
        "port": 8080,
        "protocol": "http",
        "free": False,
        "category": "gaming",
        "pingMs": 38,
        "loadPercent": 20,
        "description": "Ultra low-ping VIP Gaming node in Tokyo"
    },
    {
        "id": "in-mumbai-live",
        "name": "👑 India (Mumbai VIP Turbo)",
        "country": "IN",
        "city": "Mumbai Gigabit",
        "flag": "🇮🇳",
        "host": "45.194.41.141",
        "port": 8080,
        "protocol": "http",
        "free": False,
        "category": "streaming",
        "pingMs": 22,
        "loadPercent": 22,
        "description": "VIP Streaming optimized Mumbai tunnel"
    },
    {
        "id": "ch-europe-live",
        "name": "👑 Switzerland (Zurich VIP Privacy)",
        "country": "CH",
        "city": "Zurich Offshore",
        "flag": "🇨🇭",
        "host": "185.195.71.218",
        "port": 18080,
        "protocol": "http",
        "free": False,
        "category": "privacy",
        "pingMs": 48,
        "loadPercent": 18,
        "description": "Zero-log Swiss privacy node"
    }
]

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
                "verifiedServers": len(VERIFIED_SERVERS),
                "version": "2.5.0"
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
                "country": "Local / Test Gateway",
                "isProxied": False,
                "timestamp": int(time.time() * 1000)
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))

        elif path in ['/api/servers', '/api/servers/refresh']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": True,
                "totalServers": len(VERIFIED_SERVERS),
                "servers": VERIFIED_SERVERS
            }).encode('utf-8'))

        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self._send_cors()
            self.end_headers()
            html = f"""
            <html><body style="font-family:sans-serif;background:#060913;color:#e2e8f0;padding:40px;text-align:center;">
              <h1 style="color:#10b981;">⚡ SwiftVPN Cloud Master (Local)</h1>
              <p>Status: <b>ONLINE & VERIFIED</b> on port {PORT}</p>
              <p>Active Verified Servers: {len(VERIFIED_SERVERS)} Online</p>
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
    print(f"⚡ SwiftVPN Local Master running on port {PORT}")
    with socketserver.TCPServer(("", PORT), SwiftVPNHandler) as httpd:
        httpd.serve_forever()
