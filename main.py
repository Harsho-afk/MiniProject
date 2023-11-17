import ttkbootstrap as ttk
from tkinter import *
from PIL import *

WIDTH = 1920-200
HEIGHT = 1080
filePath = ""
penSize = 3
penColor = "black"

window = ttk.Window(themename="cosmo")
window.title("Image Editor")
window.geometry("1920x1080")
icon = ttk.PhotoImage(file="Images/icon.png")
window.iconphoto(False, icon)

leftFrame = ttk.Frame(window,width = 200,height=1080)
leftFrame.pack(side="left",fill="y")

canvas = ttk.Canvas(window,width=WIDTH,height=HEIGHT)
canvas.pack()

filterLabel = ttk.Label(leftFrame,text="Select Filter:",background="#FFFFFF")
filterLabel.pack(padx = 0, pady=2)

IMGAE_FILTERS = ["None","Contour", "Black and White", "Blur", "Detail", "Emboss", "Edge Enhance", "Sharpen", "Smooth"]

filterComobobox = ttk.Combobox(leftFrame,values=IMGAE_FILTERS,width=15)
filterComobobox.pack(padx=10,pady=5)

addImage = ttk.PhotoImage(file = 'Images/add_image.png').subsample(2)
flipImage = ttk.PhotoImage(file = 'Images/flip_image.png').subsample(12, 12)
rotateImage = ttk.PhotoImage(file = 'Images/rotate_image.png').subsample(12, 12)
colorPickerImage = ttk.PhotoImage(file = 'Images/color_picker.png').subsample(12, 12)
eraserImage = ttk.PhotoImage(file = 'Images/eraser_icon.png').subsample(12, 12)
saveImage = ttk.PhotoImage(file = 'Images/save_icon.png').subsample(12, 12)

addImageButton = ttk.Button(leftFrame, image=addImage, bootstyle="light")
addImageButton.pack()

flipButton = ttk.Button(leftFrame, image=flipImage, bootstyle="light")
flipButton.pack()

rotateButton = ttk.Button(leftFrame, image=rotateImage, bootstyle="light")
rotateButton.pack()

colorButton = ttk.Button(leftFrame, image=colorPickerImage, bootstyle="light")
colorButton.pack()

eraserButton = ttk.Button(leftFrame, image=eraserImage, bootstyle="light")
eraserButton.pack()

saveButton = ttk.Button(leftFrame, image=saveImage, bootstyle="light")
saveButton.pack()

window.mainloop()