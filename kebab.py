
import os
import re
import tkinter as tk
from tkinter import messagebox
import pythoncom
import win32com.client

def to_kebab_case(name):
    name, ext = os.path.splitext(name)
    # Remove quotes and non-alphanumeric characters except spaces, dashes, and underscores
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[_\s]+', '-', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    name = re.sub(r'([0-9])([a-zA-Z])', r'\1-\2', name)
    name = re.sub(r'([a-zA-Z])([0-9])', r'\1-\2', name)
    return name.lower() + ext

def get_selected_item():
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("Shell.Application")
    for window in shell.Windows():
        try:
            if window and window.Document:
                items = window.Document.SelectedItems()
                if items and items.Count > 0:
                    return items.Item(0).Path
        except Exception:
            continue
    return None

def rename_selected():
    path = get_selected_item()
    if not path:
        messagebox.showwarning("Selection Not Found", "No file or folder selected in Windows Explorer.")
        return

    folder, old_name = os.path.split(path)
    new_name = to_kebab_case(old_name)
    new_path = os.path.join(folder, new_name)

    try:
        os.rename(path, new_path)
        messagebox.showinfo("Renamed", f"Renamed to: {new_name}")
    except Exception as e:
        messagebox.showerror("Rename Failed", str(e))

# Main window
root = tk.Tk()
root.title("Kebab Renamer")
root.geometry("220x110+1200+700")
root.configure(bg="#F0F0F0")
root.attributes("-topmost", True)

# Allow window to be moved
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

# Header bar
title_bar = tk.Frame(root, bg="#262626", relief="raised", bd=0)
title_bar.pack(fill=tk.X)
title_label = tk.Label(title_bar, text="🔁 Kebab Renamer", bg="#262626", fg="white", font=("Segoe UI", 10, "bold"))
title_label.pack(side=tk.LEFT, padx=6)

btn_min = tk.Button(title_bar, text="–", command=root.iconify, bg="#262626", fg="white", bd=0, font=("Arial", 12))
btn_min.pack(side=tk.RIGHT, padx=5)
btn_close = tk.Button(title_bar, text="×", command=root.destroy, bg="#262626", fg="white", bd=0, font=("Arial", 12))
btn_close.pack(side=tk.RIGHT)

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", do_move)
title_bar.bind("<ButtonRelease-1>", stop_move)

# Modern rename button
btn = tk.Button(root, text="Rename to kebab-case", command=rename_selected,
                bg="#FF5722", fg="white", font=("Segoe UI", 10, "bold"),
                bd=0, relief="flat", height=2, cursor="hand2")
btn.pack(pady=20, padx=20, fill=tk.BOTH)

btn.configure(highlightthickness=0, padx=10, pady=6)

root.mainloop()
