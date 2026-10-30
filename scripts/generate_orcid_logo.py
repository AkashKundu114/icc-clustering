"""
Generate official high-resolution and vector ORCID iD logo files:
- paper/Orcidlogo.svg
- paper/Orcidlogo.png (high-res RGBA)
- paper/Orcidlogo.pdf (vector PDF)
- paper/Orcidlogo.eps (standard Encapsulated PostScript vector)
and copy identical files to springer_manuscript/
"""

import fitz  # PyMuPDF
from pathlib import Path
from PIL import Image

# Official SVG specification with green circle (#A6CE39) and white 'iD' letters
# Using two paths: first the circle in #A6CE39, then the letters 'iD' in #FFFFFF
# so that the letters are bright solid white even on non-white backgrounds!
svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <circle cx="128" cy="128" r="128" fill="#A6CE39"/>
  <path fill="#FFFFFF" d="M78.6 46.7c5.6 0 10.1 4.6 10.1 10.1s-4.5 10.1-10.1 10.1a10.1 10.1 0 0 1-10.1-10.1c0-5.6 4.5-10.1 10.1-10.1m-7.7 32.4h15.4v107.1H70.9zm38 0h41.6c39.6 0 57 28.3 57 53.6c0 27.5-21.5 53.6-56.8 53.6h-41.8zm15.4 13.9v79.4h24.5c34.9 0 42.9-26.5 42.9-39.7c0-21.5-13.7-39.7-43.7-39.7z"/>
</svg>"""

def main():
    # 1. Save SVG
    svg_path = Path("paper/Orcidlogo.svg")
    svg_path.write_text(svg_content, encoding="utf-8")
    print(f"Saved {svg_path}")

    # 2. Render to PDF and PNG via PyMuPDF
    doc = fitz.open(stream=svg_content.encode("utf-8"), filetype="svg")
    page = doc[0]
    
    # High-resolution PNG (512x512)
    pix = page.get_pixmap(dpi=288, alpha=True)
    png_path = Path("paper/Orcidlogo.png")
    pix.save(str(png_path))
    print(f"Saved {png_path} ({pix.width}x{pix.height})")

    # Vector PDF
    pdf_bytes = doc.convert_to_pdf()
    pdf_path = Path("paper/Orcidlogo.pdf")
    pdf_path.write_bytes(pdf_bytes)
    print(f"Saved {pdf_path}")

    # 3. Generate clean vector EPS
    # In PostScript, a square 256x256 bounding box with exact shapes:
    eps_content = """%!PS-Adobe-3.0 EPSF-3.0
%%Creator: ORCID iD Logo Generator
%%Title: Orcidlogo.eps
%%BoundingBox: 0 0 256 256
%%HiResBoundingBox: 0.0 0.0 256.0 256.0
%%EndComments
%%BeginProlog
save
/circtopath {
  newpath
  128 128 128 0 360 arc
  closepath
} def
%%EndProlog

%%Page: 1 1
gsave
% Green circle: #A6CE39 -> (166/255, 206/255, 57/255) = (0.65098, 0.80784, 0.22353)
0.65098 0.80784 0.22353 setrgbcolor
circtopath
fill

% White iD: scale and translate coordinate system to match SVG viewBox
% SVG origin is top-left, PostScript origin is bottom-left
1 -1 scale
0 -256 translate

1 1 1 setrgbcolor
newpath
% Dot of i
78.6 46.7 10.1 0 360 arc
fill

% Stem of i
newpath
70.9 79.1 moveto
86.3 79.1 lineto
86.3 186.2 lineto
70.9 186.2 lineto
closepath
fill

% Shape of D (outer and inner cutout using nonzero / eofill)
newpath
108.9 79.1 moveto
150.5 79.1 lineto
170.3 79.1 190.1 93.2 199.6 105.9 curveto
207.5 116.5 207.5 132.7 199.6 143.3 curveto
190.1 156.0 170.3 186.3 150.5 186.3 curveto
108.7 186.3 lineto
closepath

124.3 93.0 moveto
124.3 172.4 lineto
148.8 172.4 lineto
166.2 172.4 180.1 159.2 186.8 145.9 curveto
191.7 136.2 191.7 125.8 186.8 116.1 curveto
180.1 102.8 166.2 93.0 148.8 93.0 curveto
closepath
eofill

grestore
restore
%%EOF
"""
    eps_path = Path("paper/Orcidlogo.eps")
    eps_path.write_text(eps_content, encoding="utf-8")
    print(f"Saved {eps_path}")

    # Copy all to springer_manuscript/
    springer_dir = Path("springer_manuscript")
    for f in ["Orcidlogo.svg", "Orcidlogo.png", "Orcidlogo.pdf", "Orcidlogo.eps"]:
        src = Path("paper") / f
        dst = springer_dir / f
        dst.write_bytes(src.read_bytes())
        print(f"Copied {src} -> {dst}")

if __name__ == "__main__":
    main()
