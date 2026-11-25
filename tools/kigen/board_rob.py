"""FB-ROB: robot main board. ESP32-S3-DevKitC-1 (N16R8) on sockets, 3 low-side
MOSFET outputs (pump / valve / brake) with 5 V gate drive, 4 servo ports, sensors."""
R0805 = "Resistor_SMD:R_0805_2012Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"
SOCK22 = "Connector_PinSocket_2.54mm:PinSocket_1x22_P2.54mm_Vertical"
TB2 = "TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal"
XH = lambda n: f"Connector_JST:JST_XH_B{n}B-XH-A_1x0{n}_P2.50mm_Vertical"
HDR3 = "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"


def R(ref, val, a, b, at, blk, note=None):
    return dict(ref=ref, sym="Device:R", val=val, fp=R0805, pins={"1": a, "2": b}, at=at, blk=blk, note=note)


def C(ref, val, a, b, at, blk):
    return dict(ref=ref, sym="Device:C", val=val, fp=C0805, pins={"1": a, "2": b}, at=at, blk=blk)


P = "Nguồn pin 12 V"
M = "ESP32-S3-DevKitC-1 N16R8 (cắm socket)"
O = "Ngõ ra công suất: bơm · van · phanh (mức logic 5 V cho cổng MOSFET)"
S = "Servo DS3225 ×4 (nguồn 6,8 V riêng)"
X = "Cảm biến"

# DevKitC-1 headers (USB toward +X). J1 row at y=48.86, J3 row at y=26.0, pin 1 at x=15
J1 = {1: "+3V3", 2: "+3V3", 4: "ADC_VBAT", 5: "ADC_PRS", 6: "ADC_CHG", 7: "EXP_A", 18: "G_PUMP", 19: "G_VALVE", 20: "G_BRAKE", 21: "+5V", 22: "GND"}
J3 = {1: "GND", 4: "I2C_SDA", 5: "I2C_SCL", 6: "SV1_S", 7: "SV2_S", 8: "SV3_S", 9: "SV4_S", 17: "LVL", 18: "EXP_D", 21: "GND", 22: "GND"}

parts = [
    dict(ref="A1", sym="Connector_Generic:Conn_01x22", val="S3 J1: 3V3 3V3 RST 4 5 6 7 15 16 17 18 8 3 46 9 10 11 12 13 14 5V G", fp=SOCK22,
         pins={str(k): v for k, v in J1.items()}, at=(15.0, 48.86, 90), blk=M),
    dict(ref="A2", sym="Connector_Generic:Conn_01x22", val="S3 J3: G TX RX 1 2 42 41 40 39 38 37 36 35 0 45 48 47 21 20 19 G G", fp=SOCK22,
         pins={str(k): v for k, v in J3.items()}, at=(15.0, 26.0, 90), blk=M),
    dict(ref="#FLG3", sym="power:PWR_FLAG", val="PWR_FLAG", pins={"1": "+3V3"}, blk=M, nobom=True),
    # ---- power
    dict(ref="J1", sym="Connector_Generic:Conn_01x02", val="PIN 12V (từ BMS)", fp=TB2, pins={"1": "+12V_BAT", "2": "GND"}, at=(8.0, 79.1, 0), blk=P, hideref=True),
    dict(ref="F1", sym="Device:Fuse", val="10A mini blade", fp="Fuse:Fuseholder_Blade_Mini_Keystone_3568", pins={"1": "+12V_BAT", "2": "+12V"}, at=(60.0, 75.5, 0), blk=P),
    dict(ref="D1", sym="Device:D_TVS", val="SMBJ15CA", fp="Diode_SMD:D_SMB", pins={"1": "GND", "2": "+12V"}, at=(71.0, 67.0, 0), blk=P),
    dict(ref="C1", sym="Device:C_Polarized", val="470uF 25V", fp="Capacitor_THT:CP_Radial_D10.0mm_P5.00mm", pins={"1": "+12V", "2": "GND"}, at=(75.0, 56.0, 0), blk=P),
    dict(ref="U2", sym="Regulator_Switching:R-78E5.0-1.0", val="R-78E5.0-1.0", fp="Converter_DCDC:Converter_DCDC_RECOM_R-78E-0.5_THT", pins={"1": "+12V", "2": "GND", "3": "+5V"}, at=(59.0, 58.5, 0), blk=P),
    C("C2", "22uF", "+5V", "GND", (80.0, 44.0, 90), P),
    C("C3", "100nF", "+12V", "GND", (64.5, 63.0, 90), P),
    dict(ref="D2", sym="Device:LED", val="LED xanh 5V", fp="LED_SMD:LED_0805_2012Metric", pins={"1": "GND", "2": "LED_A"}, at=(80.5, 36.0, 90), blk=P),
    R("R20", "1k", "+5V", "LED_A", (80.5, 40.0, 90), P),
    dict(ref="#FLG1", sym="power:PWR_FLAG", val="PWR_FLAG", pins={"1": "+12V_BAT"}, blk=P, nobom=True),
    dict(ref="#FLG2", sym="power:PWR_FLAG", val="PWR_FLAG", pins={"1": "GND"}, blk=P, nobom=True),
    R("R1", "100k", "+12V", "ADC_VBAT", (9.5, 58.5, 90), P, "chia áp đo pin 12,6 V → 2,27 V"),
    R("R2", "22k", "ADC_VBAT", "GND", (9.5, 63.0, 90), P),
    C("C4", "100nF", "ADC_VBAT", "GND", (12.5, 63.0, 90), P),
]

# ---- 3 low-side outputs
outs = [("PUMP", "Bơm 12V", 20.5, "SS54", "Diode_SMD:D_SMB", "G_PUMP"),
        ("VALVE", "Van 12V", 33.0, "SS34", "Diode_SMD:D_SMA", "G_VALVE"),
        ("BRAKE", "Phanh 12V", 45.5, "SS34", "Diode_SMD:D_SMA", "G_BRAKE")]
for i, (n, lbl, xt, dio, dfp, g) in enumerate(outs, start=1):
    xc = xt + 2.54
    parts += [
        dict(ref=f"U{2+i}", sym="74xGxx:74AHCT1G125", val="74AHCT1G125", fp="Package_TO_SOT_SMD:SOT-23-5",
             pins={"1": "GND", "2": g, "3": "GND", "4": f"GD_{n}", "5": "+5V"}, at=(xc - 1.5, 54.0, 0), blk=O),
        R(f"R{10+i}", "10k", g, "GND", (xc - 5.0, 54.0, 90), O, "kéo xuống: tắt khi ESP khởi động"),
        R(f"R{13+i}", "47", f"GD_{n}", f"GATE_{n}", (xc + 1.8, 54.0, 90), O),
        R(f"R{16+i}", "10k", f"GATE_{n}", "GND", (xc + 3.8, 54.0, 90), O),
        dict(ref=f"Q{i}", sym="Device:Q_NMOS_GDS", val="AOD4184A", fp="Package_TO_SOT_SMD:TO-252-2",
             pins={"1": f"GATE_{n}", "2": f"{n}_N", "3": "GND"}, at=(xc + 0.5, 61.5, 0), blk=O),
        dict(ref=f"D{2+i}", sym="Device:D_Schottky", val=dio, fp=dfp, pins={"1": "+12V", "2": f"{n}_N"}, at=(xc, 69.3, 0), blk=O),
        dict(ref=f"J{1+i}", sym="Connector_Generic:Conn_01x02", val=f"{lbl} (+ −)", fp=TB2, pins={"1": "+12V", "2": f"{n}_N"}, at=(xt, 79.1, 0), blk=O, hideref=True),
    ]
parts.append(C("C5", "100nF", "+5V", "GND", (13.5, 55.0, 90), O))

# ---- servos
parts += [
    dict(ref="J5", sym="Connector_Generic:Conn_01x02", val="Nguồn servo 6,8V (từ buck)", fp=TB2, pins={"1": "+VSERVO", "2": "GND"}, at=(17.0, 5.0, 180), blk=S),
    dict(ref="C6", sym="Device:C_Polarized", val="1000uF 16V", fp="Capacitor_THT:CP_Radial_D10.0mm_P5.00mm", pins={"1": "+VSERVO", "2": "GND"}, at=(24.0, 6.0, 0), blk=S),
    dict(ref="#FLG4", sym="power:PWR_FLAG", val="PWR_FLAG", pins={"1": "+VSERVO"}, blk=S, nobom=True),
]
for i in range(1, 5):
    x = 38.0 + (i - 1) * 10.0
    parts += [
        dict(ref=f"J{5+i}", sym="Connector_Generic:Conn_01x03", val=f"SERVO{i} (G V S)", fp=HDR3, pins={"1": "GND", "2": "+VSERVO", "3": f"SV{i}_P"}, at=(x, 4.0, 90), blk=S),
        R(f"R{20+i}", "330", f"SV{i}_S", f"SV{i}_P", (x + 2.54, 9.5, 90), S),
    ]

# ---- sensors
parts += [
    dict(ref="J10", sym="Connector_Generic:Conn_01x03", val="ÁP SUẤT (5V G OUT)", fp=XH(3), pins={"1": "+5V", "2": "GND", "3": "PRS_OUT"}, at=(11.5, 19.5, 0), blk=X),
    R("R30", "10k", "PRS_OUT", "ADC_PRS", (14.0, 15.0, 0), X, "0,5–4,5 V → 0,33–3,0 V"),
    R("R31", "20k", "ADC_PRS", "GND", (14.0, 12.5, 0), X),
    dict(ref="J11", sym="Connector_Generic:Conn_01x03", val="MỰC NƯỚC XKC-Y25 NPN (5V G OUT)", fp=XH(3), pins={"1": "+5V", "2": "GND", "3": "LVL"}, at=(22.6, 19.5, 0), blk=X),
    R("R32", "10k", "+3V3", "LVL", (25.1, 15.0, 0), X),
    dict(ref="J12", sym="Connector_Generic:Conn_01x04", val="MLX90640 I2C (3V3 G SDA SCL)", fp=XH(4), pins={"1": "+3V3", "2": "GND", "3": "I2C_SDA", "4": "I2C_SCL"}, at=(33.7, 19.5, 0), blk=X),
    R("R33", "4k7", "+3V3", "I2C_SDA", (37.5, 15.0, 0), X),
    R("R34", "4k7", "+3V3", "I2C_SCL", (37.5, 12.5, 0), X),
    dict(ref="J13", sym="Connector_Generic:Conn_01x02", val="BÁO SẠC (CHG+ G)", fp=XH(2), pins={"1": "CHG_IN", "2": "GND"}, at=(47.3, 19.5, 0), blk=X),
    R("R35", "100k", "CHG_IN", "ADC_CHG", (48.5, 15.0, 0), X),
    R("R36", "22k", "ADC_CHG", "GND", (48.5, 12.5, 0), X),
    C("C7", "100nF", "ADC_CHG", "GND", (52.5, 13.5, 90), X),
    dict(ref="J14", sym="Connector_Generic:Conn_01x04", val="MỞ RỘNG (3V3 G IO21 IO7)", fp=XH(4), pins={"1": "+3V3", "2": "GND", "3": "EXP_D", "4": "EXP_A"}, at=(55.9, 19.5, 0), blk=X),
    C("C8", "10uF", "+3V3", "GND", (70.0, 15.0, 0), X),
]

B = dict(
    name="FB-ROB", title="FireBot – board điều khiển robot", date="2026-11-25", rev="A",
    comment="ESP32-S3-DevKitC-1 · 3 MOSFET · 4 servo · MLX90640 · áp suất · mực nước",
    parts=parts, w=84.0, h=84.0, ox=100.0, oy=100.0, corner=2.0,
    holes=[(5, 15), (79, 15), (5, 69), (79, 69)], hole_fp="MountingHole_3.2mm_M3",
    netclasses=[("Big", (1.6, 0.2, 1.0, 0.5), ["+12V_BAT", "+12V", "PUMP_N", "+VSERVO"]),
                ("Mid", (0.8, 0.2, 0.8, 0.4), ["VALVE_N", "BRAKE_N", "GND"]),
                ("P5", (0.5, 0.2, 0.8, 0.4), ["+5V", "+3V3"])],
    texts=[
        ("Arden", 78.0, 81.5, 0, "B.SilkS", 1.5),
        ("PIN 12V", 10.5, 73.0, 0, "F.SilkS", 0.9),
        ("BƠM", 23.0, 73.0, 0, "F.SilkS", 0.9), ("VAN", 35.5, 73.0, 0, "F.SilkS", 0.9), ("PHANH", 48.0, 73.0, 0, "F.SilkS", 0.9),
        ("−  6V8  +", 14.5, 10.0, 0, "F.SilkS", 0.9),
        ("G V S", 40.5, 1.6, 0, "F.SilkS", 0.8), ("S1", 40.5, 7.0, 0, "F.SilkS", 0.8), ("S2", 50.5, 7.0, 0, "F.SilkS", 0.8),
        ("S3", 60.5, 7.0, 0, "F.SilkS", 0.8), ("S4", 70.5, 7.0, 0, "F.SilkS", 0.8),
        ("ÁP", 14.0, 23.3, 0, "F.SilkS", 0.8), ("MỰC", 25.1, 23.3, 0, "F.SilkS", 0.8), ("MLX", 37.5, 23.3, 0, "F.SilkS", 0.8),
        ("SẠC", 48.5, 23.3, 0, "F.SilkS", 0.8), ("MỞ RỘNG", 59.6, 23.3, 0, "F.SilkS", 0.8),
        ("USB →", 77.5, 37.5, 90, "F.SilkS", 0.9),
    ],
)
