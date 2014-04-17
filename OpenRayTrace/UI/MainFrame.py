#Boa:MDIParent:MainFrame
##    OpenRayTrace: Free optical design software
##    Copyright (C) 2004 Andrew Wilson
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
from OpenRayTrace.UI import frames
#from OpenRayTrace.UI.frames import lens_system_ogl
#from OpenRayTrace.UI.frames import lens_data
#from OpenRayTrace.UI.frames import ray_data
#from OpenRayTrace.UI.frames import paraxial_data
#from OpenRayTrace.UI.frames import spot_diagram
#from OpenRayTrace.UI.frames import aberrations
#from OpenRayTrace.UI.frames import image
from OpenRayTrace.UI import DialogSaveQuestion
import pickle
from OpenRayTrace.UI.myCanvas import *


TITLE = 'OpenRayTrace:   '


class MainFrame(wx.MDIParentFrame):
    wxID = wx.NewId()

    [wxID_MENUEXIT, wxID_MENUNEW, 
     wxID_MENUSAVE, wxID_MENUSAVE_AS, 
    ] = map(lambda _init_coll_menu_Items: wx.NewId(), range(4))

    [wxID_MENU_DRAWINGITEMS_SPOT_DIAGRAM, 
     wxID_MENU_DRAWINGITEM_RESET_RAY_TRACE, 
    ] = map(lambda _init_coll_menu_drawing_Items: wx.NewId(), range(2))

    [wxID_] = [wx.NewId() for _init_ctrls in range(1)]

    [wxID_MENU_DRAWINGRESETRAYTRACE, 
     wxID_MENU_DRAWINGSPOTDIAGRAM, 
    ] = [wx.NewId() for _init_coll_menu_drawing_Items in range(2)]

    [wxID_MENUEXIT, wxID_MENUNEW, wxID_MENUOPEN, 
     wxID_MENUSAVE, wxID_MENUSAVEAS, 
    ] = [wx.NewId() for _init_coll_menu_Items in range(5)]

    def _init_coll_menuBar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menu, title='File')
        parent.Append(menu=self.menu_drawing, title='Drawing')

    def _init_coll_menu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wx.ID_OPEN, kind=wx.ITEM_NORMAL,
              text='&Open')
        parent.Append(help='', id=wx.ID_NEW, kind=wx.ITEM_NORMAL,
              text='New')
        parent.Append(help='', id=self.wxID_MENUSAVE, kind=wx.ITEM_NORMAL,
              text='Save')
        parent.Append(help='', id=self.wxID_MENUSAVEAS,
              kind=wx.ITEM_NORMAL, text='Save As')
        parent.Append(help='', id=self.wxID_MENUEXIT, kind=wx.ITEM_NORMAL,
              text='Exit')
        self.Bind(wx.EVT_MENU, self.OnMenuNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnMenuSave, id=self.wxID_MENUSAVE)
        self.Bind(wx.EVT_MENU, self.OnMenuSaveAs, id=self.wxID_MENUSAVEAS)
        self.Bind(wx.EVT_MENU, self.OnMenuExit, id=self.wxID_MENUEXIT)
        self.Bind(wx.EVT_MENU, self.OnMenuOpen, id=wx.ID_OPEN)

    def _init_coll_menu_drawing_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=self.wxID_MENU_DRAWINGRESETRAYTRACE,
              kind=wx.ITEM_NORMAL, text='Reset Ray Trace View')
        parent.Append(help='', id=self.wxID_MENU_DRAWINGSPOTDIAGRAM,
              kind=wx.ITEM_NORMAL, text='Spot Diagram')
        self.Bind(wx.EVT_MENU, self.OnMenu_drawingMenu,
              id=self.wxID_MENU_DRAWINGRESETRAYTRACE)
        self.Bind(wx.EVT_MENU, self.OnMenu_drawingMenu,
              id=self.wxID_MENU_DRAWINGSPOTDIAGRAM)

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar = wx.MenuBar()

        self.menu = wx.Menu(title='')

        self.menu_drawing = wx.Menu(title='')

        self._init_coll_menuBar_Menus(self.menuBar)
        self._init_coll_menu_Items(self.menu)
        self._init_coll_menu_drawing_Items(self.menu_drawing)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIParentFrame.__init__(self, id=MainFrame.wxID,
              name='MainFrame', parent=prnt, pos=wx.Point(239, 15),
              size=wx.Size(1200, 854),
              style=wx.SYSTEM_MENU | wx.DEFAULT_FRAME_STYLE | wx.VSCROLL | wx.HSCROLL,
              title='OpenRayTrace')
        self._init_utils()
        self.SetClientSize(wx.Size(1192, 820))
        self.Center(wx.BOTH)
        self.SetAutoLayout(True)
        self.SetMenuBar(self.menuBar)

    def __init__(self, parent, argv=()):
        self._init_ctrls(parent)                                    
        #self.Maximize()
        
        self.ogl      = frames.LensSystemOGL.LensSystemOGL(self)      
        self.lens     = frames.LensData.LensData(self)
        self.trace    = frames.RayData.RayData(self)
        self.paraxial = frames.ParaxialData.ParaxialData(self)
        self.spot     = frames.SpotDiagram.SpotDiagram(self)
        
        self.abr      = frames.Aberrations.Aberrations(self)
        self.img      = frames.Image.Image(self)
        
        if False:
            self.paraxial.Hide()        
            self.spot.Hide()        
            self.img.Hide()        
            self.trace.Hide()        
        else:
            for frame in [self.ogl, self.lens]: #, self.trace, self.paraxial, self.spot, self.img]:
                frame.Show()
            for frame in [self.abr, self.trace, self.paraxial, self.spot, self.img]:
                frame.Hide()

        self.Tile()
        self.Cascade()
        self.Tile()
        self.file_cnt = 0
        self.file_name = 'untitled'+str(self.file_cnt)+'.lns'
        self.SetTitle(TITLE + self.file_name)
        self.saveable = False
        
        showDialog = True
        if showDialog:
            msg =  'OpenRayTrace, Copyright (C) 2007 Andrew Wilson\nOpenRayTrace comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it under certain conditions (see About menu)'
            self.dlg = wx.MessageDialog(self, msg, 'GPL Copyright', wx.OK | wx.ICON_INFORMATION)
            self.dlg.ShowModal()
            #dlg.Destroy()
        if len(argv) > 1:
            assert len(argv) == 2, "Up to one filename handled."
            if argv[1].lower().endswith('.zmx'):
                from OpenRayTrace.DataModel import System
                self.file_name = argv[1]
                self.lens.setSystem(System.loadZMX(self.file_name))
            else:
                raise TypeError("Unrecognized argument: {}".format(argv[1]))
        
    def OnMenu_drawingMenu(self, event):
        id = event.GetId()
        if id == self.wxID_MENU_DRAWINGRESETRAYTRACE:
            self.ogl.reset_view()
        elif id == self.wxID_MENU_DRAWINGSPOTDIAGRAM:
            self.spot.Show()
            
        event.Skip()

    def OnMenuOpen(self, event):
        dlg = wx.FileDialog(self, "Open Lens", ".", "", "Lens file (*.lns)|*.lns|ZEMAX file (*.zmx)|*.zmx", wx.OPEN | wx.CHANGE_DIR)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.file_name = dlg.GetPath()
                self.SetTitle(TITLE + self.file_name)

                import os
                ext = os.path.splitext(self.file_name)[1].lower()
                if ext == '.lns':
                    with open(self.file_name) as fd:
                        t = pickle.load(fd)
                    self.lens.set_data(t)
                elif ext == '.zmx':
                    from OpenRayTrace.DataModel import System
                    self.lens.setSystem(System.loadZMX(self.file_name))
                self.saveable = True
        finally:
            dlg.Destroy()

    def OnMenuSave(self, event):
        self.Save()         
    def OnMenuSaveAs(self, event):
        self.saveable = False
        self.Save()
    def OnMenuExit(self, event):
        sv = DialogSaveQuestion.DialogSaveQuestion(self,self.file_name)
        sv.Show()                        
    def OnMenuNew(self, event):
        sv = DialogSaveQuestion.DialogSaveQuestion(self, self.file_name)                    
        res = sv.ShowModal()
        try:                
            if res == 0:     #yes
                self.Save()
                self.New()
            elif res == 1:   #no
                self.New()
            elif res == 2:   #cancel
                pass
        finally:
            sv.Destroy()
            
        
    def Save(self):
        if self.saveable:
            t = self.lens.get_data()
            with open(self.file_name,'w') as fd:
                a = pickle.dump(t, fd)
        else:
            dlg = wx.FileDialog(self, "Save Lens", ".", "", "*.lns", 
                                wx.SAVE | wx.OVERWRITE_PROMPT | wx.CHANGE_DIR)
            dlg.SetPath(self.file_name)
            try:
                if dlg.ShowModal() == wx.ID_OK:
                    self.file_name = dlg.GetPath()
                    self.SetTitle(TITLE + self.file_name)
                    t = self.lens.get_data()
                    with open(self.file_name,'w') as fd:
                        a = pickle.dump(t, fd)
                    self.saveable = True
            finally:
                dlg.Destroy()            

    def New(self):
        self.lens.clear_data()
        self.ogl.clear_list()
        self.spot.clear_list()
        self.img.clear_list()
        #self.abr.clear_list()
        self.saveable = False
            
        self.file_cnt += 1
        self.file_name = 'untitled'+str(self.file_cnt)+'.lns'
        self.SetTitle(TITLE + self.file_name)
