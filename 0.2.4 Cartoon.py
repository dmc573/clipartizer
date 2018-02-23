import Tkinter as TK
import PIL
from PIL import ImageTk
import math
import colorsys
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
img = original_image

def load_image(directory):
    image = PIL.Image.open(directory)
    return image

def save_image(image, directory):
    pass

def frange(start, stop, step):
    l = []
    i = float(start)
    while i <= stop:
        l.append(i)
        i += step
    return l

def cartoon(hues, tolerance):
    global img
    pix = img.load()
    width, height = img.size
    huepoints = frange(0, 1, 1/float(hues))
    for h in xrange(hues):
        recolor_group(huepoints[h], huepoints[h+1], tolerance)
    for y in xrange(height):
        for x in xrange(width):
            r,g,b = pix[x,y]
            r/=255.
            g/=255.
            b/=255.
            h,l,s = colorsys.rgb_to_hls(r,g,b)
            if l <= 0.5-tolerance/200.:
                pix[x,y] = [0,0,0]
            elif l >= 0.5+tolerance/200.:
                pix[x,y] = [255,255,255]
    return pix

def recolor_group(lower_hue, upper_hue, tolerance):
    global img
    global pix
    width, height = img.size
    pixels = 0
    hue_total = 0
    lower_luma = 0.5-tolerance/200.
    upper_luma = 0.5+tolerance/200.
    for y in xrange(height):
        for x in xrange(width):
            r,g,b = pix[x,y]
            r/=255.
            g/=255.
            b/=255.
            h,l,s = colorsys.rgb_to_hls(r,g,b)
            if h >= lower_hue and h < upper_hue and l > lower_luma and l < upper_luma:
                pixels += 1
                hue_total += h
    if pixels > 0:
        hue_average = hue_total/pixels
    for y in xrange(height):
        for x in xrange(width):
            r,g,b = img.getpixel((x,y))
            r/=255.
            g/=255.
            b/=255.
            h,l,s = colorsys.rgb_to_hls(r,g,b)
            if h >= lower_hue and h < upper_hue and l > lower_luma and l < upper_luma:
                if s-abs(l-.5)>.5-tolerance/100.:
                    s=1.
                else:
                    s=0.
                r,g,b = colorsys.hls_to_rgb(hue_average,0.5,s)
                r = int(r*255)
                g = int(g*255)
                b = int(b*255)
                pix[x,y] = [r,g,b]
    
def outline(image, tolerance, thickness, color):
    pass
    
def render():
    global img
    do_cartoon = cartoon_check.get()
    if do_cartoon:
        img = original_image.resize((400,400))
        img.putdata(cartoon(4, 50))
    else:
        img = original_image
    w = 1280
    oldw, oldh = img.size
    h = w*oldh/oldw
    if h > 720:
        h = 720
        w = h*oldw/oldh
    small_image = img.resize((w,h))
    tkimg = ImageTk.PhotoImage(small_image)
    canvas.img = tkimg


    

#############
# Create GUI
#############

canvas = TK.Canvas(root, width=1280, height=720, background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=3)

#Button Testing
outline_check = TK.IntVar()
cartoon_check = TK.IntVar()

edge_button = TK.Checkbutton(root, text="Outline", variable=outline_check)
edge_button.grid(row=1, column=1)
cartoon_button = TK.Checkbutton(root, text="Cartoon", variable=cartoon_check)
cartoon_button.grid(row=1, column=0)
render_button = TK.Button(root, text='Render', command=render)
render_button.grid(row=1, column=2)


# File save text and buttons
file_text = TK.Label(root, text='New File:')
file_text.grid(row=3, column=0)
file_entry = TK.Entry(root, textvariable=file_strvar)
file_entry.grid(row=3,column=1)
save_button = TK.Button(root, text='Save', command=save_image)
save_button.grid(row=3, column=2)

# Convert the small image to Tk format and add to center of canvas
#Cartoonify

root.mainloop()