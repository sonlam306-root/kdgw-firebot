# Profile KD-GW cho trạm chính

Điều phối nhiệm vụ, relay sạc 12,6 V, bơm tiếp nước + phao, cầu ESP-NOW ↔ MQTT, dashboard.

Trang dashboard **Trạm gọi cháy**: Dạy vị trí (Ghi mép trái / Ghi mép phải / Thêm điểm / Robot tự dò), Thử không phun. Kiểm tra khi lưu: 2 mép đủ xa trong ảnh, 100 ≤ s_R − s_L ≤ 2 500 mm, phía A không rơi vào vùng cấm M0 (ADR-11, ADR-12).

Khung định vị (ADR-13): KD-GW lưu cấu hình {phía, lỗ cột camera} → {Δs_L, Δs_R, u_L, u_R}; khi dùng ở cột P2/P6 thì s_L = s_cột + Δs_L.
