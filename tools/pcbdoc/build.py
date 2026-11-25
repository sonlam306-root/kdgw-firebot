import sys, subprocess; sys.path.insert(0, '/home/claude/tools/pcbdoc'); from sheet import page
D = '/home/claude/firebot-pcb'
page(f'{D}/p_trk', 'FB-TRK — board module ray (9 board, M0…M8), đẩy cả 2 tầng ray', '76 × 56 mm · 2 lớp · 4 lỗ M2.5 khớp trụ đỡ hộp module_box (64 × 44) · DRC 0 lỗi · rev A',
 f'{D}/FB-TRK/FB-TRK_top.png', f'{D}/FB-TRK/FB-TRK_bottom.png',
 [('Gán chân ESP32-C3 SuperMini', [('GPIO5/6/7', 'IN1 / IN2 / IN3 (PWM 3 pha)'), ('GPIO10', 'EN driver (kéo xuống 10k)'), ('GPIO2', 'nFAULT driver (kéo lên)'),
   ('GPIO0/1/3', 'HALL1 / HALL2 / HALL3'), ('GPIO8', 'công tắc hành trình'), ('GPIO20/21', 'RS485 RO / DI'), ('GPIO4', 'RS485 DE/RE (mặc định nhận)')]),
  ('Đầu nối', [('J1', '12 V vào (sau công tắc tơ)'), ('J2 / J9', 'VM driver ray dưới / ray trên'), ('J3 / J4', 'RS485 vào / ra (A B GND)'),
   ('J5', 'Hall: 5V GND H1 H2 H3 (JST-XH)'), ('J6 (2×8)', 'Hàng dưới: ray dưới · hàng trên: ray trên'), ('J7', 'Công tắc hành trình (chỉ M0, M8)'), ('JP1', 'Jumper 120 Ω (chỉ M0, M8)')])],
 ['Mỗi module 2 driver DRV8313 (SimpleFOC Mini) chạy song song cùng tín hiệu: cuộn ray trên lắp thẳng hàng và CÙNG PHA với ray dưới (ADR-10).',
  'Nối dây Dupont vào J6 theo chữ in trên driver (v1.0 và v1.1 khác thứ tự chân). Cuộn ray dưới → driver hàng DƯỚI, ray trên → hàng TRÊN.',
  'Cuộn dây 3 pha nối vào cọc M1 M2 M3 của driver, giữ cùng thứ tự pha A-B-C ở cả 2 tầng; VM lấy từ J2 và J9.',
  'Kiểm tra lại thứ tự chân in trên ESP32-C3 SuperMini trước khi hàn socket (vài lô có khác biệt); chữ in trên PCB ghi sẵn để so.',
  'U2 R-78E5.0-0.5 thay 7805, không cần tản nhiệt. Cầu chì mini 3 A cho mỗi module.',
  'Mặt dưới góc phải có chữ "Arden".'])
page(f'{D}/p_rob', 'FB-ROB — board điều khiển robot', '84 × 84 mm · 2 lớp · 4 lỗ M3 khớp trụ khay điện tử (74 × 54) · DRC 0 lỗi · rev A',
 f'{D}/FB-ROB/FB-ROB_top.png', f'{D}/FB-ROB/FB-ROB_bottom.png',
 [('Gán chân ESP32-S3-DevKitC-1', [('GPIO42/41/40/39', 'Servo 1…4 (qua 330 Ω)'), ('GPIO12/13/14', 'Bơm / van / phanh (qua 74AHCT1G125)'),
   ('GPIO4', 'đo pin (100k/22k)'), ('GPIO5', 'áp suất mực nước (10k/20k)'), ('GPIO6', 'báo đang sạc (100k/22k)'), ('GPIO47', 'XKC-Y25 chống tràn'),
   ('GPIO1/2', 'I2C SDA/SCL → MLX90640'), ('GPIO21, GPIO7', 'cổng mở rộng')]),
  ('Đầu nối', [('J1', 'Pin 12 V từ BMS'), ('J2 / J3 / J4', 'Bơm / van / phanh (+12V, −)'), ('J5', 'Nguồn servo 6,8 V từ buck 5 A'), ('J6…J9', 'Servo G V S'),
   ('J10…J14', 'Áp suất, mực, MLX, sạc, mở rộng')])],
 ['MOSFET AOD4184A được kích 5 V qua 74AHCT1G125; điện trở kéo xuống giữ bơm/van tắt và phanh đóng khi ESP khởi động hoặc mất điện.',
  'Phanh là nam châm điện nhả phanh: mất điều khiển → MOSFET tắt → lò xo đóng phanh (fail-safe).',
  'Đường bơm rộng 1,6 mm: đặt đồng 2 oz, hoặc phủ thêm thiếc dọc đường +12V–bơm nếu dùng 1 oz.',
  'DevKitC-1 cắm socket, cổng USB quay ra mép phải để nạp code. Không dùng GPIO35–37 (PSRAM octal của bản N16R8).',
  'Kiểm tra khoảng cách 2 hàng chân DevKitC (đã vẽ 22,86 mm) bằng thước trước khi hàn socket. Mặt dưới góc phải có chữ "Arden".'])
for n in ['FB-TRK', 'FB-ROB']:
    pass
subprocess.run(['pdfunite', f'{D}/p_trk.pdf', f'{D}/FB-TRK/FB-TRK_schematic.pdf', f'{D}/p_rob.pdf', f'{D}/FB-ROB/FB-ROB_schematic.pdf', f'{D}/FireBot_mach_in.pdf'], check=True)
