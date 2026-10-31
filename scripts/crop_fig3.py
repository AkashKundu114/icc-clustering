from PIL import Image

im = Image.open("springer_manuscript/figures/fig03_real_data_stability.png")
print("Size of fig03:", im.size)
# The image is a multi-panel figure. Let's see its aspect ratio.
w, h = im.size
# Panel (a) is on the left
panel_a = im.crop((0, 0, int(w * 0.55), h))
panel_a.save("scripts/panel_a_preview.png")
print("Saved panel_a_preview.png")
