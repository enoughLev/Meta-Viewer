# -*- mode: python ; coding: utf-8 -*-

import glob
import os

block_cipher = None

# Сбор всех картинок из папки img/
image_files = [(f, 'img') for f in glob.glob('img\*')]
var_files = [(f, 'var') for f in glob.glob('var\*')]
# Добавление отдельного файла базы данных
datas = [
    ('Database\MetaViewerDB.db', 'Database'),
] + image_files + var_files

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    cipher=block_cipher,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='MetaViewer',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    #console=True,
    disable_windowed_traceback=False,
    bootloader_ignore_signals=False,
    runtime_tmpdir=None,
    target_arch=None,
)
