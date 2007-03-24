#!/usr/bin/env python
#Boa:App:BoaApp

##    Copyright 2004, 2004 Andrew Wilson andrewwilson@alum.mit.edu
##
##    This file is part of OpenRayTrace.

##

##    OpenRayTrace is free software; you can redistribute it and/or modify

##    it under the terms of the GNU General Public License as published by

##    the Free Software Foundation; either version 2 of the License, or

##    (at your option) any later version.

##

##    OpenRayTrace is distributed in the hope that it will be useful,

##    but WITHOUT ANY WARRANTY; without even the implied warranty of

##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the

##    GNU General Public License for more details.

##

##    You should have received a copy of the GNU General Public License

##    along with OpenRayTrace; if not, write to the Free Software

##    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA





from wxPython.wx import *

#import wxFrameRayTrace
import wxMainFrame

modules ={'myCanvas': [0, '', 'myCanvas.py'],
 'myGLCanvas': [0, '', 'myGLCanvas.py'],
 'ray_trace': [0, '', 'ray_trace.py'],
 'wxDialogSaveQuestion': [0, '', 'wxDialogSaveQuestion.py'],
 'wxMDIChildFrame_aberrations': [0, '', 'wxMDIChildFrame_aberrations.py'],
 'wxMDIChildFrame_image': [0, '', 'wxMDIChildFrame_image.py'],
 'wxMDIChildFrame_lens_data': [0, '', 'wxMDIChildFrame_lens_data.py'],
 'wxMDIChildFrame_lens_system_ogl': [0,
                                     '',
                                     'wxMDIChildFrame_lens_system_ogl.py'],
 'wxMDIChildFrame_paraxial_data': [0, '', 'wxMDIChildFrame_paraxial_data.py'],
 'wxMDIChildFrame_ray_data': [0, '', 'wxMDIChildFrame_ray_data.py'],
 'wxMDIChildFrame_spot_diagram': [0, '', 'wxMDIChildFrame_spot_diagram.py'],
 'wxMainFrame': [0, '', 'wxMainFrame.py']}

class BoaApp(wxApp):
    def OnInit(self):
        wxInitAllImageHandlers()
        
        self.main = wxMainFrame.create(None)
        
        #self.main = wxFrameRayTrace.create(None)
        # needed when running from Boa under Windows 9X
        self.SetTopWindow(self.main)
        self.main.Show();self.main.Hide();self.main.Show()
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
