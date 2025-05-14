"""
FortVista - Explore Maharashtra's Majestic Forts
------------------------------------------------
Developed by: Kiran Choudhari
GitHub: https://github.com/kiranchoudhari9
Date: May 2025

An educational Python application that allows users to explore the historical forts
of Maharashtra using a GUI interface with voice search and map features.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import webbrowser
import speech_recognition as sr  

# --- Fort Data ---
forts_data = {
    "Shivneri": {
        "Location": "Pune",
        "History": "Birthplace of Chhatrapati Shivaji Maharaj.",
        "Significance": "Historical site with an important legacy.",
        "Image": "images/shivneri.jpg",
        "Coordinates": (19.1930949, 73.852896)
    },
    "Sinhagad": {
        "Location": "Pune",
        "History": "Known for the Battle of Sinhagad (1670).",
        "Significance": "Great trekking destination.",
        "Image": "images/sinhagad.jpg",
        "Coordinates": (18.3772, 73.7413)
    },
    "Raigad": {
        "Location": "Raigad",
        "History": "Capital of Chhatrapati Shivaji Maharaj’s kingdom.",
        "Significance": "Famous for the Samadhi of Shivaji Maharaj and its architecture.",
        "Image": "images/raigad.jpg",
        "Coordinates": (18.233678, 73.440674)
    },
    "Pratapgad": {
        "Location": "Satara",
        "History": "Known for the Battle of Pratapgad (1659).",
        "Significance": "Tourist attraction with historical importance.",
        "Image": "images/pratapgad.jpg",
        "Coordinates": (17.9861, 73.6233)
    },
    "Rajgad": {
        "Location": "Pune",
        "History": "Shivaji Maharaj’s first capital before Raigad.",
        "Significance": "A popular trekking destination.",
        "Image": "images/rajgad.jpg",
        "Coordinates": (18.2864, 73.6797)
    },
    "Torna": {
        "Location": "Pune",
        "History": "First fort captured by Shivaji Maharaj in 1643.",
        "Significance": "Trekking destination with scenic views.",
        "Image": "images/torna.jpg",
        "Coordinates": (18.2967, 73.6674)
    },
    "Lohagad": {
        "Location": "Pune",
        "History": "Famous for the Battle of Lohagad.",
        "Significance": "A fort popular for trekking.",
        "Image": "images/lohagad.jpg",
        "Coordinates": (18.7741, 73.4195)
    },
    "Korigad": {
        "Location": "Lonavala",
        "History": "Historical fort with great views.",
        "Significance": "Known for its well-preserved structures.",
        "Image": "images/korigad.jpg",
        "Coordinates": (18.7394, 73.3467)
    },
    "Khanderi": {
        "Location": "Alibaug",
        "History": "A fort located near the coastal region.",
        "Significance": "Known for its coastal defense role.",
        "Image": "images/khanderi.jpg",
        "Coordinates": (18.6424, 72.8721)
    },
    "Murud Janjira": {
        "Location": "Raigad",
        "History": "An island fort with a rich history.",
        "Significance": "A maritime stronghold during medieval times.",
        "Image": "images/murud_janjira.jpg",
        "Coordinates": (18.2667, 72.9347)
    }
}

# --- Function to Open Google Maps ---
def open_map(lat, lon):
    map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    webbrowser.open(map_url)

# --- Function to Search Forts ---
def search_forts():
    query = entry.get().strip().lower()
    matching_forts = [fort for fort in forts_data if query in fort.lower()]
    text_display.delete("1.0", tk.END)
    image_label.config(image='', text='')
    map_label.config(text="")

    if matching_forts:
        display_container.pack(pady=20, fill=tk.BOTH, expand=True)
        image_label.pack(pady=(10, 5))
        map_label.pack(pady=(0, 10))

        for fort in matching_forts:
            info = forts_data[fort]
            result_text = (
                f"🏰 {fort} Fort\n"
                f"📍 Location: {info['Location']}\n"
                f"📜 History: {info['History']}\n"
                f"⭐ Significance: {info['Significance']}\n\n"
            )
            coordinates_text = f"🗺 Click here for map: {info['Coordinates'][0]:.4f}, {info['Coordinates'][1]:.4f}"
            map_label.config(text=coordinates_text)
            map_label.bind("<Button-1>", lambda e, lat=info['Coordinates'][0], lon=info['Coordinates'][1]: open_map(lat, lon))
            text_display.insert(tk.END, result_text)

            if "Image" in info:
                image_path = info["Image"]
                if os.path.exists(image_path):
                    img = Image.open(image_path)
                    img = img.resize((400, 400), Image.Resampling.LANCZOS)
                    img_photo = ImageTk.PhotoImage(img)
                    image_label.config(image=img_photo)
                    image_label.image = img_photo
                else:
                    image_label.config(text="Image not found.", fg="black", bg="white")
    else:
        messagebox.showwarning("Not Found", "❌ No matching forts found. Try a different keyword.")

# --- Placeholder Logic ---
def on_entry_click(event):
    if entry.get() == "Enter fort name...":
        entry.delete(0, tk.END)
        entry.config(fg="black")

def on_focus_out(event):
    if entry.get() == "":
        entry.insert(0, "Enter fort name...")
        entry.config(fg="gray")

# --- Voice Search Function ---
def voice_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Listening", "Please say the name of the fort...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        messagebox.showinfo("Recognized", f"You said: {query}")
        entry.delete(0, tk.END)
        entry.insert(0, query)
        search_forts()
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Sorry, I could not understand the audio.")
    except sr.RequestError:
        messagebox.showerror("Error", "There was a problem with the speech recognition service.")

# --- GUI Setup ---
root = tk.Tk()
root.title("FortVista")
root.state("zoomed")
root.configure(bg="#2C3E50")

# --- Colors ---
PRIMARY_COLOR = "#2C3E50"
SECONDARY_COLOR = "#2980B9"
TEXT_COLOR = "#FFFFFF"
WHITE = "#FFFFFF"
TEXT_BG_COLOR = "#F9F9F9"

# --- Main Container ---
overlay = tk.Frame(root, bg=PRIMARY_COLOR)
overlay.place(relwidth=1, relheight=1)

# --- Header ---
welcome_title = tk.Label(overlay, text="Welcome to FortVista", font=("Helvetica", 32, "bold"),
                         bg=PRIMARY_COLOR, fg=TEXT_COLOR)
welcome_title.pack(pady=(10, 5))

header = tk.Label(overlay, text="Explore Maharashtra's Majestic Forts",
                  font=("Helvetica", 18, "italic"), bg=PRIMARY_COLOR, fg="#BDC3C7")
header.pack(pady=(0, 25))

# --- Search Section ---
search_box = tk.Frame(overlay, bg=PRIMARY_COLOR)
search_box.pack(pady=10)

entry = tk.Entry(search_box, width=30, font=("Helvetica", 14), fg="gray")
entry.insert(0, "Enter fort name...")
entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focus_out)
entry.grid(row=0, column=0, ipady=6, padx=(0, 10))

search_btn = tk.Button(search_box, text="🔍 Search", font=("Helvetica", 12, "bold"),
                       bg=SECONDARY_COLOR, fg=TEXT_COLOR, width=14, relief="flat", command=search_forts)
search_btn.grid(row=0, column=1)

voice_btn = tk.Button(search_box, text="🎙 Voice Search", font=("Helvetica", 12, "bold"),
                      bg=SECONDARY_COLOR, fg=TEXT_COLOR, width=14, relief="flat", command=voice_search)
voice_btn.grid(row=0, column=2, padx=(10, 0))

# --- Hidden Display Section ---
display_container = tk.Frame(overlay, bg=WHITE, bd=2, relief="groove")

# --- Text Display ---
text_frame = tk.Frame(display_container, bg=WHITE)
text_frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)

text_display = tk.Text(text_frame, font=("Helvetica", 12), wrap="word", height=10,
                       bg=WHITE, fg="black", insertbackground="black", bd=0)
text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame, command=text_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_display.config(yscrollcommand=scrollbar.set)

# --- Image Display ---
image_label = tk.Label(display_container, bg=WHITE)

# --- Map Label ---
map_label = tk.Label(display_container, font=("Helvetica", 12, "italic"),
                     bg=WHITE, fg="#2980B9", cursor="hand2")
map_label.pack(pady=(5, 10))

# --- Footer ---
footer = tk.Label(overlay, text="Developed by Kiran Choudhari", font=("Helvetica", 10),
                  bg=PRIMARY_COLOR, fg="#BDC3C7")
footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
