# -*- mode: python -*-

block_cipher = None


#a = Analysis(['kotnetcli.py'],
a = Analysis(['../kotnetcli.py'],
             pathex=['/home/gijs/Scripts/kotnetcli/compilation/build'],
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
             runtime_hooks=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='kotnetcli-lin',
          debug=False,
          strip=None,
          upx=True,
          console=True )
