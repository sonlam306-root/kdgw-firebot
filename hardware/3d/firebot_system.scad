// =====================================================================
// FireBot — mô hình TOÀN HỆ THỐNG (để xem / xuất bản vẽ, không in)
// Dùng lại chi tiết trong firebot.scad
// view: system | robot | robot_side | station | plan
// =====================================================================
include <firebot.scad>
part = "none";
view = "system";
$fn = 32;

L1 = 2500;        // đoạn thẳng 1 (5 module)
L2 = 1500;        // đoạn thẳng 2 (3 module)
zL = floor_z - rail_h;          // đáy ray dưới
zU = floor_z + rail_gap;        // đáy ray trên
post_y = hand_y - 20;           // tâm cột sắt lỗ (phía A)
rob_x  = 1700;                  // vị trí robot khi xem toàn hệ thống
fire   = [2000, 4300, 0];       // khay lửa demo (phía B, ngoài chữ L)

// ---------------- ray đơn giản hoá cho toàn tuyến ----------------
module rail_simple(L, coils=true){
  color("Silver") translate([0,-rail_t/2,0]) cube([L, rail_t, rail_h]);
  if(coils) for(m=[0:floor(L/module_L)-1]) {
    color("MediumSeaGreen") translate([m*module_L+25, rail_t/2, base_z0]) cube([450, base_t, base_z1-base_z0]);
    for(i=[0:14]) color("Peru") translate([m*module_L+25+i*coil_pitch+1, rail_t/2+base_t, coil_z0]) cube([coil_w, coil_face-rail_t/2-base_t, coil_h]);
  }
}
module rail_curve(coils=true){
  // tâm cong tại gốc; ray từ góc 0° (điểm (R,0)) tới 90° (điểm (0,R))
  color("Silver") rotate_extrude(angle=90, $fn=96) translate([curve_R-rail_t/2, 0]) square([rail_t, rail_h]);
  if(coils){
    color("MediumSeaGreen") rotate_extrude(angle=90, $fn=96) translate([curve_R+rail_t/2, base_z0]) square([base_t, base_z1-base_z0]);
    n = floor((PI*curve_R/2 - 40)/coil_pitch);
    for(i=[0:n-1]) rotate([0,0,(20+ (i+0.5)*coil_pitch)/curve_R*180/PI])
      color("Peru") translate([curve_R+rail_t/2+base_t, -coil_w/2, coil_z0]) cube([coil_face-rail_t/2-base_t, coil_w, coil_h]);
  }
}
// đặt một vật dọc tuyến theo khoảng cách s (mm) tính từ đầu tuyến
module at_s(s){
  if(s <= L1) translate([s,0,0]) children();
  else if(s <= L1 + PI*curve_R/2) {
    a = (s-L1)/curve_R*180/PI;
    translate([L1, -curve_R, 0]) rotate([0,0,-a]) translate([0, curve_R, 0]) children();
  } else translate([L1+curve_R, -curve_R-(s-L1-PI*curve_R/2), 0]) rotate([0,0,-90]) children();
}
Ltot = L1 + PI*curve_R/2 + L2;

module level(z, coils){
  translate([0,0,z]){
    rail_simple(L1, coils);
    translate([L1, -curve_R, 0]) rotate([0,0,0]) rail_curve(coils);
    translate([L1+curve_R, -curve_R, 0]) rotate([0,0,-90]) rail_simple(L2, coils);
    // thanh treo tại mỗi mối nối + giữa cua
    for(s=[0:module_L:L1]) color("Orange") at_s(s) hanger();
    color("Orange") at_s(L1 + PI*curve_R/4) hanger();
    for(k=[0:3]) color("Orange") at_s(L1 + PI*curve_R/2 + k*module_L) hanger();
  }
}
// khung sắt lỗ: cột mỗi ~1,25 m + 2 thanh ngang dọc tuyến phía A
module frame(){
  hmax = zU + rail_h + 120;
  post_s = [0, 1250, 2500, L1+PI*curve_R/4, L1+PI*curve_R/2, L1+PI*curve_R/2+750, Ltot];
  for(s=post_s) at_s(s) color("SteelBlue") translate([-20, post_y-20, 0]) difference(){ cube([40,40,hmax]); translate([2,2,-1]) cube([40,40,hmax+2]); }
  for(z=[zL+han_z0+5, zU+han_z0+5]) for(i=[0:len(post_s)-2]) {
    p1 = s2p(post_s[i]); p2 = s2p(post_s[i+1]);
    color("SteelBlue") hull(){ translate([p1[0],p1[1],z]) cube([4,4,30],center=true); translate([p2[0],p2[1],z]) cube([4,4,30],center=true); }
  }
}
// toạ độ tâm cột (phía A) theo s
function s2p(s) = s <= L1 ? [s, post_y] :
  s <= L1+PI*curve_R/2 ? let(a=(s-L1)/curve_R) [L1 + (curve_R+post_y)*sin(a*180/PI), -curve_R + (curve_R+post_y)*cos(a*180/PI)] :
  [L1+curve_R+post_y, -curve_R-(s-L1-PI*curve_R/2)];

// ---------------- ROBOT (hệ toạ độ ray dưới: Z=0 là đáy ray) ----------------
Lb = 200;   // khoảng cách 2 bogie
module arm_link(len, d=34){ hull(){ sphere(d=d); translate([len,0,0]) sphere(d=d*0.85); } }
module robot(spray=true){
  // bogie + bánh
  for(x=[-Lb/2, Lb/2]) translate([x,0,0]){
    color("Gold") bogie(true);
    for(dx=[-wb/2, wb/2], z=[-wheel_cz, rail_h+wheel_cz]) color("DimGray") translate([dx,0,z]) rotate([-90,0,0]) cylinder(d=w_od, h=w_w, center=true);
    color("Goldenrod") translate([-12, 35, -50]) cube([24, 20, 66]);         // giá treo từ chốt xoay
  }
  // thân robot treo ngược
  color("SteelBlue", 0.9) translate([-170, -50, -230]) cube([340, 170, 180]);
  color("White") translate([-60, 120.5, -150]) cube([120, 0.5, 40]);           // nhãn
  color("Black") translate([-140, 30, -51]) cube([40, 40, 2]);                // tấm đồng sạc trên lưng
  color("DarkSlateGray") translate([-150, 0, -228]) cube([120, 100, 70]);     // hộp pin kín (ẩn trong thân)
  // tay máy 3 khớp ở đáy thân, phía trước
  translate([110, 60, -230]){
    color("DimGray") translate([0,0,-30]) cylinder(d=60, h=30);                // khớp 1: xoay ngang
    color("Black") translate([0,0,-48]) rotate([90,0,0]) cylinder(d=36, h=50, center=true); // khớp 2
    rotate([0,0,90]) translate([0,0,-48]) {
      rotate([0,40,0]) {
        color("OrangeRed") arm_link(140);                                     // khâu 1
        translate([140,0,0]) {
          color("Black") rotate([90,0,0]) cylinder(d=32, h=44, center=true);  // khớp 3
          rotate([0,-55,0]) {
            color("OrangeRed") arm_link(120, 28);                             // khâu 2
            translate([120,0,0]) {
              color("Goldenrod") rotate([0,90,0]) cylinder(d=10, h=150);       // đầu phun ống cứng
              color("Black") translate([150,0,0]) rotate([0,90,0]) cylinder(d1=12, d2=6, h=14);
              color("Teal") translate([10,-12,14]) cube([30,24,16]);           // MLX90640
              color("DarkRed") translate([-14,-10,-26]) cube([28,20,18]);      // van điện từ
            }
          }
        }
      }
    }
  }
}
// ---------------- BÌNH NƯỚC (hệ toạ độ ray trên) ----------------
module tank_unit(){
  for(x=[-Lb/2, Lb/2]) translate([x,0,0]){
    color("Khaki") bogie(false);
    for(dx=[-wb/2, wb/2], z=[-wheel_cz, rail_h+wheel_cz]) color("DimGray") translate([dx,0,z]) rotate([-90,0,0]) cylinder(d=w_od, h=w_w, center=true);
    color("DarkKhaki") translate([-12, 35, 44]) cube([24, 20, 50]);
  }
  color("Tan") translate([-130, -25, 92]) cube([260, 160, 8]);                // khay đỡ
  color("LightSkyBlue", 0.75) translate([-110, -15, 100]) cube([220, 150, 120]); // bình ~4 L
  color("RoyalBlue", 0.5) translate([-109, -14, 101]) cube([218, 148, 85]);     // mực nước
  color("White") translate([50, 45, 220]) cylinder(d=40, h=18);                  // miệng rót
  color("Black") translate([-90, 120, 205]) cube([14, 16, 14]);                  // cảm biến điện dung đỉnh
}
module ty_rods(){
  for(x=[-Lb/2, Lb/2]) color("Black") translate([x, plate_y1+12, zL+rail_h+wheel_cz]) cylinder(d=8, h=zU-wheel_cz-(zL+rail_h+wheel_cz));
  color("Black") translate([-80, 115, zL-50]) cylinder(d=10, h=zU+100-(zL-50));  // ống nước bình -> bơm
}
module water_jet(){
  // tia nước minh hoạ: parabol từ đầu phun tới khay lửa
  p0 = [rob_x+110, 470, zL-300];
  for(t=[0:0.04:0.96]) {
    a = p0 + t*(fire+[0,0,60]-p0) + [0,0, 900*t*(1-t)];
    b = p0 + (t+0.04)*(fire+[0,0,60]-p0) + [0,0, 900*(t+0.04)*(1-t-0.04)];
    color("DeepSkyBlue", 0.7) hull(){ translate(a) sphere(d=10); translate(b) sphere(d=10); }
  }
}
// ---------------- TRẠM CHÍNH (đầu tuyến, module 0) ----------------
module station(){
  // tấm chặn cuối ray
  for(z=[zL, zU]) color("Black") translate([-12, -20, z]) cube([12, 60, rail_h]);
  // giá má sạc: từ thanh treo phía A vòng xuống dưới ray
  color("Orange") translate([90, -110, zL-60]) cube([40, 110, 12]);
  color("Orange") translate([90, -110, zL-60]) cube([40, 12, 70]);
  color("Goldenrod") translate([96, 20, zL-52]) cube([28, 50, 4]);              // 2 má đồng lò xo
  // bể chứa + bơm tiếp nước + vòi rót tới miệng bình
  color("LightSkyBlue", 0.8) translate([150, 350, 0]) cube([300, 220, 280]);    // bể 10 L trên giá
  color("Gray") translate([140, 340, 280]) cube([320, 240, 6]);
  color("DimGray") translate([200, 360, 286]) cube([60, 40, 50]);               // bơm 12V
  color("Black") translate([228, 380, 336]) cylinder(d=10, h=zU+260-336);
  color("Black") translate([228, 380, zU+260]) rotate([90,0,0]) cylinder(d=10, h=330);
  color("Black") translate([228, 50, zU+260]) cylinder(d=10, h=-30);
  // hộp KD-GW trên cột
  color("WhiteSmoke") translate([-30, post_y-150, zL-300]) cube([150, 100, 220]);
  color("Red") translate([30, post_y-150.5, zL-130]) rotate([90,0,0]) cylinder(d=40, h=8); // nút dừng khẩn
}
module camera_pole(){
  color("Gray") translate([3700, 3800, 0]) cylinder(d=40, h=2400);
  color("Black") translate([3700, 3800, 2400]) rotate([0,30,-140]) cube([120, 60, 60], center=true);
}
module fire_tray(){
  color("DimGray") translate(fire) cylinder(d=200, h=40);
  color("OrangeRed") translate(fire+[0,0,40]) cylinder(d1=120, d2=0, h=140);
}
module floor_plate(){ color("Gainsboro") translate([-1200, -2700, -2]) cube([5200, 7600, 2]); }

module system(){
  floor_plate();
  level(zL, true);
  level(zU, false);
  frame();
  translate([rob_x, 0, zL]) robot();
  translate([rob_x, 0, zU]) tank_unit();
  translate([rob_x, 0, 0]) ty_rods();
  water_jet();
  station();
  camera_pole();
  fire_tray();
}
module robot_closeup(){
  translate([0,0,zL]) { color("Silver") translate([-400,-rail_t/2,0]) cube([800,rail_t,rail_h]); robot(); }
  translate([0,0,zU]) { color("Silver") translate([-400,-rail_t/2,0]) cube([800,rail_t,rail_h]); tank_unit(); }
  ty_rods();
  for(x=[-250, 250], z=[zL, zU]) color("Orange") translate([x,0,z]) hanger();
}

if(view=="system")     system();
if(view=="robot")      robot_closeup();
if(view=="station")    { translate([0,0,0]) { level(zL,true); level(zU,false); station(); translate([250,0,zL]) robot(); translate([250,0,zU]) tank_unit(); translate([250,0,0]) ty_rods(); } }
