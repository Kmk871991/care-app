
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

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
        self.root.title("Folder Renamer (Versioned Backup + Logs)")
        self.selected_path = ""
        self.backup_selected = tk.StringVar()
        self.keep_backup = tk.BooleanVar(value=False)

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

        self.undo_label = tk.Label(root, text="Select backup to undo:")
        self.undo_label.pack(pady=5)

        self.backup_combo = ttk.Combobox(root, textvariable=self.backup_selected)
        self.backup_combo.pack(pady=5)

        self.keep_check = tk.Checkbutton(root, text="Keep backup after undo", variable=self.keep_backup)
        self.keep_check.pack(pady=5)

        self.undo_button = tk.Button(root, text="Undo Rename", command=self.undo_rename)
        self.undo_button.pack(pady=5)

        self.quick_undo_button = tk.Button(root, text="Undo Last Action", command=self.undo_last_backup)
        self.quick_undo_button.pack(pady=5)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_path = path
            self.load_backups()

    def load_backups(self):
        backup_root = os.path.join(self.selected_path, "_backup_names")
        if os.path.exists(backup_root):
            backups = [f for f in os.listdir(backup_root) if os.path.isdir(os.path.join(backup_root, f))]
            backups.sort(reverse=True)
            self.backup_combo['values'] = backups
            if backups:
                self.backup_combo.current(0)
        else:
            self.backup_combo['values'] = []

    def log_action(self, action, case, count):
        log_path = os.path.join(self.selected_path, "rename_log.txt")
        with open(log_path, "a") as log:
            log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action} | {case} | {count} folders\n")

    def convert(self):
        selected_case = self.case_combo.get()
        if not selected_case:
            messagebox.showerror("Error", "Please select a case format.")
            return

        try:
            func = CASE_FUNCTIONS[selected_case]
            folder_pairs = []

            for dirpath, dirnames, _ in os.walk(self.selected_path, topdown=False):
                for dirname in dirnames:
                    old_path = os.path.join(dirpath, dirname)
                    new_name = func(dirname)
                    new_path = os.path.join(dirpath, new_name)
                    if new_name != dirname:
                        folder_pairs.append((old_path, new_path))
                        os.rename(old_path, new_path)

            if folder_pairs:
                backup_root = os.path.join(self.selected_path, "_backup_names")
                backup_dir = os.path.join(backup_root, f"backup_{selected_case}")
                os.makedirs(backup_dir, exist_ok=True)

                with open(os.path.join(backup_dir, "folder_pairs.txt"), "w") as f:
                    for old, new in folder_pairs:
                        f.write(old + "|" + new + "\n")

                self.load_backups()
                self.log_action("RENAME", selected_case, len(folder_pairs))
                messagebox.showinfo("Success", f"Renamed using {selected_case}. Backup saved.")

            else:
                messagebox.showinfo("Info", "No folder names needed renaming.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def undo_rename(self):
        selected_backup = self.backup_selected.get()
        if not selected_backup:
            messagebox.showerror("Error", "Please select a backup to undo.")
            return

        self.perform_undo(selected_backup)

    def undo_last_backup(self):
        values = self.backup_combo['values']
        if values:
            self.perform_undo(values[0])
        else:
            messagebox.showerror("Error", "No backups available to undo.")

    def perform_undo(self, backup_name):
        try:
            backup_file = os.path.join(self.selected_path, "_backup_names", backup_name, "folder_pairs.txt")
            if not os.path.exists(backup_file):
                messagebox.showerror("Error", "Backup file not found.")
                return

            with open(backup_file, "r") as f:
                folder_pairs = [line.strip().split("|") for line in f.readlines()]

            folder_pairs.sort(key=lambda x: x[1].count(os.sep), reverse=True)

            for old_path, new_path in folder_pairs:
                if os.path.exists(new_path):
                    os.rename(new_path, old_path)

            if not self.keep_backup.get():
                shutil.rmtree(os.path.join(self.selected_path, "_backup_names", backup_name))

            self.load_backups()
            self.log_action("UNDO", backup_name.replace("backup_", ""), len(folder_pairs))
            messagebox.showinfo("Success", f"Undo successful from {backup_name}.")

        except Exception as e:
            messagebox.showerror("Undo Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderRenamerApp(root)
    root.mainloop()
