import tkinter as tk
from tkinter import filedialog

# Create a Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Use the file dialog to open a file
file_path = filedialog.askopenfilename()

# Check if a file was selected
if file_path:
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        # Now you can work with the contents of the selected file

# Don't forget to start the Tkinter main loop if your application requires it
# root.mainloop()
