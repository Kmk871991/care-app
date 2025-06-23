
[Setup]
AppName=CaRe
AppVersion=1.0
DefaultDirName={pf}\CaRe
DefaultGroupName=CaRe
OutputBaseFilename=CaRe Installer
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\care.exe
UninstallDisplayName=CaRe - Folder/File Renamer Tool

[Files]
Source: "D:\Git\care-app\CaRe\dist\CaRe.exe"; DestName: "CaRe.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CaRe"; Filename: "{app}\care.exe"
Name: "{group}\Uninstall CaRe"; Filename: "{uninstallexe}"
Name: "{commondesktop}\CaRe"; Filename: "{app}\care.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"
