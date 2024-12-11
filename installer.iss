; NBSCleaning_Tool Installer Script

[Setup]
AppName=NBSCleaning_Tool
AppVersion=1.2
DefaultDirName={pf}\NBSCleaning_Tool
DefaultGroupName=NBSCleaning_Tool
OutputBaseFilename=NBSCleaning_Tool_Installer
SetupIconFile=icons\logo.ico
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
LicenseFile=license.txt
SetupLogging=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop Icon"; GroupDescription: "Additional Icons"; Flags: checkedonce

[Files]
; Main executable and dependencies
Source: "build\exe.win-amd64-3.9\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\exe.win-amd64-3.9\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
; License file
Source: "license.txt"; DestDir: "{app}"
; Include the icons directory
Source: "icons\*"; DestDir: "{app}\icons"; Flags: recursesubdirs createallsubdirs

[Icons]
; Shortcut to the main application
Name: "{group}\NBSCleaning_Tool"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall NBSCleaning_Tool"; Filename: "{uninstallexe}"
Name: "{commondesktop}\NBSCleaning_Tool"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
; Run the program after installation
Filename: "{app}\main.exe"; Description: "Launch NBSCleaning_Tool"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    WizardForm.FinishedLabel.Caption := 'The installation of NBSCleaning_Tool is complete.';
  end;
end;
