#!/usr/bin/env python3
"""Static preview server WITH HTTP Range support, so <video> can seek.

Python's stock http.server ignores Range headers and always returns 200 with
the whole file, which makes browsers treat the video as unseekable. Netlify
serves Range correctly in production; this closes the gap locally.

Usage: python3 range_server.py <port> <directory>
"""
import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class RangeHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        rng = self.headers.get("Range")
        if not rng:
            return super().send_head()

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None

        size = os.fstat(f.fileno()).st_size
        m = re.match(r"bytes=(\d*)-(\d*)$", rng.strip())
        if not m:
            f.close()
            self.send_error(400, "Malformed Range header")
            return None

        start_s, end_s = m.groups()
        if start_s:
            start = int(start_s)
            end = int(end_s) if end_s else size - 1
        else:  # suffix form: bytes=-N means the last N bytes
            if not end_s:
                f.close()
                self.send_error(400, "Malformed Range header")
                return None
            start = max(0, size - int(end_s))
            end = size - 1
        end = min(end, size - 1)

        if start >= size or start > end:
            f.close()
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None

        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        f.seek(start)
        return _Slice(f, end - start + 1)

    def end_headers(self):
        if not self._headers_buffer or not any(
            b.lower().startswith(b"accept-ranges") for b in self._headers_buffer
        ):
            self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


class _Slice:
    """File wrapper that stops after n bytes, so copyfile sends only the range."""

    def __init__(self, f, n):
        self.f, self.left = f, n

    def read(self, amt=-1):
        if self.left <= 0:
            return b""
        if amt is None or amt < 0:
            amt = self.left
        data = self.f.read(min(amt, self.left))
        self.left -= len(data)
        return data

    def close(self):
        self.f.close()


if __name__ == "__main__":
    port, directory = int(sys.argv[1]), sys.argv[2]
    handler = partial(RangeHandler, directory=directory)
    ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
