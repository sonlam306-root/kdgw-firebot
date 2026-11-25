# Firmware trạm gọi cháy (ESP32-S3-CAM)

Camera + cảm biến lửa IR + nút nhấn; mỗi trạm biết sẵn 1 vị trí đích trên ray; gửi lệnh qua ESP-NOW tới KD-GW.

## Vị trí đích (ADR-12)
Trạm không gửi toạ độ của mình, chỉ gửi `{station_id, u, xác nhận camera+IR}` qua ESP-NOW.
KD-GW giữ bảng dạy 2 điểm `{side, u_L, s_L, u_R, s_R}` của từng trạm (lưu NVS trạm + KD-GW) và nội suy
`s = s_L + (u − u_L)/(u_R − u_L)·(s_R − s_L)`, bù né cột nếu phía A, rồi gửi `{s, side}` cho robot.
Hướng dẫn đo cho người dùng: `docs/Huong_dan_dat_tram_goi_chay.pdf`.
