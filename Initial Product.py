import Tkinter as TK
import PIL
import math
import os.path

root = TK.Tk()

def load_image(directory):
    image = PIL.Image.open(directory)
    return image

def save_image(image, directory):
    pass
    
def cartoon(image, tolerance):
    pass
    
def outline(image, tolerance, thickness, color):
    pass

#############
# Create GUI
#############

canvas = TK.Canvas(root, width=600, height=600, background='#FFFFFF')
canvas.grid(row=0, rowspan=2, column=1)

small_image = original_image.resize((w,h))

# Convert the small image to Tk format and add to center of canvas
tkimg = PIL.ImageTk.PhotoImage(small_image)
canvas.img = tkimg
canvas_imageID = canvas.create_image(w/2, h/2, image=tkimg)

root.mainloop()