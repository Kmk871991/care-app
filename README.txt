# Folder Renamer with Versioned Backups, Undo Options, and Logging

Features:
- Recursively renames all subfolders using chosen case style
- Creates separate backup for each case (e.g., `backup_kebab-case`)
- Option to keep or delete backup after undo
- "Undo Last Action" button
- Logs all renames and undos to `rename_log.txt`

## How to Use
1. Run `folder_renamer.py`
2. Select folder
3. Choose case format → Convert
4. Select backup from dropdown → Undo
5. Or use "Undo Last Action" to quickly revert latest change
6. Check `rename_log.txt` for history

## Create .exe:
```
pip install pyinstaller
pyinstaller --onefile --windowed folder_renamer.py
```
