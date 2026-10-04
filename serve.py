import os
import urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 8080
DIRECTORY = "/home/piyush/13lgame-dummy"
UPSTREAM = "https://13lwin6.com"

class CloneHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Force browser to never cache old files
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        # If file doesn't exist locally, try fetching from 13lwin6.com with 1.5s timeout
        if not os.path.exists(path) and not path.endswith('/'):
            clean_path = self.path.split("?")[0]
            try:
                req_url = UPSTREAM + clean_path
                req = urllib.request.Request(req_url, headers={
                    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
                    "Referer": "https://13lwin6.com/"
                })
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    if resp.status == 200:
                        data = resp.read()
                        os.makedirs(os.path.dirname(path), exist_ok=True)
                        with open(path, "wb") as f:
                            f.write(data)
            except Exception:
                pass
        return super().send_head()

if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), CloneHandler)
    print(f"Threading clone server running on port {PORT}...")
    server.serve_forever()
