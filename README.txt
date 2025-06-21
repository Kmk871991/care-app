# Recursive Folder Renamer with Undo (Windows GUI)

✅ Rename all subfolders (even nested ones) recursively  
✅ Undo operation restores folders back and deletes the backup

## How to Use
1. Run `folder_renamer.py`
2. Select a folder
3. Choose case style
4. Click "Convert Recursively"
5. To undo, click "Undo Rename"

## Build EXE
```
pip install pyinstaller
pyinstaller --onefile --windowed folder_renamer.py
```
Find the EXE in the `dist/` folder.
