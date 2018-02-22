import Tkinter as TK
import PIL
from PIL import ImageTk
import math
import os.path

root = TK.Tk()

###########
#Load Image
###########

__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'Hopetoun_falls.jpg')
print 'loading: ' + filename

original_image = PIL.Image.open(filename)
new_image = original_image


def load_image(directory):
    image = PIL.Image.open(directory)
    return image

def save_image(image, directory):
    pass

def frange(start, stop, step):
    l = []
    i = start
    while i <= stop:
        l.append(i)
        i += step
    return l

def rgb_to_hue(r,g,b):
    r /= 255.
    g /= 255.
    b /= 255.
    mx = max(r,g,b)
    mn = min(r,g,b)
    if r==mx:
        hue = (g-b)/(mx-mn)
    elif g==mx:
        hue = 2.0 + (b-r)/(mx-mn)
    elif b==mx:
        hue = 4.0 + (r-g)/(mx-mn)
    else:
        raise IOError('NoMax')
    hue *= 60.
    while hue < 0:
        hue += 60.
    return hue

def hue_to_rgb(hue):
    hue /= 120.
    if hue < 1:
        r = (1-hue)*255
        g = hue*255
        b = 0
    elif hue < 2:
        hue -= 1
        r = 0
        g = (1-hue)*255
        b = hue*255
    elif hue < 3:
        hue -= 2
        r = hue*255
        g = 0
        b = (1-hue)*255
    else:
        raise IOError('NotValidHue')
    mx = max(r,g,b)
    factor = 255/mx
    r *= factor
    g *= factor
    b *= factor
    return (r,g,b)
    
def cartoon(image, hues, values):
    huepoints = frange(0, 360, 360/hues)
    valuepoints = frange(0, 100, 100/values)
    for h in xrange(hues):
        for v in xrange(values):
            recolorgroup(huepoints[h], huepoints[h+1], valuepoints[v], valuepoints[v+1])
    pass

def recolorgroup(lower_hue, upper_hue, lower_value, higher_value):
    pass
    
def outline(image, tolerance, thickness, color):
    pass

#############
# Create GUI
#############

canvas = TK.Canvas(root, width=600, height=600, background='#FFFFFF')
canvas.grid(row=0, rowspan=2, column=1)

original_image = load_image(filename)
w = 1280
oldw, oldh = original_image.size
h = w*oldh/oldw
if h > 1080:
    h = 1080
    w = h*oldw/oldh
small_image = original_image.resize((w,h))

# Convert the small image to Tk format and add to center of canvas
small_image = new_image.resize((w,h))
print small_image
tkimg = ImageTk.PhotoImage(small_image)
canvas.img = tkimg
canvas_imageID = canvas.create_image(w/2, h/2, image=tkimg)

root.mainloop()