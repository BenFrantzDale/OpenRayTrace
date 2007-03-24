#Boa:MDIParent:wxMainFrame
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
import wxMDIChildFrame_lens_system_ogl
import wxMDIChildFrame_lens_data
import wxMDIChildFrame_ray_data
import wxMDIChildFrame_paraxial_data
import wxMDIChildFrame_spot_diagram
import wxMDIChildFrame_aberrations
import wxMDIChildFrame_image
import wxDialogSaveQuestion
import pickle
from myCanvas import *


TITLE = 'OpenRayTrace:   '

def create(parent):
    return wxMainFrame(parent)

[wxID_WXMAINFRAME] = map(lambda _init_ctrls: wx.NewId(), range(1))

[wxID_WXMAINFRAMEMENUEXIT, wxID_WXMAINFRAMEMENUNEW, wxID_WXMAINFRAMEMENUOPEN, 
 wxID_WXMAINFRAMEMENUSAVE, wxID_WXMAINFRAMEMENUSAVE_AS, 
] = map(lambda _init_coll_menu_Items: wx.NewId(), range(5))

[wxID_WXMAINFRAMEMENU_DRAWINGITEMS_SPOT_DIAGRAM, 
 wxID_WXMAINFRAMEMENU_DRAWINGITEM_RESET_RAY_TRACE, 
] = map(lambda _init_coll_menu_drawing_Items: wx.NewId(), range(2))

[wxID_WXMAINFRAME] = [wx.NewId() for _init_ctrls in range(1)]

[wxID_WXMAINFRAMEMENU_DRAWINGRESETRAYTRACE, 
 wxID_WXMAINFRAMEMENU_DRAWINGSPOTDIAGRAM, 
] = [wx.NewId() for _init_coll_menu_drawing_Items in range(2)]

[wxID_WXMAINFRAMEMENUEXIT, wxID_WXMAINFRAMEMENUNEW, wxID_WXMAINFRAMEMENUOPEN, 
 wxID_WXMAINFRAMEMENUSAVE, wxID_WXMAINFRAMEMENUSAVEAS, 
] = [wx.NewId() for _init_coll_menu_Items in range(5)]

class wxMainFrame(wx.MDIParentFrame):
    def _init_coll_menuBar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.menu, title='File')
        parent.Append(menu=self.menu_drawing, title='Drawing')

    def _init_coll_menu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_WXMAINFRAMEMENUOPEN, kind=wx.ITEM_NORMAL,
              text='Open')
        parent.Append(help='', id=wxID_WXMAINFRAMEMENUNEW, kind=wx.ITEM_NORMAL,
              text='New')
        parent.Append(help='', id=wxID_WXMAINFRAMEMENUSAVE, kind=wx.ITEM_NORMAL,
              text='Save')
        parent.Append(help='', id=wxID_WXMAINFRAMEMENUSAVEAS,
              kind=wx.ITEM_NORMAL, text='Save As')
        parent.Append(help='', id=wxID_WXMAINFRAMEMENUEXIT, kind=wx.ITEM_NORMAL,
              text='Exit')
        self.Bind(wx.EVT_MENU, self.OnMenu, id=wxID_WXMAINFRAMEMENUNEW)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=wxID_WXMAINFRAMEMENUSAVE)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=wxID_WXMAINFRAMEMENUSAVEAS)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=wxID_WXMAINFRAMEMENUEXIT)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=wxID_WXMAINFRAMEMENUOPEN)

    def _init_coll_menu_drawing_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_WXMAINFRAMEMENU_DRAWINGRESETRAYTRACE,
              kind=wx.ITEM_NORMAL, text='Reset Ray Trace View')
        parent.Append(help='', id=wxID_WXMAINFRAMEMENU_DRAWINGSPOTDIAGRAM,
              kind=wx.ITEM_NORMAL, text='Spot Diagram')
        self.Bind(wx.EVT_MENU, self.OnMenu_drawingMenu,
              id=wxID_WXMAINFRAMEMENU_DRAWINGRESETRAYTRACE)
        self.Bind(wx.EVT_MENU, self.OnMenu_drawingMenu,
              id=wxID_WXMAINFRAMEMENU_DRAWINGSPOTDIAGRAM)

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
        wx.MDIParentFrame.__init__(self, id=wxID_WXMAINFRAME,
              name='wxMainFrame', parent=prnt, pos=wx.Point(239, 15),
              size=wx.Size(1200, 854),
              style=wx.SYSTEM_MENU | wx.DEFAULT_FRAME_STYLE | wx.VSCROLL | wx.HSCROLL,
              title='OpenRayTrace')
        self._init_utils()
        self.SetClientSize(wx.Size(1192, 820))
        self.Center(wx.BOTH)
        self.SetAutoLayout(True)
        self.SetMenuBar(self.menuBar)

    def __init__(self, parent):
        self._init_ctrls(parent)                                    
        self.Maximize()
        
        
                
        self.ogl      = wxMDIChildFrame_lens_system_ogl.create(self)      
        self.lens     = wxMDIChildFrame_lens_data.create(self)
        self.trace    = wxMDIChildFrame_ray_data.create(self)
        self.paraxial = wxMDIChildFrame_paraxial_data.create(self)
        self.spot     = wxMDIChildFrame_spot_diagram.create(self)
        
        self.abr      = wxMDIChildFrame_aberrations.create(self)
        self.img      = wxMDIChildFrame_image.create(self)
        
        self.paraxial.Hide()        
        self.spot.Hide()        
        self.img.Hide()        
        self.trace.Hide()        
        
        self.Tile()
        self.Cascade()
        self.Tile()
        self.file_cnt = 0
        self.file_name = 'untitled'+str(self.file_cnt)+'.lns'
        self.SetTitle(TITLE + self.file_name)
        self.saveable = False
        
        showDialog = False
        if(showDialog):
            msg =  'OpenRayTrace, Copyright (C) 2007 Andrew Wilson\nOpenRayTrace comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it under certain conditions (see About menu)'
            dlg = wxMessageDialog(self,msg,
            'GPL Copyright', wxOK | wxICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        
    def OnMenu_drawingMenu(self, event):
        id = event.GetId()
        if(id == wxID_WXMAINFRAMEMENU_DRAWINGRESETRAYTRACE):                        
            self.ogl.reset_view()
        elif(id == wxID_WXMAINFRAMEMENU_DRAWINGSPOTDIAGRAM):
            self.spot.Show()
            
            
        event.Skip()

    def OnMenu(self, event):
        id = event.GetId()
        if(id == wxID_WXMAINFRAMEMENUNEW):    
            sv = wxDialogSaveQuestion.create(self,self.file_name)                    
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
            
            
        elif(id == wxID_WXMAINFRAMEMENUOPEN):
            dlg = wxFileDialog(self, "Open Lens", ".", "", "*.lns", wxOPEN | wxCHANGE_DIR)
            try:
                if dlg.ShowModal() == wxID_OK:
                    self.file_name = dlg.GetPath()
                    self.SetTitle(TITLE + self.file_name)

                    fd = open(self.file_name)      
                    t = pickle.load(fd)
                    fd.close()
                    
                    self.lens.set_data(t)
                    self.saveable = True
            finally:
                dlg.Destroy()
                        
        elif(id == wxID_WXMAINFRAMEMENUSAVE):                        
            self.Save()                        
        elif(id == wxID_WXMAINFRAMEMENUSAVE_AS):
            self.saveable = False
            self.Save()
        elif(id == wxID_WXMAINFRAMEMENUEXIT):
            sv = wxDialogSaveQuestion.create(self,self.file_name)
            sv.Show()                        
        event.Skip()
            
        
    def Save(self):
        if(self.saveable):
                t = self.lens.get_data()
                fd = open(self.file_name,'w')
                a = pickle.dump(t,fd)        
                fd.close()
        else:
            dlg = wxFileDialog(self, "Save Lens", ".", "", "*.lns", wxSAVE | wxOVERWRITE_PROMPT | wxCHANGE_DIR)
            dlg.SetPath(self.file_name)
            try:
                if dlg.ShowModal() == wxID_OK:
                    self.file_name = dlg.GetPath()
                    self.SetTitle(TITLE + self.file_name)
                    t = self.lens.get_data()
                    fd = open(self.file_name,'w')
                    a = pickle.dump(t,fd)        
                    fd.close()
                    self.saveable = True
            finally:
                dlg.Destroy()            

    def New(self):
        self.lens.clear_data()
        self.ogl.clear_list()
        self.spot.clear_list()
        self.img.clear_list()
        self.abr.clear_list()
        self.saveable = False
            
        self.file_cnt += 1
        self.file_name = 'untitled'+str(self.file_cnt)+'.lns'
        self.SetTitle(TITLE + self.file_name)
