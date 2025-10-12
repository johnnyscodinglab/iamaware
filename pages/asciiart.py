import streamlit as st
from PIL import Image, ImageSequence
import html
import requests 
import base64

st.title('Convert Image to ASCII Art')

# Get Image from the user
placeholder_url = "https://i.pinimg.com/originals/87/b7/ec/87b7ec06ec561a0693537c7c548ea049.gif"
url = st.text_input('Input Image URL:', value=placeholder_url)
r = requests.get(url)
input_imagename = "images/input.gif"
with open(input_imagename, "wb") as file:
    file.write(r.content)


c1,c2,c3 = st.columns(3)

# === Input / Output ===
gif_path = input_imagename             # your GIF
svg_path = "images/ascii_output.svg"

# === CUSTOMIZATION ===
width_chars = c1.slider('Density:', 50, 500, 200, 10)              # number of characters per line (more = sharper)
char_aspect = 0.5
font_size = c2.slider('Font Size:', 5, 50, 9, 1)                 # character size
colorcols = c3.columns(3)
fill_color = colorcols[0].color_picker("Font Color:", "#009DF9")       # default text color
bg_color = colorcols[1].color_picker("Background Color:", "#ffffff")           # default background color
invert_colors = colorcols[2].checkbox('Invert Colors:', False)        # set to True to swap text/background colors
white_threshold = c1.slider('White Threshold:', 0, 255, 245, 5)
frame_duration = c2.slider('Frame Duration:', 0.01, 0.3, 0.1)          # seconds per frame
levels = c3.text_input('Characters (Dark -> Light):', "m =.d")

# Character gradient (dark → light)

# === APPLY COLOR INVERSION ===
if invert_colors:
    fill_color, bg_color = bg_color, fill_color  # swap
    # optional tweak for inverted mode — more contrast
    white_threshold = 230  

def frame_to_ascii(frame, width_chars=100):
    gray = frame.convert("L")
    w, h = gray.size
    new_h = max(1, int((h / w) * width_chars * char_aspect))
    gray = gray.resize((width_chars, new_h))
    pixels = list(gray.getdata())
    rows = [pixels[i * width_chars:(i + 1) * width_chars] for i in range(new_h)]
    ascii_lines = []
    for row in rows:
        line = []
        for px in row:
            if px >= white_threshold:
                line.append(" ")
            else:
                idx = int((px / 255) * (len(levels) - 1))
                line.append(levels[idx])
        ascii_lines.append("".join(line))
    return ascii_lines


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


# === Load GIF frames ===
gif = Image.open(gif_path)
frames = [frame.copy().convert("RGBA") for frame in ImageSequence.Iterator(gif)]
ascii_frames = [frame_to_ascii(f, width_chars) for f in frames]

n_frames = len(ascii_frames)
total_duration = round(n_frames * frame_duration, 3)

# === SVG Layout ===
line_height = int(font_size * 1.05)
height_chars = len(ascii_frames[0])
svg_width = max(300, int(width_chars * (font_size * 0.6)))
svg_height = height_chars * line_height + 40

# === CSS keyframes ===
css_keyframes, frame_rules = [], []
for i in range(n_frames):
    pct_start = (i / n_frames) * 100
    pct_end = ((i + 1) / n_frames) * 100
    name = f"f{i}"
    css_keyframes.append(
        f"@keyframes {name} {{"
        f" 0%{{opacity:0;}} {pct_start:.4f}%{{opacity:0;}} "
        f" {pct_start:.4f}%{{opacity:1;}} {pct_end:.4f}%{{opacity:1;}} "
        f" {pct_end:.4f}%{{opacity:0;}} 100%{{opacity:0;}} }}"
    )
    frame_rules.append(
        f".frame{i}{{animation:{name} {total_duration}s steps(1,end) infinite;}}"
    )

style_block = (
    "<style type=\"text/css\">\n"
    + "\n".join(css_keyframes) + "\n"
    + "\n".join(frame_rules) + "\n"
    "</style>"
)

# === Build text frames ===
text_blocks = []
for i, ascii_frame in enumerate(ascii_frames):
    tspans = []
    for j, line in enumerate(ascii_frame):
        esc = html.escape(line)
        y = font_size + j * line_height
        tspans.append(f'<tspan x="0" y="{y}">{esc}</tspan>')
    text_blocks.append(
        f'<text class="frame{i}" xml:space="preserve" '
        f'font-family="monospace" font-size="{font_size}" '
        f'fill="{fill_color}" opacity="0">'
        + "\n".join(tspans)
        + "</text>"
    )

# === Final SVG ===
svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{svg_width}" height="{svg_height}"
     viewBox="0 0 {svg_width} {svg_height}"
     preserveAspectRatio="xMidYMid meet">
  <rect width="100%" height="100%" fill="{bg_color}"/>
  {style_block}
  <g transform="translate(20,20)">
    {"".join(text_blocks)}
  </g>
</svg>
'''

with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"✅ Saved {svg_path}")
print(f"   Font: {font_size}px, Text: {fill_color}, Background: {bg_color}, Inverted: {invert_colors}")
st.download_button(
    label="Download SVG",
    data=svg,
    file_name="ascii_art.svg",
    mime="image/svg+xml"
)

render_svg(svg)

# st.image(SVG(filename=svg_path))