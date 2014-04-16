#setup.py
from distutils.core import setup
import py2exe
import glob
import os, sys

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.0.1"
        self.company_name = ""
        self.copyright = "Copyright Andrew K Wilson 2007"
        self.name = "OpenRayTrace"

################################################################
# A program using wx

# The manifest will be inserted as resource into test_wx.exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
#
# Another option would be to store it in a file named
# test_wx.exe.manifest, and copy it with the data_files option into
# the dist-dir.
#
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24
other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="OpenRayTrace"))],

test_wx = Target(
    # used for the versioninfo resource
    description = "OpenRayTrace",

    # what to build
    script = "wxAppRayTrace.py",
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="OpenRayTrace"))],
##    icon_resources = [(1, "icon.ico")],
    dest_base = "OpenRayTrace")

setup(options = {"py2exe":{"compressed": 2,
                           "optimize": 2,
                           "ascii": 1,
                           "packages":["encodings"],
                           "bundle_files":1,
                           }},
      zipfile = None,
      data_files =[("Demo Lenses",glob.glob("Demo Lenses\\*.*")),
                   ],
      console = [test_wx])



