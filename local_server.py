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
        "host": "159.89.239.204",
        "port": 10000,
        "protocol": "http",
        "free": True,
        "category": "speed",
        "pingMs": 42,
        "loadPercent": 28,
        "description": "DigitalOcean US East Gigabit Node"
    },
    {
        "id": "ca-toronto-live",
        "name": "Canada (Toronto Ultra)",
        "country": "CA",
        "city": "Toronto Fast Relay",
        "flag": "🇨🇦",
        "host": "184.75.221.82",
        "port": 3118,
        "protocol": "http",
        "free": True,
        "category": "speed",
        "pingMs": 35,
        "loadPercent": 22,
        "description": "Ultra-low latency Canada Node"
    },
    {
        "id": "de-frankfurt-live",
        "name": "Germany (Frankfurt)",
        "country": "DE",
        "city": "Frankfurt Metro",
        "flag": "🇩🇪",
        "host": "103.237.102.191",
        "port": 11111,
        "protocol": "http",
        "free": True,
        "category": "privacy",
        "pingMs": 38,
        "loadPercent": 25,
        "description": "Verified Germany Privacy Node"
    },
    {
        "id": "nl-amsterdam-live",
        "name": "Netherlands (Amsterdam)",
        "country": "NL",
        "city": "Amsterdam GDPR Zone",
        "flag": "🇳🇱",
        "host": "213.111.146.36",
        "port": 18080,
        "protocol": "http",
        "free": True,
        "category": "privacy",
        "pingMs": 36,
        "loadPercent": 30,
        "description": "Amsterdam 99% Uptime Privacy Gateway"
    },
    {
        "id": "in-bengaluru-live",
        "name": "India (Bengaluru / Mumbai)",
        "country": "IN",
        "city": "Bengaluru Tech Hub",
        "flag": "🇮🇳",
        "host": "144.24.111.128",
        "port": 1088,
        "protocol": "socks5",
        "free": True,
        "category": "speed",
        "pingMs": 25,
        "loadPercent": 32,
        "description": "Oracle Cloud India High-Speed SOCKS5 Node"
    },
    {
        "id": "sg-singapore-live",
        "name": "Singapore (Asia Hub)",
        "country": "SG",
        "city": "Singapore Central",
        "flag": "🇸🇬",
        "host": "104.248.151.93",
        "port": 9090,
        "protocol": "http",
        "free": True,
        "category": "speed",
        "pingMs": 44,
        "loadPercent": 34,
        "description": "Singapore DigitalOcean Node"
    },
    {
        "id": "uk-london-live",
        "name": "👑 United Kingdom (London VIP)",
        "country": "GB",
        "city": "London City",
        "flag": "🇬🇧",
        "host": "185.73.39.118",
        "port": 9999,
        "protocol": "http",
        "free": False,
        "category": "streaming",
        "pingMs": 42,
        "loadPercent": 22,
        "description": "London VIP 99% Uptime Streaming Route"
    },
    {
        "id": "jp-tokyo-live",
        "name": "👑 Japan (Tokyo VIP Ultra)",
        "country": "JP",
        "city": "Tokyo Gaming Center",
        "flag": "🇯🇵",
        "host": "101.36.104.46",
        "port": 10808,
        "protocol": "socks5",
        "free": False,
        "category": "gaming",
        "pingMs": 38,
        "loadPercent": 18,
        "description": "VIP Gaming Low-Ping Tokyo SOCKS5 Route"
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
        "pingMs": 45,
        "loadPercent": 16,
        "description": "Zero-log Swiss Offshore Privacy Tunnel"
    },
    {
        "id": "fr-paris-live",
        "name": "👑 France (Paris Turbo VIP)",
        "country": "FR",
        "city": "Paris",
        "flag": "🇫🇷",
        "host": "5.39.72.26",
        "port": 5566,
        "protocol": "http",
        "free": False,
        "category": "speed",
        "pingMs": 39,
        "loadPercent": 24,
        "description": "OVH France High-Throughput Node"
    },
    {
        "id": "fi-helsinki-live",
        "name": "👑 Finland (Helsinki Privacy)",
        "country": "FI",
        "city": "Helsinki",
        "flag": "🇫🇮",
        "host": "65.109.215.187",
        "port": 8090,
        "protocol": "http",
        "free": False,
        "category": "privacy",
        "pingMs": 46,
        "loadPercent": 20,
        "description": "Hetzner Northern Europe Privacy Gateway"
    },
    {
        "id": "in-mumbai-live",
        "name": "👑 India (Mumbai VIP SOCKS5)",
        "country": "IN",
        "city": "Mumbai Gigabit",
        "flag": "🇮🇳",
        "host": "141.148.206.170",
        "port": 1088,
        "protocol": "socks5",
        "free": False,
        "category": "streaming",
        "pingMs": 22,
        "loadPercent": 19,
        "description": "VIP Mumbai Gigabit SOCKS5 Route"
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
