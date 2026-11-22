#!/usr/bin/env python3
"""
Genera todos los iconos de ZEUS a partir de una sola definición geométrica.

Salida:
  assets/icons/*            -> favicon, PNG para PWA (any + maskable), logo SVG
  android/res/*             -> Adaptive Icon (vector), capa monocromática (iconos
                               temáticos de One UI / Android 13+) y PNG legacy
  android/play-store-icon-512.png

Requisitos:  pip install cairosvg pillow
Uso:         python3 tools/make_icons.py
"""
import math, os, io
import cairosvg
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def out(*p):
    path = os.path.join(ROOT, *p); os.makedirs(os.path.dirname(path), exist_ok=True); return path

# ───────────── Geometría (lienzo adaptive de 108×108, centro 54,54) ─────────────
C = 54
R = 28            # radio del medidor
SW = 6.5          # grosor del medidor
A0, A_END = 135, 405          # arco de 270° con la abertura abajo
A_FILL = A0 + 0.80 * 270      # carga mostrada: 80 %
BOLT_SCALE = 0.82
BOLT_RAW = [(43,36),(68,36),(55.5,49.5),(66,49.5),(41,72),(50.5,57.5),(40.5,57.5),(53,44),(43,44)]
BOLT = [(C + (x-C)*BOLT_SCALE, C + (y-C)*BOLT_SCALE) for x, y in BOLT_RAW]

# Paleta
NAVY_1, NAVY_2 = "#0D2318", "#050F0A"   # verde bosque profundo
GREEN, LIME = "#2BEA8A", "#B2F04A"     # esmeralda -> lima
ICE = "#EAFFD0"

def pt(a, r=R):
    return C + r*math.cos(math.radians(a)), C + r*math.sin(math.radians(a))
def arc(a0, a1, r=R):
    x0, y0 = pt(a0, r); x1, y1 = pt(a1, r)
    return f"M{x0:.2f} {y0:.2f}A{r} {r} 0 {1 if a1-a0>180 else 0} 1 {x1:.2f} {y1:.2f}"
def poly(points):
    return "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in points) + "Z"

TRACK, FILL, BOLT_D = arc(A0, A_END), arc(A0, A_FILL), poly(BOLT)

DEFS = f'''<defs>
<linearGradient id="bg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="108" y2="108"><stop offset="0" stop-color="{NAVY_1}"/><stop offset="1" stop-color="{NAVY_2}"/></linearGradient>
<linearGradient id="ring" gradientUnits="userSpaceOnUse" x1="24" y1="84" x2="84" y2="24"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{LIME}"/></linearGradient>
<linearGradient id="bolt" gradientUnits="userSpaceOnUse" x1="54" y1="36" x2="54" y2="72"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="{ICE}"/></linearGradient>
<radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="54" cy="54" r="40"><stop offset="0" stop-color="#2BEA8A" stop-opacity=".28"/><stop offset="1" stop-color="#2BEA8A" stop-opacity="0"/></radialGradient>
</defs>'''
BG = '<rect width="108" height="108" fill="url(#bg)"/><circle cx="54" cy="54" r="40" fill="url(#glow)"/>'
MARK = (f'<path d="{TRACK}" fill="none" stroke="{GREEN}" stroke-opacity=".22" stroke-width="{SW}" stroke-linecap="round"/>'
        f'<path d="{FILL}" fill="none" stroke="url(#ring)" stroke-width="{SW}" stroke-linecap="round"/>'
        f'<path d="{BOLT_D}" fill="url(#bolt)" stroke="url(#bolt)" stroke-width="1.2" stroke-linejoin="round"/>')

def svg(body, view=(0,0,108,108), size=512, clip=None):
    x, y, w, h = view
    clip_def = f'<clipPath id="c">{clip}</clipPath>' if clip else ''
    g_open = '<g clip-path="url(#c)">' if clip else '<g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{size}" height="{size}">'
            f'{DEFS}{clip_def}{g_open}{body}</g></svg>')

def png(svg_str, path, size):
    cairosvg.svg2png(bytestring=svg_str.encode(), write_to=path, output_width=size, output_height=size)

# ───────────── Web / PWA ─────────────
# "any": recorte 84×84 (el medidor ocupa ~74 %) con esquinas redondeadas
CROP_ANY = (12, 12, 84, 84)
rounded = '<rect x="12" y="12" width="84" height="84" rx="19"/>'
any_svg = svg(BG + MARK, CROP_ANY, clip=rounded)
open(out('assets','icons','logo.svg'),'w').write(any_svg)
open(out('assets','icons','favicon.svg'),'w').write(any_svg)
for s in (192, 512):
    png(any_svg, out('assets','icons',f'icon-{s}.png'), s)
png(any_svg, out('assets','icons','favicon-32.png'), 32)

# "maskable": fondo a sangre; el medidor queda dentro del 80 % central (zona segura)
CROP_MASK = (6, 6, 96, 96)
mask_svg = svg(BG + MARK, CROP_MASK)
for s in (192, 512):
    png(mask_svg, out('assets','icons',f'icon-maskable-{s}.png'), s)

# ───────────── Android ─────────────
# Icono de Play Store: cuadrado a sangre (Google aplica la máscara)
png(svg(BG + MARK, CROP_ANY), out('android','play-store-icon-512.png'), 512)

# PNG legacy (API < 26) en todas las densidades
DENS = {'mdpi':48, 'hdpi':72, 'xhdpi':96, 'xxhdpi':144, 'xxxhdpi':192}
sq = '<rect x="12" y="12" width="84" height="84" rx="17"/>'
ci = '<circle cx="54" cy="54" r="42"/>'
for d, s in DENS.items():
    png(svg(BG + MARK, CROP_ANY, clip=sq), out('android','res',f'mipmap-{d}','ic_launcher.png'), s)
    png(svg(BG + MARK, CROP_ANY, clip=ci), out('android','res',f'mipmap-{d}','ic_launcher_round.png'), s)

# Vector drawables ---------------------------------------------------------
NS = 'xmlns:android="http://schemas.android.com/apk/res/android" xmlns:aapt="http://schemas.android.com/aapt"'
def lin(attr, x1, y1, x2, y2, stops):
    items = "\n".join(f'          <item android:offset="{o}" android:color="{c}"/>' for o, c in stops)
    return (f'    <aapt:attr name="android:{attr}">\n'
            f'      <gradient android:type="linear" android:startX="{x1}" android:startY="{y1}" android:endX="{x2}" android:endY="{y2}">\n{items}\n      </gradient>\n'
            f'    </aapt:attr>')

background = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- Capa de fondo del icono adaptativo de ZEUS (108dp). -->
<vector {NS}
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
  <path android:pathData="M0,0h108v108h-108z">
{lin('fillColor',0,0,108,108,[(0,NAVY_1),(1,NAVY_2)])}
  </path>
  <path android:pathData="M54,54m-40,0a40,40 0 1,1 80,0a40,40 0 1,1 -80,0">
    <aapt:attr name="android:fillColor">
      <gradient android:type="radial" android:centerX="54" android:centerY="54" android:gradientRadius="40">
        <item android:offset="0" android:color="#472BEA8A"/>
        <item android:offset="1" android:color="#002BEA8A"/>
      </gradient>
    </aapt:attr>
  </path>
</vector>
'''

foreground = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- Capa frontal: medidor de carga + rayo en Z. Todo queda dentro de la zona
     segura de 66dp (círculo de radio 33 centrado en 54,54). -->
<vector {NS}
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
  <!-- Pista del medidor -->
  <path android:pathData="{TRACK}"
      android:strokeColor="#382BEA8A" android:strokeWidth="{SW}" android:strokeLineCap="round"/>
  <!-- Carga (80 %) -->
  <path android:pathData="{FILL}" android:strokeWidth="{SW}" android:strokeLineCap="round">
{lin('strokeColor',24,84,84,24,[(0,GREEN),(1,LIME)])}
  </path>
  <!-- Rayo en Z -->
  <path android:pathData="{BOLT_D}" android:strokeWidth="1.2" android:strokeLineJoin="round">
{lin('fillColor',54,36,54,72,[(0,'#FFFFFF'),(1,ICE)])}
{lin('strokeColor',54,36,54,72,[(0,'#FFFFFF'),(1,ICE)])}
  </path>
</vector>
'''

mono = f'''<?xml version="1.0" encoding="utf-8"?>
<!-- Capa monocromática para iconos temáticos (Android 13+ / One UI 5+).
     El sistema la tiñe con los colores del tema; solo cuenta el canal alfa. -->
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
  <path android:pathData="{TRACK}"
      android:strokeColor="#59000000" android:strokeWidth="{SW}" android:strokeLineCap="round"/>
  <path android:pathData="{FILL}"
      android:strokeColor="#FF000000" android:strokeWidth="{SW}" android:strokeLineCap="round"/>
  <path android:pathData="{BOLT_D}" android:fillColor="#FF000000"
      android:strokeColor="#FF000000" android:strokeWidth="1.2" android:strokeLineJoin="round"/>
</vector>
'''

adaptive = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
    <monochrome android:drawable="@drawable/ic_launcher_monochrome" />
</adaptive-icon>
'''
for name, txt in {'drawable/ic_launcher_background.xml': background,
                  'drawable/ic_launcher_foreground.xml': foreground,
                  'drawable/ic_launcher_monochrome.xml': mono,
                  'mipmap-anydpi-v26/ic_launcher.xml': adaptive,
                  'mipmap-anydpi-v26/ic_launcher_round.xml': adaptive}.items():
    open(out('android','res',name),'w').write(txt)

# Vista previa (ayuda a revisar y para el README): squircle, círculo y monocromo
def mono_svg(color="#D9F7B8", bg="#16241B"):
    body = (f'<rect width="108" height="108" fill="{bg}"/>'
            f'<path d="{TRACK}" fill="none" stroke="{color}" stroke-opacity=".35" stroke-width="{SW}" stroke-linecap="round"/>'
            f'<path d="{FILL}" fill="none" stroke="{color}" stroke-width="{SW}" stroke-linecap="round"/>'
            f'<path d="{BOLT_D}" fill="{color}" stroke="{color}" stroke-width="1.2" stroke-linejoin="round"/>')
    return svg(body, (0,0,108,108), clip='<circle cx="54" cy="54" r="40"/>')
tiles = []
for sv in (svg(BG+MARK,(0,0,108,108),clip='<rect x="18" y="18" width="72" height="72" rx="24"/>'),
           svg(BG+MARK,(0,0,108,108),clip='<circle cx="54" cy="54" r="36"/>'),
           mono_svg()):
    tiles.append(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sv.encode(), output_width=360, output_height=360))).convert('RGBA'))
sheet = Image.new('RGBA', (360*3, 360), (24, 30, 44, 255))
for i, t in enumerate(tiles): sheet.alpha_composite(t, (360*i, 0))
sheet.save(out('docs','icon-preview.png'))
print("OK")
