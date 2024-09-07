# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\abelb\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\tkinterdnd2\\tkdnd\\win-x64', 'tkinterdnd2'), ('C:\\Users\\abelb\\Downloads\\trial\\.venv\\Lib\\site-packages\\ifcopenshell\\express\\ifc2x3.exp', 'ifcopenshell\\express'), ('C:\\\\Users\\\\abelb\\\\Downloads\\\\trial\\\\.venv\\\\Lib\\\\site-packages\\\\ifcopenshell\\\\express\\drag.png', 'ifcopenshell/express'), ('C:\\\\Users\\\\abelb\\\\Downloads\\\\trial\\\\.venv\\\\Lib\\\\site-packages\\\\ifcopenshell\\\\express\\dark-light.png', 'ifcopenshell/express')],
    hiddenimports=['matplotlib.backends.backend_pdf', 'ifcopenshell', 'ifcopenshell.express.rules', 'ifcopenshell.express.rules.IFC2X3'],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
