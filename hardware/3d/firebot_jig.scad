// FireBot — khung định vị trạm gọi cháy (ADR-13)
// Thanh định vị bằng sắt V lỗ bắt cứng vào chân cột khung: lắp lại ở triển lãm chỉ cần
// cắm thanh vào chân cột, cắm cột camera vào đúng lỗ → vị trí camera so với ray luôn như cũ.
// jp = "scene" | "post_lock" | "mast_base" | "cam_head" | "tray_base" | "none"
include <firebot_system.scad>
include <firebot_parts2.scad>
p = "none";
view = "none";
jp = "scene";
$fn = 48;

// ---- kích thước sắt V lỗ và vị trí
ang = 40; ang_t = 2.0; cl = 0.6;          // thanh V 40×40×2, khe hở lắp
bar_x = 24;                                 // mặt trong cánh đứng của thanh (cách tâm cột theo X)
bar_len = 3000;                             // 2 thanh 1,5 m nối bằng ke sắt lỗ
m8 = 8.6; m8n = 13.4; m5 = 5.3;
mast_d = 25.4;                              // ống nhôm Ø25,4 (1") dài 1 400 mm
mast_h = 1400;
cam_tilt = 40;                              // camera chúc xuống 40°, nhìn về phía ray
y_tray = 1800;                              // ví dụ: khay lửa demo cách ray 1,8 m
y_mast = 2700;                              // ví dụ: cột camera ở lỗ cách ray 2,7 m

// rãnh ôm thanh V (cánh nằm trên sàn + cánh đứng ở x = bar_x), chạy dọc Y
module bar_channel(len){
  translate([bar_x - cl, -len/2, -1]) cube([ang + 2*cl, len, ang_t + cl + 1]);
  translate([bar_x - cl, -len/2, -1]) cube([ang_t + 2*cl, len, ang + 2]);
}
module bar_angle(len){
  color("SteelBlue") { translate([bar_x, 0, 0]) cube([ang, len, ang_t]); translate([bar_x, 0, 0]) cube([ang_t, len, ang]); }
}

// ---- 1. khoá chân cột: ôm góc cột + kẹp thanh định vị, 4 bulông M8
module post_lock(){
  difference(){
    translate([-44, -44, 0]) cube([114, 88, 50]);
    // hốc ôm cột (góc cột tại (-20,-20), 2 cánh 40×2)
    translate([-20 - cl, -20 - cl, -1]) cube([ang_t + 2*cl, 40 + 2*cl, 52]);
    translate([-20 - cl, -20 - cl, -1]) cube([40 + 2*cl, ang_t + 2*cl, 52]);
    translate([-17.4, -17.4, -1]) cube([37.4, 37.4, 52]);          // lòng cột rỗng
    bar_channel(200);
    // bulông xuyên cánh cột (2 phương) + bẫy đai ốc
    translate([-45, 0, 20]) rotate([0, 90, 0]) cylinder(d=m8, h=40);
    translate([-45, 0, 20]) rotate([0, 90, 0]) cylinder(d=m8n, h=12, $fn=6);
    translate([0, -45, 20]) rotate([-90, 0, 0]) cylinder(d=m8, h=40);
    translate([0, -45, 20]) rotate([-90, 0, 0]) cylinder(d=m8n, h=12, $fn=6);
    // 2 bulông kẹp cánh đứng của thanh
    for(y=[-25, 25]) {
      translate([8, y, 20]) rotate([0, 90, 0]) cylinder(d=m8, h=70);
      translate([8, y, 20]) rotate([0, 90, 0]) cylinder(d=m8n, h=10, $fn=6);
    }
    // vạch chỉ hướng phía B (khắc nổi ở mặt trên)
  }
  translate([34, -38, 50]) linear_extrude(1.2) text("B →", size=8, halign="left", font="DejaVu Sans:style=Bold");
}

// ---- 2. đế cột camera: kẹp thanh ở đúng 1 lỗ, ống Ø25,4 đứng thẳng
module mast_base(){
  difference(){
    union(){
      translate([16, -45, 0]) cube([96, 90, 50]);
      translate([88, 0, 0]) cylinder(d=mast_d + 16, h=90);
    }
    bar_channel(200);
    translate([88, 0, 30]) cylinder(d=mast_d + 0.4, h=70);               // lỗ cắm ống
    translate([88, 0, 70]) rotate([0, 90, 0]) cylinder(d=m5, h=30);       // vít M5 giữ ống
    translate([8, 0, 20]) rotate([0, 90, 0]) cylinder(d=m8, h=60);        // bulông định vị qua lỗ thanh
    translate([8, 0, 20]) rotate([0, 90, 0]) cylinder(d=m8n, h=10, $fn=6);
  }
}

// ---- 3. đầu camera: ôm đỉnh ống, chốt M4 khoá hướng, mặt bắt hộp trạm chúc 40°
module cam_head(){
  difference(){
    union(){
      cylinder(d=mast_d + 12, h=50);
      hull(){ translate([-15, -mast_d/2 - 2, 20]) cube([30, 6, 30]); translate(head_p) rotate([cam_tilt, 0, 0]) cube([50, 6, 50], center=true); }
    }
    translate([0, 0, -1]) cylinder(d=mast_d + 0.4, h=36);
    translate([-30, 0, 15]) rotate([0, 90, 0]) cylinder(d=4.4, h=60);   // chốt khoá hướng (khoan ống 1 lần)
    translate(head_p) rotate([cam_tilt, 0, 0]) rotate([90, 0, 0]) cylinder(d=6.8, h=20, center=true); // bulông 1/4"
  }
}
head_p = [0, -44, 62];
// hộp trạm gọi bắt vào mặt nghiêng: mặt trước hộp nhìn chúc xuống cam_tilt, về phía ray (−Y)
module head_box(){ translate(head_p) rotate([cam_tilt, 0, 0]) translate([0, -3 - 10 - gc[1]/2, -gc[2]/2]) call_box(); }

// ---- 4. đế khay lửa demo: kẹp thanh ở 1 lỗ; khay inox Ø200 tì vào 2 chốt → tâm khay luôn cách thanh như nhau
tray_peg = [124, 45];                                    // vị trí 2 chốt (x, ±y)
tray_cx = tray_peg[0] + sqrt(pow(100 + 6, 2) - pow(tray_peg[1], 2));   // ≈ 220
module tray_base(){
  difference(){
    union(){
      translate([16, -30, 0]) cube([60, 60, 50]);
      translate([60, -60, 0]) cube([72, 120, 6]);
      for(sy=[-1, 1]) translate([tray_peg[0], sy*tray_peg[1], 0]) cylinder(d=12, h=26);
    }
    bar_channel(200);
    translate([8, 0, 18]) rotate([0, 90, 0]) cylinder(d=m8, h=60);
    translate([8, 0, 18]) rotate([0, 90, 0]) cylinder(d=m8n, h=10, $fn=6);
  }
}

// ---- cảnh lắp: 1 cột (P2), ray, robot đang phun, thanh định vị sang phía B
module jig_scene(){
  // ray 2 tầng đoạn ngắn + robot + bình
  translate([0, 0, zL]) { color("Silver") translate([-900, -rail_t/2, 0]) cube([1800, rail_t, rail_h]); robot(); }
  translate([0, 0, zU]) { color("Silver") translate([-900, -rail_t/2, 0]) cube([1800, rail_t, rail_h]); tank_unit(); }
  ty_rods();
  for(x=[-500, 500], z=[zL, zU]) color("Orange") translate([x, 0, z]) hanger();
  // cột sắt lỗ + 2 thanh ngang dọc tuyến
  color("SteelBlue") translate([-20, post_y - 20, 0]) difference(){ cube([40, 40, zU + rail_h + 120]); translate([2, 2, -1]) cube([40, 40, zU + rail_h + 122]); }
  for(z=[zL + han_z0 + 5, zU + han_z0 + 5]) color("SteelBlue") translate([-900, post_y - 2, z - 15]) cube([1800, 4, 30]);
  color("Gainsboro") translate([-1200, post_y - 300, -2]) cube([2600, bar_len + 600, 2]);
  // thanh định vị + các khối in
  translate([0, post_y - 44, 0]) bar_angle(bar_len);
  translate([0, post_y, 0]) color("Orange") post_lock();
  translate([0, y_mast, 0]) { color("Orange") mast_base(); color("LightGray") translate([88, 0, 30]) cylinder(d=mast_d, h=mast_h); }
  translate([88, y_mast, 30 + mast_h - 35]) { color("Orange") cam_head(); color("Red") head_box(); }
  translate([0, y_tray, 0]) { color("Orange") tray_base(); color("DimGray") translate([tray_cx, 0, 0]) cylinder(d=200, h=36); color("OrangeRed") translate([tray_cx, 0, 36]) cylinder(d1=110, d2=0, h=130); }
  // tầm nhìn camera (minh hoạ)
  color("Red", 0.12) hull(){ translate([88, y_mast - 60, mast_h + 20]) sphere(d=8); translate([-700, 1000, 1]) cube([1600, 1500, 1]); }
}

if(jp == "scene")     jig_scene();
if(jp == "post_lock") post_lock();
if(jp == "mast_base") mast_base();
if(jp == "cam_head")  cam_head();
if(jp == "tray_base") tray_base();
