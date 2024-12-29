# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
import os

block_cipher = None

# Collect Streamlit data files
streamlit_data = collect_data_files('streamlit')

added_files = [
    ('circular_channel_calculator.py', '.'),
    ('fix_metadata.py', '.'),
    ('assets', 'assets'),
] + streamlit_data

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'streamlit',
        'streamlit.web.bootstrap',
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.secrets',
        'streamlit.elements',
        'streamlit.elements.image',
        'scipy',
        'scipy.optimize',
        'scipy.special.cython_special',
        'numpy',
        'pandas',
        'altair',
        'matplotlib',
        'plotly',
        'watchdog',
        'tornado',
        'importlib_metadata',
        'streamlit.web.server.server',
        'streamlit.web.server.server_util',
        'streamlit.elements.widgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Circular_Channel_Calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)