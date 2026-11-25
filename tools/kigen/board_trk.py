"""FB-TRK: track module board (x9). ESP32-C3 SuperMini + MAX3485 + R-78E 5V,
Hall inputs, header to a DRV8313 (SimpleFOC Mini) driver, limit switch."""
R0805 = "Resistor_SMD:R_0805_2012Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"
SOCK8 = "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical"
TB2 = "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal"
TB3 = "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-3-5.08_1x03_P5.08mm_Horizontal"
XH = lambda n: f"Connector_JST:JST_XH_B{n}B-XH-A_1x0{n}_P2.50mm_Vertical"


def R(ref, val, a, b, at, blk, note=None):
    return dict(ref=ref, sym="Device:R", val=val, fp=R0805, pins={"1": a, "2": b}, at=at, blk=blk, note=note)


def C(ref, val, a, b, at, blk):
    return dict(ref=ref, sym="Device:C", val=val, fp=C0805, pins={"1": a, "2": b}, at=at, blk=blk)


P = "Nguồn 12 V → 5 V"
M = "ESP32-C3 SuperMini (cắm socket)"
RS = "RS485 (bus dọc tuyến)"
H = "Cảm biến Hall + công tắc hành trình"
D = "Driver 3 pha DRV8313 (SimpleFOC Mini, nối bằng dây Dupont)"

parts = [
    # ---- power
    dict(ref="J1", sym="Connector_Generic:Conn_01x02", val="12V IN", fp=TB2, pins={"1": "+12V_IN", "2": "GND"}, at=(70.5, 30.0, 90), blk=P),
    dict(ref="F1", sym="Device:Fuse", val="3A mini blade", fp="Fuse:Fuseholder_Blade_Mini_Keystone_3568", pins={"1": "+12V_IN", "2": "+12V"}, at=(52.0, 30.5, 90), blk=P),
    dict(ref="D1", sym="Device:D_TVS", val="SMBJ15CA", fp="Diode_SMD:D_SMB", pins={"1": "GND", "2": "+12V"}, at=(60.0, 30.0, 90), blk=P),
    dict(ref="C1", sym="Device:C_Polarized", val="220uF 25V", fp="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm", pins={"1": "+12V", "2": "GND"}, at=(46.0, 13.0, 0), blk=P),
    dict(ref="U2", sym="Regulator_Switching:R-78E5.0-0.5", val="R-78E5.0-0.5", fp="Converter_DCDC:Converter_DCDC_RECOM_R-78E-0.5_THT", pins={"1": "+12V", "2": "GND", "3": "+5V"}, at=(39.0, 21.0, 270), blk=P),
    C("C2", "10uF", "+5V", "GND", (32.5, 21.0, 90), P),
    C("C3", "100nF", "+12V", "GND", (44.0, 31.5, 0), P),
    dict(ref="J2", sym="Connector_Generic:Conn_01x02", val="12V → VM driver", fp=TB2, pins={"1": "+12V", "2": "GND"}, at=(70.5, 17.5, 90), blk=P),
    dict(ref="D2", sym="Device:LED", val="LED xanh 5V", fp="LED_SMD:LED_0805_2012Metric", pins={"1": "GND", "2": "LED_A"}, at=(35.0, 27.0, 90), blk=P),
    R("R10", "1k", "+5V", "LED_A", (35.0, 31.0, 90), P),
    dict(ref="#FLG1", sym="power:PWR_FLAG", val="PWR_FLAG", pins={"1": "+12V_IN"}, blk=P, nobom=True),
    dict(ref="#FLG2", sym="power:PWR_FLAG", val="PWR_FLAG", pins={"1": "GND"}, blk=P, nobom=True),
    # ---- MCU (two 1x8 sockets; USB-C toward the bottom edge)
    dict(ref="A1", sym="Connector_Generic:Conn_01x08", val="C3 hàng phải: 5V G 3V3 4 3 2 1 0", fp=SOCK8,
         pins={"1": "+5V", "2": "GND", "3": "+3V3", "4": "RS_DE", "5": "HALL3", "6": "DRV_nFT", "7": "HALL2", "8": "HALL1"},
         at=(25.24, 44.0, 180), blk=M),
    dict(ref="A2", sym="Connector_Generic:Conn_01x08", val="C3 hàng trái: 5 6 7 8 9 10 20 21", fp=SOCK8,
         pins={"1": "DRV_IN1", "2": "DRV_IN2", "3": "DRV_IN3", "4": "LIM", "6": "DRV_EN", "7": "RS_RO", "8": "RS_DI"},
         at=(10.0, 44.0, 180), blk=M),
    C("C7", "10uF", "+3V3", "GND", (17.6, 48.5, 0), M),
    dict(ref="#FLG3", sym="power:PWR_FLAG", val="PWR_FLAG", pins={"1": "+3V3"}, blk=M, nobom=True),
    # ---- RS485
    dict(ref="U1", sym="Interface_UART:MAX3485", val="MAX3485 (SP3485)", fp="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
         pins={"1": "RS_RO", "2": "RS_DE", "3": "RS_DE", "4": "RS_DI", "5": "GND", "6": "RS_A", "7": "RS_B", "8": "+3V3"},
         at=(45.0, 39.0, 0), blk=RS),
    C("C8", "100nF", "+3V3", "GND", (45.0, 34.5, 0), RS),
    R("R7", "10k", "RS_DE", "GND", (39.5, 39.0, 90), RS, "DE/RE kéo xuống: mặc định nhận"),
    R("R8", "120", "RS_A", "RS_T", (52.5, 37.0, 0), RS, "điện trở cuối tuyến"),
    dict(ref="JP1", sym="Connector_Generic:Conn_01x02", val="TERM 120R", fp="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
         pins={"1": "RS_T", "2": "RS_B"}, at=(56.5, 37.0, 90), blk=RS, note="cắm jumper ở module M0 và M8"),
    dict(ref="J3", sym="Connector_Generic:Conn_01x03", val="RS485 IN (A B G)", fp=TB3, pins={"1": "RS_A", "2": "RS_B", "3": "GND"}, at=(31.0, 51.4, 0), blk=RS),
    dict(ref="J4", sym="Connector_Generic:Conn_01x03", val="RS485 OUT (A B G)", fp=TB3, pins={"1": "RS_A", "2": "RS_B", "3": "GND"}, at=(48.5, 51.4, 0), blk=RS),
    # ---- Hall + limit
    dict(ref="J5", sym="Connector_Generic:Conn_01x05", val="HALL (5V G H1 H2 H3)", fp=XH(5),
         pins={"1": "+5V", "2": "GND", "3": "HALL1", "4": "HALL2", "5": "HALL3"}, at=(14.0, 4.0, 0), blk=H),
    R("R1", "10k", "+3V3", "HALL1", (13.5, 11.0, 90), H),
    R("R2", "10k", "+3V3", "HALL2", (16.5, 11.0, 90), H),
    R("R3", "10k", "+3V3", "HALL3", (19.5, 11.0, 90), H),
    C("C4", "1nF", "HALL1", "GND", (13.5, 15.5, 90), H),
    C("C5", "1nF", "HALL2", "GND", (16.5, 15.5, 90), H),
    C("C6", "1nF", "HALL3", "GND", (19.5, 15.5, 90), H),
    dict(ref="J7", sym="Connector_Generic:Conn_01x02", val="LIMIT (SW G)", fp=XH(2), pins={"1": "LIM", "2": "GND"}, at=(4.0, 22.0, 90), blk=H),
    # ---- driver header
    dict(ref="J6", sym="Connector_Generic:Conn_01x08", val="DRV: IN1 IN2 IN3 EN nFT nRT nSP G", fp="Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical",
         pins={"1": "DRV_IN1", "2": "DRV_IN2", "3": "DRV_IN3", "4": "DRV_EN", "5": "DRV_nFT", "6": "DRV_nRT", "7": "DRV_nSP", "8": "GND"},
         at=(31.0, 4.0, 90), blk=D),
    R("R4", "10k", "+3V3", "DRV_nFT", (36.0, 10.0, 0), D),
    R("R5", "10k", "+3V3", "DRV_nRT", (36.0, 13.0, 0), D),
    R("R6", "10k", "+3V3", "DRV_nSP", (36.0, 16.0, 0), D),
    R("R9", "10k", "DRV_EN", "GND", (28.0, 11.0, 90), D, "EN kéo xuống: driver tắt khi khởi động"),
]

B = dict(
    name="FB-TRK", title="FireBot – board module ray (×9)", date="2026-11-25", rev="A",
    comment="ESP32-C3 SuperMini · MAX3485 · R-78E5.0 · 3 Hall · DRV8313",
    parts=parts, w=76.0, h=56.0, ox=100.0, oy=100.0, corner=2.0,
    holes=[(6, 6), (70, 6), (6, 50), (70, 50)], hole_fp="MountingHole_2.7mm_M2.5",
    netclasses=[("Power", (1.0, 0.2, 1.0, 0.5), ["+12V_IN", "+12V", "GND"]), ("P5", (0.5, 0.2, 0.8, 0.4), ["+5V", "+3V3"])],
    texts=[
        ("Arden", 66, 53.5, 0, "B.SilkS", 1.5),
        ("+12V", 63.5, 30.0, 0, "F.SilkS", 0.9), ("GND", 63.5, 24.9, 0, "F.SilkS", 0.9),
        ("VM+", 63.5, 17.5, 0, "F.SilkS", 0.9), ("GND", 63.5, 12.4, 0, "F.SilkS", 0.9),
        ("A    B    G", 36.1, 45.2, 0, "F.SilkS", 0.9), ("A    B    G", 53.6, 45.2, 0, "F.SilkS", 0.9), ("RS485 IN", 36.1, 43.6, 0, "F.SilkS", 0.8), ("RS485 OUT", 53.6, 43.6, 0, "F.SilkS", 0.8),
        ("5V G H1 H2 H3", 19.0, 8.0, 0, "F.SilkS", 0.8),
        ("1 2 3 E F R S G", 40.0, 7.2, 0, "F.SilkS", 0.8),
        ("USB-C", 17.6, 53.0, 0, "F.SilkS", 0.9),
        ("5V G 3V3 4 3 2 1 0", 28.5, 35.0, 90, "F.SilkS", 0.8),
        ("5 6 7 8 9 10 20 21", 6.8, 35.0, 90, "F.SilkS", 0.8),
        ("LIM", 4.0, 16.5, 0, "F.SilkS", 0.8), ("TERM", 57.8, 34.3, 0, "F.SilkS", 0.8),
    ],
)
