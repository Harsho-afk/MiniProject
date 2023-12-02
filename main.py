import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab

# defining global variables
WIDTH = 1720
HEIGHT = 1080
file_path = ""
pen_size = 3
pen_color = "black"

image = None
photo_image = None

# function to open the image file
def open_image():
    global file_path, image, photo_image
    file_path = filedialog.askopenfilename(title="Open Image File",filetypes=[("Image Files","*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    if file_path:
        global image, photo_image
        image = Image.open(file_path)
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(WIDTH/2,HEIGHT/2, anchor="center", image=photo_image)
        

def flip_image():
    try:
        global image, photo_image
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(WIDTH/2,HEIGHT/2, anchor="center", image=photo_image)
    except:
        showerror(title='Flip Image Error', message='Please select an image to flip!')


# function for rotating the image
def rotate_image():
    try:
        global image, photo_image
        image = image.transpose(Image.ROTATE_90)
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(WIDTH/2,HEIGHT/2, anchor="center", image=photo_image)
    except:
        showerror(title='Rotate Image Error', message='Please select an image to rotate!')

# function for applying filters to the opened image file
filtersApplied = []
def apply_filter(filter):
    global image, photo_image
    try:
        if filter == "Black and White" and filtersApplied.count("Black and White") == 0:
            image = ImageOps.grayscale(image)
            filtersApplied.append("Black and White")
        elif filter == "Blur"and filtersApplied.count("Blur") == 0:
            image = image.filter(ImageFilter.BLUR)
            filtersApplied.append("Blur")
        elif filter == "Contour"and filtersApplied.count("Contour") == 0:
            image = image.filter(ImageFilter.CONTOUR)
            filtersApplied.append("Contour")
        elif filter == "Detail"and filtersApplied.count("Detail") == 0:
            image = image.filter(ImageFilter.DETAIL)
            filtersApplied.append("Detail")
        elif filter == "Emboss"and filtersApplied.count("Emboss") == 0:
            image = image.filter(ImageFilter.EMBOSS)
            filtersApplied.append("Emboss")
        elif filter == "Edge Enhance"and filtersApplied.count("Edge Enhance") == 0:
            image = image.filter(ImageFilter.EDGE_ENHANCE)
            filtersApplied.append("Edge Enhance")
        elif filter == "Sharpen"and filtersApplied.count("Sharpen") == 0:
            image = image.filter(ImageFilter.SHARPEN)
            filtersApplied.append("Sharpen")
        elif filter == "Smooth"and filtersApplied.count("Smooth") == 0:
            image = image.filter(ImageFilter.SMOOTH)
            filtersApplied.append("Smooth")
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(WIDTH/2,HEIGHT/2, anchor="center", image=photo_image)
        
    except:
        showerror(title='Error', message='Please select an image first!')

# function for drawing lines on the opened image
def draw(event):
    global file_path
    if file_path:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")


# function for changing the pen color
def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

# Erase Function
def erase_lines():
    global file_path
    if file_path:
        canvas.delete("oval")

# Save Image
def save_image():
    global file_path

    if file_path:
        image = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(), canvas.winfo_rooty() + canvas.winfo_height()))
        
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        
        if file_path:
            if askyesno(title='Save Image', message='Do you want to save this image?'):
                image.save(file_path)

# WINDOW
root = ttk.Window(themename="cosmo")
root.title("Image Editor")
root.geometry("1920x1080+0+0")
icon = ttk.PhotoImage(file='Images/icon.png')
root.iconphoto(False, icon)

# WIDGET
left_frame = ttk.Frame(root, width=200, height=720)
left_frame.pack(side="left", fill="y")

# CANVAS
canvas = ttk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()
canvas.bind("<B1-Motion>", draw)

# button for filters
def on_combobox_select(event):
    selected_value = filter_combobox.get()
    apply_filter(selected_value)

filter_label = ttk.Label(left_frame, text="Select Filter:", background="white")
filter_label.pack(padx=0, pady=2)
image_filters = ["Contour", "Black and White", "Blur", "Detail", "Emboss", "Edge Enhance", "Sharpen", "Smooth"]
filter_combobox = ttk.Combobox(left_frame, values=image_filters, width=15)
filter_combobox.set("Select an option")
filter_combobox.bind("<<ComboboxSelected>>", on_combobox_select)
filter_combobox.pack(padx=10, pady=5)  
image_icon = ttk.PhotoImage(file = 'Images/add.png').subsample(12, 12)
flip_icon = ttk.PhotoImage(file = 'Images/flip.png').subsample(12, 12)
rotate_icon = ttk.PhotoImage(file = 'Images/rotate.png').subsample(12, 12)
color_icon = ttk.PhotoImage(file = 'Images/color.png').subsample(12, 12)
erase_icon = ttk.PhotoImage(file = 'Images/erase.png').subsample(12, 12)
save_icon = ttk.PhotoImage(file = 'Images/saved.png').subsample(12, 12)

# button for adding/opening the image file
image_button = ttk.Button(left_frame, image=image_icon, bootstyle="light", command=open_image)
image_button.pack(pady=5)

# button for flipping the image file
flip_button = ttk.Button(left_frame, image=flip_icon, bootstyle="light", command=flip_image)
flip_button.pack(pady=5)

# button for rotating the image file
rotate_button = ttk.Button(left_frame, image=rotate_icon, bootstyle="light", command=rotate_image)
rotate_button.pack(pady=5)

# button for choosing pen color
color_button = ttk.Button(left_frame, image=color_icon, bootstyle="light", command=change_color)
color_button.pack(pady=5)

# button for erasing the lines drawn over the image file
erase_button = ttk.Button(left_frame, image=erase_icon, bootstyle="light", command=erase_lines)
erase_button.pack(pady=5)

# button for saving the image file
save_button = ttk.Button(left_frame, image=save_icon, bootstyle="light", command=save_image)
save_button.pack(pady=5)

root.mainloop()