// =====================================================================
// FireBot — thư viện chi tiết in 3D, đợt 1: RAY + MODULE THỬ (M0)
// Hệ toạ độ: X dọc ray, Y ngang ray, Z thẳng đứng (mm).
// Thanh ray nhôm dẹt dựng đứng: Y từ -rail_t/2..+rail_t/2, Z 0..rail_h
//   Phía A (Y < 0): thanh treo -> khung sắt lỗ. Phía A LUÔN là phía TRONG cua.
//   Phía B (Y > 0): cuộn dây, bogie, robot. Phía B LUÔN là phía NGOÀI cua.
// Xuất từng chi tiết: openscad -D 'part="hanger"' -o hanger.stl firebot.scad
// =====================================================================
part = "assembly";   // hanger | bobbin | coil_seg | coil_seg_hall | coil_seg_curve
                     // bogie_lower | bogie_upper | spacer | jig | assembly | section
$fn = 48;

// ---------- Ray ----------
rail_h   = 60;     // chiều cao thanh nhôm dẹt (đề xuất 60x6)
rail_t   = 6;      // bề dày
module_L = 500;    // chiều dài 1 module thẳng
curve_R  = 600;    // bán kính cua, đo tại tâm ray dưới
floor_z  = 1200;   // mép TRÊN ray dưới cách sàn 1,2 m
rail_gap = 200;    // khe hở giữa mép trên ray dưới và mép dưới ray trên

// ---------- Động cơ tuyến tính ----------
tau        = 22.5;           // bước cực nam châm
coil_pitch = 4*tau/3;        // = 30: 3 cuộn / 4 cực
coil_n     = 5;              // số cuộn mỗi đoạn giá
seg_len    = coil_n*coil_pitch;   // 150 mm, 3 đoạn = 15 cuộn = 450 mm / module
coil_w     = 28;   // kích thước ngoài cuộn theo X
coil_h     = 30;   // theo Z
coil_z0    = 15;   // đáy cuộn (Z)
core_w     = 10;   core_h = 12;   // lõi bobbin (rỗng)
fl         = 1;    // bề dày mặt bích bobbin
wind       = 10;   // chiều dài quấn theo Y
base_t     = 3;    // đế giá cuộn
base_z0    = 5;    base_z1 = 57;
gap        = 3;    // khe hở cuộn dây - nam châm
mag        = [20, 30, 5];   // nam châm NdFeB khối X x Z x Y (từ hoá theo Y)
mag_n      = 4;             // số nam châm mỗi bogie
back_t     = 1.6;           // thép lót lưng
hall_z     = 48.5;          // tâm cảm biến Hall (TO-92) theo Z
hall_dx    = 2*tau/3;       // 15 mm = 120° điện

// ---------- Bánh xe & bogie ----------
w_od     = 22;     // bạc đạn rãnh U (ôm mép dẹt 6 mm)
w_w      = 7;
w_groove = 2;      // độ sâu rãnh
axle_d   = 6.3;    // trục M6 cấp 12.9, vòng bi U626ZZ 6x22x7
sleeve_d = 8.2;    // ống lót thép 6x8 xuyên tấm bogie
wb       = 90;     // khoảng trục bogie (qua được R600)
bog_len  = 116;
bog_t    = 5;      // phần lưng sau túi nam châm

// ---------- Thanh treo ----------
han_w   = 60;  han_t = 8;
han_z0  = 10;  han_z1 = 50;
arm_len = 100;          // khoảng cách mặt ray -> mặt khung sắt
arm_w   = 60;           // = han_w để in nằm nghiêng, thớ in chạy dọc tay đòn
end_t   = 6;   end_h = 76;
slot_w  = 8.8; slot_l = 20;   // rãnh cho bu lông M8 vào sắt lỗ
m5 = 5.5;  m3 = 3.4;  m6 = 6.4;  m8 = 8.6;

// ---------- Suy ra ----------
coil_face = rail_t/2 + base_t + fl + wind + fl;   // 18
mag_face  = coil_face + gap;                       // 21
pocket_d  = mag[2] + back_t;                       // 6.6
plate_y1  = mag_face + pocket_d + bog_t;           // ~32.6
wheel_cz  = w_od/2 - w_groove;                      // tâm bánh cách mép ray
hand_y    = -rail_t/2 - han_t - arm_len - end_t;   // mặt sau thanh treo = mặt khung

// =====================================================================
// THANH TREO + NỐI RAY (đặt tại mỗi mối nối module, phía A)
// 4 bu lông M5 xuyên ray tại X=±13 (mỗi đầu ray 2 lỗ), Z=20/40
// Đầu còn lại: 2 rãnh đứng bắt M8 vào sắt lỗ, chỉnh cao ±10 mm
// =====================================================================
module hanger(){
  zc = (han_z0+han_z1)/2;
  difference(){
    union(){
      translate([-han_w/2, -rail_t/2-han_t, han_z0]) cube([han_w, han_t, han_z1-han_z0]);
      translate([-arm_w/2, -rail_t/2-han_t-arm_len, han_z0]) cube([arm_w, arm_len, han_z1-han_z0]);
      translate([-han_w/2, hand_y, zc-end_h/2]) cube([han_w, end_t, end_h]);
      // gân tăng cứng hai bên
      for(s=[-1,1]) hull(){
        translate([s*(arm_w/2)-(s>0?4:0), -rail_t/2-han_t-arm_len, zc-end_h/2]) cube([4, 1, end_h]);
        translate([s*(arm_w/2)-(s>0?4:0), -rail_t/2-han_t-arm_len+40, han_z0]) cube([4, 1, han_z1-han_z0]);
      }
    }
    for(x=[-13,13], z=[20,40]) translate([x,0,z]) rotate([90,0,0]) cylinder(d=m5, h=60, center=true);
    for(x=[-20,20]) translate([x, hand_y+end_t/2, zc]) hull()
      for(dz=[-slot_l/2, slot_l/2]) translate([0,0,dz]) rotate([90,0,0]) cylinder(d=slot_w, h=end_t+2, center=true);
    for(y=[30, 62]) translate([0, -rail_t/2-han_t-y, zc]) rotate([0,90,0]) cylinder(d=24, h=arm_w+2, center=true);
    // vạch tâm mối nối
    translate([-0.5, -rail_t/2-han_t-0.6, han_z0-1]) cube([1, 1, han_z1-han_z0+2]);
  }
}

// =====================================================================
// BOBBIN cuộn dây (in đứng, trục quấn theo Z khi in; khi lắp trục quấn theo Y)
// =====================================================================
module bobbin(){
  difference(){
    union(){
      translate([-coil_w/2, -coil_h/2, 0]) cube([coil_w, coil_h, fl]);
      translate([-coil_w/2, -coil_h/2, fl+wind]) cube([coil_w, coil_h, fl]);
      translate([-core_w/2, -core_h/2, 0]) cube([core_w, core_h, 2*fl+wind]);
    }
    translate([-core_w/2+1.2, -core_h/2+1.2, -1]) cube([core_w-2.4, core_h-2.4, 2*fl+wind+2]);
    translate([core_w/2-0.5, -0.8, -1]) cube([coil_w/2, 1.6, fl+2]);   // rãnh ra dây
  }
}

// bobbin ở vị trí lắp (trục quấn theo +Y), tâm X tại 0
module bobbin_placed(){
  translate([0, rail_t/2+base_t, coil_z0+coil_h/2]) rotate([-90,0,0]) bobbin();
}

// =====================================================================
// GIÁ CUỘN DÂY — 1 đoạn 5 cuộn, dài 150 mm, bắt vào mặt B của ray bằng M3
// hall=true: thêm dải giữ 3 cảm biến Hall TO-92 cách nhau 15 mm (120° điện)
// =====================================================================
module coil_unit(i){
  x = coil_pitch/2 + i*coil_pitch;
  translate([x,0,0]) children();
}
module seg_base_piece(x0, x1){
  translate([x0, rail_t/2, base_z0]) cube([x1-x0, base_t, base_z1-base_z0]);
}
module seg_pocket_rim(){
  // viền định vị bobbin, cao 1.5 mm
  difference(){
    translate([-coil_w/2-1.2, rail_t/2+base_t, coil_z0-1.2]) cube([coil_w+2.4, 1.5, coil_h+2.4]);
    translate([-coil_w/2-0.2, rail_t/2+base_t-1, coil_z0-0.2]) cube([coil_w+0.4, 4, coil_h+0.4]);
  }
}
module coil_seg(hall=false){
  difference(){
    union(){
      seg_base_piece(0, seg_len);
      for(i=[0:coil_n-1]) coil_unit(i) seg_pocket_rim();
      if(hall) translate([coil_pitch/2-6, rail_t/2+base_t, hall_z-3]) cube([2*hall_dx+12, coil_face-rail_t/2-base_t-0.5, 6]);
    }
    // lỗ bắt M3 (đầu bu lông phía A, đai ốc phía B)
    for(x=[12, seg_len/2, seg_len-12], z=[8.5, 53.5])
      translate([x, 0, z]) rotate([90,0,0]) cylinder(d=m3, h=30, center=true);
    for(x=[12, seg_len/2, seg_len-12], z=[8.5, 53.5])
      translate([x, rail_t/2+base_t, z]) rotate([-90,0,0]) cylinder(d=6.4, h=3, $fn=6);
    // khe cắm Hall TO-92 (4.6 x 3.6), mặt cảm biến hướng ra nam châm
    if(hall) for(k=[0:2]) translate([coil_pitch/2 + k*hall_dx - 2.3, coil_face-0.5-3.6, hall_z-2.5]) cube([4.6, 3.6+1, 8]);
    // lỗ luồn dây giữa các cuộn
    for(i=[0:coil_n-2]) translate([coil_pitch*(i+1), rail_t/2-1, coil_z0+coil_h/2]) rotate([-90,0,0]) cylinder(d=3, h=base_t+2);
  }
}
// bản cong cho module cua (phía B là phía ngoài cua)
module coil_seg_curve(){
  Rb = curve_R + rail_t/2;            // bán kính mặt B
  dth = coil_pitch / (curve_R + coil_face) * 180 / PI;
  difference(){
    union(){
      for(i=[0:coil_n-1]) {
        rotate([0,0,-(i+0.5)*dth]) translate([0, curve_R, 0]) children_unit_curve();
      }
      for(i=[0:coil_n-1]) hull(){
        rotate([0,0,-i*dth])     translate([0, curve_R, 0]) translate([-0.01, rail_t/2, base_z0]) cube([0.02, base_t, base_z1-base_z0]);
        rotate([0,0,-(i+1)*dth]) translate([0, curve_R, 0]) translate([-0.01, rail_t/2, base_z0]) cube([0.02, base_t, base_z1-base_z0]);
      }
    }
    for(a=[0.15, 0.5, 0.85]*coil_n*dth, z=[8.5, 53.5])
      rotate([0,0,-a]) translate([0, curve_R, z]) rotate([90,0,0]) cylinder(d=m3, h=30, center=true);
  }
}
module children_unit_curve(){ seg_pocket_rim(); }

// =====================================================================
// BOGIE RAY DƯỚI — 4 bánh rãnh U (2 trên tải, 2 dưới chống nhấc),
// túi 4 nam châm xen kẽ N/S + thép lót, chốt xoay đứng M6 cho thân robot
// =====================================================================
module bogie(magnets=true, upper=false){
  difference(){
    union(){
      translate([-bog_len/2, mag_face, -wheel_cz-8]) cube([bog_len, plate_y1-mag_face, rail_h+2*wheel_cz+16]);
      // khối chốt xoay
      translate([-14, plate_y1, rail_h/2-14]) cube([28, 22, 28]);
      // tai bắt thanh ty M8: bogie dưới ở mặt trên, bogie trên ở mặt dưới
      if(!upper) translate([-12, plate_y1, rail_h+wheel_cz+8-10]) cube([24, 22, 10]);
      else        translate([-12, plate_y1, -wheel_cz-8]) cube([24, 22, 10]);
    }
    for(x=[-wb/2, wb/2], z=[-wheel_cz, rail_h+wheel_cz])
      translate([x, 0, z]) rotate([-90,0,0]) cylinder(d=sleeve_d, h=80);
    if(magnets){
      for(k=[0:mag_n-1]) translate([-(mag_n-1)*tau/2 + k*tau - (mag[0]+0.3)/2, mag_face-0.01, coil_z0+coil_h/2-(mag[1]+0.3)/2])
        cube([mag[0]+0.3, mag[2]+0.01, mag[1]+0.3]);
      // rãnh thép lót lưng chạy suốt dãy
      translate([-((mag_n-1)*tau+mag[0])/2-0.2, mag_face+mag[2], coil_z0+coil_h/2-(mag[1]+0.4)/2])
        cube([(mag_n-1)*tau+mag[0]+0.4, back_t+0.2, mag[1]+0.4]);
    }
    translate([0, plate_y1+12, rail_h/2]) cylinder(d=m6, h=40, center=true);         // chốt xoay
    if(!upper) translate([0, plate_y1+12, rail_h+wheel_cz+3]) cylinder(d=m8, h=30, center=true); // thanh ty
    else        translate([0, plate_y1+12, -wheel_cz-3]) cylinder(d=m8, h=30, center=true);
    // lỗ giảm khối lượng
    for(x=[-30, 30]) translate([x, plate_y1-1, rail_h+wheel_cz-2]) rotate([-90,0,0]) cylinder(d=10, h=bog_t+2, center=true);
  }
}

// ống cách trục bánh (in, hoặc thay ống nhôm 6/12 mm)
module spacer(){ difference(){ cylinder(d=12, h=mag_face-w_w/2-0.6); translate([0,0,-1]) cylinder(d=axle_d, h=40);} }

// =====================================================================
// DƯỠNG KHOAN lỗ thanh treo: chụp lên mép trên ray, tì đầu ray vào gờ chặn
// =====================================================================
module jig(){
  difference(){
    translate([-5, -rail_t/2-5, 12]) cube([40, rail_t+10, rail_h+5-12]);
    translate([0, -rail_t/2-0.15, 0]) cube([60, rail_t+0.3, rail_h+0.01]);
    for(z=[20, 40]) translate([13, 0, z]) rotate([90,0,0]) cylinder(d=m5, h=40, center=true);
    translate([20, 0, rail_h-1]) cube([60, 1, 20]);   // khe ngắm
  }
}

// =====================================================================
// LẮP RÁP & MẶT CẮT (để kiểm tra, không in)
// =====================================================================
module rail_bar(L){ color("Silver") translate([0, -rail_t/2, 0]) cube([L, rail_t, rail_h]); }
module wheel(){ color("DimGray") rotate([-90,0,0]) difference(){ cylinder(d=w_od, h=w_w, center=true); } }
module slotted_post(h){ color("SteelBlue") translate([0, hand_y-40, 0]) difference(){ cube([40, 40, h]); translate([2, 2, -1]) cube([40, 40, h+2]); } }

module lower_level(){
  rail_bar(module_L);
  for(x=[0, module_L]) color("Orange") translate([x,0,0]) hanger();
  for(s=[0:2]) color("LightGreen") translate([25 + s*seg_len, 0, 0]) coil_seg(hall = (s==0));
  for(s=[0:2], i=[0:coil_n-1]) color("Peru") translate([25 + s*seg_len + coil_pitch/2 + i*coil_pitch, 0, 0]) bobbin_placed();
  translate([module_L/2, 0, 0]) {
    color("Gold") bogie(true);
    color("Red", 0.8) for(k=[0:mag_n-1]) translate([-(mag_n-1)*tau/2 + k*tau - mag[0]/2, mag_face, coil_z0]) cube([mag[0], mag[2], mag[1]]);
    for(x=[-wb/2, wb/2], z=[-wheel_cz, rail_h+wheel_cz]) translate([x,0,z]) wheel();
  }
}
module upper_level(){
  rail_bar(module_L);
  for(x=[0, module_L]) color("Orange") translate([x,0,0]) hanger();
  // ray trên cũng có cuộn dây (ADR-10): cùng pha với ray dưới, không cần Hall
  for(s=[0:2]) color("LightGreen") translate([25 + s*seg_len, 0, 0]) coil_seg(hall = false);
  for(s=[0:2], i=[0:coil_n-1]) color("Peru") translate([25 + s*seg_len + coil_pitch/2 + i*coil_pitch, 0, 0]) bobbin_placed();
  translate([module_L/2, 0, 0]) {
    color("Khaki") bogie(true, true);
    color("Red", 0.8) for(k=[0:mag_n-1]) translate([-(mag_n-1)*tau/2 + k*tau - mag[0]/2, mag_face, coil_z0]) cube([mag[0], mag[2], mag[1]]);
    for(x=[-wb/2, wb/2], z=[-wheel_cz, rail_h+wheel_cz]) translate([x,0,z]) wheel();
  }
}
module assembly(){
  zL = floor_z - rail_h;
  zU = floor_z + rail_gap;
  translate([0,0,zL]) lower_level();
  translate([0,0,zU]) upper_level();
  // thanh ty nối 2 bogie
  color("Black") translate([module_L/2, plate_y1+12, zL+rail_h+wheel_cz]) cylinder(d=8, h=zU-zL-rail_h-wheel_cz+ -wheel_cz+10);
  // khung sắt lỗ (cột đứng tại mỗi mối nối)
  for(x=[-20, module_L-20]) translate([x, 0, 0]) slotted_post(zU + rail_h + 150);
  // khối robot (giữ chỗ) treo dưới ray, khối bình (giữ chỗ) trên ray trên
  color("SkyBlue", 0.6) translate([module_L/2-150, -60, zL-wheel_cz-30-180]) cube([300, 120, 180]);
  color("SkyBlue", 0.6) translate([module_L/2-12, plate_y1, zL-wheel_cz-40]) cube([24, 24, rail_h/2+wheel_cz+40]);
  color("LightBlue", 0.6) translate([module_L/2-110, -70, zU+rail_h+wheel_cz+12]) cube([220, 140, 190]);
  // sàn
  color("Gainsboro") translate([-100, -400, -2]) cube([module_L+200, 800, 2]);
}

if(part=="hanger")         translate([0,0,han_w/2]) rotate([0,90,0]) hanger();
if(part=="bobbin")         bobbin();
if(part=="coil_seg")       rotate([90,0,0]) translate([0, -rail_t/2, 0]) coil_seg(false);
if(part=="coil_seg_hall")  rotate([90,0,0]) translate([0, -rail_t/2, 0]) coil_seg(true);
if(part=="coil_seg_curve") translate([0,-curve_R,-base_z0]) coil_seg_curve();
if(part=="bogie_lower")    translate([0,0,-mag_face]) rotate([90,0,0]) bogie(true);
if(part=="bogie_upper")    translate([0,0,-mag_face]) rotate([90,0,0]) bogie(true, true);  // ray trên cũng có nam châm (ADR-10)
if(part=="spacer")         spacer();
if(part=="jig")            translate([0,0,rail_h+5]) rotate([180,0,0]) jig();
if(part=="assembly")       assembly();
if(part=="lower")          lower_level();
if(part=="section")        intersection(){ translate([-module_L/2-10,0,0]) lower_level(); translate([-6,-300,-200]) cube([12, 600, 400]); }
