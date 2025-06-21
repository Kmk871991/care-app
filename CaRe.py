
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
        self.root.title("Folder Case Renamer with Undo")
        self.selected_path = ""
        self.subfolders = []

        self.label = tk.Label(root, text="Select a folder:")
        self.label.pack(pady=5)

        self.select_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.select_button.pack(pady=5)

        self.listbox = tk.Listbox(root, width=60, height=10)
        self.listbox.pack(pady=5)

        self.case_label = tk.Label(root, text="Select case format:")
        self.case_label.pack(pady=5)

        self.case_combo = ttk.Combobox(root, values=list(CASE_FUNCTIONS.keys()))
        self.case_combo.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert)
        self.convert_button.pack(pady=10)

        self.undo_button = tk.Button(root, text="Undo Rename", command=self.undo_rename)
        self.undo_button.pack(pady=5)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_path = path
            self.refresh_subfolders()

    def refresh_subfolders(self):
        self.listbox.delete(0, tk.END)
        self.subfolders = [f for f in os.listdir(self.selected_path) if os.path.isdir(os.path.join(self.selected_path, f))]
        for folder in self.subfolders:
            self.listbox.insert(tk.END, folder)

    def convert(self):
        selected_case = self.case_combo.get()
        if not selected_case:
            messagebox.showerror("Error", "Please select a case format.")
            return

        try:
            func = CASE_FUNCTIONS[selected_case]
            backup_dir = os.path.join(self.selected_path, "_backup_names")
            os.makedirs(backup_dir, exist_ok=True)

            with open(os.path.join(backup_dir, "original_names.txt"), "w") as f:
                for folder in self.subfolders:
                    f.write(folder + "\n")

            for folder in self.subfolders:
                new_name = func(folder)
                if new_name and new_name != folder:
                    os.rename(
                        os.path.join(self.selected_path, folder),
                        os.path.join(self.selected_path, new_name)
                    )

            messagebox.showinfo("Success", "Folder names converted successfully!")
            self.refresh_subfolders()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def undo_rename(self):
        try:
            backup_dir = os.path.join(self.selected_path, "_backup_names")
            backup_file = os.path.join(backup_dir, "original_names.txt")

            if not os.path.exists(backup_file):
                messagebox.showerror("Error", "No backup file found.")
                return

            with open(backup_file, "r") as f:
                original_names = [line.strip() for line in f.readlines()]

            current_folders = [f for f in os.listdir(self.selected_path)
                               if os.path.isdir(os.path.join(self.selected_path, f)) and f != "_backup_names"]

            if len(current_folders) != len(original_names):
                messagebox.showerror("Error", "Mismatch in folder counts. Cannot undo safely.")
                return

            for curr, orig in zip(sorted(current_folders), original_names):
                os.rename(
                    os.path.join(self.selected_path, curr),
                    os.path.join(self.selected_path, orig)
                )

            shutil.rmtree(backup_dir)
            messagebox.showinfo("Success", "Folders restored and backup deleted.")
            self.refresh_subfolders()

        except Exception as e:
            messagebox.showerror("Undo Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderRenamerApp(root)
    root.mainloop()
