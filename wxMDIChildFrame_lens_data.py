from __future__ import division
#Boa:MDIChild:wxMDIChildFrame_lens_data
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
import wx.grid
from wx.grid import *
import wxDialog_wavelengths

from myCanvas import *
import os, string
from cmath import *
import math
import numpy as np
from ray_trace import *
from numpy.linalg import norm
from OpenRayTrace import DataModel


WIDTH=640.0
HEIGHT=480.0

FLENGTH = 0
POWER = 1
CURVATURE = 2
RADIUS = 3
THICKNESS = 4
APERATURE_RADIUS = 5
GLASS = 6
BENDING = 7
BENT_C  = 8
BENT_R  = 9

def create(parent):
    return wxMDIChildFrame_lens_data(parent)

[wxID_WXMDICHILDFRAME_LENS_DATA, 
 wxID_WXMDICHILDFRAME_LENS_DATABUTTON_COMPUTE_ALL, 
 wxID_WXMDICHILDFRAME_LENS_DATABUTTON_IMAGE, 
 wxID_WXMDICHILDFRAME_LENS_DATABUTTON_SPOT_DIAGRAMS, 
 wxID_WXMDICHILDFRAME_LENS_DATABUTTON_WAVE_LENGTHS, 
 wxID_WXMDICHILDFRAME_LENS_DATACHECKBOX_AUTOFOCUS, 
 wxID_WXMDICHILDFRAME_LENS_DATAGRID1, 
 wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_POWER, 
 wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_RADIUS, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICBOX1, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT1, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_EFL, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_MAG, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_MG, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_OBJ_HEIGHT, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_PARAXIAL_FOCUS, 
 wxID_WXMDICHILDFRAME_LENS_DATATEXTCTRL_OBJECT_HEIGHT, 
] = map(lambda _init_ctrls: wx.NewId(), range(17))



[wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_BK7, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_DIRECT, 
] = map(lambda _init_coll_menu_glass_Items: wx.NewId(), range(2))

[wxID_WXMDICHILDFRAME_LENS_DATAMENU1COPY, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU1DELETE, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_AFTER, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_BEFORE, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU1PASTE, 
] = map(lambda _init_coll_row_menu_Items: wx.NewId(), range(5))

[wxID_WXMDICHILDFRAME_LENS_DATAMENU_THICKNESSITEMS0] = map(lambda _init_coll_menu_thickness_Items: wx.NewId(), range(1))

[wxID_WXMDICHILDFRAME_LENS_DATA, 
 wxID_WXMDICHILDFRAME_LENS_DATABUTTON_COMPUTE_ALL, 
 wxID_WXMDICHILDFRAME_LENS_DATABUTTON_IMAGE, 
 wxID_WXMDICHILDFRAME_LENS_DATABUTTON_SPOT_DIAGRAMS, 
 wxID_WXMDICHILDFRAME_LENS_DATABUTTON_WAVE_LENGTHS, 
 wxID_WXMDICHILDFRAME_LENS_DATACHECKBOX_AUTOFOCUS, 
 wxID_WXMDICHILDFRAME_LENS_DATAGRID1, 
 wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_POWER, 
 wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_RADIUS, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICBOX1, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXTEFFECTIVEFOCALLENGTH, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_EFL, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_MAG, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_MG, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_OBJ_HEIGHT, 
 wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_PARAXIAL_FOCUS, 
 wxID_WXMDICHILDFRAME_LENS_DATATEXTCTRL_OBJECT_HEIGHT, 
] = [wx.NewId() for _init_ctrls in range(17)]


class wxMDIChildFrame_lens_data(wx.MDIChildFrame):
    col_labels = ('f-length','power','curvature','radius','thickness','aperature radius','glass','bending','bent c','bent r')
    MENU_GLASSBK7 = wx.NewId()
    MENU_GLASSDIRECT = wx.NewId()
    MENU_THICKNESSPARAXIALFOCUS = wx.NewId()

    [DATAROW_MENUCOPY, 
     DATAROW_MENUDELETE, 
     DATAROW_MENUINSERTAFTER, 
     DATAROW_MENUINSERTBEFORE, 
     DATAROW_MENUPASTE] = [wx.NewId() for _ in range(5)]
    @staticmethod
    def surfToRowData(surf):
        """Given a DataModel.Surface, return the row of values as a dictionary."""
        getter = {'f-length': lambda s: None,
                  'power': lambda s: None,
                  'curvature': lambda s: 1/s.R if hasattr(s, 'R') else 0.0,
                  'radius': lambda s: s.R if hasattr(s, 'R') else np.inf,
                  'thickness': lambda s: s.thickness,
                  'aperature radius': lambda s: s.semidiam,
                  'glass': lambda s: s.n(None),
                  'bending': lambda s: None,
                  'bent c': lambda s: None,
                  'bent r': lambda s: None}
        return dict((label, getter[label](surf)) for label in wxMDIChildFrame_lens_data.col_labels)
            
    def _init_coll_boxSizerBottom_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.grid1, 1, border=0, flag=0)

    def _init_coll_staticBoxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.gridBagSizerComputations, 0, border=0, flag=0)

    def _init_coll_flexGridSizerLensDataMain_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.boxSizertop, 0, border=0, flag=0)
        parent.AddSizer(self.boxSizerBottom, 0, border=0, flag=0)

    def _init_coll_flexGridSizerLensDataMain_Growables(self, parent):
        # generated method, don't edit

        parent.AddGrowableRow(1)
        parent.AddGrowableCol(0)

    def _init_coll_gridBagSizerTop_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.radioButton_const_power, (0, 0), border=0, flag=0,
              span=(1, 1))
        parent.AddWindow(self.radioButton_const_radius, (1, 0), border=0,
              flag=0, span=(1, 1))
        parent.AddWindow(self.checkBox_autofocus, (2, 0), border=0, flag=0,
              span=(1, 1))
        parent.AddWindow(self.staticText_obj_height, (0, 1), border=0, flag=0,
              span=(1, 1))
        parent.AddWindow(self.textCtrl_object_height, (1, 1), border=0, flag=0,
              span=(1, 1))
        parent.AddWindow(self.button_wave_lengths, (2, 1), border=0, flag=0,
              span=(1, 1))
        parent.AddSizer(self.staticBoxSizer1, (0, 2), border=0, flag=0, span=(3,
              1))
        parent.AddWindow(self.staticText_efl, (2, 8), border=0, flag=0, span=(1,
              1))
        parent.AddWindow(self.staticText_mg, (1, 7), border=0, flag=0, span=(1,
              1))
        parent.AddWindow(self.staticText_mag, (1, 8), border=0, flag=0, span=(1,
              1))
        parent.AddWindow(self.staticTextEffectiveFocalLength, (2, 7), border=0,
              flag=0, span=(1, 1))
        parent.AddWindow(self.staticText_paraxial_focus, (3, 7), border=0,
              flag=0, span=(1, 1))

    def _init_coll_boxSizertop_Items(self, parent):
        # generated method, don't edit

        parent.AddSizer(self.gridBagSizerTop, 0, border=0, flag=0)

    def _init_coll_gridBagSizerComputations_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button_spot_diagrams, (0, 0), border=0, flag=0,
              span=(1, 1))
        parent.AddWindow(self.button_image, (1, 0), border=0, flag=0, span=(1,
              1))
        parent.AddWindow(self.button_compute_all, (0, 1), border=0, flag=0,
              span=(1, 1))

    def _init_coll_row_menu_Items(self, parent):
        for ID, text in [(self.DATAROW_MENUINSERTBEFORE, 'Insert Before'),
                         (self.DATAROW_MENUINSERTAFTER,  'Insert After'),
                         (self.DATAROW_MENUDELETE,       'Delete'),
                         (self.DATAROW_MENUCOPY,         'Copy'),
                         (self.DATAROW_MENUPASTE,        'Paste')]:
            parent.Append(id=ID, text=text, kind=wx.ITEM_NORMAL, help='')
            self.Bind(id=ID, event=wx.EVT_MENU, handler=self.OnRow_menuitems0Menu)

    def _init_coll_menu_glass_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
                      id=self.MENU_GLASSDIRECT,
                      kind=wx.ITEM_NORMAL, text='Direct')
        parent.Append(help='', id=self.MENU_GLASSBK7,
                      kind=wx.ITEM_NORMAL, text='BK7')
        self.Bind(wx.EVT_MENU, self.OnMenu_glassitems0Menu,
                  id=self.MENU_GLASSDIRECT)
        self.Bind(wx.EVT_MENU, self.OnMenu_glassitems0Menu,
                  id=self.MENU_GLASSBK7)

    def _init_coll_menu_thickness_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='',
              id=self.MENU_THICKNESSPARAXIALFOCUS,
              kind=wx.ITEM_NORMAL, text='Paraxial Focus')
        self.Bind(wx.EVT_MENU, self.OnMenu_thicknessitems0Menu,
              id=self.MENU_THICKNESSPARAXIALFOCUS)

    def _init_sizers(self):
        # generated method, don't edit
        self.flexGridSizerLensDataMain = wx.FlexGridSizer(cols=0, hgap=0,
              rows=2, vgap=0)

        self.boxSizertop = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizerBottom = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.gridBagSizerTop = wx.GridBagSizer(hgap=0, vgap=0)

        self.staticBoxSizer1 = wx.StaticBoxSizer(box=self.staticBox1,
              orient=wx.VERTICAL)

        self.gridBagSizerComputations = wx.GridBagSizer(hgap=0, vgap=0)

        self._init_coll_flexGridSizerLensDataMain_Items(self.flexGridSizerLensDataMain)
        self._init_coll_flexGridSizerLensDataMain_Growables(self.flexGridSizerLensDataMain)
        self._init_coll_boxSizertop_Items(self.boxSizertop)
        self._init_coll_boxSizerBottom_Items(self.boxSizerBottom)
        self._init_coll_gridBagSizerTop_Items(self.gridBagSizerTop)
        self._init_coll_staticBoxSizer1_Items(self.staticBoxSizer1)
        self._init_coll_gridBagSizerComputations_Items(self.gridBagSizerComputations)

        self.SetSizer(self.flexGridSizerLensDataMain)

    def _init_utils(self):
        # generated method, don't edit
        self.menu_thickness = wx.Menu(title='')

        self.menu_glass = wx.Menu(title='')

        self.row_menu = wx.Menu(title='')

        self._init_coll_menu_thickness_Items(self.menu_thickness)
        self._init_coll_menu_glass_Items(self.menu_glass)
        self._init_coll_row_menu_Items(self.row_menu)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_WXMDICHILDFRAME_LENS_DATA,
              name='wxMDIChildFrame_lens_data', parent=prnt, pos=wx.Point(505,
              364), size=wx.Size(847, 373), style=wx.DEFAULT_FRAME_STYLE,
              title='Lens Data')
        self._init_utils()
        self.SetClientSize(wx.Size(839, 339))
        self.Bind(EVT_CLOSE, self.OnWxmdichildframe_lens_dataClose)

        self.grid1 = wx.grid.Grid(id=wxID_WXMDICHILDFRAME_LENS_DATAGRID1,
              name='grid1', parent=self, pos=wx.Point(0, 87), size=wx.Size(839,
              773), style=0)
        self.grid1.Bind(EVT_GRID_CELL_CHANGE, self.OnGrid1GridCellChange)
        self.grid1.Bind(EVT_GRID_SELECT_CELL, self.OnGrid1GridCellChange) # To allow highlighting the active row.
        self.grid1.Bind(EVT_GRID_CELL_RIGHT_CLICK,
              self.OnGrid1GridCellRightClick)
        self.grid1.Bind(EVT_GRID_LABEL_RIGHT_CLICK,
              self.OnGrid1GridLabelRightClick)

        self.radioButton_const_power = wx.RadioButton(id=wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_POWER,
              label='Const Power/F-length', name='radioButton_const_power',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(136, 13), style=0)
        self.radioButton_const_power.SetValue(True)
        self.radioButton_const_power.Bind(EVT_RADIOBUTTON,
              self.OnRadiobutton_const_powerRadiobutton)

        self.radioButton_const_radius = wx.RadioButton(id=wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_RADIUS,
              label='Const Radius', name='radioButton_const_radius',
              parent=self, pos=wx.Point(0, 22), size=wx.Size(79, 13), style=0)
        self.radioButton_const_radius.SetValue(False)
        self.radioButton_const_radius.Bind(EVT_RADIOBUTTON,
              self.OnRadiobutton_const_radiusRadiobutton)

        self.staticText_paraxial_focus = wx.StaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_PARAXIAL_FOCUS,
              label='', name='staticText_paraxial_focus', parent=self,
              pos=wx.Point(436, 67), size=wx.Size(0, 13), style=0)

        self.checkBox_autofocus = wx.CheckBox(id=wxID_WXMDICHILDFRAME_LENS_DATACHECKBOX_AUTOFOCUS,
              label='Autofocus (paraxial)', name='checkBox_autofocus',
              parent=self, pos=wx.Point(0, 44), size=wx.Size(120, 13), style=0)
        self.checkBox_autofocus.SetValue(False)

        self.textCtrl_object_height = wx.TextCtrl(id=wxID_WXMDICHILDFRAME_LENS_DATATEXTCTRL_OBJECT_HEIGHT,
              name='textCtrl_object_height', parent=self, pos=wx.Point(136, 22),
              size=wx.Size(100, 21),
              style=wx.TAB_TRAVERSAL | wx.TE_PROCESS_TAB | wx.TE_PROCESS_ENTER,
              value='1.0')
        self.textCtrl_object_height.Enable(True)
        self.textCtrl_object_height.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, 'MS Shell Dlg'))
        self.textCtrl_object_height.Bind(EVT_TEXT,
              self.OnTextctrl_object_heightText)

        self.button_compute_all = wx.Button(id=wxID_WXMDICHILDFRAME_LENS_DATABUTTON_COMPUTE_ALL,
              label='Compute All', name='button_compute_all', parent=self,
              pos=wx.Point(316, 17), size=wx.Size(75, 23), style=0)
        self.button_compute_all.Bind(EVT_BUTTON,
              self.OnButton_compute_allButton)

        self.staticText_obj_height = wx.StaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_OBJ_HEIGHT,
              label='Object Height', name='staticText_obj_height', parent=self,
              pos=wx.Point(136, 0), size=wx.Size(65, 13), style=0)

        self.button_wave_lengths = wx.Button(id=wxID_WXMDICHILDFRAME_LENS_DATABUTTON_WAVE_LENGTHS,
              label='Wave Lengths', name='button_wave_lengths', parent=self,
              pos=wx.Point(136, 44), size=wx.Size(88, 23), style=0)
        self.button_wave_lengths.Bind(EVT_BUTTON,
              self.OnButton_wave_lengthsButton)

        self.button_spot_diagrams = wx.Button(id=wxID_WXMDICHILDFRAME_LENS_DATABUTTON_SPOT_DIAGRAMS,
              label='Spot Diagram', name='button_spot_diagrams', parent=self,
              pos=wx.Point(241, 17), size=wx.Size(75, 23), style=0)
        self.button_spot_diagrams.Bind(EVT_BUTTON,
              self.OnButton_spot_diagramsButton)

        self.staticBox1 = wx.StaticBox(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICBOX1,
              label='Computations', name='staticBox1', parent=self,
              pos=wx.Point(236, 0), size=wx.Size(160, 68), style=0)

        self.button_image = wx.Button(id=wxID_WXMDICHILDFRAME_LENS_DATABUTTON_IMAGE,
              label='Image', name='button_image', parent=self, pos=wx.Point(241,
              40), size=wx.Size(75, 23), style=0)
        self.button_image.Bind(EVT_BUTTON, self.OnButton_imageButton)

        self.staticText_mg = wx.StaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_MG,
              label='Transverse Magnification', name='staticText_mg',
              parent=self, pos=wx.Point(436, 22), size=wx.Size(160, 13),
              style=0)

        self.staticText_mag = wx.StaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_MAG,
              label='', name='staticText_mag', parent=self, pos=wx.Point(596,
              22), size=wx.Size(0, 13), style=0)

        self.staticTextEffectiveFocalLength = wx.StaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXTEFFECTIVEFOCALLENGTH,
              label='EFL:', name='staticTextEffectiveFocalLength', parent=self,
              pos=wx.Point(436, 44), size=wx.Size(22, 13), style=0)

        self.staticText_efl = wx.StaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_EFL,
              label='', name='staticText_efl', parent=self, pos=wx.Point(596,
              44), size=wx.Size(0, 13), style=0)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.waves = wxDialog_wavelengths.create(self)
        self.__system = DataModel.System([])
        
        
        self.grid1.CreateGrid(max(1,self.rows), self.cols)

        for i, label in enumerate(self.col_labels):
            self.grid1.SetColLabelValue(i, label)
        self.grid1.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        self.grid1.AutoSize()
                

        for row in range(self.rows):
            for col in range(self.cols):
                self.grid1.SetCellEditor(row, col, apply(GridCellFloatEditor, []))

        #self.n = []
        #self.c = []
        #self.t = []
        #self.c_unbent = [0 for i in range(self.rows)]                
            
        self.hold_power = self.radioButton_const_power.GetValue()        
        self.hold_radius = self.radioButton_const_radius.GetValue()        

        self.Layout()
        self.Centre()
        self.object_height = float(self.textCtrl_object_height.GetValue())
        self.rays = 100
        
        
    @property
    def rows(self): return len(self.__system)
    @property
    def cols(self): return len(self.col_labels)
    
    def setSystem(self, system):
        if system is not self.__system:
            self.__system = system
            self._sync_grid_to_system()

    def OnWxframeopenmodalSize(self, event):
        event.Skip()
    
    def OnRadiobutton_const_powerRadiobutton(self, event=None):
        self.hold_power = True
        self.hold_radius = False
 #       event.Skip()

    def OnRadiobutton_const_radiusRadiobutton(self, event=None):
        self.hold_power = False
        self.hold_radius = True
    

    def OnGrid1GridCellChange(self, event=None,r=None,c=None):  
        ##        self.grid1.AutoSize()
        if event is not None:
            r = event.GetRow()
            c = event.GetCol() 
        
        val = self.grid1.GetCellValue(r,c)
        #print r,c,val
        
        if val != '':
            rowData = self.surfToRowData(self.__system.surfaces[r])
            if str(rowData[self.col_labels[c]]) == val:
                return # Value not actually changed.
            val = float(val)                                    
            draw = self.fill_in_values(r,c,val)    
            self.update_display(event)

            #compute paraxial focus
            y = 0.0
            u = 1.0
            if np.isfinite(self.t[0]):
                l, y, u = paraxial_ray(y,u,self.t,self.n,self.c)
            else:
                l, y, u = paraxial_ray(y,u,self.t[1:],self.n[1:],self.c[1:])
            #print u
            mag = u[0] / u[-1]
            print 'paraixal ray:'
            print l
            print y
            print u
            print 'mag',mag
                
            self.staticText_mag.SetLabel(str(mag))
            if self.checkBox_autofocus.GetValue():
                self.grid1.SetCellValue(len(self.t)-1,THICKNESS,str(l))
                draw = self.fill_in_values(len(self.t)-1,THICKNESS,l)            
                self.update_display()                            
         
                                                 
            x   = [0] * self.rays
            y   = [0] * self.rays
            z   = [0] * self.rays
            X   = [0] * self.rays
            Y   = [0] * self.rays
            Z   = [0] * self.rays
            cnt = 0
            
            surf_i = 0
            for surf_i in range(len(self.t)): # Make surf_i index the first surface with finite non-zero thickness. 
                if np.isfinite(self.t[surf_i]) and self.t[surf_i] != 0: break
            
            if len(self.t) > 1:
                # Loop over field points:
                for fp_i, objPt, color in [(10, (0,0,0), (0.8,0.2,0.2)),
                                           (10, (0,self.object_height,0), (0.2,0.8,0.2))]:
                    for i in range(-fp_i//2+1, fp_i//2):
                        #go to aperature radius
                        assert self.t[surf_i] != 0
                        direction = [None, (i/(fp_i/2.0)) * self.h[surf_i+1] / norm([self.h[surf_i+1], self.t[surf_i]]), 0.0]
                        direction[0] = np.sqrt(1.0 - direction[1]**2 - direction[2]**2)
                        x[i],y[i],z[i],X[i],Y[i],Z[i] = skew_ray(objPt, direction,
                                                                 self.t[surf_i:],self.n[surf_i:],self.c[surf_i:],self.t_cum[surf_i:],self.h[surf_i:])

                        self.GetParent().ogl.draw_ray(x[i],y[i],z[i],cnt,self.t_cum[surf_i:], color=color)
                        cnt+=1
                
                        
                if False:
                    ray_1 = 10
                    for i in range(-ray_1//2+1, ray_1//2):
                        #go to aperature radius
                        if self.t[surf_i] != 0:
                            Yi = (i/(ray_1/2.0)) * self.h[surf_i+1] / norm([self.h[surf_i+1], self.t[surf_i]])
                            Zi = 0.0                
                            Xi =  np.sqrt(1.0 - Yi**2 - Zi**2)
                            x[i],y[i],z[i],X[i],Y[i],Z[i] = skew_ray((0,self.object_height,0),(Xi,Yi,Zi),
                                                                     self.t[surf_i:],self.n[surf_i:],self.c[surf_i:],self.t_cum[surf_i:],self.h[surf_i:])
                            self.GetParent().ogl.draw_ray(x[i],y[i],z[i],cnt, self.t_cum, color = (0.2,0.8,0.2))
                            cnt+=1

                                                                                                                
                
                if not len(self.t_cum) or self.t_cum[-1] == 0: 
                    k = 1
                else:
                    k = self.t_cum[-1] # Cumulative thickness.
                self.GetParent().ogl.K = k
        
##                #calc third order aberrations
##            
                #we need data from axial ray 
                #calc efL

                (l,y,u)    = paraxial_ray2(self.h[surf_i+1], 0.0,self.t,self.n,self.c)
                (lp,yp,up) = paraxial_ray2(0.0, 0.1,self.t,self.n,self.c)
                num = (y[surf_i]*up[surf_i] - u[surf_i]*yp[surf_i])
                den = (u[surf_i]*up[-1] - up[0]*u[-1])                
                if (den != 0):
                    efl = num/den
                    self.staticText_efl.SetLabel(str(efl))



##                #(l,y,u) = self.paraxial_ray2(18.5, 0)
##                #print y,u
##            
##                if(len(y) > 1):
##                    #data from a principal ray
##                    (lp,yp,up) = paraxial_ray2(0.0, 0.1,self.t,self.n,self.c)
##                    #(lp,yp,up) = self.paraxial_ray2(-6.3, 0.25)
##                    #print yp,up
##                    self.GetParent().trace.calc_third_order_abberations(y,u,yp,up,self.n,self.c)
           
        
                #self.GetParent().abr.calc_abr(self.t,self.n,self.c,self.t_cum,self.h,self.object_height)
                
        
    
    def fill_in_values(self,r,c,val):                               
        print 'fill_in_values',(r,c,val)
        self._sync_system_to_grid(r, c, val)
        #AUTOFILL SOME STUFF
        if (self.grid1.GetCellValue(r,GLASS) == ''):
            self.grid1.SetCellValue(r,GLASS,str(1))
            
        if (self.grid1.GetCellValue(r,THICKNESS) == ''):
            self.grid1.SetCellValue(r,THICKNESS,str(0))     
                
        if (self.grid1.GetCellValue(r,CURVATURE) == ''):
            self.grid1.SetCellValue(r,CURVATURE,str(0))
            
        if (self.grid1.GetCellValue(r,RADIUS) == ''):
            self.grid1.SetCellValue(r,RADIUS,str(0))            
        
        if (self.grid1.GetCellValue(r,APERATURE_RADIUS) == ''):
            self.grid1.SetCellValue(r,APERATURE_RADIUS,str(1.0))

        if (self.grid1.GetCellValue(r,BENDING) == ''):
            self.grid1.SetCellValue(r,BENDING,str(0.0))
                    
        if c == FLENGTH: #focal length changed
            if val == 0:
                val = '' # Shorthand for flat is zero.
            self.grid1.SetCellValue(r,POWER,str(1.0/val)) #set power            
            if (self.grid1.GetCellValue(r+1,APERATURE_RADIUS) == ''):
                self.grid1.SetCellValue(r+1,APERATURE_RADIUS,str(1.0))
            if (self.grid1.GetCellValue(r+1,GLASS) == ''):
                self.grid1.SetCellValue(r+1,GLASS,str(1))            
            if (self.grid1.GetCellValue(r+1,THICKNESS) == ''):
                self.grid1.SetCellValue(r+1,THICKNESS,str(0)) 
            if (self.grid1.GetCellValue(r+1,BENDING) == ''):
                self.grid1.SetCellValue(r+1,BENDING,str(0))                                                         
            self.update_radius(r)            
                
        if c == POWER: #power has changed    
            self.grid1.SetCellValue(r,FLENGTH,str(1.0/val))
            
            if (self.grid1.GetCellValue(r+1,APERATURE_RADIUS) == ''):
                self.grid1.SetCellValue(r+1,APERATURE_RADIUS,str(1.0))
            if (self.grid1.GetCellValue(r+1,GLASS) == ''):
                self.grid1.SetCellValue(r+1,GLASS,str(1))            
            if (self.grid1.GetCellValue(r+1,THICKNESS) == ''):
                self.grid1.SetCellValue(r+1,THICKNESS,str(0))                 
            if (self.grid1.GetCellValue(r+1,BENDING) == ''):
                self.grid1.SetCellValue(r+1,BENDING,str(0))                                                                         
            self.update_radius(r)
                                    
        if(c == CURVATURE): #curvature changed
            #update the radius
            if(val != 0):
                self.grid1.SetCellValue(r,RADIUS,str(1.0/val))
            else:
                self.grid1.SetCellValue(r,RADIUS,str(0.0))
                
            self.update_power(r)                                            
                        
        if(c == RADIUS): #radius changed
            #update the curvature
            
            if(val != 0):
                self.grid1.SetCellValue(r,CURVATURE,str(1.0/val))
            else:
                self.grid1.SetCellValue(r,CURVATURE,str(0.0))
            
##            if(self.grid1.GetCellValue(r,POWER) == ''):
##                self.radioButton_const_radius.SetValue(True)
##                self.OnRadiobutton_const_radiusRadiobutton()
            self.update_power(r)                                
                        
        if(c == THICKNESS): #thickness changed
            if(self.hold_power):
                self.update_radius(r)
            elif(self.hold_radius):        
                self.update_power(r)
                        
        if(c == GLASS):#GLASS CHANGED            
            if(self.hold_power):
                self.update_radius(r)
            elif(self.hold_radius):                
                self.update_power(r)                
        
        #c = BENDING
        #if(c == BENDING):#GLASS CHANGED            
        cnew = float(self.grid1.GetCellValue(r,CURVATURE)) + float( self.grid1.GetCellValue(r,BENDING))
        #print cnew
        self.grid1.SetCellValue(r,BENT_C, str(cnew))
        if(cnew == 0):
            self.grid1.SetCellValue(r,BENT_R, str(0.0))
        else:
            self.grid1.SetCellValue(r,BENT_R, str(1.0/cnew))

        if(c ==POWER or c == FLENGTH):
            cnew = float(self.grid1.GetCellValue(r+1,CURVATURE)) + float( self.grid1.GetCellValue(r,BENDING))
            #print cnew
            self.grid1.SetCellValue(r+1,BENT_C, str(cnew))
            if(cnew == 0):
                self.grid1.SetCellValue(r+1,BENT_R, str(0.0))
            else:
                self.grid1.SetCellValue(r+1,BENT_R, str(1.0/cnew))
                        
            self.update_power(r)

        #self.grid1.SetCellValue(r,BENT_C,self.grid1.GetCellValue(r,CURVATURE))            
        #self.grid1.SetCellValue(r,BENT_R,self.grid1.GetCellValue(r,RADIUS))            


        return True

    def update_display(self, event=None):
        print 'update_display',event
        thickness = 0                
        
        self.t = []
        self.t_cum = None
        self.c = []
        self.n = []
        self.h = []
        surf_i = []
            
        t1 = 0
        colors = [self.GetParent().ogl._lensSurfaceColor] * self.rows
        row = self.grid1.GetGridCursorRow()
        if event is not None:
            row = event.GetRow()
            #print "Row:", row, event.GetRow()
            if row is not None and row < self.rows:
                colors[row] = (1.0,0.0,0.0)
        for i, surf in enumerate(self.__system):                        
            if (surf.thickness is not None or #                bent_c           != '' or
                surf.semidiam is not None):
                
                #if not np.isfinite(float(thickness)): continue # Skip object or image at infinity.
        
                self.c.append(float(1/surf.R))
                self.h.append(float(surf.semidiam))
                surf_i.append(i)
                self.n.append(surf.n(None))
            
            
                t1 += float(surf.thickness)
                self.t.append(float(surf.thickness))
        # We want t_cum to be the positions of each surface. Need to deel with infinate thicknesses at ends of the system.
        if len(self.t) == 0 or np.isfinite(self.t[0]):
            self.t_cum = np.hstack([[0], np.cumsum(self.t)])
        else:
            self.t_cum = np.hstack([[-np.inf, 0], np.cumsum(self.t[1:])])
            
        l = range(1,self.rows)
        self.GetParent().ogl.draw_lenses(self.t,surf_i,self.t_cum,self.c,self.n,self.h,colors=colors)


    def update_power(self,r):            
        print 'update_power',(r,)
        #import epdb;epdb.st()
        if(self.grid1.GetCellValue(r+1,CURVATURE) != ''):
            n = self.grid1.GetCellValue(r,GLASS)
            if(n != ''):
                n = float(n)
            else:
                return -1
            
            if(n != 1):  
                #update the power
                c1 = float(self.grid1.GetCellValue(r,CURVATURE))
                c2 = float(self.grid1.GetCellValue(r+1,CURVATURE))                                            
            
                t   = self.grid1.GetCellValue(r,THICKNESS)
                if(t != ''):
                    t = float(t)
                else:
                    return -1                                    
                                    
                phi = (n-1.0) * (c1 - c2)+(n-1.0)*(n-1.0)/n*t*c1*c2
                self.grid1.SetCellValue(r,POWER,str(phi))
                self.grid1.SetCellValue(r,FLENGTH,str(1.0/phi))
            
        if r and self.grid1.GetCellValue(r-1,CURVATURE) != '': # then we are end of lens
            n = self.grid1.GetCellValue(r-1,GLASS)                
            if n != '':
                n = float(n)
            else:
                return -1

            if n != 1:
                # update the power
                c1 = float(self.grid1.GetCellValue(r-1,CURVATURE))
                c2 = float(self.grid1.GetCellValue(r,CURVATURE))            

                t = self.grid1.GetCellValue(r-1,THICKNESS)
                if t != '':
                    t = float(t)
                else:
                    return -1                                    

                phi = (n-1.0) * (c1 - c2)+(n-1.0)*(n-1.0)/n*t*c1*c2
                self.grid1.SetCellValue(r-1,POWER,str(phi))
                self.grid1.SetCellValue(r-1,FLENGTH,str(1.0/phi))

    def update_radius(self,r):        
            print 'update_radius',(r,)
            phi = self.grid1.GetCellValue(r,POWER)
            if(phi != ''):
                phi = float(phi)
            else:
                return -1
            
            n   = self.grid1.GetCellValue(r,GLASS)
            if(n != ''):
                n = float(n)
            else:
                return -1
            
            
            t   = self.grid1.GetCellValue(r,THICKNESS)
            if(t != ''):
                t = float(t)
            else:
                return -1

            if n**2 - phi * n * t < 0:
                return -1
            rad = (2*n+2*math.sqrt(n*n - phi*n*t)*(n-1)) / (2*n*phi)
            
            #calc r so that r1 = r2 = r   
            #rad = val * 2 * ( n - 1 )
            self.grid1.SetCellValue(r,RADIUS,str(rad))
            self.grid1.SetCellValue(r+1,RADIUS,str(-rad))
            
            if(rad != 0):
                self.grid1.SetCellValue(r,CURVATURE,str(1.0/rad))
                self.grid1.SetCellValue(r+1,CURVATURE,str(-1.0/rad))                
            else:
                self.grid1.SetCellValue(r,CURVATURE,str(0.0))
                self.grid1.SetCellValue(r+1,CURVATURE,str(0.0))  
                
                
    def get_data(self):
        t =  []
        tble = self.grid1.GetTable()                     
        for r in range(self.rows):
            t.append([tble.GetValue(r,c) for c in range(len(self.col_labels))])
        
        #print 'saving unbent as ',self.c_unbent
        return t
        

    def set_data(self, data):
        self._sync_grid_to_system()
        for ri, row in enumerate(data):
            for ci, cell in enumerate(row):
                strval = str(cell) if cell is not None else ''
                self.grid1.SetCellValue(ri, ci, strval)
        for r in range(self.rows):
            self.OnGrid1GridCellChange(None,r,CURVATURE)

    def _sync_grid_to_system(self):
        newNumRows = max(1, self.rows)
        if self.grid1.GetNumberRows() < newNumRows:
            self.grid1.InsertRows(self.grid1.GetNumberRows(), newNumRows - self.grid1.GetNumberRows())
        #return # Stuff below isn't implemented.
        for ri, surface in enumerate(self.__system):
            rowData = self.surfToRowData(surface)
            for ci, col_label in enumerate(self.col_labels):
                cell = rowData[col_label]
                strval = str(cell) if cell is not None else ''
                self.grid1.SetCellValue(ri, ci, strval)
        for r in range(self.rows):
            self.OnGrid1GridCellChange(None,r,CURVATURE)


    def _sync_system_to_grid(self, r, c, val):
        """Sync the given entry to the system model."""
        surface = self.__system.surfaces[r]
        label = self.col_labels[c]
        if label == 'curvature': surface.R = 1.0 / val
        elif label == 'radius': surface.R = val
        elif label == 'thickness': surf.thickness = val
        elif label == 'aperature radius': surf.semidiam = val
        elif label == 'glass': surf.glass = DataModel.SimpleGlass(val)
        else:
            print "Unimplemented."
            
    def clear_data(self):       
        for r in range(self.rows):
            [self.grid1.SetCellValue(r,c,'') for c in range(len(self.col_labels))]

    def OnGrid1GridCellRightClick(self, event):
        r = event.GetRow()
        c = event.GetCol()
        self.grid1.SelectBlock(r,c,r,c)
        self.grid1.SetGridCursor(r,c)
        
        offset =  self.grid1.GetPosition()
        pos    =  event.GetPosition()
        pos.x += offset.x
        pos.y += offset.y
        
        if(c == THICKNESS):             
            self.PopupMenu(self.menu_thickness,pos)
        elif(c == GLASS):
            id = self.PopupMenu(self.menu_glass,pos)
        
        event.Skip()

    def OnGrid1GridLabelRightClick(self, event):
        r = event.GetRow()
        c = event.GetCol()
        
        self.grid1.SetGridCursor(r,0)
        offset = self.grid1.GetPosition()
        pos    = event.GetPosition()
        pos.x += offset.x - 80
        pos.y += offset.y
                        
        self.PopupMenu(self.row_menu,pos)
        event.Skip()

    def OnRow_menuitems0Menu(self, event):
        r, c = self.grid1.GetGridCursorRow(), self.grid1.GetGridCursorCol()
        id = event.GetId()
        
        if id == self.DATAROW_MENUINSERTAFTER:
            self.grid1.InsertRows(r+1)
            self.rows+=1
        elif id == self.DATAROW_MENUINSERTBEFORE:
            self.grid1.InsertRows(r)            
            self.rows+=1
        elif id == self.DATAROW_MENUDELETE:
            self.grid1.DeleteRows(r)
            self.rows-=1
            
            
##        if(id ==   wxID_WXMDICHILDFRAME_LENS_DATAMENU1COPY):
##            print 'not yet implemented'
##        if(id == wxID_WXMDICHILDFRAME_LENS_DATAMENU1PASTE):
##            print 'not yet implemented'
            
        event.Skip()
        

    def OnMenu_thicknessitems0Menu(self, event):
        (r,c) = (self.grid1.GetGridCursorRow(),self.grid1.GetGridCursorCol())
        id = event.GetId()
        if(id == wxID_WXMDICHILDFRAME_LENS_DATAMENU_THICKNESSITEMS0):
            self.checkBox_autofocus.SetValue(True)
            self.OnGrid1GridCellChange(None,r, c)
            self.checkBox_autofocus.SetValue(False)
    
    def OnMenu_glassitems0Menu(self, event):
        (r,c) = (self.grid1.GetGridCursorRow(),self.grid1.GetGridCursorCol())
        id = event.GetId()
        if(id == self.MENU_GLASSDIRECT):            
            self.grid1.SetCellValue(r,c,'')
        elif(id == selfMENU_GLASSBK7):            
            self.grid1.SetCellValue(r,c,'BK7')
 
 
        #event.Skip()

    def OnTextctrl_object_heightText(self, event):
        self.object_height = float(self.textCtrl_object_height.GetValue())
        self.OnGrid1GridCellChange(event=None,r=0,c=THICKNESS)               
        event.Skip()

    def OnButton_compute_allButton(self, event):
        self.OnButton_spot_diagramsButton()
        self.OnButton_imageButton()

    def OnButton_wave_lengthsButton(self, event):
        self.waves.Show()                                                         
        event.Skip()

    def OnButton_spot_diagramsButton(self, event = None):
        if(not self.GetParent().spot.IsShown()):
            self.GetParent().spot.Show()
        self.GetParent().spot.draw_spots(self.t,self.n,self.c,self.t_cum,self.h,self.object_height)            
        
        

    def OnButton_imageButton(self, event= None):           
        if(not self.GetParent().img.IsShown()):
            self.GetParent().img.Show()

        img = np.array([[1,1,1,1,1],
                        [1,0,1,.8,1],    
                        [1,1,1,1,1],
                        [1,.5,1,0,1],
                        [1,1,1,1,1],
                        [1,1,1,1,1]])                                     
        self.GetParent().img.draw_image(img,self.object_height,self.t,self.n,self.c,self.t_cum,self.h)

    def OnWxmdichildframe_lens_dataClose(self, event):
        self.Hide()


def loadZMXAsTable(zmxfilename):
    colLabels = dict((label.strip(), i) for i, label in enumerate(wxMDIChildFrame_lens_data.col_labels))
    surfaces = []
    with open(zmxfilename, 'r') as fh:
        lines = fh.readlines()
    apertureStop = None
    i = -1
    while i < len(lines) - 1:
        i += 1
        line = lines[i]
        if line.startswith('SURF'):
            isStop = False
            glass_n = 1.0
            row = [None] * len(colLabels) # New blank row.
            while i < len(lines) - 1:
                i += 1
                line = lines[i]
                if 'STOP' in line:
                    isStop = True
                elif 'TYPE STANDARD' in line or 'TYPE EVENASPH' in line:
                    pass # Other surfaces not implemented.
                elif 'CURV' in line:
                    row[colLabels['curvature']] = float(line.split()[1])
                elif 'DIAM' in line:
                    row[colLabels['aperature radius']] = float(line.split()[1]) / 2.0
                elif 'DISZ' in line:
                    row[colLabels['thickness']] = float(line.split()[1])
                elif 'GLAS' in line:
                    parts = line.split()
                    row[colLabels['glass']] = float(parts[4])
                    # glass_name = parts[1]
                if not line.startswith(' '):
                    i -= 1
                    try:
                        surfaces.append(row)
                    except Exception as e:
                        print ctor, e
                        import epdb; epdb.st()
                    break
    return surfaces
