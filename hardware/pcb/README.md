# FireBot – mạch in (rev A, 2026-11-25)

| Board | Kích thước | SL | Gắn vào | File gửi xưởng |
|---|---|---|---|---|
| FB-TRK (module ray, 2 driver: ray dưới + ray trên) | 76 × 56 mm, 2 lớp | 9 (+1 dự phòng) | hộp `module_box`, 4 trụ M2.5 (64 × 44) | `FB-TRK/FB-TRK_gerber.zip` |
| FB-ROB (robot) | 84 × 84 mm, 2 lớp | 1 (+1 dự phòng) | khay `electronics_tray`, 4 trụ M3 (74 × 54) | `FB-ROB/FB-ROB_gerber.zip` |

- Mở bằng KiCad 7 trở lên: `*.kicad_pro`, sơ đồ `*.kicad_sch`, mạch `*.kicad_pcb`. Sơ đồ nối bằng nhãn net, chưa vẽ dây.
- Đặt hàng: FR4 1,6 mm. FB-ROB nên chọn đồng 2 oz vì đường bơm chịu ~5 A.
- Kiểm tra DRC: 0 lỗi, 0 chỗ chưa nối, ở cả hai board.
- Mỗi board có chữ "Arden" ở mặt dưới, góc phải. Không in tên board.
- Danh sách linh kiện: `*_bom.csv`. Toạ độ linh kiện cho SMT: `*_cpl.csv`.

**Kiểm tra trước khi hàn**
1. **ESP32-C3 SuperMini:** so chữ in trên PCB với chữ in trên module, vì vài lô xếp chân khác.
2. **ESP32-S3-DevKitC-1:** đo khoảng cách 2 hàng chân, bản vẽ dùng 22,86 mm.
3. **SimpleFOC Mini:** bản v1.0 và v1.1 xếp chân khác nhau, nên nối dây Dupont theo tên chân.
