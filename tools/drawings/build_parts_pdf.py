# Catalog chi tiết in 3D FireBot (đợt 1 + 2) → PDF A3
import json, subprocess, textwrap
import pdfkit as K
from pdfkit import Page, INK, QUIET, RED
TH = "/home/claude/firebot-3d/thumbs"; P2 = "/home/claude/firebot-3d/png2"
st = json.load(open("/tmp/partstats.json"))
G = [
 ("Ray & động cơ", [
  ("hanger", "Thanh treo + nối ray", "PETG 4 tường 40 %, in nằm nghiêng. Có thể thay bằng ke sắt lỗ + tấm kẹp in (đỡ ~3 kg nhựa)."),
  ("bobbin", "Bobbin cuộn dây", "PETG 3 tường 25 %. Quấn ~250 vòng dây emay Ø0,5."),
  ("coil_seg", "Giá cuộn dây thẳng", "Ray dưới 16 + ray trên 24 (ray trên không cần Hall). Bắt M3 xuyên ray."),
  ("coil_seg_hall", "Giá cuộn có dải Hall", "Đoạn đầu mỗi module; 3 khe Hall TO-92 cách 15 mm."),
  ("coil_seg_curve", "Giá cuộn cong R600", "Cho module cua M5; in đứng."),
  ("bogie_lower", "Bogie ray dưới", "PETG 5 tường 50 %. Túi 4 nam châm 20×30×5 + thép lót 1,5 mm."),
  ("bogie_upper", "Bogie ray trên", "Có túi 4 nam châm như bogie dưới (ADR-10); tai thanh ty M8 ở mặt dưới."),
  ("spacer", "Ống cách trục bánh", "Hoặc ống nhôm 5/9 mm cắt sẵn."),
  ("jig", "Dưỡng khoan lỗ thanh treo", "Chụp mép trên ray, tì đầu ray vào gờ chặn."),
  ("end_stop", "Chặn cuối ray", "Đệm cao su + hốc công tắc KW11; bắt chung bulông thanh treo cuối.")]),
 ("Thân robot", [
  ("body_front", "Thân robot — nửa trước", "PETG/ASA 3 tường 20 %, in úp (nóc xuống bàn). Khe thông gió hông."),
  ("body_rear", "Thân robot — nửa sau", "Hốc tấm đồng sạc trên nóc, lỗ ống nước vào, lỗ PG7."),
  ("lid_front", "Nắp đáy trước", "Rãnh gioăng 2 mm; lỗ bắt đế tay máy + lỗ ống nước ra."),
  ("lid_rear", "Nắp đáy sau", "Lỗ bắt giá bơm và hộp pin."),
  ("hanger_robot", "Giá treo thân từ chốt xoay", "PETG 6 tường 50 %. Ôm khối chốt bogie, bulông M6 làm trục."),
  ("battery_box", "Hộp pin kín", "Pin 3S2P 18650 + BMS; 4 trụ ốc cấy nắp."),
  ("battery_lid", "Nắp hộp pin", "Có rãnh gioăng."),
  ("pump_cradle", "Giá bơm màng 12V", "2 yên Ø40, khe dây rút; lót cao su chống rung."),
  ("electronics_tray", "Khay mạch robot", "Mạch 80×60 + ESP32-S3 DevKit.")]),
 ("Tay máy 3 khớp", [
  ("arm_base", "Đế khớp 1 (xoay ngang)", "Servo DS3225 đứng, trục xuống; bắt dưới nắp đáy trước."),
  ("yaw_plate", "Bàn xoay + khối khớp 2", "Cần support cho khe servo nằm ngang."),
  ("link1", "Khâu 1 — 140 mm", "Càng ôm khớp 2, khối servo khớp 3; ống PU 8×5 trong lòng."),
  ("link2", "Khâu 2 — 120 mm, đầu phun", "Kẹp ống phun cứng Ø10, đế van điện từ, đế MLX90640.")]),
 ("Bình nước", [
  ("hanger_tank", "Giá đỡ khay từ chốt xoay", "Giống giá treo thân nhưng hướng lên."),
  ("tank_tray_front", "Khay đỡ bình — nửa trước", "Ghép 2 nửa bằng M4 ở gờ giữa."),
  ("tank_tray_rear", "Khay đỡ bình — nửa sau", "Có lỗ Ø21 cho đầu ra bình."),
  ("tank_baffle", "Vách chắn sóng", "Chèn ngang trong bình nhựa 4 L."),
  ("level_clip", "Kẹp cảm biến mực nước", "Giữ cảm biến điện dung chống tràn, dây đai."),
  ("fill_funnel", "Phễu rót", "Gắn vào nắp bình, đón vòi rót của trạm.")]),
 ("Trạm chính", [
  ("charge_holder", "Giá má sạc", "Bắt thanh sắt lỗ ngang, 2 tiếp điểm lò xo Ø7 (+/−)."),
  ("refill_holder_a", "Giá vòi rót — mảnh A", "Bắt thanh sắt lỗ ngang ray trên."),
  ("refill_holder_b", "Giá vòi rót — mảnh B", "Tay vươn tới miệng bình, kẹp ống Ø10.")]),
 ("Trạm gọi cháy & hộp mạch", [
  ("call_box", "Hộp trạm gọi cháy", "ESP32-S3-CAM + cảm biến lửa + nút Ø16 + LED + còi; đế ren 1/4\"."),
  ("call_lid_1", "Nắp trạm gọi cháy (1, 2)", "Chữ nổi 'GỌI CHÁY / TRẠM n'. Có file cho trạm 1 và 2."),
  ("module_box", "Hộp mạch module ray", "2 lỗ PG7, tai rãnh M8 bắt sắt lỗ."),
  ("module_lid_M3", "Nắp hộp module (M0…M8)", "Chữ nổi số module; 9 file riêng.")])]
QTY_OVERRIDE = {"call_lid_1": 2, "module_lid_M3": 9, "coil_seg": 40, "coil_seg_curve": 12, "bobbin": 300}
K.TOTAL = 6
pages = []

# ---- Tờ 1: tổng quan ----
pg = Page(1, "Chi tiết in 3D — tổng quan đợt 1 + 2", "Toàn bộ chi tiết in cho ray, robot, tay máy, bình, trạm chính, 2 trạm gọi cháy, 9 hộp mạch · sinh từ firebot.scad + firebot_parts2.scad")
pg.image(f"{P2}/robot_asm.png", 22, 72, 470, 404)
pg.text(30, 490, "Robot lắp từ chi tiết đợt 2: thân 2 nửa, giá treo chốt xoay, tay máy 3 khớp DS3225.", 9, fill=QUIET, italic=True)
pg.image(f"{P2}/call_station.png", 500, 72, 250, 250)
pg.text(510, 336, "Trạm gọi cháy (×2) trên cột / chân máy ảnh.", 9, fill=QUIET, italic=True)
rows = []; tot_n = 0; tot_g = 0
for grp, items in G:
    n = 0; g = 0
    for f, _, _ in items:
        q = QTY_OVERRIDE.get(f, st[f]["qty"]); n += q; g += q*st[f]["g"]
    rows.append([grp, str(len(items)), str(n), f"{g/1000:.2f} kg"]); tot_n += n; tot_g += g
rows.append(["Tổng", str(sum(len(i) for _, i in G)), str(tot_n), f"{tot_g/1000:.1f} kg"])
pg.text(770, 92, "Khối lượng in", 13, w="700")
pg.table(770, 100, ["Nhóm", "Loại", "Số chi tiết", "Nhựa (ước)"], rows, [170, 50, 80, 90], 9.5, 17)
pg.text(770, 260, "Ước tính nhựa: thể tích STL × 1,27 g/cm³ × 0,5 (tường + infill),", 8.5, fill=QUIET)
pg.text(770, 273, "tấm mỏng × 0,95. Riêng 22 thanh treo đã chiếm ~3,3 kg.", 8.5, fill=QUIET)
pg.text(30, 520, "Mua kèm (không in)", 12, w="700")
buy = [["Bình nhựa PP chữ nhật ~4 L (~220×150×120) + đầu nối ra ren", "Ống PU 8×5 mm ~3 m + co nối nhanh"],
       ["Ống đồng / inox Ø10 dài 150 mm làm đầu phun + béc Ø2–2,5", "Van điện từ 12V thường đóng (ren 1/4\")"],
       ["Vòng bi U626ZZ 6×22×7 (16) + trục M6 12.9 + ống lót 6×8", "Nam châm NdFeB 20×30×5 (16 viên) + thép lót 1,5 mm (4 tấm)"],
       ["Bulông M3/M4/M5/M6/M8, ốc cấy nhiệt M3, thanh ty M8", "Gioăng cao su 2 mm, đệm cao su, dây rút"],
       ["2 tiếp điểm lò xo Ø7 + tấm đồng 30×29 mm", "Nút nhấn đỏ Ø16, còi 5V, LED 5 mm (×2 trạm)"]]
pg.table(30, 528, ["", ""], buy, [360, 360], 9, 15)
pg.rect(770, 300, 390, 150, "#fdf2e9", "#e59866", 0.8, 4)
pg.text(780, 318, "Lưu ý khi in", 10.5, w="700", fill="#a04000")
for i, t in enumerate(["Bàn in tối thiểu 220 × 220 × 190 mm (thân robot cao 180).",
                       "Dùng PETG cho gần nước và cuộn dây nóng; PLA chỉ cho dưỡng khoan.",
                       "Kích thước servo, bát servo, cảm biến lấy theo thông số phổ biến:",
                       "đo linh kiện thật rồi sửa tham số ở đầu file .scad trước khi in.",
                       "In thử 1 bộ module M0 trước (thanh treo, 3 giá cuộn, 1 bogie).",
                       "Mỗi file STL đã xoay sẵn mặt phẳng xuống bàn."]):
    pg.text(780, 336+i*17, "• " + t, 9.2)
pages.append(pg)

# ---- Tờ 2–6: thẻ chi tiết ----
cards = [(grp, f, nm, note) for grp, items in G for f, nm, note in items]
per = 8; cw, ch = 286, 330
for pi in range(0, len(cards), per):
    n = 2 + pi//per
    chunk = cards[pi:pi+per]
    grps = ", ".join(dict.fromkeys(c[0] for c in chunk))
    pg = Page(n, f"Chi tiết in 3D — {grps}", "Mỗi thẻ: hình chi tiết (hướng in), số lượng cả dự án, kích thước bao (mm), khối lượng nhựa ước tính / cái")
    for i, (grp, f, nm, note) in enumerate(chunk):
        x = 24 + (i % 4)*cw; y = 76 + (i//4)*ch
        pg.rect(x, y, cw-10, ch-12, "#ffffff", "#bbb", 0.7, 6)
        pg.image(f"{TH}/{f}.png", x+6, y+6, cw-22, 190)
        q = QTY_OVERRIDE.get(f, st[f]["qty"]); d = st[f]["dim"]
        pg.text(x+10, y+214, nm, 11, w="700")
        pg.text(x+10, y+230, f"{f}.stl" if f not in QTY_OVERRIDE else f.replace("_1", "_n").replace("_M3", "_Mn") + ".stl", 8.5, fill=QUIET)
        pg.text(x+10, y+248, f"SL: {q}   ·   {d[0]}×{d[1]}×{d[2]} mm   ·   ~{st[f]['g']} g", 9.5, fill=RED, w="700")
        for j, line in enumerate(textwrap.wrap(note, 46)[:3]):
            pg.text(x+10, y+266+j*14, line, 9)
    pages.append(pg)

K.TOTAL = len(pages)
files = []
for pgx in pages:
    sv = f"{K.OUT}/parts{pgx.n}.svg"; pf = f"{K.OUT}/parts{pgx.n}.pdf"
    open(sv, "w").write(pgx.svg()); subprocess.run(["rsvg-convert", "-f", "pdf", "-o", pf, sv], check=True); files.append(pf)
subprocess.run(["pdfunite", *files, "/home/claude/firebot-3d/FireBot_chi_tiet_in_3D.pdf"], check=True)
print(len(pages), "pages")
