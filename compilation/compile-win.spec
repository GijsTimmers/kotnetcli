# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\kotnetcli.py'],
             pathex=['/home/gijs/Scripts/kotnetcli/build'],
             hiddenimports = ['keyring.backends.file',
                 'keyring.backends.Gnome',
                 'keyring.backends.Google',
                 'keyring.backends.keyczar',
                 'keyring.backends.kwallet',
                 'keyring.backends.multi',
                 'keyring.backends.OS_X',
                 'keyring.backends.pyfs',
                 'keyring.backends.SecretService',
                 'keyring.backends.Windows'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='kotnetcli-win.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
