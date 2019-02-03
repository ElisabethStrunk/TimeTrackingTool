from PIL import Image
filename = r'app_logo.png'
img = Image.open(filename)
img.save('app_logo.ico')
