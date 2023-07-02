from PIL import Image

im1 = Image.open("static/1.png")
im2 = Image.open("static/1.jpeg")

for _ in range(100):
    back_im = im2.copy()
    back_im.paste(im1)
    back_im.save("res.jpg", quality=95)
