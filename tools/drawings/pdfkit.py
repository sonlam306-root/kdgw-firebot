# Ghép bộ bản vẽ FireBot thành PDF A3 ngang
import base64, math, os, subprocess
from PIL import Image
D = "/home/claude/firebot-3d/png"
OUT = "/home/claude/firebot-3d/pdf"; os.makedirs(OUT, exist_ok=True)
PW, PH = 1190, 842
TOTAL = 6
RED = "#c0392b"; INK = "#1b1b1b"; QUIET = "#555"; BLUE = "#2c5282"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

class Page:
    def __init__(self, n, title, sub):
        self.o = []; self.n = n; self.title = title; self.sub = sub
    def add(self, s): self.o.append(s)
    def rect(self, x, y, w, h, fill="none", stroke="#444", sw=1, rx=0, op=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def text(self, x, y, s, size=10, anchor="start", w="400", fill=INK, italic=False):
        st = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{fill}" font-family="DejaVu Sans"{st}>{esc(s)}</text>')
    def line(self, x1, y1, x2, y2, stroke="#888", sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
    def path(self, d, stroke="#444", sw=1, fill="none", dash=None, op=1):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" fill-opacity="{op}"{dd}/>')
    def circle(self, x, y, r, fill="white", stroke="#444", sw=1):
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def image(self, path, x, y, w, h):
        im = Image.open(path); iw, ih = im.size
        s = min(w/iw, h/ih); dw, dh = iw*s, ih*s; ox, oy = x+(w-dw)/2, y+(h-dh)/2
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        self.add(f'<image x="{ox:.1f}" y="{oy:.1f}" width="{dw:.1f}" height="{dh:.1f}" href="data:image/png;base64,{b64}"/>')
        return ox, oy, s
    def balloons(self, ox, oy, s, items, r=9):
        # items: (num, px, py, dx, dy) toạ độ ảnh gốc, độ lệch bóng theo pt
        for num, px, py, dx, dy in items:
            x, y = ox+px*s, oy+py*s; bx, by = x+dx, y+dy
            self.line(x, y, bx, by, RED, 0.8); self.circle(x, y, 1.6, RED, RED)
            self.circle(bx, by, r, "white", RED, 1); self.text(bx, by+3.5, str(num), 9.5, "middle", "700", RED)
    def table(self, x, y, cols, rows, widths, size=9, lh=15, head_fill="#eef2f7"):
        tw = sum(widths)
        self.rect(x, y, tw, lh, head_fill, "#999", 0.6)
        cx = x
        for c, w in zip(cols, widths): self.text(cx+4, y+lh-4.5, c, size, w="700"); cx += w
        for i, r in enumerate(rows):
            yy = y+lh*(i+1)
            self.rect(x, yy, tw, lh, "#ffffff" if i % 2 == 0 else "#f7f7f7", "#ccc", 0.4)
            cx = x
            for c, w in zip(r, widths): self.text(cx+4, yy+lh-4.5, c, size); cx += w
        return y+lh*(len(rows)+1)
    def svg(self):
        h = [f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 {PW} {PH}">',
             f'<rect width="{PW}" height="{PH}" fill="white"/>',
             f'<rect x="14" y="14" width="{PW-28}" height="{PH-28}" fill="none" stroke="#222" stroke-width="1.4"/>']
        h.append(f'<text x="30" y="44" font-size="20" font-weight="700" fill="{INK}" font-family="DejaVu Sans">{esc(self.title)}</text>')
        h.append(f'<text x="30" y="63" font-size="10.5" fill="{QUIET}" font-family="DejaVu Sans">{esc(self.sub)}</text>')
        # khung tên
        x0, y0, w, hh = PW-14-430, PH-14-62, 430, 62
        tb = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{hh}" fill="white" stroke="#222" stroke-width="1.2"/>',
              f'<line x1="{x0}" y1="{y0+22}" x2="{x0+w}" y2="{y0+22}" stroke="#222" stroke-width="0.8"/>',
              f'<line x1="{x0+300}" y1="{y0}" x2="{x0+300}" y2="{y0+hh}" stroke="#222" stroke-width="0.8"/>',
              f'<text x="{x0+8}" y="{y0+16}" font-size="11.5" font-weight="700" fill="{INK}" font-family="DejaVu Sans">FIREBOT — Robot chữa cháy chạy ray</text>',
              f'<text x="{x0+8}" y="{y0+37}" font-size="9.5" fill="{INK}" font-family="DejaVu Sans">{esc(self.title)}</text>',
              f'<text x="{x0+8}" y="{y0+53}" font-size="8.5" fill="{QUIET}" font-family="DejaVu Sans">Thiết kế: Trần Nguyễn Sơn Lâm · Concept v0.1 (trước M0)</text>',
              f'<text x="{x0+308}" y="{y0+16}" font-size="10" font-weight="700" fill="{INK}" font-family="DejaVu Sans">Tờ {self.n}/{TOTAL}</text>',
              f'<text x="{x0+308}" y="{y0+37}" font-size="9" fill="{INK}" font-family="DejaVu Sans">Khổ A3 · đơn vị mm</text>',
              f'<text x="{x0+308}" y="{y0+53}" font-size="9" fill="{INK}" font-family="DejaVu Sans">Ngày 25/11/2026</text>']
        return "\n".join(h + self.o + tb + ["</svg>"])

