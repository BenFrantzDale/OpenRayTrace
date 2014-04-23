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





import wx

from OpenRayTrace.UI import MainFrame

class OpenRayTraceApp(wx.App):
    def OnInit(self):
        import sys
        self.main = MainFrame.MainFrame(None, sys.argv)
        self.main.Show()
        return True

def main():
    application = OpenRayTraceApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
