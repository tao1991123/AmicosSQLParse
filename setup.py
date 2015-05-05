from distutils.core import setup
import py2exe
import sys,os
  
if sys.version_info.major >= 3.0:
    opt_bundle_files = 2
else:
    opt_bundle_files = 1
	
includes = ["platform","cmd","code","pdb"]
options = {"py2exe":
         { "compressed": 1,
            "optimize": 2,
            "includes": includes,
            "bundle_files": opt_bundle_files,
         }
      }
setup(
    version = "1.0.0",
    description = "Amicos SQL Parse",
    options = options,
    zipfile=None,
    #console=[{"script": "mainGUI.py", "icon_resources": [(1, "py.ico")] }],
    windows=[{"script": "mainGUI.py", "icon_resources": [(1, "sql.ico")] }],
)