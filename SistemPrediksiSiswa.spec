# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('models', 'models'), ('utils', 'utils'), ('database', 'database'), ('pages', 'pages')],
    hiddenimports=['customtkinter', 'PIL', 'PIL.Image', 'pandas', 'openpyxl', 'sklearn', 'joblib', 'sklearn.ensemble', 'sklearn.tree', 'sklearn.linear_model', 'sklearn.preprocessing', 'sklearn.model_selection', 'matplotlib', 'matplotlib.backends.backend_tkagg', 'reportlab', 'reportlab.lib', 'reportlab.platypus'],
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
    name='SistemPrediksiSiswa',
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
