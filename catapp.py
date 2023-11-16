
# Cat Application Project #

import io
import requests
import random 
import tkinter as tk
from ttkbootstrap import Style, ttk
from PIL import Image, ImageTk, ImageOps
from tkinter import filedialog, messagebox

# API URLs
image_api = "https://cataas.com/cat"  # Fetching cat images
fact_api = "https://catfact.ninja/fact"  # Fetching cat facts

# Window Settings
window = tk.Tk()
window.title("Cat Application")
window.geometry("600x800")
window.resizable(False, False)
style = Style(theme="darkly")
window.config(bg="#343a40")  # Set the background color of the window

# Function to fetch a cat fact from the API
def fetch_cat_fact():
    try:
        fact_response = requests.get(fact_api)
        fact_response.raise_for_status()
        fact_json = fact_response.json()
        return fact_json['fact']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch cat fact: {str(e)}")

# Function to fetch a random cat picture from the API
def fetch_cat_picture():
    try:
        pic_response = requests.get(image_api)
        pic_response.raise_for_status()
        pic_bytes = pic_response.content
        pic_data_stream = io.BytesIO(pic_bytes)
        cat_image_pil = Image.open(pic_data_stream)
        return cat_image_pil.resize((300, 300))
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch cat picture: {str(e)}")

# Function to update the cat fact text on the canvas
def update_cat_fact_canvas(cat_fact):
    text_canvas.delete("all")
    text_canvas.create_text(10, 10, text=cat_fact, anchor=tk.NW, width=340, font=("TkDefaultFont", 13), fill="white")

# Function to update the cat picture on the label
def update_cat_picture_label(cat_image_pil):
    cat_image = ImageTk.PhotoImage(cat_image_pil)
    pic_label.config(image=cat_image)
    pic_label.image = cat_image
    cat.save_image = cat_image_pil

# Main cat function
def cat():
    try:
        # Fetch a cat fact
        cat_fact = fetch_cat_fact()
        # Display the cat fact
        update_cat_fact_canvas(cat_fact)
        # Fetch a cat picture
        cat_image_pil = fetch_cat_picture()
        # Display the cat picture in the GUI
        update_cat_picture_label(cat_image_pil)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")

# Save Cat Pictures Function
def save_cat_image():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            cat_image_pil = cat.save_image
            cat_image_pil_rgb = cat_image_pil.convert("RGB")
            cat_image_pil_rgb.save(file_path, "JPEG")
            messagebox.showinfo("Save Image", "Image saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {str(e)}")

# Function to display a random cat health tip
def display_health_tip():

    # List of health tips
    cat_health_tips = [
        "Regular vet check-ups are essential for your cat's health.",
        "Provide fresh water for your cat at all times.",
        "Maintain a balanced diet to keep your cat at a healthy weight.",
        "Keep your cat's litter box clean to prevent health issues.",
        "Give your cat plenty of opportunities to play and exercise.",
    ]

    random_tip = random.choice(cat_health_tips)
    text_canvas.delete("all")
    text_canvas.create_text(10, 10, text="Cat Health Tip:\n" + random_tip, anchor=tk.NW, width=340, font=("TkDefaultFont", 13), fill="white")

# Text Function
def fact_text(text):
    text_canvas.create_text(10, 10, text=text, anchor=tk.NW, width=340, font=("TkDefaultFont", 13), fill="white")

# Exit Confirmation
def confirm_exit():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        window.destroy()

# Frame for the cat image with a border
image_frame = tk.Frame(window, bg="white", borderwidth=2, relief=tk.RIDGE)
image_frame.pack(padx=10, pady=10)

# Frame for the text display with a border
text_frame = tk.Frame(window, bg="white", borderwidth=2, relief=tk.RIDGE)
text_frame.pack(padx=10, pady=10)

# Element formating
pic_label = tk.Label(image_frame)
pic_label.pack()

text_canvas = tk.Canvas(text_frame, width=400, height=200)
text_canvas.pack()

generate_button = ttk.Button(window, text="Generate Fact/Image", command=cat)
generate_button.pack(padx=10, pady=10)

health_tip_button = ttk.Button(window, text="Cat Health Tip", command=display_health_tip)
health_tip_button.pack(padx=10, pady=10)

save_button = ttk.Button(window, text="Save Image", command=save_cat_image)
save_button.pack(padx=10, pady=10)

# Exit confirmation behavior
window.protocol("WM_DELETE_WINDOW", confirm_exit)

# Main Application Loop
window.mainloop()