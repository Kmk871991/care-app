
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def to_pascal_case_smart(name):
    import re
    base, ext = os.path.splitext(name)
    clean = re.sub(r"[_\-\.]", " ", base)
    parts = re.findall(r'[A-Za-z]+|\d+', clean)

    result = ""
    for i, part in enumerate(parts):
        if part.isdigit() and i != 0:
            result += "_" + part
        else:
            result += part.capitalize()
    return result + ext

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_var.set(file_path)

def rename_file():
    file_path = entry_var.get()
    if not file_path or not os.path.isfile(file_path):
        messagebox.showerror("Error", "Please select a valid file.")
        return

    folder, old_name = os.path.split(file_path)
    new_name = to_pascal_case_smart(old_name)
    new_path = os.path.join(folder, new_name)

    try:
        os.rename(file_path, new_path)
        messagebox.showinfo("Success", f"Renamed to: {new_name}")
        entry_var.set(new_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("PascalCase File Renamer")

entry_var = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

entry = tk.Entry(frame, textvariable=entry_var, width=60)
entry.grid(row=0, column=0, padx=5, pady=5)

browse_btn = tk.Button(frame, text="Browse File", command=select_file)
browse_btn.grid(row=0, column=1, padx=5, pady=5)

rename_btn = tk.Button(frame, text="Rename to PascalCase", command=rename_file)
rename_btn.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
