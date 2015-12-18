# -*- mode: python -*-

block_cipher = None


a = Analysis(['lekture.py'],
             pathex=['/Users/reno/Documents/GITs/lekture'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='lekture',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon/lekture.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='lekture')
app = BUNDLE(coll,
             name='lekture.app',
             icon='icon/lekture.icns',
             bundle_identifier=None)
