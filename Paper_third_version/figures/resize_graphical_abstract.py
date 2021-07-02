from PIL import Image
image = Image.open('Graphical_Abstract.tif')
image_resize=image.resize((255,100))
image_resize.save("Graphical_Abstract.png")
