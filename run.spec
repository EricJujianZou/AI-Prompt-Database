# -*- mode: python ; coding: utf-8 -*-

# PyInstaller spec file for PromptAssist
# This file ensures all resources (icons, stylesheets) are properly bundled

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Icons need to be in 'icons/' folder relative to _MEIPASS
        ('src/icons/logo.ico', 'icons'),
        ('src/icons/logo.png', 'icons'),
        # Stylesheet at root level of _MEIPASS
        ('src/style.qss', '.'),
        # DO NOT bundle .env file - security risk!
        # Users should configure via config.json in AppData
    ],
    hiddenimports=[
        'winotify',
        'keyboard',
        'httpx',
        'pydantic',
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'win32api',
        'win32con',
        'win32gui',
        'winsound',
        'dotenv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PromptAssist',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/icons/logo.ico',
)
