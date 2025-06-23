# Folder Renamer App with Undo & Cleanup (Windows GUI)

Features:
- Select folder
- Rename subfolders to selected case style
- Backup original names
- Undo rename and auto-delete backup folder

## Usage:
1. Run `folder_renamer.py`
2. Select folder
3. Choose case style → click "Convert"
4. To restore → click "Undo Rename" (backup is deleted automatically)

## Create .exe
```
pip install pyinstaller
pyinstaller --onefile --windowed folder_renamer.py
```
Find the EXE in the `dist/` folder.
