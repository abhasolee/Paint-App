from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from PIL import ImageGrab
from tkinter import filedialog
from tkinter import messagebox


# Configuring window
root = Tk()
root.title("Paint App")
root.geometry('900x600+250-0')

# Setting the initial value of brush color
global brush_color
brush_color = " "


# Function to set brush color
def set_brush_color():
    # Choosing a color
    my_color = colorchooser.askcolor()

    # Returning the brush color
    global brush_color
    brush_color = my_color[1]


# Function to change canvas color
def change_canvas_color():
    # Choosing a color
    my_color = colorchooser.askcolor()

    # Changing the bg of the canvas
    my_canvas.config(bg="{}".format(my_color[1]))


# Function to get first position of mouse
def get_current_xy(event):
    global first_x, first_y
    first_x = event.x
    first_y = event.y


# Function to get released position of mouse
def get_released_xy(event):
    global released_x, released_y
    released_x, released_y = event.x, event.y

    # Getting the value of slider
    w = int(brush_size_slider.get())
    if w == 0:
        w = 1

    # Creating shapes
    if brush_type_var.get() == "Round":
        draw = my_canvas.create_oval(
            first_x, first_y, released_x, released_y, width=w)

        # Configuring the brush color
        if brush_color != " ":
            my_canvas.itemconfig(draw, fill="{}".format(
                brush_color), outline="{}".format(brush_color))

    elif brush_type_var.get() == "Rectangle":
        draw = my_canvas.create_rectangle(
            first_x, first_y, released_x, released_y, width=w)

        # Configuring the brush color
        if brush_color != " ":
            my_canvas.itemconfig(draw, fill="{}".format(
                brush_color), outline="{}".format(brush_color))


# Function to create a line while dragging the mouse
def create_line(event):
    global first_x, first_y

    # Getting the value of slider
    w = int(brush_size_slider.get())
    if w == 0:
        w = 1

    if brush_type_var.get() == "Line":
        # Create a line
        draw = my_canvas.create_line(first_x, first_y, event.x,
                                     event.y, width=w)

        # Configuring the brush color
        if brush_color != " ":
            my_canvas.itemconfig(draw, fill="{}".format(brush_color))

        # Make a new starting position
        first_x, first_y = event.x, event.y


# Function to save canvas drawing to png
def save_to_png(widget):
    # Getting the top left of canvas
    x = root.winfo_x() + widget.winfo_x()
    # 22 is added because of the pady of the body frame
    y = root.winfo_y() + widget.winfo_y() + 22

    # Getting the bottom part
    x1 = x + widget.winfo_width()
    y1 = y + widget.winfo_height()

    # Calling the save as window
    filename = filedialog.asksaveasfilename(title="Select File",
                                            filetypes=(
                                                ('PNG files', "*.png"), ("All Files", "*.*"))
                                            )

    # Showing a message box
    response = messagebox.showinfo("Saved", "Your Image has been saved")

    try:
        # Grabbing the canvas image and saving it
        if response == "ok":
            ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
    except ValueError:
        pass


# Function to clear canvas
def clear_canvas():
    my_canvas.delete("all")
    my_canvas.config(bg="white")


# Create title frame
title_frame = Frame(root, width=900, height=50)
title_frame.grid(row=0, column=0)

# Create a title label in title frame
title_label = Label(title_frame, text="Draw Your Thoughts",
                    font=('Adrenaline', 27, 'bold'), fg="#F7882F")
title_label.config(anchor=CENTER)
title_label.pack()

# Create canvas
my_canvas = Canvas(root, width=800, height=350,
                   relief=SUNKEN, highlightthickness=2, bd=1, highlightbackground="#F7C331")
my_canvas.grid(row=1, column=0, padx=50, columnspan=4)


# Create body frame
body_frame = Frame(root, width=850, height=200)
body_frame.grid(row=2, column=0, pady=20)

# Create label frames
brush_size = LabelFrame(body_frame, text="Brush Size",
                        width=100, height=150, bd=2)
brush_size.grid(row=0, column=0, padx=30)

brush_type = LabelFrame(body_frame, text="Brush Type",
                        width=150, height=100, bd=2)
brush_type.grid(row=0, column=1, padx=30)

bg_color = LabelFrame(body_frame, text="Change background",
                      width=200, height=120, bd=2)
bg_color.grid(row=0, column=2, padx=30)

other_option = LabelFrame(body_frame, text="Other",
                          width=150, height=110, bd=2)
other_option.grid(row=0, column=3, padx=20)

# Create a slider
brush_size_slider = ttk.Scale(brush_size, from_=50, to=1, orient=VERTICAL)
brush_size_slider.place(relx=0.5, rely=0.45, anchor=CENTER)

# Create radio buttons
brush_type_var = StringVar()
round_brush = ttk.Checkbutton(brush_type, text="Round",
                              variable=brush_type_var, onvalue="Round")
round_brush.place(relx=0, rely=0)

slash_brush = ttk.Checkbutton(brush_type, text="Line",
                              variable=brush_type_var, onvalue="Line")
slash_brush.place(relx=0, rely=0.3)

diamond_brush = ttk.Checkbutton(
    brush_type, text="Rectangle", variable=brush_type_var, onvalue="Rectangle")
diamond_brush.place(relx=0, rely=0.6)

# Create buttons for color change
change_bg_button = Button(
    bg_color, text="Change Canvas Color", font=('Coves', 18), fg="#F7882F", command=change_canvas_color)
change_bg_button.place(relx=0.15, rely=0)

change_brush_color_button = Button(
    bg_color, text="Change Brush Color", font=('Coves', 18), fg="#F7882F", command=set_brush_color)
change_brush_color_button.place(relx=0.15, rely=0.5)

# Create buttons for other options
clear_screen_button = Button(
    other_option, text="Clear Screen", font=('Coves', 18), fg="#d8ab4e", command=clear_canvas)
clear_screen_button.place(relx=0.15, rely=0)

save_button = Button(other_option, text="Save To PNG",
                     font=('Coves', 18), fg="#d8ab4e", command=lambda: save_to_png(my_canvas))
save_button.place(relx=0.15, rely=0.5)

# Binding mouse-click events
my_canvas.bind("<Button-1>", get_current_xy)
my_canvas.bind("<B1-Motion>", create_line)
my_canvas.bind("<ButtonRelease-1>", get_released_xy)

root.mainloop()
