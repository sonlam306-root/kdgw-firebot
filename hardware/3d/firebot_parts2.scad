// =====================================================================
// FireBot — chi tiết in 3D ĐỢT 2: robot, tay máy, bình, trạm chính,
// trạm gọi cháy, hộp mạch. Dùng chung tham số với firebot.scad.
// Hệ toạ độ robot: gốc tại tâm robot theo X, Z = 0 là đáy ray dưới,
// thân robot X -170..170, Y -50..120, Z -230..-50.
// Xuất: openscad -D 'p="body_front"' -o body_front.stl firebot_parts2.scad
// =====================================================================
include <firebot.scad>
part = "none";
p = "preview";
id = 1;                 // số trạm gọi cháy / số module trên nắp hộp
$fn = 40;
font_b = "DejaVu Sans:style=Bold";

// ---------- thân robot ----------
B  = [170, 170, 180];   // một nửa thân: X x Y x Z
by0 = -50; bz0 = -230; bz1 = -50;
wt = 2.4; tt = 4; rim = 8;
m4 = 4.4; m3i = 4.2;    // M3 dùng ốc cấy nhiệt Ø4.2
hang_x = 100;           // vị trí giá treo theo X (đối xứng)
hang_holes = [[-18, 48], [18, 48], [-18, 64], [18, 64]];
// ---------- servo DS3225 ----------
srv_l = 40.4; srv_w = 20.4; srv_h = 40.5;
srv_ear = 55; srv_ear_y = 28;   // tai cách đáy servo 28 mm
srv_off = 10;                   // trục ra lệch tâm thân 10 mm
horn_r = 8;                     // 4 lỗ M3 của bát servo kim loại
blk_y0 = -24; blk_y1 = 21;      // khối ôm servo theo trục khớp
fork_in1 = 24.5; fork_in0 = -28.5; cheek = 5;

// =====================================================================
// THÂN ROBOT — 2 nửa (trước / sau), in úp, mở đáy, bắt bulông M4 ở mép giữa
// =====================================================================
module body_half(front=true){
  difference(){
    union(){
      difference(){
        translate([0, by0, bz0]) cube(B);
        translate([-1, by0+wt, bz0-1]) cube([B[0]-wt+1, B[1]-2*wt, B[2]-tt+1]);
      }
      // mép ghép tại X = 0 (khung chữ U)
      difference(){
        translate([0, by0, bz0]) cube([5, B[1], B[2]]);
        translate([-1, by0+wt+rim, bz0-1]) cube([7, B[1]-2*wt-2*rim, B[2]-tt-rim+1]);
      }
      // gờ đáy bắt nắp
      difference(){
        translate([0, by0, bz0]) cube([B[0], B[1], 5]);
        translate([5+rim, by0+wt+rim, bz0-1]) cube([B[0]-wt-2*rim-5, B[1]-2*wt-2*rim, 7]);
      }
      // trụ ốc cấy dưới nóc cho giá treo
      for(h=hang_holes) translate([hang_x+h[0], h[1], bz1-tt-10]) cylinder(d=9, h=10.1);
      // gân nóc
      for(y=[0, 90]) translate([0, y, bz1-tt-8]) cube([B[0]-wt, 2.4, 8.1]);
    }
    for(h=hang_holes) translate([hang_x+h[0], h[1], bz1-tt-11]) cylinder(d=m3i+0.2, h=20);
    // lỗ ghép 2 nửa
    for(y=[by0+wt+4, by0+B[1]-wt-4], z=[bz0+30, bz0+90, bz0+150]) translate([0, y, z]) rotate([0,90,0]) cylinder(d=m4, h=20, center=true);
    for(y=[by0+60, by0+110]) translate([0, y, bz1-tt-4]) rotate([0,90,0]) cylinder(d=m4, h=20, center=true);
    // lỗ ốc nắp đáy (ốc cấy M3 từ dưới)
    for(pp=lid_holes()) translate([pp[0], pp[1], bz0-1]) cylinder(d=m3i, h=8);
    if(!front){
      translate([130, 5, bz1-1.5]) cube([30, 29, 2]);                    // hốc tấm đồng sạc
      for(y=[12, 27]) translate([145, y, bz1-6]) cylinder(d=4, h=10);     // lỗ dây sạc
      translate([80, 105, bz1-6]) cylinder(d=12.5, h=10);                // ống nước từ bình vào
      translate([30, 105, bz1-6]) cylinder(d=12.5, h=10);                // ống luồn dây (PG7)
    }
    // ô nhãn thông gió hông (phía B)
    if(front) translate([50, by0+B[1]-1, bz0+80]) cube([70, 3, 30]);
  }
  if(front) translate([50, by0+B[1]-2.4, bz0+80]) for(i=[0:6]) translate([5+i*10, 0, 0]) cube([3, 2.4, 30]);
}
function lid_holes() = [ for(x=[18, 60, 105, 150]) for(y=[by0+wt+rim/2+0.5, by0+B[1]-wt-rim/2-0.5]) [x, y] ];

// nắp đáy (mỗi nửa một tấm), rãnh gioăng 2 mm
module body_lid(front=true){
  difference(){
    translate([0, by0, 0]) cube([B[0], B[1], 4]);
    for(pp=lid_holes()) translate([pp[0], pp[1], -1]) cylinder(d=3.4, h=10);
    for(pp=lid_holes()) translate([pp[0], pp[1], -1]) cylinder(d=6.5, h=2.5);
    // rãnh gioăng
    difference(){
      translate([4, by0+3.5, 2.5]) cube([B[0]-9, B[1]-7, 2]);
      translate([6, by0+5.5, 2]) cube([B[0]-13, B[1]-11, 3]);
    }
    if(front){
      translate([110, 60, -1]) for(a=[45:90:315]) rotate([0,0,a]) translate([32,0,0]) cylinder(d=m4, h=10);
      translate([110, 60, -1]) cylinder(d=14, h=10);        // dây servo khớp 1
      translate([60, 60, -1])  cylinder(d=12.5, h=10);      // ống nước ra tay máy
    } else {
      // lỗ bắt giá bơm + khay pin
      for(x=[30, 140], y=[0, 70]) translate([x, y, -1]) cylinder(d=m4, h=10);
      for(x=[40, 120], y=[95, 110]) translate([x, y-0, -1]) cylinder(d=m4, h=10);
    }
  }
}

// =====================================================================
// GIÁ TREO TỪ CHỐT XOAY BOGIE — dir = -1 (xuống thân robot), +1 (lên khay bình)
// ôm khối chốt (Z 16..44) bằng 2 tai, bulông M6 thẳng đứng làm trục xoay
// =====================================================================
py = plate_y1 + 12;
module pivot_hanger(dir=-1){
  wy0 = 62; wy1 = 70;
  ztop = dir < 0 ? 51 : 92-6;
  zbot = dir < 0 ? -44 : 9;
  difference(){
    union(){
      for(z=[9, 45]) hull(){
        translate([0, py, z]) cylinder(r=11, h=6);
        translate([-14, wy0, z]) cube([28, wy1-wy0, 6]);
      }
      translate([-14, wy0, zbot]) cube([28, wy1-wy0, ztop-zbot]);
      if(dir < 0){
        translate([-28, 40, -50]) cube([56, 30, 6]);
        for(s=[-1,1]) hull(){ translate([s*14-(s>0?4:0), wy0, -44]) cube([4, 8, 1]); translate([s*14-(s>0?4:0), wy0-20, -44]) cube([4, 1, 1]); translate([s*14-(s>0?4:0), wy0, -20]) cube([4, 8, 1]); }
      } else {
        translate([-28, 40, 86]) cube([56, 30, 6]);
        for(s=[-1,1]) hull(){ translate([s*14-(s>0?4:0), wy0, 85]) cube([4, 8, 1]); translate([s*14-(s>0?4:0), wy0-20, 85]) cube([4, 1, 1]); translate([s*14-(s>0?4:0), wy0, 60]) cube([4, 8, 1]); }
      }
    }
    translate([0, py, 0]) cylinder(d=m6, h=120, center=true);
    for(h=hang_holes) translate([h[0], h[1], dir<0 ? -51 : 85]) cylinder(d=m4, h=10);
    for(h=hang_holes) translate([h[0], h[1], dir<0 ? -46 : 90]) cylinder(d=8, h=10);   // hốc đầu bulông
  }
}

// =====================================================================
// HỘP PIN KÍN 3S2P 18650 + BMS (cạnh trong 80 x 62 x 62)
// =====================================================================
module battery_box(){
  difference(){
    union(){
      translate([-43, -34, 0]) cube([86, 68, 66]);
      for(x=[-49, 49], y=[-20, 20]) hull(){ translate([x, y, 0]) cylinder(d=12, h=5); translate([x>0?40:-43, y-6, 0]) cube([3, 12, 5]); }
    }
    translate([-40, -31, 3]) cube([80, 62, 70]);
    for(x=[-49, 49], y=[-20, 20]) translate([x, y, -1]) cylinder(d=m4, h=10);
    for(x=[-38, 38], y=[-29, 29]) translate([x, y, 55]) cylinder(d=m3i, h=12);
    translate([0, 34, 40]) rotate([90,0,0]) cylinder(d=12.5, h=8, center=true);   // PG7
  }
  for(x=[-38, 38], y=[-29, 29]) translate([x, y, 3]) difference(){ cylinder(d=8, h=63); translate([0,0,52]) cylinder(d=m3i, h=12); }
}
module battery_lid(){
  difference(){
    union(){ translate([-43, -34, 0]) cube([86, 68, 3]); translate([-39.6, -30.6, 3]) difference(){ cube([79.2, 61.2, 4]); translate([2,2,-1]) cube([75.2, 57.2, 6]); } }
    for(x=[-38, 38], y=[-29, 29]) translate([x, y, -1]) cylinder(d=3.4, h=10);
    translate([-41, -32, 1.8]) difference(){ cube([82, 64, 2]); translate([1.5,1.5,-1]) cube([79, 61, 4]); }  // rãnh gioăng
  }
}

// GIÁ BƠM MÀNG 12V — 2 yên đỡ thân Ø40, rãnh dây rút
module pump_cradle(){
  difference(){
    union(){
      translate([-65, -35, 0]) cube([130, 70, 4]);
      for(x=[-35, 35]) translate([x-6, -30, 0]) cube([12, 60, 28]);
    }
    for(x=[-35, 35]) translate([x, 0, 30]) rotate([0,90,0]) cylinder(d=40.5, h=14, center=true);
    for(x=[-35, 35], y=[-24, 24]) translate([x, y, 8]) cube([14, 4, 8], center=true);
    for(x=[-55, 55], y=[-25, 25]) translate([x, y, -1]) cylinder(d=m4, h=10);
    for(x=[-20, 0, 20]) translate([x, 0, -1]) cylinder(d=5, h=10);   // rãnh thoát nước
  }
}
// KHAY MẠCH ROBOT — mạch 80x60 (lỗ 74x54) + ESP32-S3 DevKit
module electronics_tray(){
  difference(){
    translate([-60, -45, 0]) cube([120, 90, 3]);
    for(x=[-50, 50], y=[-35, 35]) translate([x, y, -1]) cylinder(d=m4, h=10);
    for(x=[-45, 45]) translate([x, 0, -1]) cylinder(d=10, h=10);
  }
  for(x=[-37, 37], y=[-27, 27]) translate([x-20, y, 3]) difference(){ cylinder(d=7, h=6); cylinder(d=m3i-0.6, h=7); }
  for(y=[-12, 12]) translate([42, y, 3]) difference(){ cube([6, 3, 10], center=false); }
}

// =====================================================================
// TAY MÁY 3 KHỚP — servo DS3225, ống PU 8x5 đi trong lòng khâu
// =====================================================================
// khối ôm servo, trục khớp = trục Y qua gốc; servo nằm, trục ra hướng +Y
module servo_block(){
  difference(){
    translate([-38, blk_y0, -13]) cube([58, blk_y1-blk_y0, 26]);
    // thân servo (đặt từ phía +Y), tai tựa trên gờ tại Y = -21+28
    translate([-srv_off-srv_l/2, -21, -srv_w/2]) cube([srv_l, 50, srv_w]);
    translate([-srv_off-srv_ear/2, -21+srv_ear_y, -srv_w/2]) cube([srv_ear, 20, srv_w]);
    for(s=[-1,1], z=[-5, 5]) translate([-srv_off+s*24.75, -21+srv_ear_y-8, z]) rotate([-90,0,0]) cylinder(d=2.6, h=9);
    translate([-srv_off-srv_l/2-6, -10, -4]) cube([7, 12, 8]);   // khe dây servo
  }
  // trụ trục phụ phía -Y (bulông vai M5 + ốc cấy)
  translate([0, blk_y0, 0]) rotate([90,0,0]) difference(){ cylinder(d=14, h=4); translate([0,0,-1]) cylinder(d=6.4, h=6); }
}
// càng ôm khớp (2 má): má +Y bắt bát servo, má -Y quay trên bulông vai M5
module fork(len){
  for(side=[1, -1]){
    y0 = side > 0 ? fork_in1 : fork_in0 - cheek;
    difference(){
      hull(){ translate([0, y0, 0]) rotate([-90,0,0]) cylinder(r=17, h=cheek); translate([len-1, y0, -13]) cube([1, cheek, 26]); }
      if(side > 0){
        translate([0, y0-1, 0]) rotate([-90,0,0]) cylinder(d=8, h=cheek+2);
        for(a=[0:90:270]) rotate([0,a,0]) translate([horn_r, y0-1, 0]) rotate([-90,0,0]) cylinder(d=3.3, h=cheek+2);
        translate([0, y0-0.5, 0]) rotate([-90,0,0]) cylinder(d=25.4, h=2);
      } else translate([0, y0-1, 0]) rotate([-90,0,0]) cylinder(d=5.3, h=cheek+2);
    }
  }
}
// thân khâu rỗng (ống nước PU 8x5 chạy bên trong)
module link_tube(x0, x1){
  W = fork_in1 + cheek - (fork_in0 - cheek); yc = (fork_in1 + cheek + fork_in0 - cheek)/2;
  difference(){
    translate([x0, yc-W/2, -13]) cube([x1-x0, W, 26]);
    translate([x0-1, yc-W/2+2.4, -13+2.4]) cube([x1-x0+2, W-4.8, 26-4.8]);
  }
}
module link1(L=140){
  difference(){
    union(){
      fork(34);
      link_tube(30, L-36);
      translate([L, 0, 0]) servo_block();
    }
    translate([42, -2, 10]) cylinder(d=10, h=10);          // ống nước vào (vòng qua khớp 2)
    translate([L-46, -2, 10]) cylinder(d=10, h=10);        // ống nước ra (vòng qua khớp 3)
  }
}
module link2(L=120){
  difference(){
    union(){
      fork(34);
      link_tube(30, L-10);
      // đầu khâu: kẹp ống phun cứng Ø10, giá van, đế MLX90640
      translate([L-14, -2, 0]) rotate([0,90,0]) cylinder(d=24, h=40);
      translate([L-50, -20, 13]) cube([40, 36, 3]);                       // đế van điện từ
      translate([L-6, -19, 13]) cube([30, 34, 3]);                        // đế MLX90640
    }
    translate([L-20, -2, 0]) rotate([0,90,0]) cylinder(d=10.2, h=60);      // lỗ ống phun cứng
    translate([L+6, -2.6, -14]) cube([20, 1.2, 14]);                       // khe kẹp
    translate([L+16, -20, -7]) rotate([-90,0,0]) cylinder(d=3.3, h=40);    // bulông kẹp M3
    translate([L-46, -2, 10]) cylinder(d=10, h=10);
    for(x=[L-44, L-16], y=[-16, 12]) translate([x, y, 12]) cube([3, 4, 6]);    // khe dây rút van
    for(x=[L-1, L+19], y=[-14, 10]) translate([x, y, 12]) cylinder(d=2.7, h=6);  // lỗ M2.5 module nhiệt
    translate([42, -2, 10]) cylinder(d=10, h=10);
  }
}
// khớp 1: vỏ ôm servo đứng, bắt dưới nắp đáy trước
module arm_base(){
  difference(){
    union(){
      cylinder(d=80, h=5);
      translate([0,0,-44]) cylinder(d=66, h=44);
    }
    for(a=[45:90:315]) rotate([0,0,a]) translate([32,0,-1]) cylinder(d=m4, h=10);
    // servo đứng, trục xuống, trục quay trùng tâm
    translate([-srv_off-srv_l/2, -srv_w/2, -45]) cube([srv_l, srv_w, 60]);
    translate([-srv_off-srv_ear/2, -srv_w/2, -29]) cube([srv_ear, srv_w, 60]);
    translate([0, 0, -50]) cylinder(d=27, h=10);
    translate([-30, -3, -1]) cube([12, 6, 10]);
  }
}
// bàn xoay khớp 1 + khối servo khớp 2 treo dưới
module yaw_plate(){
  difference(){
    union(){
      cylinder(d=66, h=6);
      translate([-28, -20, -26]) cube([58, 40, 26.1]);          // cổ nối xuống khối khớp 2
      translate([10, 0, -39]) servo_block();
    }
    translate([0,0,-1]) cylinder(d=8, h=10);
    for(a=[0:90:270]) rotate([0,0,a]) translate([horn_r, 0, -1]) cylinder(d=3.3, h=10);
    translate([0,0,4]) cylinder(d=25.4, h=3);
    translate([-24, 0, -30]) cylinder(d=12, h=40);              // lỗ ống nước xuyên bàn xoay
  }
}
// =====================================================================
// BÌNH NƯỚC — khay đỡ 2 nửa, vách chắn sóng, kẹp cảm biến, phễu rót
// (bình mua sẵn: hộp nhựa PP ~4 L, ~220 x 150 x 120, khoan lỗ + ren ống)
// =====================================================================
module tank_tray_half(front=true){
  difference(){
    union(){
      translate([0, -25, 0]) cube([130, 160, 4]);
      difference(){ translate([0, -25, 0]) cube([130, 160, 16]); translate([-1, -22, 3]) cube([128, 154, 20]); }
      translate([0, -25, -12]) cube([4, 160, 12]);      // gờ ghép giữa
    }
    for(h=hang_holes) translate([100+h[0], h[1], -1]) cylinder(d=m4, h=10);
    for(y=[0, 55, 110]) translate([0, y, -6]) rotate([0,90,0]) cylinder(d=m4, h=12, center=true);
    if(!front) translate([80, 100, -1]) cylinder(d=21, h=10);            // lỗ đầu ra bình
    for(x=[30, 70], y=[20, 90]) translate([x, y, -1]) cylinder(d=6, h=10);  // lỗ thoát nước
  }
}
module tank_baffle(){
  difference(){
    cube([140, 3, 100]);
    for(x=[20, 45, 70, 95, 120]) translate([x, -1, 18]) rotate([-90,0,0]) cylinder(d=14, h=6);
    for(x=[32, 57, 82, 107]) translate([x, -1, 60]) rotate([-90,0,0]) cylinder(d=10, h=6);
    translate([66, -1, 90]) cube([8, 6, 11]);
  }
}
module level_clip(){       // giữ cảm biến mực nước điện dung (thân ~28x28x14) áp thành bình
  difference(){
    union(){ translate([-18, -10, 0]) cube([36, 20, 34]); for(x=[-24, 24]) translate([x-4, -10, 0]) cube([8, 3, 34]); }
    translate([-14.5, -7.5, 3]) cube([29, 15, 40]);
    for(x=[-24, 24]) translate([x, -12, 17]) cube([3, 10, 12], center=true);
    translate([0, 0, -1]) cylinder(d=6, h=5);
  }
}
module fill_funnel(){
  difference(){
    union(){ cylinder(d1=22, d2=70, h=40); translate([0,0,-18]) cylinder(d=21.4, h=18); cylinder(d=34, h=3); }
    translate([0,0,1]) cylinder(d1=16, d2=66, h=40);
    translate([0,0,-20]) cylinder(d=16, h=22);
  }
}

// =====================================================================
// TRẠM CHÍNH
// =====================================================================
// giá má sạc: bắt vào mặt thanh sắt lỗ ngang (phía A), luồn dưới ray,
// 2 tiếp điểm lò xo Ø7 hướng xuống, nằm trong vùng Y 12/28 của tấm đồng robot
module charge_holder(){
  y0 = hand_y; z_top = 45; z_arm = -40;
  difference(){
    union(){
      translate([-20, y0, z_arm]) cube([40, 6, z_top-z_arm]);
      translate([-20, y0, z_arm]) cube([40, 45-y0, 10]);
      for(s=[-1,1]) hull(){ translate([s*20-(s>0?4:0), y0, z_arm]) cube([4, 40, 1]); translate([s*20-(s>0?4:0), y0, z_arm+40]) cube([4, 6, 1]); translate([s*20-(s>0?4:0), y0, z_arm+9]) cube([4, 40, 1]); }
      translate([-14, 4, z_arm-6]) cube([28, 36, 6]);
    }
    for(z=[20, 40]) translate([0, y0+3, z]) hull(){ for(dx=[-8, 8]) translate([dx,0,0]) rotate([90,0,0]) cylinder(d=slot_w, h=8, center=true); }
    for(y=[12, 28]) translate([0, y, z_arm-10]) cylinder(d=7.2, h=30);     // tiếp điểm lò xo (+ / -)
    translate([-3, 0, z_arm+4]) cube([6, 46, 3]);                         // rãnh dây
  }
}
// giá vòi rót tiếp nước — 2 mảnh: A bắt thanh ngang ray trên, B có tay vươn tới miệng bình
module refill_holder_a(){
  y0 = hand_y;
  difference(){
    translate([-20, y0, 10]) cube([40, 6, 150]);
    for(z=[20, 40]) translate([0, y0+3, z]) hull(){ for(dx=[-8, 8]) translate([dx,0,0]) rotate([90,0,0]) cylinder(d=slot_w, h=8, center=true); }
    for(z=[135, 150]) translate([0, y0+3, z]) rotate([90,0,0]) cylinder(d=m5, h=10, center=true);
  }
}
module refill_holder_b(){
  y0 = hand_y; zt = 262;
  difference(){
    union(){
      translate([-20, y0+6, 125]) cube([40, 6, zt+8-125]);
      translate([-20, y0+6, zt]) cube([40, 45-y0+6, 8]);
      translate([0, 45, zt-10]) cylinder(d=22, h=18);
      for(s=[-1,1]) hull(){ translate([s*20-(s>0?4:0), y0+6, zt]) cube([4, 50, 8]); translate([s*20-(s>0?4:0), y0+6, zt-50]) cube([4, 6, 1]); }
    }
    for(z=[135, 150]) translate([0, y0+9, z]) rotate([90,0,0]) cylinder(d=m5, h=10, center=true);
    translate([0, 45, zt-12]) cylinder(d=10.4, h=30);
    translate([-0.6, 40, zt-12]) cube([1.2, 12, 30]);
    translate([0, 56, zt-2]) rotate([0,90,0]) cylinder(d=3.3, h=30, center=true);
  }
}
// chặn cuối ray (phía B), bắt chung 2 bulông M5 của thanh treo cuối; hốc công tắc hành trình KW11
module end_stop(){
  difference(){
    translate([-25, rail_t/2, 10]) cube([25, 40, 40]);
    for(z=[20, 40]) translate([-13, 0, z]) rotate([-90,0,0]) cylinder(d=m5, h=60);
    for(z=[20, 40]) translate([-13, rail_t/2+5, z]) rotate([-90,0,0]) cylinder(d=9.5, h=60);
    translate([-26, rail_t/2+18, 18]) cube([4, 20, 24]);                   // đệm cao su
    translate([-21, rail_t/2+14, 50-7]) cube([20.4, 10.4, 8]);             // KW11-3Z
    for(x=[-17, -7.5]) translate([x, rail_t/2+19, 30]) cylinder(d=2.4, h=30);
  }
}

// =====================================================================
// TRẠM GỌI CHÁY (x2) — ESP32-S3 CAM + cảm biến lửa IR + nút gọi cháy + còi
// =====================================================================
gc = [90, 66, 46];    // ngoài
module call_box(){
  difference(){
    translate([-gc[0]/2, -gc[1]/2, 0]) cube(gc);
    translate([-gc[0]/2+2.4, -gc[1]/2+2.4, 2.4]) cube([gc[0]-4.8, gc[1]-4.8, gc[2]]);
    // mặt trước (-Y): camera, cảm biến lửa, nút, LED
    translate([-14, -gc[1]/2-1, 34]) rotate([-90,0,0]) cylinder(d=14, h=5);
    translate([14, -gc[1]/2-1, 34]) rotate([-90,0,0]) cylinder(d=10.5, h=5);
    translate([0, -gc[1]/2-1, 15]) rotate([-90,0,0]) cylinder(d=16.3, h=5);
    translate([28, -gc[1]/2-1, 15]) rotate([-90,0,0]) cylinder(d=5.2, h=5);
    // hông: lưới còi, đáy: cổng USB-C
    for(i=[-2:2], j=[-1:1]) translate([gc[0]/2-3, i*5, 22+j*5]) rotate([0,90,0]) cylinder(d=2.5, h=5);
    translate([-6, -10, -1]) cube([12, 7, 4]);
    
  }
  for(x=[-gc[0]/2+5.5, gc[0]/2-5.5], y=[-gc[1]/2+5.5, gc[1]/2-5.5]) translate([x, y, 1]) difference(){ cylinder(d=8, h=gc[2]-1.5); translate([0,0,gc[2]-13]) cylinder(d=m3i, h=13); }
  // đế gắn chân máy ảnh 1/4" + khe dây đai bó cột
  translate([0, gc[1]/2-0.5, gc[2]/2]) rotate([-90,0,0]) difference(){
    union(){ cylinder(d=22, h=10); translate([-30, -18, 0]) cube([60, 6, 6]); translate([-30, 12, 0]) cube([60, 6, 6]); }
    translate([0,0,-1]) cylinder(d=6.8, h=12);
    translate([0,0,3]) cylinder(d=12.8, h=6, $fn=6);
    for(x=[-24, 24]) translate([x, -20, 2]) cube([4, 40, 3]);
  }
}
module call_lid(n=1){
  difference(){
    translate([-gc[0]/2, -gc[1]/2, 0]) cube([gc[0], gc[1], 3]);
    for(x=[-gc[0]/2+5.5, gc[0]/2-5.5], y=[-gc[1]/2+5.5, gc[1]/2-5.5]) translate([x, y, -1]) cylinder(d=3.4, h=6);
  }
  color("Red") translate([0, 8, 3]) linear_extrude(1.2) text("GỌI CHÁY", size=9, font=font_b, halign="center", valign="center");
  translate([0, -12, 3]) linear_extrude(1.2) text(str("TRẠM ", n), size=8, font=font_b, halign="center", valign="center");
}

// HỘP MẠCH MODULE RAY (x9) — mạch ~70 x 50, 2 lỗ PG7, tai bắt sắt lỗ
mb = [86, 66, 34];
module module_box(){
  difference(){
    union(){
      translate([-mb[0]/2, -mb[1]/2, 0]) cube(mb);
      translate([-mb[0]/2-22, -15, 0]) cube([mb[0]+44, 30, 4]);
    }
    translate([-mb[0]/2+2.4, -mb[1]/2+2.4, 2.4]) cube([mb[0]-4.8, mb[1]-4.8, mb[2]]);
    for(s=[-1,1]) translate([s*(mb[0]/2+11), 0, -1]) hull(){ for(dy=[-6,6]) translate([0,dy,0]) cylinder(d=slot_w, h=6); }
    for(y=[-14, 14]) translate([mb[0]/2-3, y, 18]) rotate([0,90,0]) cylinder(d=12.5, h=6);
    for(x=[-mb[0]/2+5, mb[0]/2-5], y=[-mb[1]/2+5, mb[1]/2-5]) translate([x, y, mb[2]-10]) cylinder(d=m3i, h=11);
  }
  for(x=[-mb[0]/2+5, mb[0]/2-5], y=[-mb[1]/2+5, mb[1]/2-5]) translate([x, y, 0]) difference(){ cylinder(d=8, h=mb[2]); translate([0,0,mb[2]-10]) cylinder(d=m3i, h=11); }
  for(x=[-32, 32], y=[-22, 22]) translate([x, y, 2.4]) difference(){ cylinder(d=6, h=5); cylinder(d=2.5, h=6); }
}
module module_lid(n=0){
  difference(){
    translate([-mb[0]/2, -mb[1]/2, 0]) cube([mb[0], mb[1], 3]);
    for(x=[-mb[0]/2+5, mb[0]/2-5], y=[-mb[1]/2+5, mb[1]/2-5]) translate([x, y, -1]) cylinder(d=3.4, h=6);
  }
  translate([0, 4, 3]) linear_extrude(1.2) text(str("M", n), size=20, font=font_b, halign="center", valign="center");
  translate([0, -20, 3]) linear_extrude(1.2) text("FIREBOT", size=6, font=font_b, halign="center", valign="center");
}

// =====================================================================
// LẮP RÁP XEM TRƯỚC (robot + bình trên 1 đoạn ray)
// =====================================================================
module arm_assembly(){
  // gốc tại tâm khớp 1 dưới nắp đáy trước (toạ độ robot X 110, Y 60, Z -230)
  color("DimGray") arm_base();
  translate([0,0,-50]) rotate([0,0,90]) {
    color("SlateGray") translate([0,0,-6]) yaw_plate();
    translate([10, 0, -45]) rotate([0, 40, 0]) {
      color("OrangeRed") link1(140);
      translate([140, 0, 0]) rotate([0, -55, 0]) color("Coral") link2(120);
    }
  }
}
module robot_preview(){
  for(s=[1,-1]) mirror([s<0?1:0,0,0]) {
    color("SteelBlue", 0.55) body_half(s>0);
    color("LightSteelBlue") translate([0,0,bz0-4]) body_lid(s>0);
    for(x=[hang_x]) translate([x, 0, 0]) color("Goldenrod") pivot_hanger(-1);
  }
  translate([110, 60, bz0-4]) arm_assembly();
  color("DarkSlateGray") translate([-90, 35, bz0+2]) battery_box();
  color("Gray") translate([-85, 60, bz0+2]) translate([0,0,0]) pump_cradle();
}

if(p=="body_front")      rotate([180,0,0]) translate([0,0,-bz1]) body_half(true);
if(p=="body_rear")       rotate([180,0,0]) translate([0,0,-bz1]) body_half(false);
if(p=="lid_front")       body_lid(true);
if(p=="lid_rear")        body_lid(false);
if(p=="hanger_robot")    translate([0,0,70]) rotate([-90,0,0]) pivot_hanger(-1);
if(p=="hanger_tank")     translate([0,0,70]) rotate([-90,0,0]) pivot_hanger(1);
if(p=="battery_box")     battery_box();
if(p=="battery_lid")     battery_lid();
if(p=="pump_cradle")     pump_cradle();
if(p=="electronics_tray") electronics_tray();
if(p=="arm_base")        translate([0,0,5]) rotate([180,0,0]) arm_base();
if(p=="yaw_plate")       translate([0,0,6]) rotate([180,0,0]) yaw_plate();
if(p=="link1")           rotate([90,0,0]) translate([0, -fork_in0+cheek, 0]) link1(140);
if(p=="link2")           rotate([90,0,0]) translate([0, -fork_in0+cheek, 0]) link2(120);
if(p=="tank_tray_front") rotate([180,0,0]) translate([0,0,-16]) tank_tray_half(true);
if(p=="tank_tray_rear")  rotate([180,0,0]) translate([0,0,-16]) tank_tray_half(false);
if(p=="tank_baffle")     translate([0,0,3]) rotate([90,0,0]) tank_baffle();
if(p=="level_clip")      level_clip();
if(p=="fill_funnel")     translate([0,0,40]) rotate([180,0,0]) fill_funnel();
if(p=="charge_holder")   translate([0,0,20]) rotate([0,90,0]) charge_holder();
if(p=="refill_holder_a") rotate([90,0,0]) translate([0,-hand_y,0]) refill_holder_a();
if(p=="refill_holder_b") translate([0,0,20]) rotate([0,90,0]) refill_holder_b();
if(p=="end_stop")        rotate([0,90,0]) end_stop();
if(p=="call_box")        call_box();
if(p=="call_lid")        call_lid(id);
if(p=="module_box")      module_box();
if(p=="module_lid")      module_lid(id);
if(p=="robot_preview")   robot_preview();
