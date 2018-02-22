import Tkinter as TK
import PIL
from PIL import ImageTk
import math
import os.path

root = TK.Tk()

filter_intvar = TK.IntVar()  # used with radio button
filter_intvar.set(0)
file_strvar = TK.StringVar()  # used with filename entry
file_strvar.set('landscape_new.jpg')  # set a default new name

###########
#Load Image
###########

__dir__ = os.path.dirname(os.path.abspath(__file__))  
filename = os.path.join(__dir__, 'Hopetoun_falls.jpg')
print 'loading: ' + filename

original_image = PIL.Image.open(filename)
new_image = original_image.resize((300,300))


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
    if mn == mx:
        hue = -1
    elif r==mx:
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

def hue_to_rgb(hue, value=1):
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
    factor = 255./mx*value
    r *= factor
    g *= factor
    b *= factor
    return (int(r),int(g),int(b))
    
def cartoon(hues, values):
    global new_image
    huepoints = frange(0, 360, 360/hues)
    valuepoints = frange(0, 1, 1/values)
    for h in xrange(hues):
        for v in xrange(values):
            recolor_group(huepoints[h], huepoints[h+1], valuepoints[v], valuepoints[v+1])

def recolor_group(lower_hue, upper_hue, lower_value, higher_value):
    global new_image
    w, h = new_image.size
    hues = 0
    hue_total = 0
    values = 0
    value_total = 0
    for y in xrange(h):
        for x in xrange(w):
            r,g,b = new_image.getpixel((x,y))
            hue = rgb_to_hue(r,g,b)
            value = (r+g+b)/3./255.
            if hue >= lower_hue and hue < upper_hue:
                hues += 1
                hue_total += hue
            if value >= lower_value and value < higher_value:
                values += 1
                value_total += value
    if hues > 0:
        hue_average = hue_total/hues
    if values > 0:
        value_average = value_total/values
    for y in xrange(h):
        for x in xrange(w):
            r,g,b = new_image.getpixel((x,y))
            hue = rgb_to_hue(r,g,b)
            #value = (r+g+b)/3./256.
            value = .5
            change_pixel = False
            if hue >= lower_hue and hue < upper_hue:
                hue = hue_average
                change_pixel = True
            if value >= lower_value and value < higher_value:
                value = value_average
                change_pixel = True
            if change_pixel == True:
                rgb = hue_to_rgb(hue, value)
                new_image.putpixel((x,y),rgb)
    
def outline(image, tolerance, thickness, color):
    pass

#############
# Create GUI
#############

canvas = TK.Canvas(root, width=600, height=600, background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=2)

#Button Testing
outline_check = TK.IntVar()
cartoon_check = TK.IntVar()

edge_button = TK.Checkbutton(root, text="Outline", variable=outline_check)
edge_button.grid(row=1, column=1)
cartoon_button = TK.Checkbutton(root, text="Cartoon", variable=cartoon_check)
cartoon_button.grid(row=1, column=0)


# File save text and buttons
file_text = TK.Label(root, text='New File:')
file_text.grid(row=3, column=0)
file_entry = TK.Entry(root, textvariable=file_strvar)
file_entry.grid(row=3,column=1)
save_button = TK.Button(root, text='save', command=save_image)
save_button.grid(row=3, column=2)

# Convert the small image to Tk format and add to center of canvas
#Cartoonify
cartoon(8,1)

w = 1280
oldw, oldh = new_image.size
h = w*oldh/oldw
if h > 1080:
    h = 1080
    w = h*oldw/oldh
small_image = new_image.resize((w,h))
tkimg = ImageTk.PhotoImage(small_image)
canvas.img = tkimg
try:
    canvas_imageID = canvas.create_image(w/2, h/2, image=tkimg)
except:
    pass


root.mainloop()