import os
import re
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, ttk

selected_image = None

def reformat_text(text):
    # Add a new line after "Parameters:"
    text = re.sub(r"(parameters: |Negative prompt: )", r"\1\n\n", text)

    # Add a new line after "Negative prompt:"
    text = re.sub(r"(Negative prompt: )", r"\n\1", text)

    # Add a new line before "Steps:"
    text = re.sub(r"(Steps:)", r"\n\1", text)

    return text

def open_file_explorer():
    global selected_image

    # Open file explorer to select an image file
    image_path = filedialog.askopenfilename()

    # Read image metadata
    with Image.open(image_path) as image:
        metadata = image.info

        # Print all metadata key-value pairs
        metadata_text = ""
        for key, value in metadata.items():
            metadata_text += f"{key}: {value}\n"

        # Save the selected image globally
        selected_image = image

        # Update the image preview
        update_image_preview()

    # Clear the text box
    text_box.delete(1.0, tk.END)

    formatted_metadata = reformat_text(metadata_text)
    text_box.insert(tk.END, formatted_metadata)

def update_image_preview():
    global selected_image

    if selected_image is not None:
        # Resize image to fit within the available space
        image = selected_image.copy()
        image.thumbnail((right_frame.winfo_width(), right_frame.winfo_height()))

        # Update the image preview
        image_preview = ImageTk.PhotoImage(image)
        image_label.configure(image=image_preview)
        image_label.image = image_preview

def on_window_resize(event):
    # Update the image preview when the window is resized
    update_image_preview()

# Create the GUI window
window = tk.Tk()
window.title("Image Metadata Viewer")
window.geometry("1000x550")

# Create a frame for the left section (button and metadata)
left_frame = ttk.Frame(window)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

# Create a button for file explorer
button = ttk.Button(left_frame, text="Select Image", command=open_file_explorer)
button.pack(anchor=tk.NW)

# Create a label for formatted metadata
label = ttk.Label(left_frame, text="Formatted Metadata:")
label.pack(pady=10)

# Create a text box with vertical scrollbar
text_frame = ttk.Frame(left_frame)
text_frame.pack(fill=tk.BOTH, expand=True)

text_box = Text(text_frame, wrap=tk.WORD)
scrollbar = Scrollbar(text_frame, command=text_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.configure(yscrollcommand=scrollbar.set)
text_box.pack(fill=tk.BOTH, expand=True)

# Create a frame for the right section (image preview)
right_frame = ttk.Frame(window)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a label for image preview
image_label = ttk.Label(right_frame)
image_label.pack(fill=tk.BOTH, expand=True)

# Bind the resize event to update the image preview
window.bind("<Configure>", on_window_resize)

# Run the GUI window
window.mainloop()
