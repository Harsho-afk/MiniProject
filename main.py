import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab, ImageEnhance

# defining global variables
WIDTH = 1720
HEIGHT = 1080
pen_size = 3
pen_color = "black"
brightness_factor = 1.0
contrast_factor = 1.0
drawing_mode = False
flip = None

current_image_path = None
original_image = None
displayed_image = None
image_history = []
history_index = -1

# display image
def display_image(image):
    global canvas,displayed_image
    if image:
        resized_image = image.resize((int(WIDTH/2), int(HEIGHT/2)), Image.LANCZOS)
        displayed_image = ImageTk.PhotoImage(image)
        canvas.create_image(WIDTH/2,HEIGHT/2, anchor="center", image=displayed_image)
    else:
        print("error")


# function to open the image file
def open_image():
    global original_image,displayed_image,current_image_path,canvas
    file_path = filedialog.askopenfilename(title="Open Image File",filetypes=[("Image Files","*.png *.jpg *.jpeg *.gif *.bmp *.ico")])
    if file_path:
        original_image = Image.open(file_path)
        current_image_path = file_path
        save_to_history(original_image)
        display_image(original_image)

# function to flip image
def flip_image():
    global original_image,displayed_image,flip
    if original_image:
        match flip:
            case "None":
                return
            case "Horizontal":
                fliped_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
            case "Vertical":
                fliped_image = original_image.transpose(Image.FLIP_TOP_BOTTOM)
        save_to_history(fliped_image)
        display_image(fliped_image)
        original_image = fliped_image
    else:
        showerror(title='Flip Image Error', message='Please select an image to flip!')


# function for rotating the image
def rotate_image():
    global original_image,displayed_image
    if original_image:
        rotated_image = original_image.transpose(Image.ROTATE_90)
        save_to_history(rotated_image)
        display_image(rotated_image)
        original_image = rotated_image
    else:
        showerror(title='Rotate Image Error', message='Please select an image to rotate!')

# function for applying filters to the opened image file
filtersApplied = []
def apply_filter(filter,fromRedo):
    global original_image,displayed_image,filtersApplied
    if original_image:
        if filter == "Black and White" and filtersApplied.count("Black and White") == 0:
            filtered_image = ImageOps.grayscale(original_image)
            filtersApplied.append("Black and White")
        elif filter == "Blur"and filtersApplied.count("Blur") == 0:
            filtered_image = original_image.filter(ImageFilter.BLUR)
            filtersApplied.append("Blur")
        elif filter == "Contour"and filtersApplied.count("Contour") == 0:
            filtered_image = original_image.filter(ImageFilter.CONTOUR)
            filtersApplied.append("Contour")
        elif filter == "Detail"and filtersApplied.count("Detail") == 0:
            filtered_image = original_image.filter(ImageFilter.DETAIL)
            filtersApplied.append("Detail")
        elif filter == "Emboss"and filtersApplied.count("Emboss") == 0:
            filtered_image = original_image.filter(ImageFilter.EMBOSS)
            filtersApplied.append("Emboss")
        elif filter == "Edge Enhance"and filtersApplied.count("Edge Enhance") == 0:
            filtered_image = original_image.filter(ImageFilter.EDGE_ENHANCE)
            filtersApplied.append("Edge Enhance")
        elif filter == "Sharpen"and filtersApplied.count("Sharpen") == 0:
            filtered_image = original_image.filter(ImageFilter.SHARPEN)
            filtersApplied.append("Sharpen")
        elif filter == "Smooth"and filtersApplied.count("Smooth") == 0:
            filtered_image = original_image.filter(ImageFilter.SMOOTH)
            filtersApplied.append("Smooth")
        if not fromRedo:
            save_to_history(filtered_image)
        display_image(filtered_image)
        original_image = filtered_image
    else:
        showerror(title='Filter Image Error', message='Please select an image first!')

# function to update brightness
def update_brightness():
    global original_image,displayed_image,brightness_var
    if original_image:
        brightness_factor = brightness_var.get()
        enhanced_image = ImageEnhance.Brightness(original_image).enhance(brightness_factor)
        #save_to_history(enhanced_image)
        display_image(enhanced_image)

# fucntion to update contrast
def update_contrast():
    global original_image,displayed_image,contrast_var
    if original_image:
        contrast_factor = contrast_var.get()
        enhanced_image = ImageEnhance.Contrast(original_image).enhance(contrast_factor)
        #save_to_history(enhanced_image)
        display_image(enhanced_image)

# fucntion to save image to list after a change
def save_to_history(image):
    global image_history, history_index
    if image:
        image_history = image_history[: history_index + 1]
        image_history.append(image.copy())
        history_index = len(image_history) - 1

# undo function
undo_filters = []
def undo():
    global original_image,history_index,filtersApplied,undo_filters
    if history_index > 0:
        history_index -= 1
        original_image = image_history[history_index].copy()
        display_image(original_image)
        if filtersApplied:
            undo_filters.append(filtersApplied.pop())
    return history_index

# redo function
def redo():
    global original_image,history_index,undo_filters
    if history_index < len(image_history) - 1:
        history_index += 1
        original_image = image_history[history_index].copy()
        if undo_filters:
            apply_filter(undo_filters.pop(),True)
        display_image(original_image)
        
    return history_index

# draw fucntions
def start_drawing():
    global drawing_mode,current_draw
    drawing_mode = True
    current_draw = []

def stop_drawing():
    global drawing_mode
    drawing_mode = False

def draw(event):
    global drawing_mode,current_draw
    if drawing_mode:
        x, y = event.x, event.y
        current_draw.append((x, y))
        canvas.create_line(current_draw, fill=pen_color, width=pen_size, tags="line")


# function for changing the pen color
def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

# erase function
def erase_lines():
    global canvas,current_draw
    current_draw = []
    canvas.delete("line")
    
# combobox fucntion for filters
def on_combobox_selectFilter(event):
    selected_value = filter_combobox.get()
    apply_filter(selected_value,False)

# combobox fucntion for flip
def on_combobox_selectFlip(event):
    global flip
    flip = flip_combobox.get()

# save Image
def save_image():
    global current_image_path

    if current_image_path:
        image = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(), canvas.winfo_rooty() + canvas.winfo_height()))
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        
        if file_path:
            if askyesno(title='Save Image', message='Do you want to save this image?'):
                image.save(file_path)

# window
root = ttk.Window(themename="cosmo")
root.title("Image Editor")
root.geometry("1920x1080+0+0")
icon = ttk.PhotoImage(file='Images/icon.png')
root.iconphoto(False, icon)

# widget
left_frame = ttk.Frame(root,width=200, height=720)
left_frame.pack(side="left", fill="y")

# canvas
canvas = ttk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# add all images
image_icon = ttk.PhotoImage(file = 'Images/add.png').subsample(12, 12)
flip_icon = ttk.PhotoImage(file = 'Images/flip.png').subsample(12, 12)
rotate_icon = ttk.PhotoImage(file = 'Images/rotate.png').subsample(12, 12)
color_icon = ttk.PhotoImage(file = 'Images/color.png').subsample(12, 12)
erase_icon = ttk.PhotoImage(file = 'Images/erase.png').subsample(12, 12)
save_icon = ttk.PhotoImage(file = 'Images/saved.png').subsample(12, 12)

# button for opening the image file
image_button = ttk.Button(left_frame, image=image_icon, bootstyle="light",command=open_image)
image_button.pack(pady=5)

# filters combobox  
filter_label = ttk.Label(left_frame, text="Select Filter:", background="white")
filter_label.pack(padx=0, pady=2)
image_filters = ["Contour", "Black and White", "Blur", "Detail", "Emboss", "Edge Enhance", "Sharpen", "Smooth"]
filter_combobox = ttk.Combobox(left_frame,bootstyle="dark", values=image_filters, width=15)
filter_combobox.set("Select an option")
filter_combobox.bind("<<ComboboxSelected>>", on_combobox_selectFilter)
filter_combobox.pack(padx=10, pady=5) 

# flip combobox
flip_label = ttk.Label(left_frame,text="Select Flip:",background="white")
flip_label.pack(padx=0,pady=2)
flip_options=["None","Horizontal","Vertical"]
flip_combobox = ttk.Combobox(left_frame,bootstyle="dark",values=flip_options,width=15)
flip_combobox.set("Select an option")
flip_combobox.bind("<<ComboboxSelected>>",on_combobox_selectFlip)
flip_combobox.pack(padx=10,pady=5)

# flip button
flip_button = ttk.Button(left_frame, image=flip_icon,bootstyle="light", command=flip_image)
flip_button.pack(pady=5)

# rotate button
rotate_button = ttk.Button(left_frame, image=rotate_icon,bootstyle="light", command=rotate_image)
rotate_button.pack(pady=5)

# pen color button
color_button = ttk.Button(left_frame, image=color_icon,bootstyle="light", command=change_color)
color_button.pack(pady=5)

# erase button
erase_button = ttk.Button(left_frame, image=erase_icon, bootstyle="light",command=erase_lines)
erase_button.pack(pady=5)

# save button
save_button = ttk.Button(left_frame, image=save_icon,bootstyle="light", command=save_image)
save_button.pack(pady=5)

# slider bar for brightness
brightness_label = ttk.Label(left_frame,bootstyle="dark",text="Brightness:")
brightness_label.pack(pady=5)

brightness_var = ttk.DoubleVar()
brightness_var.set(1.0)
brightness_scale = ttk.Scale(left_frame, from_=0.1, to=2.0, length=200, bootstyle="dark",orient=ttk.HORIZONTAL, variable=brightness_var,command=lambda x: update_brightness())
brightness_scale.pack(pady=5)

# slider bar for contrast
contrast_label = ttk.Label(left_frame,bootstyle="dark",text="Contrast:")
contrast_label.pack(pady=5)

contrast_var = ttk.DoubleVar()
contrast_var.set(1.0)
contrast_scale = ttk.Scale(left_frame, from_=0.1, to=2.0, length=200,bootstyle="dark", orient=ttk.HORIZONTAL, variable=contrast_var,command=lambda x: update_contrast())
contrast_scale.pack(pady=5)

# draw button
start_drawing_button = ttk.Button(left_frame, bootstyle="dark-outline",text="Start Drawing", command=start_drawing)
start_drawing_button.pack(pady=5)

stop_drawing_button = ttk.Button(left_frame, bootstyle="dark-outline",text="Stop Drawing", command=stop_drawing)
stop_drawing_button.pack(pady=5)

canvas.bind("<Button-1>", draw)
canvas.bind("<B1-Motion>", draw)

# undo button
undo_button = ttk.Button(left_frame, bootstyle="dark-outline",text="Undo", command=undo)
undo_button.pack(pady=5)

# redo button
redo_button = ttk.Button(left_frame, bootstyle="dark-outline",text="Redo", command=redo)
redo_button.pack(pady=5)

root.mainloop()