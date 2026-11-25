# FireBot — chi tiết in 3D, đợt 1: ray + module thử (M0)

Toàn bộ chi tiết sinh từ một file tham số `firebot.scad` (OpenSCAD 2021+).
Đổi kích thước ở đầu file, rồi xuất lại:

```
openscad -D 'part="hanger"' -o hanger.stl firebot.scad
```

`part` nhận: `hanger`, `bobbin`, `coil_seg`, `coil_seg_hall`, `coil_seg_curve`,
`bogie_lower`, `bogie_upper`, `spacer`, `jig`, `assembly` (xem lắp ráp, không in).

## Quy ước phía (quan trọng)
- **Phía A** (Y < 0): thanh treo → khung sắt lỗ. Luôn là **phía trong cua**.
- **Phía B** (Y > 0): cuộn dây, bogie, robot. Luôn là **phía ngoài cua**.
  Dãy nam châm thẳng đi qua cua sẽ lệch ra ngoài, nên cuộn dây đặt ở phía ngoài
  thì khe hở chỉ tăng lên, không bao giờ va.
- Mép trên ray dưới cao **1200 mm** so với sàn; ray trên cao hơn 260 mm (mép trên 1460).

## Số lượng cần in
| Chi tiết | File | Thử M0 | Cả tuyến 5 m |
|---|---|---|---|
| Thanh treo + nối ray | hanger.stl | 2 | 22 (11/ray) |
| Bobbin cuộn dây | bobbin.stl | 15 (+3 dự phòng) | 150 |
| Giá cuộn dây thẳng | coil_seg.stl | 2 | 16 |
| Giá cuộn dây thẳng có Hall | coil_seg_hall.stl | 1 | 8 |
| Giá cuộn dây cong R600 | coil_seg_curve.stl | – | 6 |
| Bogie ray dưới (có túi nam châm) | bogie_lower.stl | 1 | 2 |
| Bogie ray trên | bogie_upper.stl | – | 2 |
| Ống cách trục bánh | spacer.stl | 4 | 16 |
| Dưỡng khoan lỗ thanh treo | jig.stl | 1 | 1 |

## Thông số in đề xuất
- Vật liệu: **PETG** (cuộn dây nóng lên khi chạy; PLA mềm ở ~55 °C).
- Thanh treo, bogie: 4 tường, 5 lớp trên/dưới, infill 40 % gyroid.
  Thanh treo in nằm nghiêng (đã xoay sẵn) để thớ in chạy dọc tay đòn.
- Bobbin, giá cuộn: 3 tường, infill 25 %.
- Tất cả đã đặt sẵn mặt phẳng xuống bàn in, không cần support
  (trừ lỗ ngang trên thanh treo, có thể để cầu).

## Mua kèm (chốt mã ở BOM, T-004)
- Nhôm dẹt **60×6 mm** (không còn là 40×6: cuộn dây và nam châm cao hơn thì lực đẩy lớn hơn).
- Bạc đạn **rãnh U** ôm mép thanh 6 mm, Ø22, U626ZZ lỗ 6 → dùng mép vuông của thanh, không phải vát V.
- Nam châm NdFeB khối **20×30×5 mm** (từ hoá theo chiều 5 mm), 4 viên/bogie, xếp xen kẽ N-S.
- Thép lót lưng 1,5 mm, 88×30 mm; bu lông M5 (thanh treo), trục bánh M6×50 cấp 12.9 + ống lót thép 6×8, M3 (giá cuộn), M6 (chốt xoay), M8 (khung, thanh ty).
- Hall TO-92 loại lưỡng cực, chốt (latch), 3 cái/module.
- Dây đồng emay ~0,5 mm: mỗi cuộn khoảng 250 vòng (đo điện trở các cuộn, lệch nhau ≤ 5 %).

## Thông số động cơ (đã khoá trong file)
- Bước cực τ = 22,5 mm; bước cuộn = 30 mm (3 cuộn / 4 cực); 15 cuộn/module, 3 pha × 5 cuộn.
- Hall cách nhau 15 mm (120° điện), đặt trên dải Hall ở đoạn giá đầu mỗi module.
- Khe hở cuộn – nam châm 3 mm. Đổi bước cực sau khi đo M0 thì toàn bộ giá tự cập nhật.

## Còn làm ở đợt sau
- Giá cuộn cong có dải Hall; thân robot treo ngược + hộp pin kín; tay máy 3 khớp có đường ống trong lòng;
  đầu phun ống cứng; bogie bình + giá bình 3–4 L; chi tiết trạm chính (má sạc, vòi rót).
