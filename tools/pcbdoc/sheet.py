import base64, sys, subprocess, html
from PIL import Image
W, H = 1190.55, 841.89  # A3 landscape pt
def img(path, x, y, w):
    im = Image.open(path); h = w * im.size[1] / im.size[0]
    b = base64.b64encode(open(path, 'rb').read()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{b}"/>', h
def page(out, title, sub, top, bot, tables, notes):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="DejaVu Sans">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="30" y="42" font-size="22" font-weight="bold" fill="#222">{html.escape(title)}</text>',
         f'<text x="30" y="62" font-size="11" fill="#555">{html.escape(sub)}</text>']
    a, h1 = img(top, 30, 80, 400); s.append(a)
    s.append(f'<text x="30" y="{80+h1+14}" font-size="10" fill="#555">Mặt trên (F.Cu + lụa)</text>')
    b, h2 = img(bot, 445, 80, 400); s.append(b)
    s.append(f'<text x="445" y="{80+h2+14}" font-size="10" fill="#555">Mặt dưới, nhìn từ dưới lên (B.Cu)</text>')
    y0 = 80 + max(h1, h2) + 36
    x = 862; y = 80
    for tt, rows in tables:
        s.append(f'<text x="{x}" y="{y}" font-size="11.5" font-weight="bold" fill="#b3261e">{html.escape(tt)}</text>'); y += 6
        for r in rows:
            y += 13.2
            s.append(f'<text x="{x}" y="{y}" font-size="8.5" fill="#222">{html.escape(r[0])}</text>')
            s.append(f'<text x="{x+88}" y="{y}" font-size="8.5" fill="#444">{html.escape(r[1])}</text>')
        y += 20
    yy = max(y0, 80) 
    s.append(f'<text x="30" y="{yy}" font-size="11.5" font-weight="bold" fill="#b3261e">Ghi chú lắp ráp</text>')
    for n in notes:
        yy += 15; s.append(f'<text x="30" y="{yy}" font-size="9.5" fill="#222">• {html.escape(n)}</text>')
    s.append('</svg>')
    open(out + '.svg', 'w').write('\n'.join(s))
    subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', out + '.pdf', out + '.svg'], check=True)
