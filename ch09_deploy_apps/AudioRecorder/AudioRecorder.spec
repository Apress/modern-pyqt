# -*- mode: python -*-

block_cipher = None


a = Analysis(['audio_recorder.py'],
             # Be sure to set the path name
             pathex=['/path/to/AudioRecorder'],
             binaries=[],
             # Use datas to specify resources not in .qrc
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          # Set the name of the executable
          name='AudioRecorder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          # Hide the console by setting its value to False
          # Set the icon for the executable
          console=False , icon='resources/icons/mic_icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='AudioRecorder')
app = BUNDLE(coll,
             # Set the name of the app
             name='AudioRecorder.app',
             # Set the icon for the app
             icon='resources/icons/mic_icon.icns',
             bundle_identifier=None)
