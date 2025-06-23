
import os
import re
import json
import tkinter as tk
from tkinter import messagebox
import pythoncom
import win32com.client

BACKUP_FILE = os.path.join(os.path.dirname(__file__), "rename_backlog.json")

def to_kebab_case(name):
    name, ext = os.path.splitext(name)
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[_\s]+', '-', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    name = re.sub(r'([0-9])([a-zA-Z])', r'\1-\2', name)
    name = re.sub(r'([a-zA-Z])([0-9])', r'\1-\2', name)
    return name.lower() + ext

def get_selected_items():
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("Shell.Application")
    all_paths = []
    for window in shell.Windows():
        try:
            if window and window.Document:
                items = window.Document.SelectedItems()
                for i in range(items.Count):
                    all_paths.append(items.Item(i).Path)
        except Exception:
            continue
    return all_paths

def load_backup():
    if os.path.exists(BACKUP_FILE):
        with open(BACKUP_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_backup(backup):
    with open(BACKUP_FILE, 'w') as f:
        json.dump(backup, f, indent=2)

def rename_selected():
    paths = get_selected_items()
    if not paths:
        messagebox.showwarning("Selection Not Found", "No files or folders selected.")
        return

    backup = load_backup()
    renamed = []

    for path in paths:
        folder, old_name = os.path.split(path)
        new_name = to_kebab_case(old_name)
        new_path = os.path.join(folder, new_name)
        if path != new_path:
            try:
                os.rename(path, new_path)
                renamed.append(new_name)
                backup[new_path] = path
            except Exception as e:
                messagebox.showerror("Rename Failed", f"{old_name} → {e}")
                return

    save_backup(backup)

    if renamed:
        messagebox.showinfo("Success", "Renamed:\n" + "\n".join(renamed))
    else:
        messagebox.showinfo("No Change", "All names already in kebab-case.")

def undo_selected():
    paths = get_selected_items()
    if not paths:
        messagebox.showwarning("Selection Not Found", "No files or folders selected.")
        return

    backup = load_backup()
    undone = []

    for path in paths:
        if path in backup:
            original_path = backup[path]
            try:
                os.rename(path, original_path)
                undone.append(os.path.basename(path))
                del backup[path]
            except Exception as e:
                messagebox.showerror("Undo Failed", f"{path} → {e}")
                return

    save_backup(backup)

    if undone:
        messagebox.showinfo("Undone", "Restored:\n" + "\n".join(undone))
    else:
        messagebox.showinfo("Nothing to Undo", "No matching entries in backup.")

# GUI
root = tk.Tk()
root.title("Kebab Renamer + Undo")
root.geometry("260x140+1200+700")
root.configure(bg="#F0F0F0")
root.attributes("-topmost", True)

def start_move(event): root.x, root.y = event.x, event.y
def stop_move(event): root.x, root.y = None, None
def do_move(event):
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"+{x}+{y}")

# Header
title_bar = tk.Frame(root, bg="#262626", relief="raised", bd=0)
title_bar.pack(fill=tk.X)
tk.Label(title_bar, text="🔁 Kebab Renamer + Undo", bg="#262626", fg="white",
         font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=6)
tk.Button(title_bar, text="–", command=root.iconify, bg="#262626", fg="white",
          bd=0, font=("Arial", 12)).pack(side=tk.RIGHT, padx=5)
tk.Button(title_bar, text="×", command=root.destroy, bg="#262626", fg="white",
          bd=0, font=("Arial", 12)).pack(side=tk.RIGHT)

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", do_move)
title_bar.bind("<ButtonRelease-1>", stop_move)

# Buttons
tk.Button(root, text="Rename to kebab-case", command=rename_selected,
          bg="#FF5722", fg="white", font=("Segoe UI", 10, "bold"),
          bd=0, relief="flat", height=2, cursor="hand2").pack(pady=5, padx=20, fill=tk.BOTH)

tk.Button(root, text="Undo Rename", command=undo_selected,
          bg="#607D8B", fg="white", font=("Segoe UI", 10, "bold"),
          bd=0, relief="flat", height=2, cursor="hand2").pack(pady=5, padx=20, fill=tk.BOTH)

root.mainloop()
