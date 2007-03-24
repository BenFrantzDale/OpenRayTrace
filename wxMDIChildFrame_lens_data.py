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



from wxPython.wx import *
from wxPython.grid import *
import wxDialog_wavelengths

from myCanvas import *
import os, string
from cmath import *
import math
from Numeric import *
from ray_trace import *


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
] = map(lambda _init_ctrls: wxNewId(), range(17))



[wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_BK7, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_DIRECT, 
] = map(lambda _init_coll_menu_glass_Items: wxNewId(), range(2))

[wxID_WXMDICHILDFRAME_LENS_DATAMENU1COPY, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU1DELETE, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_AFTER, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_BEFORE, 
 wxID_WXMDICHILDFRAME_LENS_DATAMENU1PASTE, 
] = map(lambda _init_coll_row_menu_Items: wxNewId(), range(5))

[wxID_WXMDICHILDFRAME_LENS_DATAMENU_THICKNESSITEMS0] = map(lambda _init_coll_menu_thickness_Items: wxNewId(), range(1))

class wxMDIChildFrame_lens_data(wxMDIChildFrame):
    def _init_coll_row_menu_Items(self, parent):
        # generated method, don't edit

        parent.Append(helpString='',
              id=wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_BEFORE,
              item='Insert Before', kind=wxITEM_NORMAL)
        parent.Append(helpString='',
              id=wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_AFTER,
              item='Insert After', kind=wxITEM_NORMAL)
        parent.Append(helpString='',
              id=wxID_WXMDICHILDFRAME_LENS_DATAMENU1DELETE, item='Delete',
              kind=wxITEM_NORMAL)
        parent.Append(helpString='', id=wxID_WXMDICHILDFRAME_LENS_DATAMENU1COPY,
              item='Copy', kind=wxITEM_NORMAL)
        parent.Append(helpString='',
              id=wxID_WXMDICHILDFRAME_LENS_DATAMENU1PASTE, item='Paste',
              kind=wxITEM_NORMAL)
        EVT_MENU(self, wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_BEFORE,
              self.OnRow_menuitems0Menu)
        EVT_MENU(self, wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_AFTER,
              self.OnRow_menuitems0Menu)
        EVT_MENU(self, wxID_WXMDICHILDFRAME_LENS_DATAMENU1DELETE,
              self.OnRow_menuitems0Menu)

    def _init_coll_menu_thickness_Items(self, parent):
        # generated method, don't edit

        parent.Append(helpString='',
              id=wxID_WXMDICHILDFRAME_LENS_DATAMENU_THICKNESSITEMS0,
              item='Paraxial Focus', kind=wxITEM_NORMAL)
        EVT_MENU(self, wxID_WXMDICHILDFRAME_LENS_DATAMENU_THICKNESSITEMS0,
              self.OnMenu_thicknessitems0Menu)

    def _init_coll_menu_glass_Items(self, parent):
        # generated method, don't edit

        parent.Append(helpString='',
              id=wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_DIRECT,
              item='Direct', kind=wxITEM_RADIO)
        parent.Append(helpString='',
              id=wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_BK7, item='BK7',
              kind=wxITEM_RADIO)
        EVT_MENU(self, wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_DIRECT,
              self.OnMenu_glassitems0Menu)
        EVT_MENU(self, wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_BK7,
              self.OnMenu_glassitems0Menu)

    def _init_utils(self):
        # generated method, don't edit
        self.menu_thickness = wxMenu(title='')
        self._init_coll_menu_thickness_Items(self.menu_thickness)

        self.menu_glass = wxMenu(title='')
        self._init_coll_menu_glass_Items(self.menu_glass)

        self.row_menu = wxMenu(title='')
        self._init_coll_row_menu_Items(self.row_menu)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxMDIChildFrame.__init__(self, id=wxID_WXMDICHILDFRAME_LENS_DATA,
              name='wxMDIChildFrame_lens_data', parent=prnt, pos=wxPoint(493,
              289), size=wxSize(847, 807), style=wxDEFAULT_FRAME_STYLE,
              title='Lens Data')
        self._init_utils()
        self.SetClientSize(wxSize(839, 773))
        EVT_CLOSE(self, self.OnWxmdichildframe_lens_dataClose)

        self.grid1 = wxGrid(id=wxID_WXMDICHILDFRAME_LENS_DATAGRID1,
              name='grid1', parent=self, pos=wxPoint(0, 120), size=wxSize(736,
              640), style=0)
        EVT_GRID_CELL_CHANGE(self.grid1, self.OnGrid1GridCellChange)
        EVT_GRID_CELL_RIGHT_CLICK(self.grid1, self.OnGrid1GridCellRightClick)
        EVT_GRID_LABEL_RIGHT_CLICK(self.grid1, self.OnGrid1GridLabelRightClick)

        self.radioButton_const_power = wxRadioButton(id=wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_POWER,
              label='Const Power/F-length', name='radioButton_const_power',
              parent=self, pos=wxPoint(8, 8), size=wxSize(136, 13), style=0)
        self.radioButton_const_power.SetValue(True)
        EVT_RADIOBUTTON(self.radioButton_const_power,
              wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_POWER,
              self.OnRadiobutton_const_powerRadiobutton)

        self.radioButton_const_radius = wxRadioButton(id=wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_RADIUS,
              label='Const Radius', name='radioButton_const_radius',
              parent=self, pos=wxPoint(8, 32), size=wxSize(79, 13), style=0)
        self.radioButton_const_radius.SetValue(False)
        EVT_RADIOBUTTON(self.radioButton_const_radius,
              wxID_WXMDICHILDFRAME_LENS_DATARADIOBUTTON_CONST_RADIUS,
              self.OnRadiobutton_const_radiusRadiobutton)

        self.staticText_paraxial_focus = wxStaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_PARAXIAL_FOCUS,
              label='', name='staticText_paraxial_focus', parent=self,
              pos=wxPoint(928, 312), size=wxSize(0, 13), style=0)

        self.checkBox_autofocus = wxCheckBox(id=wxID_WXMDICHILDFRAME_LENS_DATACHECKBOX_AUTOFOCUS,
              label='Autofocus (paraxial)', name='checkBox_autofocus',
              parent=self, pos=wxPoint(8, 56), size=wxSize(120, 13), style=0)
        self.checkBox_autofocus.SetValue(False)

        self.textCtrl_object_height = wxTextCtrl(id=wxID_WXMDICHILDFRAME_LENS_DATATEXTCTRL_OBJECT_HEIGHT,
              name='textCtrl_object_height', parent=self, pos=wxPoint(208, 24),
              size=wxSize(100, 21),
              style=wxTAB_TRAVERSAL | wxTE_PROCESS_TAB | wxTE_PROCESS_ENTER,
              value='1.0')
        self.textCtrl_object_height.Enable(True)
        self.textCtrl_object_height.SetFont(wxFont(8, wxSWISS, wxNORMAL,
              wxNORMAL, False, 'MS Shell Dlg'))
        EVT_TEXT(self.textCtrl_object_height,
              wxID_WXMDICHILDFRAME_LENS_DATATEXTCTRL_OBJECT_HEIGHT,
              self.OnTextctrl_object_heightText)

        self.button_compute_all = wxButton(id=wxID_WXMDICHILDFRAME_LENS_DATABUTTON_COMPUTE_ALL,
              label='Compute All', name='button_compute_all', parent=self,
              pos=wxPoint(544, 56), size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.button_compute_all,
              wxID_WXMDICHILDFRAME_LENS_DATABUTTON_COMPUTE_ALL,
              self.OnButton_compute_allButton)

        self.staticText_obj_height = wxStaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_OBJ_HEIGHT,
              label='Object Height', name='staticText_obj_height', parent=self,
              pos=wxPoint(224, 8), size=wxSize(65, 13), style=0)

        self.button_wave_lengths = wxButton(id=wxID_WXMDICHILDFRAME_LENS_DATABUTTON_WAVE_LENGTHS,
              label='Wave Lengths', name='button_wave_lengths', parent=self,
              pos=wxPoint(216, 64), size=wxSize(88, 23), style=0)
        EVT_BUTTON(self.button_wave_lengths,
              wxID_WXMDICHILDFRAME_LENS_DATABUTTON_WAVE_LENGTHS,
              self.OnButton_wave_lengthsButton)

        self.button_spot_diagrams = wxButton(id=wxID_WXMDICHILDFRAME_LENS_DATABUTTON_SPOT_DIAGRAMS,
              label='Spot Diagram', name='button_spot_diagrams', parent=self,
              pos=wxPoint(320, 24), size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.button_spot_diagrams,
              wxID_WXMDICHILDFRAME_LENS_DATABUTTON_SPOT_DIAGRAMS,
              self.OnButton_spot_diagramsButton)

        self.staticBox1 = wxStaticBox(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICBOX1,
              label='Computations', name='staticBox1', parent=self,
              pos=wxPoint(312, 8), size=wxSize(328, 80), style=0)

        self.button_image = wxButton(id=wxID_WXMDICHILDFRAME_LENS_DATABUTTON_IMAGE,
              label='Image', name='button_image', parent=self, pos=wxPoint(320,
              56), size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.button_image,
              wxID_WXMDICHILDFRAME_LENS_DATABUTTON_IMAGE,
              self.OnButton_imageButton)

        self.staticText_mg = wxStaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_MG,
              label='Transverse Magnification', name='staticText_mg',
              parent=self, pos=wxPoint(664, 24), size=wxSize(160, 13), style=0)

        self.staticText_mag = wxStaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_MAG,
              label='', name='staticText_mag', parent=self, pos=wxPoint(728,
              40), size=wxSize(0, 13), style=0)

        self.staticText1 = wxStaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT1,
              label='EFL:', name='staticText1', parent=self, pos=wxPoint(672,
              80), size=wxSize(22, 13), style=0)

        self.staticText_efl = wxStaticText(id=wxID_WXMDICHILDFRAME_LENS_DATASTATICTEXT_EFL,
              label='', name='staticText_efl', parent=self, pos=wxPoint(696,
              80), size=wxSize(0, 13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.waves = wxDialog_wavelengths.create(self)
        
        
        self.rows = 40
        self.col_label = ['f-length  ','power    ','curvature    ','radius   ','thickness    ','aperature radius ','glass    ','bending','bent c','bent r']
        self.grid1.CreateGrid(self.rows,len(self.col_label))

        [self.grid1.SetColLabelValue(i,self.col_label[i]) for i in range(len(self.col_label))]
        self.grid1.SetDefaultCellAlignment(wxALIGN_CENTRE,wxALIGN_CENTRE)
        
        self.grid1.AutoSize()
                
        for row in range(self.rows):
            for col in range(len(self.col_label)):
                self.grid1.SetCellEditor(row, col, apply(wxGridCellFloatEditor,[]))                    

        self.n = []
        self.c = []
        self.t = []
        self.c_unbent = [0 for i in range(self.rows)]                
            
        self.hold_power = self.radioButton_const_power.GetValue()        
        self.hold_radius = self.radioButton_const_radius.GetValue()        

        self.Layout()
        self.Centre()
        self.object_height = float(self.textCtrl_object_height.GetValue())
        self.rays = 100
        
        

    def OnWxframeopenmodalSize(self, event):
        event.Skip()
    
    def OnRadiobutton_const_powerRadiobutton(self, event=NULL):
        self.hold_power = True
        self.hold_radius = False
 #       event.Skip()

    def OnRadiobutton_const_radiusRadiobutton(self, event=NULL):
        self.hold_power = False
        self.hold_radius = True
    

    def OnGrid1GridCellChange(self, event=NULL,r=NULL,c=NULL):        
        self.grid1.AutoSize()
        if(event != NULL):
            r = event.GetRow()
            c = event.GetCol() 
        
        val = self.grid1.GetCellValue(r,c)
        #print r,c,val
        if(val != ''):
            val = float(val)                                    
            draw = self.fill_in_values(r,c,val)            
            self.update_display()                            


            #compute paraxial focus
            y = 0.0
            u = 1.0
            (l,y,u) = paraxial_ray(y,u,self.t,self.n,self.c)                
            #print u
            mag = u[0]/u[len(u)-1]
                
            self.staticText_mag.SetLabel(str(mag))
            if(self.checkBox_autofocus.GetValue()):
                self.grid1.SetCellValue(len(self.t)-1,THICKNESS,str(l))
                draw = self.fill_in_values(len(self.t)-1,THICKNESS,l)            
                self.update_display()                            
         
                                                 
            x   = [0 for i in range(self.rays)]
            y   = [0 for i in range(self.rays)]
            z   = [0 for i in range(self.rays)]
            X   = [0 for i in range(self.rays)]
            Y   = [0 for i in range(self.rays)]
            Z   = [0 for i in range(self.rays)]
            cnt = 0
            
            if(len(self.t) > 1):                                                        
                ray_0 = 10
                for i in range(-ray_0/2+1, ray_0/2):                        
                    #go to aperature radius
                
                    if(self.t[0] !=0):
                        Yi = (i/(ray_0/2.0)) * self.h[1]/pow(self.h[1] * self.h[1] + self.t[0]*self.t[0],0.5)
                        Zi = 0.0                                  
                        Xi =  math.pow(1.0 - Yi*Yi - Zi*Zi, 0.5)
                        (x[i],y[i],z[i],X[i],Y[i],Z[i]) = skew_ray((0,0,0),(Xi,Yi,Zi),self.t,self.n,self.c,self.t_cum,self.h)                                
    
                        self.GetParent().ogl.draw_ray(x[i],y[i],z[i],cnt,self.t_cum,color = [1.0,0.0,0.0])
                        cnt+=1
                
                        
                ray_1 = 10
                for i in range(-ray_1/2+1, ray_1/2):
                    #go to aperature radius
                    if(self.t[0] !=0):    
                        Yi = (i/(ray_1/2.0)) * self.h[1]/pow(self.h[1] * self.h[1] + self.t[0]*self.t[0],0.5)
                        Zi = 0.0                
                        Xi =  math.pow(1.0 - Yi*Yi - Zi*Zi, 0.5)
                        (x[i],y[i],z[i],X[i],Y[i],Z[i]) = skew_ray((0,self.object_height,0),(Xi,Yi,Zi),self.t,self.n,self.c,self.t_cum,self.h) 


                        self.GetParent().ogl.draw_ray(x[i],y[i],z[i],cnt, self.t_cum,color = [0.0,1.0,0.0])
                        cnt+=1
                
                                                                                                                
                
                k = self.t_cum[len(self.t_cum)-1]                     
                self.GetParent().ogl.set_k(k)
        
##                #calc third order aberrations
##            
                #we need data from axial ray 
                #calc efL

                (l,y,u)    = paraxial_ray2(self.h[1], 0.0,self.t,self.n,self.c)
                (lp,yp,up) = paraxial_ray2(0.0, 0.1,self.t,self.n,self.c)
                num = (y[0]*up[0] - u[0]*yp[0])
                den = (u[0]*up[len(up)-1] - up[0]*u[len(u)-1])                
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
           
        
                self.GetParent().abr.calc_abr(self.t,self.n,self.c,self.t_cum,self.h,self.object_height)
                
        

        
    
    
    
    
    
    def fill_in_values(self,r,c,val):                               
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
                    
        if(c == FLENGTH): #focal length changed
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
                
        if(c == POWER): #power has changed    
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

    def update_display(self):
        thickness = 0                
                
        
        self.t = []
        self.t_cum = []        
        self.t_cum.append(0)
        self.c = []
        self.n = []
        self.h = []
        surf = []
            
        t1 = 0
        for i in range(self.rows):                        
            if( (self.grid1.GetCellValue(i,THICKNESS)        != '') |
                (self.grid1.GetCellValue(i,BENT_C)        != '') |
                (self.grid1.GetCellValue(i,APERATURE_RADIUS) != '') ):                                
            
        
                self.c.append(float(self.grid1.GetCellValue(i,BENT_C))) 
                
                self.h.append(float(self.grid1.GetCellValue(i,APERATURE_RADIUS)))
                surf.append(i)    
                    
                self.n.append(float(self.grid1.GetCellValue(i,GLASS)))
            
            
            if(self.grid1.GetCellValue(i,THICKNESS) != ''):
                t1 += (float(self.grid1.GetCellValue(i,THICKNESS))) 
                self.t.append(float(self.grid1.GetCellValue(i,THICKNESS)))
                self.t_cum.append(t1)

                                
        l = range(1,self.rows)
        
        self.GetParent().ogl.draw_lens(self.t,surf,self.t_cum,self.c,self.n,self.h)
        
        


    def update_power(self,r):            
        
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
            
        if(r!=0):                  
                                        
            if(self.grid1.GetCellValue(r-1,CURVATURE) != ''):#then we are end of lens
                n = self.grid1.GetCellValue(r-1,GLASS)                
                if(n != ''):
                    n = float(n)
                else:
                    return -1
            
                if(n != 1):
                    #update the power
                    c1 = float(self.grid1.GetCellValue(r-1,CURVATURE))
                    c2 = float(self.grid1.GetCellValue(r,CURVATURE))            
            
                    t   = self.grid1.GetCellValue(r-1,THICKNESS)
                    if(t != ''):
                        t = float(t)
                    else:
                        return -1                                    
                                                          
                    phi = (n-1.0) * (c1 - c2)+(n-1.0)*(n-1.0)/n*t*c1*c2
                    self.grid1.SetCellValue(r-1,POWER,str(phi))
                    self.grid1.SetCellValue(r-1,FLENGTH,str(1.0/phi))

    def update_radius(self,r):        
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

            rad = ((2*n+2*math.pow((n*n - phi*n*t),.5))*(n-1))/(2*n*phi)
            
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
            t.append([tble.GetValue(r,c) for c in range(len(self.col_label))])
        
        #print 'saving unbent as ',self.c_unbent
        return t
        

    def set_data(self,data):                
        for r in range(self.rows):
            [self.grid1.SetCellValue(r,c,data[r][c]) for c in range(len(self.col_label) )]
        for r in range(self.rows):
            self.OnGrid1GridCellChange(NULL,r,CURVATURE)
                        
            
    def clear_data(self):       
        for r in range(self.rows):
            [self.grid1.SetCellValue(r,c,'') for c in range(len(self.col_label))]

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
        (r,c) = (self.grid1.GetGridCursorRow(),self.grid1.GetGridCursorCol())
        id = event.GetId()
        
        
        if(id ==  wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_AFTER):
            self.grid1.InsertRows(r+1)
            self.rows+=1
        elif(id ==  wxID_WXMDICHILDFRAME_LENS_DATAMENU1INSERT_BEFORE):
            self.grid1.InsertRows(r)            
            self.rows+=1
        elif(id ==   wxID_WXMDICHILDFRAME_LENS_DATAMENU1DELETE):            
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
            self.OnGrid1GridCellChange(NULL,r, c)
            self.checkBox_autofocus.SetValue(False)
    
    def OnMenu_glassitems0Menu(self, event):
        (r,c) = (self.grid1.GetGridCursorRow(),self.grid1.GetGridCursorCol())
        id = event.GetId()
        if(id == wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_DIRECT):            
            self.grid1.SetCellValue(r,c,'')
        elif(id == wxID_WXMDICHILDFRAME_LENS_DATAMENU_GLASSITEMS_BK7):            
            self.grid1.SetCellValue(r,c,'BK7')
 
        #event.Skip()

    def OnTextctrl_object_heightText(self, event):
        self.object_height = float(self.textCtrl_object_height.GetValue())
        self.OnGrid1GridCellChange(event=NULL,r=0,c=THICKNESS)               
        event.Skip()

    def OnButton_compute_allButton(self, event):
        self.OnButton_spot_diagramsButton()
        self.OnButton_imageButton()

    def OnButton_wave_lengthsButton(self, event):
        self.waves.Show()                                                         
        event.Skip()

    def OnButton_spot_diagramsButton(self, event = NULL):
        if(not self.GetParent().spot.IsShown()):
            self.GetParent().spot.Show()
        self.GetParent().spot.draw_spots(self.t,self.n,self.c,self.t_cum,self.h,self.object_height)            
        
        

    def OnButton_imageButton(self, event= NULL):           
        if(not self.GetParent().img.IsShown()):
            self.GetParent().img.Show()

        img = array([[1,1,1,1,1],
                     [1,0,1,.8,1],    
                     [1,1,1,1,1],
                     [1,.5,1,0,1],
                     [1,1,1,1,1],
                     [1,1,1,1,1] ])                                     
        self.GetParent().img.draw_image(img,self.object_height,self.t,self.n,self.c,self.t_cum,self.h)

    def OnWxmdichildframe_lens_dataClose(self, event):
        self.Hide()




        
    
    