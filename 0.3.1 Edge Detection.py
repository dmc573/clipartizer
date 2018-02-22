import Tkinter as TK
import PIL
from PIL import ImageTk
import math
import os.path
import cv2

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
new_image = original_image

def load_image(directory):
    image = PIL.Image.open(directory)
    return image

def save_image(image, directory):
    new_image_filename = os.path.join(__dir__, file_strvar.get())
    new_image.save(new_image_filename)
    print 'saving: ' + new_image_filename
    
def cartoon(image, hues, values):
    pass
    
def outline(image, tolerance, thickness, color):
    im = cv2.imread('Hopetoun_falls.jpg')
    edges = cv2.Canny(im,25,255,L2gradient=False)
    TK.imshow(edges,cmap='gray')
    TK.show()

#############
# Create GUI
#############

canvas = TK.Canvas(root, width=600, height=600, background='#FFFFFF')
canvas.grid(row=0, column=0, columnspan=2)

original_image = load_image(filename)
w = 1280
oldw, oldh = original_image.size
h = w*oldh/oldw
if h > 1080:
    h = 1080
    w = h*oldw/oldh
small_image = original_image.resize((w,h))

#Button Testing
outline = TK.IntVar()
cartoon = TK.IntVar()

edge = TK.Checkbutton(root, text="Outline", variable=outline)
edge.grid(row=1, column=1)
cartoon = TK.Checkbutton(root, text="Cartoon", variable=cartoon)
cartoon.grid(row=1, column=0)


# File save text and buttons
file_text = TK.Label(root, text='New File:')
file_text.grid(row=3, column=0)
file_entry = TK.Entry(root, textvariable=file_strvar)
file_entry.grid(row=3,column=1)
save_button = TK.Button(root, text='save', command=save_image)
save_button.grid(row=3, column=2)

# Convert the small image to Tk format and add to center of canvas
small_image = new_image.resize((w,h))
print small_image
tkimg = ImageTk.PhotoImage(small_image)
canvas.img = tkimg
try:
    canvas_imageID = canvas.create_image(w/2, h/2, image=tkimg)
except TclError:
    pass

root.mainloop()