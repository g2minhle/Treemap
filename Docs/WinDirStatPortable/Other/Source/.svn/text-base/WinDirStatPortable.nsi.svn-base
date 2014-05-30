;Copyright (C) 2004-2010 John T. Haller of PortableApps.com

;Website: http://portableapps.com/WinDirStatPortable

;This software is OSI Certified Open Source Software.
;OSI Certified is a certification mark of the Open Source Initiative.

;This program is free software; you can redistribute it and/or
;modify it under the terms of the GNU General Public License
;as published by the Free Software Foundation; either version 2
;of the License, or (at your option) any later version.

;This program is distributed in the hope that it will be useful,
;but WITHOUT ANY WARRANTY; without even the implied warranty of
;MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;GNU General Public License for more details.

;You should have received a copy of the GNU General Public License
;along with this program; if not, write to the Free Software
;Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

!define NAME "WinDirStatPortable"
!define PORTABLEAPPNAME "WinDirStat Portable"
!define APPNAME "WinDirStat"
!define VER "1.6.0.0"
!define WEBSITE "PortableApps.com/WinDirStatPortable"
!define DEFAULTEXE "WinDirStat.exe"
!define DEFAULTAPPDIR "WinDirStat"
!define DEFAULTSETTINGSDIR "settings"
!define LAUNCHERLANGUAGE "English"

;=== Program Details
Name "${PORTABLEAPPNAME}"
OutFile "..\..\${NAME}.exe"
Caption "${PORTABLEAPPNAME} | PortableApps.com"
VIProductVersion "${VER}"
VIAddVersionKey ProductName "${PORTABLEAPPNAME}"
VIAddVersionKey Comments "Allows ${APPNAME} to be run from a removable drive.  For additional details, visit ${WEBSITE}"
VIAddVersionKey CompanyName "PortableApps.com"
VIAddVersionKey LegalCopyright "John T. Haller"
VIAddVersionKey FileDescription "${PORTABLEAPPNAME}"
VIAddVersionKey FileVersion "${VER}"
VIAddVersionKey ProductVersion "${VER}"
VIAddVersionKey InternalName "${PORTABLEAPPNAME}"
VIAddVersionKey LegalTrademarks "PortableApps.com is a Trademark of Rare Ideas, LLC."
VIAddVersionKey OriginalFilename "${NAME}.exe"
;VIAddVersionKey PrivateBuild ""
;VIAddVersionKey SpecialBuild ""

;=== Runtime Switches
CRCCheck On
WindowIcon Off
SilentInstall Silent
AutoCloseWindow True
RequestExecutionLevel user
XPStyle on

; Best Compression
SetCompress Auto
SetCompressor /SOLID lzma
SetCompressorDictSize 32
SetDatablockOptimize On

;=== Include
;(Standard NSIS)
!include FileFunc.nsh
!insertmacro GetParameters ;Requires NSIS 2.40 or better
!include Registry.nsh

;(Custom)
!include ReadINIStrWithDefault.nsh
!include GetWindowsVersion.nsh

;=== Program Icon
Icon "..\..\App\AppInfo\appicon.ico"

;=== Languages
LoadLanguageFile "${NSISDIR}\Contrib\Language files\${LAUNCHERLANGUAGE}.nlf"
!include PortableApps.comLauncherLANG_${LAUNCHERLANGUAGE}.nsh

Var PROGRAMDIRECTORY
Var SETTINGSDIRECTORY
Var ADDITIONALPARAMETERS
Var EXECSTRING
Var SECONDARYLAUNCH
Var DISABLESPLASHSCREEN
Var FAILEDTORESTOREKEY
Var WINDOWSVERSION
Var MISSINGFILEORPATH
Var APPLANGUAGE


Section "Main"
	;=== Check if already running
	System::Call 'kernel32::CreateMutexA(i 0, i 0, t "${NAME}") i .r1 ?e'
	Pop $0
	StrCmp $0 0 CheckINI
		StrCpy $SECONDARYLAUNCH "true"

	CheckINI:
		${ReadINIStrWithDefault} $ADDITIONALPARAMETERS "$EXEDIR\${NAME}.ini" "${NAME}" "AdditionalParameters" ""
		${ReadINIStrWithDefault} $DISABLESPLASHSCREEN "$EXEDIR\${NAME}.ini" "${NAME}" "DisableSplashScreen" "false"
		StrCpy $PROGRAMDIRECTORY "$EXEDIR\App\${DEFAULTAPPDIR}"
		StrCpy $SETTINGSDIRECTORY "$EXEDIR\Data\${DEFAULTSETTINGSDIR}"

		IfFileExists "$PROGRAMDIRECTORY\${DEFAULTEXE}" FoundProgramEXE

	;NoProgramEXE:
		;=== Program executable not where expected
		StrCpy $MISSINGFILEORPATH ${DEFAULTEXE}
		MessageBox MB_OK|MB_ICONEXCLAMATION `$(LauncherFileNotFound)`
		Abort
		
	FoundProgramEXE:
		;=== Check if running
		StrCmp $SECONDARYLAUNCH "true" GetPassedParameters
		FindProcDLL::FindProc "WinDirStat.exe"
		StrCmp $R0 "1" WarnAnotherInstance
		FindProcDLL::FindProc "WinDirStatA.exe"
		StrCmp $R0 "1" WarnAnotherInstance DisplaySplash

	WarnAnotherInstance:
		MessageBox MB_OK|MB_ICONEXCLAMATION `$(LauncherAlreadyRunning)`
		Abort
	
	DisplaySplash:
		StrCmp $DISABLESPLASHSCREEN "true" CheckWindowsVersion
			;=== Show the splash screen while processing registry entries
			InitPluginsDir
			File /oname=$PLUGINSDIR\splash.jpg "${NAME}.jpg"
			newadvsplash::show /NOUNLOAD 1200 0 0 -1 /L $PLUGINSDIR\splash.jpg
	
	CheckWindowsVersion:
		Call GetWindowsVersion
		Pop $WINDOWSVERSION
		StrCpy $WINDOWSVERSION $WINDOWSVERSION 2
		StrCmp $WINDOWSVERSION '95' UseANSIEXE
		StrCmp $WINDOWSVERSION '98' UseANSIEXE
		StrCmp $WINDOWSVERSION 'ME' UseANSIEXE

	;UseUnicodeEXE:
		StrCpy $EXECSTRING `"$PROGRAMDIRECTORY\WinDirStat.exe"`
		Goto GetPassedParameters
	
	UseANSIEXE:
		StrCpy $EXECSTRING `"$PROGRAMDIRECTORY\WinDirStatA.exe"`
		
	GetPassedParameters:
		;=== Get any passed parameters
		${GetParameters} $0
		StrCmp "'$0'" "''" AdditionalParameters
			StrCpy $EXECSTRING `$EXECSTRING $0`

	AdditionalParameters:
		StrCmp $ADDITIONALPARAMETERS "" SettingsDirectory

		;=== Additional Parameters
		StrCpy $EXECSTRING `$EXECSTRING $ADDITIONALPARAMETERS`
	
	SettingsDirectory:
		;=== Set the settings directory if we have a path
		IfFileExists "$SETTINGSDIRECTORY\WinDirStat.reg" RegistryBackup
			CreateDirectory $SETTINGSDIRECTORY
			CopyFiles /SILENT "$EXEDIR\App\DefaultData\settings\WinDirStat.reg" $SETTINGSDIRECTORY
	
	RegistryBackup:
		StrCmp $SECONDARYLAUNCH "true" LaunchAndExit
		;=== Backup the registry
		${registry::KeyExists} "HKEY_CURRENT_USER\Software\Seifert-BackupByWinDirStatPortable" $R0
		StrCmp $R0 "0" RestoreSettings
		${registry::KeyExists} "HKEY_CURRENT_USER\Software\Seifert" $R0
		StrCmp $R0 "-1" RestoreSettings
		${registry::MoveKey} "HKEY_CURRENT_USER\Software\Seifert" "HKEY_CURRENT_USER\Software\Seifert-BackupByWinDirStatPortable" $R0
		Sleep 100

	RestoreSettings:
		IfFileExists "$SETTINGSDIRECTORY\WinDirStat.reg" "" GetAppLanguage

	;RestoreTheKey:
		IfFileExists "$WINDIR\system32\reg.exe" "" RestoreTheKey9x
			nsExec::ExecToStack `"$WINDIR\system32\reg.exe" import "$SETTINGSDIRECTORY\WinDirStat.reg"`
			Pop $R0
			StrCmp $R0 '0' GetAppLanguage ;successfully restored key
	RestoreTheKey9x:
		${registry::RestoreKey} "$SETTINGSDIRECTORY\WinDirStat.reg" $R0
		StrCmp $R0 '0' GetAppLanguage ;successfully restored key
		StrCpy $FAILEDTORESTOREKEY "true"
	
	GetAppLanguage:
		ReadEnvStr $APPLANGUAGE "PortableApps.comLocaleID"
		StrCmp $APPLANGUAGE "" LaunchNow ;if not set, move on
		StrCmp $APPLANGUAGE 1033 SetAppLanguage
		StrCmp $APPLANGUAGE 1029 SetAppLanguage
		StrCmp $APPLANGUAGE 1043 SetAppLanguage
		StrCmp $APPLANGUAGE 1061 SetAppLanguage
		StrCmp $APPLANGUAGE 1035 SetAppLanguage
		StrCmp $APPLANGUAGE 1036 SetAppLanguage
		StrCmp $APPLANGUAGE 1031 SetAppLanguage
		StrCmp $APPLANGUAGE 1038 SetAppLanguage
		StrCmp $APPLANGUAGE 1040 SetAppLanguage
		StrCmp $APPLANGUAGE 1045 SetAppLanguage
		StrCmp $APPLANGUAGE 1049 SetAppLanguage
		StrCmp $APPLANGUAGE 1034 SetAppLanguage
		Goto LaunchNow ;Language not available, just run
	
	SetAppLanguage:
		${registry::Write} "HKEY_CURRENT_USER\Software\Seifert\WinDirStat\options" "language" $APPLANGUAGE "REG_DWORD" $R0
	
	LaunchNow:
		Sleep 100
		;=== Set install location
		${registry::Write} "HKEY_CURRENT_USER\Software\Seifert\WinDirStat" "InstDir" "$PROGRAMDIRECTORY" "REG_SZ" $R0
		Sleep 100
		ExecWait $EXECSTRING
		
	CheckRunning:
		Sleep 1000
		FindProcDLL::FindProc "WinDirStat.exe"                  
		StrCmp $R0 "1" CheckRunning
		FindProcDLL::FindProc "WinDirStatA.exe"                  
		StrCmp $R0 "1" CheckRunning
	
	;DoneRunning:
		StrCmp $FAILEDTORESTOREKEY "true" SetOriginalKeyBack
		${registry::SaveKey} "HKEY_CURRENT_USER\Software\Seifert\WinDirStat" "$SETTINGSDIRECTORY\WinDirStat.reg" "" $0
		Sleep 100
	
	SetOriginalKeyBack:
		${registry::DeleteKey} "HKEY_CURRENT_USER\Software\Seifert" $R0
		Sleep 100
		${registry::KeyExists} "HKEY_CURRENT_USER\Software\Seifert-BackupByWinDirStatPortable" $R0
		StrCmp $R0 "-1" TheEnd
		${registry::MoveKey} "HKEY_CURRENT_USER\Software\Seifert-BackupByWinDirStatPortable" "HKEY_CURRENT_USER\Software\Seifert" $R0
		Sleep 100
		Goto TheEnd
		
	LaunchAndExit:
		Exec $EXECSTRING
		
	TheEnd:
		${registry::Unload}
		newadvsplash::stop /WAIT
SectionEnd