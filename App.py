from tkinter import *
from Account import Account

account = Account()


def center_window(window, wwidth, wheight):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    wx = (screen_width - wwidth) // 2
    wy = (screen_height - wheight - 50) // 2
    window.geometry(f"{width}x{height}+{wx}+{wy}")


root = Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
width = 900
height = 600
x = (root.winfo_screenwidth()//2) - (width//2)
y = (root.winfo_screenheight()//2) - (height//2)
root.geometry("{}x{}+{}+{}".format(width, height, x, y))

root.title("CramJam")
root.iconbitmap("Assets/Logo.ico")

# Create frames
login_frame = Frame(root)
signup_frame = Frame(root)

for frame in (login_frame, signup_frame):
    frame.grid(row=0, column=0, sticky="nsew")


def show_frame(cframe):
    cframe.tkraise()


show_frame(login_frame)

# SignUp Frame ----------------------------------------------

# Load images
signup_background_img = PhotoImage(file="Assets/signup_background.png")

# Keep references to the images
signup_background_label = Label(signup_frame, image=signup_background_img)
signup_background_label.image = signup_background_img
signup_background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create and place Entry widgets
signup_entry_email = Entry(signup_frame, bd=0, bg="#d9d9d9", highlightthickness=0)
signup_entry_email.place(x=325, y=262.5, width=250, height=30)

signup_entry_username = Entry(signup_frame, bd=0, bg="#d9d9d9", highlightthickness=0)
signup_entry_username.place(x=325, y=332.5, width=250, height=30)

# Load images for buttons
img_reg = PhotoImage(file="Assets/button_register.png")
img_log1 = PhotoImage(file="Assets/button_login1.png")
img_hide1 = PhotoImage(file="Assets/password_hide1.png")
img_show1 = PhotoImage(file="Assets/password_show1.png")

# Create and place buttons
register_button = Button(signup_frame, image=img_reg, borderwidth=0, highlightthickness=0, relief="flat", bg="#d9d9d9", command=lambda: account.register(signup_entry_email.get(), signup_entry_username.get(), signup_entry_password.get()))
register_button.place(x=372.5, y=450, width=155, height=50)


def toggle_password():
    if signup_entry_password.cget("show") == '':
        signup_entry_password.config(show='●')
        show_signup_password_button.config(image=img_show1)
    else:
        signup_entry_password.config(show='')
        show_signup_password_button.config(image=img_hide1)


def check_entry_content(*args):
    if signup_entry_password.get():
        show_signup_password_button.place(x=550, y=408, width=30, height=20)
    else:
        show_signup_password_button.place_forget()


signup_password_var = StringVar()
signup_entry_password = Entry(signup_frame, bd=0, bg="#d9d9d9", highlightthickness=0, show="●", textvariable=signup_password_var)
signup_entry_password.place(x=325, y=402.5, width=220, height=30)
signup_password_var.trace("w", check_entry_content)  # Bind a callback to the Entry widget

show_signup_password_button = Button(signup_frame, image=img_show1, borderwidth=0, highlightthickness=0, relief="flat", bg="#d9d9d9", command=toggle_password)
show_signup_password_button.place(x=550, y=408, width=30, height=20)
show_signup_password_button.place_forget()

login1_button = Button(signup_frame, image=img_log1, borderwidth=0, highlightthickness=0, relief="flat", bg="#d9d9d9", command=lambda: show_frame(login_frame))
login1_button.place(x=530, y=80, width=90, height=20)

# End of SignUp Frame ---------------------------------------

# Login Frame -----------------------------------------------

login_frame.configure(bg="#d9d9d9")

# Load images
login_background_img = PhotoImage(file="Assets/login_background.png")

# Keep references to the images
login_background_label = Label(login_frame, image=login_background_img)
login_background_label.image = login_background_img
login_background_label.place(x=0, y=0, relwidth=1, relheight=1)

login_entry_username = Entry(login_frame, bd=0, bg="#d9d9d9", highlightthickness=0)
login_entry_username.place(x=325, y=273, width=250, height=30)

# Load images for buttons
img_sign = PhotoImage(file="Assets/button_signup.png")
img_log0 = PhotoImage(file="Assets/button_login0.png")
img_hide = PhotoImage(file="Assets/password_hide.png")
img_show = PhotoImage(file="Assets/password_show.png")

# Create and place buttons
login0_button = Button(login_frame, image=img_log0, borderwidth=0, highlightthickness=0, relief="flat", bg="#d9d9d9", command=lambda: account.login(login_entry_username.get(), login_entry_password.get()))
login0_button.place(x=372.5, y=420, width=155, height=50)


def toggle_password():
    if login_entry_password.cget("show") == '':
        login_entry_password.config(show='●')
        show_login_password_button.config(image=img_show)
    else:
        login_entry_password.config(show='')
        show_login_password_button.config(image=img_hide)


def check_entry_content(*args):
    if login_entry_password.get():
        show_login_password_button.place(x=550, y=359, width=30, height=20)
    else:
        show_login_password_button.place_forget()


login_password_var = StringVar()
login_entry_password = Entry(login_frame, bd=0, bg="#d9d9d9", highlightthickness=0, show="●", textvariable=login_password_var)
login_entry_password.place(x=325, y=353, width=220, height=30)
login_password_var.trace("w", check_entry_content)  # Bind a callback to the Entry widget

show_login_password_button = Button(login_frame, image=img_show, borderwidth=0, highlightthickness=0, relief="flat", bg="#d9d9d9", command=toggle_password)
show_login_password_button.place(x=550, y=359, width=100, height=30)
show_login_password_button.place_forget()  # Initially hide the button

signup_button = Button(login_frame, image=img_sign, borderwidth=0, highlightthickness=0, relief="flat", bg="#d9d9d9", command=lambda: show_frame(signup_frame))
signup_button.place(x=530, y=80, width=90, height=20)

# End of Login Frame -----------------------------------------


root.resizable(False, False)
center_window(root, 900, 584)
root.mainloop()
