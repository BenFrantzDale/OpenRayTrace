#Boa:MDIChild:wxMDIChildFrame_lens_system_ogl
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
from myCanvas import *
import os, string
from cmath import *
from math  import *


def create(parent):
    return wxMDIChildFrame_lens_system_ogl(parent)

[wxID_WXMDICHILDFRAME_LENS_SYSTEM_OGL] = map(lambda _init_ctrls: wxNewId(), range(1))

class wxMDIChildFrame_lens_system_ogl(wxMDIChildFrame):
    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxMDIChildFrame.__init__(self, id=wxID_WXMDICHILDFRAME_LENS_SYSTEM_OGL,
              name='wxMDIChildFrame_lens_system_ogl', parent=prnt,
              pos=wxPoint(448, 244), size=wxSize(604, 404),
              style=wxDEFAULT_FRAME_STYLE, title='Lens System')
        self._init_utils()
        self.SetClientSize(wxSize(596, 370))
        self.SetBackgroundColour(wxColour(0, 0, 0))
        EVT_CLOSE(self, self.OnWxmdichildframe_lens_system_oglClose)

    def __init__(self, parent):
        self._init_ctrls(parent)
                
        #self.gl_list    = []
        self.lens_list = []
        self.ray_list  = []              
        self.color = [0,0,0]
                    
        self.can = myCanvas(self)
        self.can.SetCurrent()
        self.can.centered = False
        
        self.rows = 40
        self.glListStart =  glGenLists(self.rows + 1)
        self.l = range(self.glListStart,self.glListStart + self.rows)
        self.can.set_lens_list(self.l)
                 
        
        self.rays = 100
        self.glRayListStart = glGenLists(self.rays)
        self.l = range(self.glRayListStart,self.glRayListStart + self.rays)
        self.can.set_ray_list(self.l)
        
    def clear_list(self):
        self.can.SetCurrent()
        glDeleteLists(self.glRayListStart,self.rays)                
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)
        
        glDeleteLists(self.glListStart,self.rows)                
        self.glListStart =  glGenLists(self.rows + 1)
        self.l = range(self.glListStart,self.glListStart + self.rows)
        self.can.set_lens_list(self.l)        
        self.can.DrawGL()
        

    def OnWxmdichildframe_lens_system_oglSize(self, event):
        self.can.OnSize(event)
        event.Skip()
        
    def reset_view(self):
        self.can.reset_view()
        
        
    def set_k(self,k):
        self.can.set_k(k)
        
                
    def draw_ray(self,x,y,z,ray,T_CUM,color=[1,1,1]):                                    
        self.can.SetCurrent()
        glNewList(ray + self.glRayListStart, GL_COMPILE)      
        glColorf(color[0],color[1],color[2])                
        glBegin(GL_LINE_STRIP)
        
        for i in range(len(x)):            
            glVertexf(x[i] + T_CUM[i],y[i],z[i]) 
            
        glEnd()        
        glEndList()                                
                        

    def draw_surface(self,c,t,h,n):        
        
        self.can.SetCurrent()
        
        if(c!=0):
            r = 1/c
        else:
            r = 1E5
                        
        n+=1
        
        #draw part of lens surface
        if( h*h < r*r ):
            b = pow(r*r - h*h, 0.5)        
        else:
            b = 0
            
        if(r > 0):
            a = r - b    
        else:
            a = r + b            
        inc = a / n        
        
        #calc lens shape
        y = range(n)
        x  = [(i*inc + t) for i in range(n)]
        x2 = [(i*inc - r)*(i*inc - r) for i in range(n)]                
        r2 = r*r 
        for i in range(n):
            if(x2[i] < r2):
                y[i] = pow(r2 - x2[i],.5)
            else:
                y[i] = 0
                                    
##        glBegin(GL_LINE_STRIP)    
##        for i in range(n):                    
##            glVertex3f(x[i],y[i],0)            
##        glEnd()
##      
##        glBegin(GL_LINE_STRIP)    
##        for i in range(n):                    
##            glVertex3f(x[i],-y[i],0)            
##        glEnd()
              
        for theta in range(0,359,180):      
            p = theta * 3.14159/180.0
            glBegin(GL_LINE_STRIP)    
            for i in range(n):
                glVertex3f(x[i],y[i] * cos(p),y[i]*sin(p))            
            glEnd()
        
        glColorf(1,1,1,.25)    
        glBegin(GL_LINE_STRIP)    
        for theta in range(0,365,5):      
            p = theta * 3.14159/180.0
            
            i = n-1
            glVertex3f(x[i],y[i] * cos(p),y[i]*sin(p))            
        glEnd()
        glColorf(1.0,1.0,0.0)

              
        return (x[i],y[i])
    
    
    
    def draw_lens(self,t,surf,t_cum,c,n,h):   
        self.can.SetCurrent()
        self.clear_list()
        z = [0 for i in range(self.rows)]

        for i in range(len(t)):                                                        
            glNewList(self.glListStart + surf[i], GL_COMPILE_AND_EXECUTE)        
            glColorf(1.0,1.0,1.0)                                   
            if(i == 0):
                glBegin(GL_LINES)
                glVertexf(0,0,0)
                glVertexf(t_cum[len(t_cum)-1],0,0)
                glEnd()        
        
            glColorf(1.0,1.0,0.0)                                   
            z[i] = self.draw_surface(c[i],t_cum[i],h[i],10)
            
            if(i > 0):                        
                if(n[i-1] != 1):
                    glBegin(GL_LINES)

                    glVertex3f(float(z[i-1][0]),float(z[i-1][1]),0)
                    glVertex3f(float(z[i][0])  ,float(z[i][1]),0)

                    glVertex3f(float(z[i-1][0]),-float(z[i-1][1]),0)
                    glVertex3f(float(z[i][0]),-float(z[i][1]),0)

                    glEnd()                        
                    
            glEndList()
        
        self.reset_view()
        

    def OnWxmdichildframe_lens_system_oglClose(self, event):
        self.Hide()