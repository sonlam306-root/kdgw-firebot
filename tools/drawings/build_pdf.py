# Ghép bộ bản vẽ FireBot thành PDF A3 ngang
import base64, math, os, subprocess
from PIL import Image
D = "/home/claude/firebot-3d/png"
OUT = "/home/claude/firebot-3d/pdf"; os.makedirs(OUT, exist_ok=True)
PW, PH = 1190, 842
TOTAL = 7
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
            for c, w in zip(r, widths):
                mc = int((w-8) / (size*0.52))
                if lh >= 2.6*size and len(c) > mc:
                    k = c.rfind(" ", 0, mc); k = k if k > 0 else mc
                    self.text(cx+4, yy+lh/2-2, c[:k], size); self.text(cx+4, yy+lh/2+size+0.5, c[k:].strip(), size)
                else:
                    self.text(cx+4, yy+lh-4.5, c, size)
                cx += w
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

pages = []

# ================= TỜ 1: TỔNG QUAN =================
p = Page(1, "Tổng quan hệ thống", "Ray 2 tầng chữ L dài ~5 m, cả 2 tầng có cuộn dây; trạm gọi cháy ESP32-S3-CAM → robot + bình cùng được đẩy tới, ngắm bằng cảm biến nhiệt, phun 4–5 m; trạm chính sạc + tiếp nước")
ox, oy, s = p.image(f"{D}/sys_iso.png", 26, 76, 790, 494)
p.balloons(ox, oy, s, [
    (1, 1740, 360, 0, 44), (2, 1700, 278, 30, -34), (3, 1850, 372, 24, 40), (4, 1610, 520, 34, 0),
    (5, 1454, 196, -10, -40), (6, 1452, 380, -40, 26), (7, 1400, 446, -36, 30), (8, 1040, 800, 30, -20),
    (9, 640, 1400, 34, -16), (10, 1830, 770, 34, 10), (11, 2000, 456, 34, 20), (12, 1130, 160, -34, -24),
    (13, 576, 446, -34, -20), (13, 1260, 900, 34, -20)])
p.text(840, 92, "Chú thích", 13, w="700")
p.table(840, 100, ["#", "Bộ phận"], [
    ["1", "Ray dưới nhôm 60×6 + cuộn dây động cơ tuyến tính"],
    ["2", "Ray trên nhôm 60×6 + cuộn dây (đẩy bình, ADR-10)"],
    ["3", "Thanh treo in 3D tại mỗi mối nối 0,5 m"],
    ["4", "Khung sắt lỗ: cột ~1,25 m + 2 thanh ngang"],
    ["5", "Bình nước 3–4 L trên bogie ray trên"],
    ["6", "Robot treo ngược (pin 12V, bơm, mạch)"],
    ["7", "Tay máy 3 khớp + đầu phun ống cứng"],
    ["8", "Tia nước, tầm 4–5 m (minh hoạ)"],
    ["9", "Khay lửa demo (phía B, ngoài chữ L)"],
    ["10", "Trạm chính: bể chứa + bơm tiếp nước"],
    ["11", "Hộp KD-GW + nút dừng khẩn (đầu tuyến)"],
    ["12", "Cua 90° R600 (module M5)"], ["13", "Trạm gọi cháy ×2 (ESP32-S3-CAM + IR + nút)"]], [26, 290])
yy = p.table(840, 318, ["Thông số", "Giá trị"], [
    ["Tổng chiều dài ray", "~4,94 m (2,5 + cua 0,94 + 1,5)"],
    ["Cao mép trên ray dưới", "1 200 mm so với sàn"],
    ["Khoảng 2 tầng ray", "200 mm (mép trên ray trên 1 460)"],
    ["Module ray", "9 module: M0–M4, M5 (cua), M6–M8"],
    ["Tốc độ", "1 m/s thẳng · 0,6 m/s trong cua"],
    ["Đẩy", "ĐC tuyến tính 3 pha, 12V"],
    ["Pin robot", "Li-ion 3S2P 12V + BMS"],
    ["Bình nước", "3–4 L, cảm biến mực nước liên tục"],
    ["Tầm phun", "4–5 m, đầu phun ~0,85 m so với sàn"]], [140, 176])
p.rect(840, yy+12, 316, 98, "#fdf2e9", "#e59866", 0.8, 4)
p.text(850, yy+30, "Quy ước bắt buộc", 10.5, w="700", fill="#a04000")
for i, t in enumerate(["Phía A (thanh treo, khung) luôn ở TRONG cua.",
                       "Phía B (cuộn dây, bogie, robot) luôn ở NGOÀI cua.",
                       "Phun được cả 2 phía (ADR-11); người xem không",
                       "đứng trong hướng phun khi chạy thử."]):
    p.text(850, yy+48+i*15, t, 9.5)
p.text(30, 592, "Hình phối cảnh dựng từ mô hình OpenSCAD tham số (firebot.scad + firebot_system.scad). Khối thân robot, bình, trạm là khối giữ chỗ — chi tiết in ở đợt 2.", 9, fill=QUIET, italic=True)
# sơ đồ luồng nhiệm vụ
fx, fy = 30, 616
p.text(fx, fy, "Luồng một nhiệm vụ", 12, w="700")
steps = ["Trạm gọi cháy báo", "KD-GW chọn điểm đích", "Ray đẩy robot + bình", "Cảm biến nhiệt ngắm", "Phun đến khi tắt", "Về trạm: sạc + tiếp nước"]
bw, gap = 128, 14
for i, st in enumerate(steps):
    x = fx + i*(bw+gap)
    p.rect(x, fy+12, bw, 34, "#eaf2f8" if i != 4 else "#d6eaf8", "#2e86c1", 1, 5)
    p.text(x+bw/2, fy+33, st, 9, "middle")
    if i < len(steps)-1:
        p.line(x+bw+1, fy+29, x+bw+gap-2, fy+29, "#2e86c1", 1.2)
        p.path(f"M{x+bw+gap-6} {fy+25} L{x+bw+gap-1} {fy+29} L{x+bw+gap-6} {fy+33}", "#2e86c1", 1.2)
p.text(fx, fy+66, "Dừng khẩn 2 lớp: nút cứng cắt nguồn ray qua công tắc tơ · robot tự ngắt bơm + phanh khi mất 3 nhịp heartbeat 100 ms.", 9.5)
p.text(fx, fy+82, "Phanh lò xo nhả bằng điện: mất điện = phanh. Nam châm ở phía ngoài cua nên khe hở chỉ tăng khi qua cua, không va cuộn dây.", 9.5)
pages.append(p)

# ================= TỜ 2: MẶT BẰNG =================
p = Page(2, "Mặt bằng tuyến ray", "Nhìn từ trên xuống · tỉ lệ ~1:35 · gốc toạ độ tại đầu tuyến (trạm chính), trục X dọc đoạn thẳng 1")
sc = 0.095; OX, OY = 186, 532
p.add('<clipPath id="c2"><rect x="20" y="76" width="720" height="672"/></clipPath><g clip-path="url(#c2)">')          # px/mm, gốc
P = lambda x, y: (OX + x*sc, OY - y*sc)
L1, R, L2 = 2500, 600, 1500
post_off = 137
# vùng phun minh hoạ
rx, ry = 1700, 0
for rr, op in ((5000, 0.10), (4000, 0.10)):
    pts = []
    for a in range(10, 171, 4):
        pts.append(P(rx + rr*math.cos(math.radians(a)), ry + rr*math.sin(math.radians(a))))
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    p.path(d, "#2e86c1", 0.8, dash="5 4")
for rr in (5000, 4000):
    pts = [P(rx + rr*math.cos(math.radians(a)), ry + rr*math.sin(math.radians(a))) for a in range(-170, -9, 4)]
    p.path("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts), "#e67e22", 0.8, dash="2 4")
x, y = P(rx + 600, 3250); p.text(x, y, "vòng tầm phun 4 m và 5 m phía B (robot đứng ở X = 1 700)", 9, "middle", fill="#1f618d")
x, y = P(rx - 900, -1900); p.text(x, y, "phía A cũng phun được (ADR-11), né cột ≥ 100 mm", 9, "middle", fill="#b9770e")
# ray: thẳng 1
def railpath(off):
    a = P(0, off); b = P(L1, off)
    cx, cy = P(L1, -R)
    rr = (R + off)*sc
    c = P(L1 + R + off, -R); d = P(L1 + R + off, -R - L2)
    return f"M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f} A{rr:.1f} {rr:.1f} 0 0 1 {c[0]:.1f} {c[1]:.1f} L{d[0]:.1f} {d[1]:.1f}"
p.path(railpath(0), "#7f8c8d", 4)
p.path(railpath(12), "#1e8449", 2)          # cuộn dây phía B (ngoài)
p.path(railpath(-post_off), BLUE, 1.2, dash="6 3")   # thanh sắt lỗ ngang
# mối nối module + tên module
def at(sv, off=0):
    if sv <= L1: return (sv, off), 0
    if sv <= L1 + math.pi*R/2:
        a = (sv - L1)/R
        return (L1 + (R+off)*math.sin(a), -R + (R+off)*math.cos(a)), a
    return (L1 + R + off, -R - (sv - L1 - math.pi*R/2)), math.pi/2
Lc = math.pi*R/2
joints = [0, 500, 1000, 1500, 2000, 2500, L1+Lc, L1+Lc+500, L1+Lc+1000, L1+Lc+1500]
for sv in joints + [L1 + Lc/2]:
    (x0, y0), a = at(sv, -12); (x1, y1), _ = at(sv, -60)
    p.line(*P(x0, y0), *P(x1, y1), "#e67e22", 3)
for sv in joints:
    (x0, y0), a = at(sv, 40); (x1, y1), _ = at(sv, -40)
    p.line(*P(x0, y0), *P(x1, y1), INK, 1)
names = ["M0", "M1", "M2", "M3", "M4", "M5 cua", "M6", "M7", "M8"]
mids = [250, 750, 1250, 1750, 2250, L1+Lc/2, L1+Lc+250, L1+Lc+750, L1+Lc+1250]
for nm, sv in zip(names, mids):
    (x, y), a = at(sv, 260)
    p.text(*P(x, y), nm, 9.5, "middle", "700")
# cột
posts = [0, 1250, 2500, L1+Lc/2, L1+Lc, L1+Lc+750, L1+Lc+1500]
for sv in posts:
    (x, y), a = at(sv, -post_off)
    X, Y = P(x, y); p.rect(X-3, Y-3, 6, 6, BLUE, BLUE)
# trạm chính, bể, KD-GW
X, Y = P(150, 570); p.rect(X, Y, 300*sc, 220*sc, "#aed6f1", "#2e86c1", 1)
p.text(X + 150*sc, Y - 5, "Bể 10 L + bơm", 8.5, "middle")
X, Y = P(-30, -150); p.rect(X, Y, 150*sc, 100*sc, "#eeeeee", "#555", 1)
p.text(X - 4, Y + 10, "KD-GW + dừng khẩn", 8.5, "end")
X, Y = P(80, 120); p.rect(X, Y, 340*sc, 170*sc, "#d6eaf8", "#2e86c1", 1, op=0.7)
p.text(P(250, 0)[0], P(0, -380)[1], "Robot ở trạm (sạc + tiếp nước)", 8.5, "middle", fill="#1f618d")
# khay lửa + camera
fx_, fy_ = 2000, 4300
X, Y = P(fx_, fy_); p.circle(X, Y, 100*sc, "#e74c3c", "#922b21"); p.text(X + 16, Y + 4, "Khay lửa demo (ví dụ)", 9)
for cx_, cy_, nm in ((700, 3700, "Trạm gọi cháy 1"), (3300, 2400, "Trạm gọi cháy 2")):
    X, Y = P(cx_, cy_); p.rect(X-5, Y-5, 10, 10, "#c0392b", "#922b21"); p.text(X + 9, Y + 4, nm + " (ESP32-S3-CAM)", 9)
# robot đang chạy
X, Y = P(rx, 0); p.rect(X - 170*sc, Y - 120*sc, 340*sc, 170*sc, "#5dade2", "#1f618d", 1)
p.text(X, Y + 30, "Robot", 9, "middle", "700", "#1f618d")
p.add('</g>')
# kích thước
def dimx(x1, x2, y, label, off=0):
    a = P(x1, y); b = P(x2, y)
    p.line(a[0], a[1], b[0], b[1], RED, 1); p.line(a[0], a[1]-5, a[0], a[1]+5, RED, 1); p.line(b[0], b[1]-5, b[0], b[1]+5, RED, 1)
    p.text((a[0]+b[0])/2, a[1]-5+off, label, 9.5, "middle", fill=RED)
def dimy(x, y1, y2, label):
    a = P(x, y1); b = P(x, y2)
    p.line(a[0], a[1], b[0], b[1], RED, 1); p.line(a[0]-5, a[1], a[0]+5, a[1], RED, 1); p.line(b[0]-5, b[1], b[0]+5, b[1], RED, 1)
    p.text(a[0]+6, (a[1]+b[1])/2+4, label, 9.5, fill=RED)
dimx(0, L1, -900, "2 500 (5 module × 500)")
dimy(L1 + R + 500, -R, -R - L2, "1 500 (3 × 500)")
dimx(0, 500, -1250, "500")
cx, cy = P(L1, -R); p.line(cx, cy, *P(L1 + R*0.707, -R + R*0.707), RED, 1, "3 2"); p.text(cx - 6, cy + 14, "R600 (tâm ray)", 9.5, "end", fill=RED)
p.circle(cx, cy, 2, RED, RED)
dimy(-450, 0, -post_off, "137")
p.text(P(-450, 0)[0] - 4, P(0, -post_off)[1] + 22, "tâm ray → tâm cột", 8, "end", fill=RED)
# chú giải
lx, ly = 760, 470
p.text(lx, ly, "Ký hiệu", 12, w="700")
leg = [("#7f8c8d", 4, None, "Tâm ray (2 tầng trùng nhau khi nhìn bằng)"), ("#1e8449", 2, None, "Cuộn dây — phía B, ngoài cua"),
       (BLUE, 1.2, "6 3", "Thanh sắt lỗ ngang — phía A, trong cua"), ("#e67e22", 3, None, "Thanh treo tại mối nối / giữa cua"),
       (INK, 1, None, "Ranh giới module"), ("#2e86c1", 0.8, "5 4", "Tầm phun 4 m và 5 m")]
for i, (c, w, dsh, t) in enumerate(leg):
    yy = ly + 20 + i*18
    p.line(lx, yy - 4, lx + 34, yy - 4, c, w, dsh); p.text(lx + 44, yy, t, 9.5)
p.rect(lx - 2, ly + 128, 8, 8, BLUE, BLUE); p.text(lx + 44, ly + 137, "Cột sắt lỗ đứng (7 cột)", 9.5)
p.rect(lx, ly + 158, 400, 110, "#f4f6f7", "#bbb", 0.6, 4)
for i, t in enumerate(["Đặt tuyến sao cho phía ngoài chữ L (phía B) là khoảng trống trong phòng:",
                       "vùng phun chính. Phía trong chữ L có khung nhưng vẫn phun được (né cột).",
                       "Trạm chính ở M0 (đầu đoạn thẳng 1), cuối M8 có tấm chặn.",
                       "2 trạm gọi cháy trên chân máy ảnh, mỗi trạm gắn sẵn 1 điểm đích trên ray.",
                       "Vị trí khay lửa và trạm gọi cháy trên hình chỉ là ví dụ."]):
    p.text(lx + 10, ly + 176 + i*17, t, 9.2)
pages.append(p)

# ================= TỜ 3: MẶT CẮT RAY =================
p = Page(3, "Mặt cắt ngang ray & cao độ", "Nhìn dọc theo ray · cao độ so với sàn · chi tiết ray dưới (các số đo trong mô hình tham số)")
p.image(f"{D}/section_drawing.png", 22, 70, 1146, 700)
pages.append(p)

# ================= TỜ 4: ROBOT =================
p = Page(4, "Robot, bình nước & tay máy", "Robot treo ngược dưới ray dưới; bình 3–4 L chạy trên ray trên; cả 2 bogie đều có nam châm và được đẩy cùng pha, nối bằng thanh ty M8")
ox, oy, s = p.image(f"{D}/robot_iso.png", 22, 72, 560, 460)
p.balloons(ox, oy, s, [
    (1, 720, 300, -60, -10), (2, 815, 160, -50, -10), (3, 902, 215, 60, -10), (4, 770, 395, -70, -20), (5, 763, 540, -70, 0),
    (6, 906, 600, 70, -10), (7, 990, 700, 70, 0), (8, 960, 790, 80, 10), (9, 985, 826, 80, 36), (10, 870, 960, 70, 60),
    (11, 745, 1010, 70, 25), (12, 705, 1085, -80, 10), (13, 695, 1160, 40, 40), (14, 592, 1152, -10, -60), (15, 603, 1200, 20, 40), (16, 515, 1205, -40, 20),
    (17, 840, 440, -40, 30)])
# mặt đứng (YZ) có kích thước
ex, ey = 600, 72      # khung vẽ
p.text(ex, ey + 14, "Mặt đứng nhìn dọc ray (cao độ so với sàn, mm)", 11.5, w="700")
zs, ys = 0.52, 0.52
EY0, EZ0 = ex + 190, ey + 40 + 1700*zs - 700*zs   # Y=0 tại EY0; Z=1700 ở đỉnh khung
E = lambda yv, zv: (EY0 + yv*ys, ey + 40 + (1700 - zv)*zs)
def er(y0, z0, y1, z1, fill, stroke="#555", op=1):
    a = E(y0, z1); p.rect(a[0], a[1], (y1-y0)*ys, (z1-z0)*zs, fill, stroke, 0.8, op=op)
# cột + thanh treo
er(-157, 700, -117, 1700, "#aec6e0", BLUE)
for zb in (1140, 1400):
    er(-117, zb+10, -11, zb+50, "#fad7a0", "#b9770e"); er(-123, zb-8, -117, zb+68, "#f0a020", "#b9770e")
    er(-3, zb, 3, zb+60, "#bbbbbb")
    er(21, zb-17, 33, zb+77, "#f7dc6f", "#b7950b", 0.8)
    for zc in (zb-9, zb+69): er(-3.5, zc-11, 3.5, zc+11, "#555", "#222")
er(6, 1155, 18, 1185, "#c47a3a", "#7e4a1a")           # cuộn
er(21, 1155, 26, 1185, "#e74c3c", "#922b21")          # nam châm
er(35, 1090, 55, 1156, "#d4ac0d", "#9a7d0a"); er(35, 1444, 55, 1492, "#d4ac0d", "#9a7d0a")
er(-50, 910, 120, 1090, "#5dade2", "#1f618d", 0.85)    # thân
er(-25, 1492, 135, 1500, "#c8a97e", "#8d6e63")
er(-15, 1500, 135, 1620, "#aed6f1", "#2e86c1", 0.9)
er(25, 1620, 65, 1638, "#eeeeee", "#777")
p.line(*E(44.6, 1209), *E(44.6, 1391), INK, 2.2)
p.line(*E(115, 1090), *E(115, 1500), "#1a5276", 2.6)
er(5, 880, 65, 910, "#888", "#444")
# tay máy (mặt phẳng YZ)
pts = [(35, 862), (142, 772), (258, 803), (416, 845)]
ptsA = [(35, 862), (-72, 772), (-188, 803), (-346, 845)]
p.path("M" + " L".join(f"{E(*q)[0]:.1f} {E(*q)[1]:.1f}" for q in ptsA[:3]), "#f1948a", 5, dash="6 3")
p.path(f"M{E(*ptsA[2])[0]:.1f} {E(*ptsA[2])[1]:.1f} L{E(*ptsA[3])[0]:.1f} {E(*ptsA[3])[1]:.1f}", "#d4ac0d", 2, dash="5 3")
xx_, yy_ = E(-200, 760); p.text(xx_, yy_, "tư thế phun phía A (ADR-11)", 8.5, "middle", fill=RED)
p.path("M" + " L".join(f"{E(*q)[0]:.1f} {E(*q)[1]:.1f}" for q in pts[:3]), "#e74c3c", 7)
p.path(f"M{E(*pts[2])[0]:.1f} {E(*pts[2])[1]:.1f} L{E(*pts[3])[0]:.1f} {E(*pts[3])[1]:.1f}", "#b7950b", 3)
for q in pts[:3]: p.circle(*E(*q), 5, INK, INK)
# tia nước
# nhãn
labs = [((60, 1000), "Thân robot 340×170×180", "start", (200, 1000)), ((60, 1560), "Bình ~4 L (220×150×120)", "start", (200, 1560)),
        ((44.6, 1300), "Thanh ty M8", "start", (60, 1300)), ((115, 1240), "Ống nước bình → bơm", "start", (130, 1240)),
        ((-140, 1720), "Sắt lỗ", "middle", (-137, 1690))]
for (yv, zv), t, anc, (ly_, lz) in labs:
    xx, yy = E(ly_, lz); p.text(xx, yy, t, 9, anc)
# kích thước cao độ
def dz(yv, z1, z2, label, side=-1):
    a = E(yv, z1); b = E(yv, z2)
    p.line(a[0], a[1], b[0], b[1], RED, 0.9); p.line(a[0]-4, a[1], a[0]+4, a[1], RED, 0.9); p.line(b[0]-4, b[1], b[0]+4, b[1], RED, 0.9)
    p.text(a[0] + (6 if side > 0 else -6), (a[1]+b[1])/2 + 3, label, 9, "start" if side > 0 else "end", fill=RED)
def lvl(z, label):
    a = E(-350, z); b = E(470, z)
    p.line(a[0], a[1], b[0], b[1], RED, 0.5, "3 3"); p.text(b[0] + 6, b[1] + 3, label, 9, "start", fill=RED)
for z, lb in ((1638, "+1 638 đỉnh nắp bình"), (1460, "+1 460 mép trên ray trên"), (1200, "+1 200 mép trên ray dưới"),
              (1090, "+1 090 nóc thân robot"), (910, "+910 đáy thân robot"), (845, "+~845 đầu phun (tư thế vẽ)")):
    lvl(z, lb)
dz(140, 910, 1090, "180", 1); dz(150, 1500, 1620, "120", 1)
p.text(ex + 4, ey + 40 + 1000*zs + 18, "Sàn ở cao độ 0 (không vẽ, phần dưới 700 mm được cắt bỏ).", 8.5, fill=QUIET, italic=True)
# bảng chú thích robot
p.text(30, 548, "Chú thích hình phối cảnh", 11.5, w="700")
rows = [["1", "Bình nước 3–4 L, vách chắn sóng"], ["2", "Miệng rót (trạm rót từ trên xuống)"], ["3", "Cảm biến điện dung chống tràn"],
        ["4", "Bogie ray trên (4 bánh rãnh U)"], ["5", "Thanh ty M8 nối 2 tầng"], ["6", "Ống nước bình → bơm"],
        ["7", "Bogie ray dưới + 4 nam châm"], ["8", "Giá treo thân từ chốt xoay"], ["9", "Tấm đồng sạc trên lưng robot"]]
rows2 = [["10", "Thân: pin 3S, bơm 12V, mạch ESP32-S3"], ["11", "Khớp 1 — xoay ngang"], ["12", "Khâu 1 + khớp 2 (vai)"],
         ["13", "Khớp 3 (khuỷu)"], ["14", "MLX90640 ngắm lửa"], ["15", "Van điện từ chống nhỏ giọt"],
         ["16", "Đầu phun ống cứng 150 mm"], ["17", "Bánh rãnh U Ø22 ôm mép ray"], ["", "Ống nước đi trong lòng tay máy"]]
p.table(30, 556, ["#", "Bộ phận"], rows, [24, 230], 8.6, 13.6)
p.table(294, 556, ["#", "Bộ phận"], rows2, [24, 260], 8.6, 13.6)
pages.append(p)

# ================= TỜ 5: RAY & BOGIE =================
p = Page(5, "Ray, động cơ tuyến tính & bogie", "Một module thẳng 500 mm: 15 cuộn dây (3 pha × 5), dải Hall ở đoạn giá đầu, thanh treo tại 2 mối nối")
ox, oy, s = p.image(f"{D}/lower_iso_B.png", 22, 72, 600, 450)
p.balloons(ox, oy, s, [(1, 380, 205, -30, -36), (2, 470, 330, -40, 40), (3, 1048, 512, 40, 40), (4, 640, 470, 30, 70), (5, 600, 440, -50, 60),
                       (6, 742, 360, 30, -40), (7, 300, 255, -20, -40), (8, 1000, 468, 30, -50)])
ox, oy, s = p.image(f"{D}/assembly_B.png", 630, 72, 520, 372)
p.text(640, 462, "Một module 2 tầng: cuộn dây ở cả 2 ray, 2 bogie có nam châm nối bằng thanh ty; robot / bình là khối giữ chỗ.", 9, fill=QUIET, italic=True)
y2 = p.table(30, 540, ["#", "Chi tiết", "In / mua", "Số lượng (cả tuyến)"], [
    ["1", "Thanh treo + nối ray (hanger)", "In PETG", "22"],
    ["2", "Bobbin cuộn dây 28×30, quấn ~250 vòng Ø0,5", "In PETG", "300 (2 tầng)"],
    ["3", "Giá cuộn có dải 3 Hall (coil_seg_hall)", "In PETG", "8"],
    ["4", "Bogie dưới + trên — túi 4 nam châm 20×30×5", "In PETG", "2 + 2"],
    ["5", "Khối chốt xoay M6 (liền bogie)", "—", "—"],
    ["6", "Vòng bi U626ZZ + trục M6 12.9, ống lót", "Mua", "16"],
    ["7", "Ray nhôm dẹt 60×6", "Mua", "~10 m (2 tầng)"],
    ["8", "Giá cuộn thường / cong R600", "In PETG", "40 / 12"]], [24, 270, 90, 140], 9, 15)
p.table(640, 476, ["Thông số động cơ", "Giá trị"], [
    ["Bước cực τ", "22,5 mm"], ["Bước cuộn", "30 mm (3 cuộn / 4 cực)"], ["Cuộn / module", "15 = 3 pha × 5"],
    ["Hall", "3 cái cách 15 mm (120° điện)"], ["Khe hở cuộn–nam châm", "3 mm"], ["Nam châm / bogie", "4 viên NdFeB, xen kẽ N-S"],
    ["Lực cần đạt (cổng M0)", "≥ 5 N liên tục, ~8 N đỉnh"], ["Cấp điện", "12V, 2 driver/module, chỉ module có robot"]], [170, 200], 9, 15)
p.rect(640, 640, 520, 66, "#fdf2e9", "#e59866", 0.8, 4)
p.text(650, 658, "Vì sao cuộn dây ở phía ngoài cua", 10.5, w="700", fill="#a04000")
p.text(650, 675, "Dãy nam châm thẳng dài ~88 mm đi qua cua R600 lệch khỏi ray khoảng 1,6 mm ở hai đầu.", 9.3)
p.text(650, 690, "Cuộn ở phía ngoài: khe hở chỉ tăng (3 → ~4,6 mm, lực giảm nhẹ). Cuộn ở phía trong: nam châm va cuộn.", 9.3)
pages.append(p)

# ================= TỜ 6: TRẠM CHÍNH =================
p = Page(6, "Trạm chính (M0): sạc pin & tiếp nước", "Robot nghỉ ở module M0; KD-GW điều khiển relay sạc, bơm tiếp nước, đọc phao bể chứa; nút dừng khẩn đặt cạnh hộp")
ox, oy, s = p.image(f"{D}/station_iso.png", 22, 72, 640, 480)
p.balloons(ox, oy, s, [(1, 850, 60, 60, 20), (2, 668, 300, -50, 0), (3, 685, 1080, 50, -20), (4, 600, 1130, -50, 0), (5, 1125, 530, 50, 30),
                       (6, 990, 445, 40, -60), (7, 1030, 410, 60, -30), (8, 865, 515, -60, 40)])
p.table(690, 80, ["#", "Bộ phận"], [["1", "Bình robot — miệng rót hướng lên"], ["2", "Ống + vòi rót từ trên xuống"], ["3", "Bơm tiếp nước 12V"],
                                    ["4", "Bể chứa ~10 L trên giá, có phao báo cạn"], ["5", "Hộp KD-GW + nút dừng khẩn"],
                                    ["6", "Giá 2 má đồng lò xo (chỉ có điện khi robot vào trạm)"], ["7", "Tấm chặn cuối ray"], ["8", "Robot đang ở trạm"]], [24, 420], 9.5, 16)
p.text(690, 250, "Trình tự tại trạm", 12, w="700")
seq = ["Robot vào M0 → công tắc hành trình + homing vị trí → đóng phanh.",
       "KD-GW đóng relay sạc (CC/CV 12,6 V ~2 A) qua 2 má đồng.",
       "Nếu mực nước < 95 %: bật bơm tiếp nước, ngắt khi cảm biến đỉnh báo đầy.",
       "Bể chứa cạn (phao) → báo dashboard, không bơm khô.",
       "Có báo cháy: ngắt sạc + bơm → nhả phanh → robot rời trạm ≤ 2 s.",
       "Má sạc đặt cao, phía đối diện vòi; máng hứng dưới vòi rót."]
for i, t in enumerate(seq):
    p.circle(700, 268 + i*20, 7, "#2e86c1", "#2e86c1"); p.text(700, 271.5 + i*20, str(i+1), 8.5, "middle", "700", "white")
    p.text(714, 272 + i*20, t, 9.5)
p.rect(690, 400, 460, 120, "#f4f6f7", "#bbb", 0.6, 4)
p.text(700, 418, "Tiếp theo (đợt 2 in 3D & mạch in)", 10.5, w="700")
for i, t in enumerate(["Thân robot kín nước + hộp pin; tay máy 3 khớp có đường ống trong lòng; đầu phun ống cứng.",
                       "Bogie bình + khay đỡ; giá má sạc; vòi rót; giá giữ bể chứa.",
                       "Mạch module ray: ESP32-C3 + driver 3 pha + 3 Hall + RS485 (×9).",
                       "Mạch robot: ESP32-S3, MOSFET bơm/van/phanh, I2C MLX90640, đo pin.",
                       "Trạm chính dùng KD-GW sẵn có (profile kdgw-firebot)."]):
    p.text(700, 438 + i*16, "• " + t, 9.2)
pages.append(p)

# ================= TỜ 7: PHUN 2 BÊN RAY =================
p = Page(7, "Phun hai bên ray (ADR-11)", "Khớp 1 xoay 270°: cùng một tay máy phun được phía B (ngoài) và phía A (trong, phía khung) — bên nào có cháy thì phun bên đó")
ox, oy, s = p.image(f"{D}/robot_2ben.png", 22, 72, 700, 428)
p.text(30, 520, "Nhìn dọc ray. Tay máy đậm: phun phía B; tay máy nhạt: phun phía A. Cột sắt lỗ vẽ ở xa phía sau (khác vị trí X), tia nước minh hoạ.", 9, fill=QUIET, italic=True)
y = p.table(740, 80, ["Hạng mục", "Quy định"], [
    ["Khớp 1 (xoay ngang)", "DS3225 bản 270°: 0° = dọc ray, +90° = phía B, −90° = phía A, tối đa ±135°"],
    ["Gốc tay máy", "Dời về giữa đáy thân (X 110, Y 35) để 2 bên đối xứng"],
    ["Ống nước", "PU 8×5 đi qua tâm khớp 1, chừa vòng ống cho ±135°"],
    ["Chọn phía", "Mỗi trạm gọi cháy khai sẵn điểm đích s + phía A/B"],
    ["Không rõ phía", "MLX90640 quét yaw −135…+135°, chọn điểm nóng nhất"],
    ["Cột phía A", "Cột ~1,25 m/cột: robot dừng lệch tâm cột ≥ 100 mm"],
    ["Góc cấm", "Firmware cấm yaw có tia trúng cột (±3° quanh cột)"],
    ["Thanh ngang khung", "Cao 1 155 mm; đầu phun ~840 mm, tia qua cột khi còn thấp"],
    ["Khi chạy", "Tay về tư thế đỗ (yaw 0°, gập dọc ray); chỉ mở tay khi đã dừng + đóng phanh"],
    ["Vùng cấm", "Không phun phía A trong module M0 (hộp KD-GW, bể nước)"],
    ["Khoảng cách lửa", "Phía A: cách hàng cột ≥ 0,6 m; tầm phun 4–5 m mỗi bên"]], [118, 306], 8.8, 28)
p.text(740, y + 30, "Trình tự phun", 12, w="700")
for i, t in enumerate(["Nhận lệnh: điểm đích s + phía (A/B) từ trạm gọi cháy qua KD-GW.",
                       "Ray đẩy robot + bình tới s; nếu phía A thì cộng bù để lệch cột ≥ 100 mm.",
                       "Đóng phanh → khớp 1 quay ±90° về phía có cháy → MLX90640 ngắm.",
                       "Mở van + bơm; vòng kín MLX chỉnh yaw/pitch cho tới khi điểm nóng tắt.",
                       "Tắt bơm, đóng van → tay về tư thế đỗ → nhả phanh → về trạm M0."]):
    p.text(740, y + 50 + i*16, f"{i+1}. {t}", 9.2)
pages.append(p)

files = []
for pg in pages:
    sv = f"{OUT}/page{pg.n}.svg"; pf = f"{OUT}/page{pg.n}.pdf"
    open(sv, "w").write(pg.svg())
    subprocess.run(["rsvg-convert", "-f", "pdf", "-o", pf, sv], check=True)
    files.append(pf)
subprocess.run(["pdfunite", *files, "/home/claude/firebot-3d/FireBot_ban_ve_tong_the.pdf"], check=True)
print("ok")
