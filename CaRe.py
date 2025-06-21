
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def to_pascal_case(name): return ''.join(word.capitalize() for word in name.replace('_', ' ').replace('-', ' ').split())
def to_kebab_case(name): return '-'.join(name.lower().split())
def to_camel_case(name):
    words = name.lower().split()
    return words[0] + ''.join(word.capitalize() for word in words[1:])
def to_snake_case(name): return '_'.join(name.lower().split())
def to_upper_case(name): return name.upper()
def to_lower_case(name): return name.lower()
def to_title_case(name): return name.title()
def to_sentence_case(name): 
    words = name.lower().split()
    return ' '.join([words[0].capitalize()] + words[1:]) if words else ''

CASE_FUNCTIONS = {
    "PascalCase": to_pascal_case,
    "kebab-case": to_kebab_case,
    "camelCase": to_camel_case,
    "snake_case": to_snake_case,
    "UPPERCASE": to_upper_case,
    "lowercase": to_lower_case,
    "Title Case": to_title_case,
    "Sentence case": to_sentence_case
}

class FolderRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recursive Folder Renamer with Undo")
        self.selected_path = ""
        self.folder_pairs = []

        self.label = tk.Label(root, text="Select a folder:")
        self.label.pack(pady=5)

        self.select_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.select_button.pack(pady=5)

        self.case_label = tk.Label(root, text="Select case format:")
        self.case_label.pack(pady=5)

        self.case_combo = ttk.Combobox(root, values=list(CASE_FUNCTIONS.keys()))
        self.case_combo.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert Recursively", command=self.convert)
        self.convert_button.pack(pady=10)

        self.undo_button = tk.Button(root, text="Undo Rename", command=self.undo_rename)
        self.undo_button.pack(pady=5)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_path = path

    def convert(self):
        selected_case = self.case_combo.get()
        if not selected_case:
            messagebox.showerror("Error", "Please select a case format.")
            return

        try:
            func = CASE_FUNCTIONS[selected_case]
            self.folder_pairs = []

            for dirpath, dirnames, _ in os.walk(self.selected_path, topdown=False):
                for dirname in dirnames:
                    old_path = os.path.join(dirpath, dirname)
                    new_name = func(dirname)
                    new_path = os.path.join(dirpath, new_name)
                    if new_name != dirname:
                        self.folder_pairs.append((old_path, new_path))
                        os.rename(old_path, new_path)

            if self.folder_pairs:
                backup_dir = os.path.join(self.selected_path, "_backup_names")
                os.makedirs(backup_dir, exist_ok=True)
                with open(os.path.join(backup_dir, "folder_pairs.txt"), "w") as f:
                    for old, new in self.folder_pairs:
                        f.write(old + "|" + new + "\n")

                messagebox.showinfo("Success", "All folders renamed recursively.")
            else:
                messagebox.showinfo("Info", "No folder names needed renaming.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def undo_rename(self):
        try:
            backup_dir = os.path.join(self.selected_path, "_backup_names")
            backup_file = os.path.join(backup_dir, "folder_pairs.txt")

            if not os.path.exists(backup_file):
                messagebox.showerror("Error", "No backup file found.")
                return

            with open(backup_file, "r") as f:
                folder_pairs = [line.strip().split("|") for line in f.readlines()]

            # Sort by path depth descending to avoid rename conflicts
            folder_pairs.sort(key=lambda x: x[1].count(os.sep), reverse=True)

            for old_path, new_path in folder_pairs:
                if os.path.exists(new_path):
                    os.rename(new_path, old_path)

            shutil.rmtree(backup_dir)
            messagebox.showinfo("Success", "Undo successful. Folders restored.")

        except Exception as e:
            messagebox.showerror("Undo Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderRenamerApp(root)
    root.mainloop()
