# kdgw-firebot — FireBot, robot chữa cháy chạy ray

FireBot là robot chữa cháy treo ngược dưới ray. Khi trạm gọi cháy phát hiện lửa, robot chạy tới vị trí, ngắm bằng camera nhiệt MLX90640 rồi phun nước qua tay 3 khớp. Trạm chính KD-GW vừa sạc pin vừa tiếp nước cho robot. Mọi nút điều khiển trong hệ đều dùng ESP.

| Hạng mục | Thông số |
|---|---|
| Ray | 2 tầng, nhôm dẹt 60×6 dựng đứng, dài 5 m hình chữ L, cua R600, mặt ray dưới cao 1,2 m so với sàn |
| Truyền động | Bánh xe chịu tải (vòng bi U626ZZ, trục M6 cấp 12.9); động cơ tuyến tính 12 V ở **cả 2 tầng ray**, chạy cùng pha (ADR-10) nên bình tự đẩy, robot không kéo bình; chia 9 module |
| Tốc độ | 1 m/s trên đoạn thẳng, 0,6 m/s khi vào cua |
| Phun | Tay 3 khớp, khớp 1 xoay 270° (DS3225 bản 270°): phun được **cả 2 bên ray**, bên nào có cháy thì phun bên đó (ADR-11) |
| Robot | Pin Li-ion 3S 12 V, bơm áp lực 12 V tầm phun 4–5 m, bình 3–4 L có cảm biến mực nước, phanh lò xo tự đóng khi mất điện |
| Điều khiển | KD-GW điều phối qua ESP-NOW và làm cầu sang MQTT; 2 trạm gọi cháy dùng ESP32-S3-CAM + cảm biến IR + nút nhấn |

## Thư mục

```
docs/                 bản vẽ tổng thể, catalog chi tiết in 3D, bản vẽ mạch in (PDF)
hardware/3d/          mô hình OpenSCAD tham số + STL (45 file) + ảnh render
hardware/pcb/FB-TRK/  board module ray ×9 (ESP32-C3, MAX3485, Hall, 2 driver DRV8313: ray dưới + ray trên)
hardware/pcb/FB-ROB/  board robot (ESP32-S3 DevKitC, 3 ngõ MOSFET, 4 servo, cảm biến)
firmware/             trk · rob · call · gw (chưa viết)
tools/                script sinh KiCad + autoroute (kigen), script vẽ PDF
```

## Tài liệu dự án
- SPEC (đã duyệt Checkpoint 1): https://claude.ai/artifact/Peooq6djiB6K9hsrVTQUn5
- PRODUCT (ADR-01…09): https://claude.ai/artifact/P67EzTibhUqXJA8hx2qiaA
- BOM dự toán: https://claude.ai/artifact/SVUP8KTw6aWDFcNGWLDG2Z (≈ 24,8 triệu đ, đã gồm 10 % dự phòng)

## Lắp đặt trạm gọi cháy
Đo và dạy vị trí cho từng trạm theo `docs/Huong_dan_dat_tram_goi_chay.pdf` (ADR-12): dán thước số dọc ray, đo s_L, s_R bằng chân vuông góc, dạy trạm bằng ngọn nến, chạy thử không phun.

## Bước tiếp theo — thử nghiệm M0
1. Lắp 1 module ray + bogie dưới, đo lực đẩy (cần ≥ 5 N liên tục).
2. Thử bơm 12 V: đo tầm phun và lưu lượng.
3. Thử MLX90640 với bảng tra đạn đạo.

Board có chữ "Arden" ở mặt dưới.
