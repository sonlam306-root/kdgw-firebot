# Bản vẽ mặt cắt ngang ray FireBot (nhìn dọc ray), xuất SVG
rail_h,rail_t=60,6; coil_face=18; gap=3; mag_face=21; plate_y1=32.6
han_t,arm_len,end_t=8,100,6; hand_y=-(3+han_t+arm_len+end_t)
w_od,w_g=22,2; wcz=w_od/2-w_g
floor_top=1200; rail_gap=200
out=[]
def R(x,y,w,h,fill="none",stroke="#555",sw=1.2,rx=0,op=1): out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>')
def T(x,y,s,size=13,anchor="start",w="400",fill="#222"): out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{fill}" font-family="DejaVu Sans">{s}</text>')
def L(x1,y1,x2,y2,stroke="#888",sw=1,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
def C(x,y,r,fill="#666"): out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"/>')
def dimv(x,z1,z2,label,P,side=1):
    X,Y1=P(0,z1)[0]*0+x,P(0,z1)[1]; Y2=P(0,z2)[1]
    L(x,Y1,x,Y2,"#c0392b",1.2); L(x-5,Y1,x+5,Y1,"#c0392b"); L(x-5,Y2,x+5,Y2,"#c0392b")
    T(x+8*side,(Y1+Y2)/2+4,label,12,"start" if side>0 else "end",fill="#c0392b")
W,H=1500,980
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="white"/>')

T(30,66,"Phía A (trái) = thanh treo + khung sắt lỗ, luôn ở PHÍA TRONG cua · Phía B (phải) = cuộn dây, bogie, robot, luôn ở PHÍA NGOÀI cua — vùng phun nên ở phía B",13,fill="#555")
# ---------- Panel 1: tổng thể ----------
s1=0.36; ox1,oz1=400,930
P1=lambda y,z:(ox1+y*s1, oz1-z*s1)
T(40,100,"Tổng thể (tỉ lệ ~1:28)",15,w="700")
L(*P1(-500,0),*P1(500,0),"#333",2); T(P1(-480,0)[0],P1(0,0)[1]+18,"Sàn",12)
zL=floor_top-rail_h; zU=floor_top+rail_gap
# frame stringers/posts
x,y=P1(hand_y-40,1900); R(x,y,40*s1,1900*s1,"#3b6ea5",op=0.85,stroke="#2c5282")
for z0 in (zL,zU):
    x,y=P1(-3,z0+rail_h); R(x,y,rail_t*s1+1,rail_h*s1,"#999")
    x,y=P1(hand_y,z0+50); R(x,y,(abs(hand_y)-3)*s1,40*s1,"#f0a020",stroke="#b07010")
    x,y=P1(3,z0+45); R(x,y,15*s1+1,30*s1,"#a9dfbf",stroke="#1e8449")
# robot body & tank placeholders
x,y=P1(-60,zL-wcz-30); R(x,y,120*s1,180*s1,"#7fb3d5",op=0.6,stroke="#2e86c1")
T(P1(70,0)[0],P1(0,zL-130)[1],"Robot treo ngược",12)
x,y=P1(-70,zU+rail_h+wcz+12+190); R(x,y,140*s1,190*s1,"#aed6f1",op=0.6,stroke="#2e86c1")
T(P1(80,0)[0],P1(0,zU+rail_h+110)[1],"Bình 3–4 L",12)
L(*P1(44,zL+rail_h+wcz),*P1(44,zU-wcz),"#111",2)
T(P1(55,0)[0],P1(0,(zL+zU)/2+40)[1],"thanh ty M8",11,fill="#444")
T(P1(55,0)[0],P1(0,(zL+zU)/2-10)[1],"cuộn dây ở CẢ 2 tầng ray: bình tự đẩy, không để robot kéo",11,fill="#1e8449")
# nozzle hint
T(P1(70,0)[0],P1(0,zL-250)[1],"→ đầu phun ~0,85 m",11,fill="#555")
dimv(P1(-300,0)[0],0,floor_top,"1200 (mép trên ray dưới)",P1,-1)
dimv(P1(-400,0)[0],0,zU+rail_h,f"{zU+rail_h} (mép trên ray trên)",P1,-1)
T(P1(hand_y-40,0)[0]-4,P1(0,1880)[1],"Cột/thanh sắt lỗ",11,"end",fill="#2c5282")
# ---------- Panel 2: chi tiết ray dưới ----------
s2=2.6; ox2,oz2=1050,560
P2=lambda y,z:(ox2+y*s2, oz2-z*s2)
T(640,130,"Chi tiết ray — giống nhau ở cả 2 tầng (tỉ lệ ~2,6:1, mm)",15,w="700")
# hanger (side A)
x,y=P2(-3-han_t,50); R(x,y,han_t*s2,40*s2,"#f0a020",stroke="#b07010")
x,y=P2(hand_y+end_t, 50); R(x,y,(arm_len)*s2,40*s2,"#f8c471",stroke="#b07010",op=0.6)
x,y=P2(hand_y,68); R(x,y,end_t*s2,76*s2,"#f0a020",stroke="#b07010")
x,y=P2(hand_y-40,95); R(x,y,40*s2-1,120*s2,"#3b6ea5",op=0.35,stroke="#2c5282")
T(P2(hand_y-20,0)[0],P2(0,-30)[1]+4,"sắt lỗ",12,"middle",fill="#2c5282")
for z in (20,40): L(*P2(-14,z),*P2(10,z),"#222",2)
T(P2(-62,0)[0],P2(0,58)[1],"Thanh treo (in 3D)",12,"middle",fill="#7a4a00")
T(P2(-62,0)[0],P2(0,58)[1]+16,"2 rãnh M8 chỉnh cao ±10",11,"middle",fill="#7a4a00")
# rail
x,y=P2(-3,60); R(x,y,6*s2,60*s2,"#bbbbbb",stroke="#555")
# coil seg base & coil
x,y=P2(3,57); R(x,y,3*s2,52*s2,"#7dcea0",stroke="#1e8449")
x,y=P2(6,45); R(x,y,12*s2,30*s2,"#c47a3a",stroke="#7e4a1a")
T(P2(12,0)[0],P2(0,30)[1]+4,"cuộn",11,"middle",fill="white")
x,y=P2(6,50.5); R(x,y,(coil_face-6-0.5)*s2,6*s2,"#a9dfbf",stroke="#1e8449")
T(P2(12,0)[0],P2(0,55)[1],"Hall",11,"middle",fill="#1e8449")
# magnets + back iron + bogie
x,y=P2(mag_face,45); R(x,y,5*s2,30*s2,"#e74c3c",stroke="#922b21")
x,y=P2(mag_face+5,45.2); R(x,y,1.6*s2,30.4*s2,"#555",stroke="#222")
x,y=P2(mag_face,60+wcz+8); R(x,y,(plate_y1-mag_face)*s2,(rail_h+2*wcz+16)*s2,"#f4d03f",stroke="#b7950b",op=0.55)
x,y=P2(plate_y1,44); R(x,y,22*s2,28*s2,"#f4d03f",stroke="#b7950b",op=0.55)
T(P2(plate_y1+11,0)[0],P2(0,30)[1]+4,"chốt xoay",11,"middle")
# wheels + axles
for zc in (60+wcz,-wcz):
    x,y=P2(-3.5,zc+11); R(x,y,7*s2,22*s2,"#555",stroke="#222",rx=4)
    L(*P2(-6,zc),*P2(plate_y1,zc),"#111",3)
T(P2(plate_y1+6,0)[0],P2(0,60+wcz)[1]-8,"bánh rãnh U Ø22 (chịu tải)",11)
T(P2(plate_y1+6,0)[0],P2(0,-wcz)[1]+16,"bánh chống nhấc",11)
# robot body below
x,y=P2(-60,-wcz-30); R(x,y,120*s2,14*s2,"#7fb3d5",op=0.6,stroke="#2e86c1")
T(P2(0,0)[0],P2(0,-wcz-30)[1]+32,"thân robot (treo từ chốt xoay)",12,"middle",fill="#1f618d")
# dims
def dimh(y1,y2,z,label):
    X1,Yv=P2(y1,z); X2,_=P2(y2,z)
    L(X1,Yv,X2,Yv,"#c0392b",1.2); L(X1,Yv-5,X1,Yv+5,"#c0392b"); L(X2,Yv-5,X2,Yv+5,"#c0392b")
    T((X1+X2)/2,Yv-7,label,12,"middle",fill="#c0392b")
dimh(-3,3,82,"6"); dimh(coil_face,mag_face,82,"khe 3"); dimh(3,coil_face,92,"15")
dimh(hand_y,-3,112,f"{abs(hand_y)-3} (mặt ray → mặt sắt lỗ)")
dimv(P2(-3,0)[0]-60,0,60,"60",P2,-1)
out.append('</svg>')
open('/home/claude/firebot-3d/png/section_drawing.svg','w').write("\n".join(out))
