from __future__ import division
#OpenRayTrace.UI.frames.LensSystemOGL
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
from OpenRayTrace.UI.myCanvas import *
import os, string
from cmath import *
from math  import *
import numpy as np



class LensSystemOGL(wx.MDIChildFrame):
    wxID = wx.NewId()
    _lensSurfaceColor = (0.1, 0.1, 0.1)
    def __init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=self.wxID,
                                  name='LensSystemOGL', parent=prnt,
                                  pos=wx.Point(448, 244), size=wx.Size(604, 404),
                                  style=wx.DEFAULT_FRAME_STYLE, title='Lens System')
        self.SetClientSize(wx.Size(596, 370))
        self.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.Bind(wx.EVT_CLOSE, lambda event: self.Hide, id=self.wxID)

    def __init__(self, parent):
        self.__init_ctrls(parent)
        self._frameInit = False        
        #self.gl_list    = []
        self.lens_list = []
        self.ray_list  = []              
        self.color = [0,0,0]
        
        self.Show()    
        self.can = myCanvas(self)
        self.can.centered = False
        self.rows = 40
        self.__listsInitialized = False
        self.can.glSetCurrent()
        self.__initializeLists()

    def __initializeLists(self):
        if self.__listsInitialized: return
        self.glListStart = glGenLists(self.rows + 1)
        self.l = range(self.glListStart, self.glListStart + self.rows)
        self.can.set_lens_list(self.l)
                 
        
        self.rays = 100
        self.glRayListStart = glGenLists(self.rays)
        self.l = range(self.glRayListStart,self.glRayListStart + self.rays)
        self.can.set_ray_list(self.l)
        self.__listsInitialized = True
        
    def clear_list(self):
        self.can.glSetCurrent()
        self.__initializeLists()
        glDeleteLists(self.glRayListStart,self.rays)                
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)
        
        glDeleteLists(self.glListStart,self.rows)                
        self.glListStart =  glGenLists(self.rows + 1)
        self.l = range(self.glListStart,self.glListStart + self.rows)
        self.can.set_lens_list(self.l)        
        self.can.DrawGL()
        

    def OnSize(self, event):
        self.can.OnSize(event)
        event.Skip()
        
    def reset_view(self):
        self.can.reset_view()
        
    @property 
    def K(self): return self.can.K

    @K.setter
    def K(self, k): self.can.K = k
                
    def draw_ray(self,x,y,z,ray,T_CUM=None,color=[1,1,1]):                                    
        self.can.glSetCurrent()
        glNewList(ray + self.glRayListStart, GL_COMPILE)      
        glColor(*color)
        glBegin(GL_LINE_STRIP)
        
        if T_CUM is not None:
            for i in range(len(x)) :
                glVertex(x[i] + T_CUM[i],y[i],z[i]) 
        else:
            for xyz in zip(x,y,z):
                glVertex(*xyz)
            
        glEnd()        
        glEndList()                                
                        

    def draw_surface(self,c,t,h,n):        
        self.can.glSetCurrent()
        r = 1 / c if c else 1e5
        n += 1

        #draw part of lens surface
        b = np.sqrt(r**2 - h**2) if h**2 < r**2 else 0.0
        a = r - b  if r > 0 else r + b
        inc = a / n        
        
        #calc lens shape
        y = range(n)
        x  = [(i*inc + t) for i in range(n)]
        x2 = [(i*inc - r)*(i*inc - r) for i in range(n)]                
        r2 = r*r 
        for i in range(n):
            y[i] = np.sqrt(r2 - x2[i]) if x2[i] < r2 else 0.0
              
        for theta in range(0,359,180):      
            p = theta * np.pi / 180.0
            glBegin(GL_LINE_STRIP)    

            for i in range(n):
                glVertex3f(x[i],y[i] * cos(p),y[i]*sin(p))            
            glEnd()
        
        glColor(1,1,1,.25)    
        glBegin(GL_LINE_STRIP)    
        for theta in range(0,365,5):      
            p = theta * np.pi/180.0
            

            i = n-1

            glVertex3f(x[i],y[i] * cos(p),y[i]*sin(p))            

        glEnd()
        glColor(*self._lensSurfaceColor)
              
        return x[i], y[i]
    
    
    
    def draw_lenses(self,t,surf,t_cum,c,n,h,
                    colors=None,
                    stop_index=None):
        if colors is None:
            colors = [self._lensSurfaceColor] * len(t)
        self.can.glSetCurrent()
        self.clear_list()
        z = [0] * self.rows
        for i in range(len(surf)):
            glNewList(self.glListStart + surf[i], GL_COMPILE_AND_EXECUTE)        
            glColor(1.0,1.0,1.0)
            if i == 0: # Optical axis(?)
                glBegin(GL_LINES)
                glVertex(0,0,0)
                glVertex(t_cum[-1],0,0)
                glEnd()        
        
            glColor(*colors[i])
            isFlatSameMat = (c[i] == 0 and (i == 0 or n[i-1] == n[i]))
            if i == stop_index and isFlatSameMat:
                z[i] = np.array((t_cum[i], h[i]))
            else:
                z[i] = self.draw_surface(c[i], t_cum[i], h[i], 10)
            if i > 0 and n[i-1] != 1: # Draw lens edges to previous surface?
                glBegin(GL_LINES)

                glVertex3f(float(z[i-1][0]),float(z[i-1][1]),0)
                glVertex3f(float(z[i][0])  ,float(z[i][1]),  0)

                glVertex3f(float(z[i-1][0]),-float(z[i-1][1]),0)
                glVertex3f(float(z[i][0]),  -float(z[i][1]),  0)

                glEnd()
            if i == stop_index:
                glBegin(GL_LINES)
                Y, Z = z[i]
                d = Z * 0.1 # Edge length
                for sgn in (-1, 1):
                    glVertex(Y, Z*sgn); glVertex(Y, (Z + d)*sgn)
                    glVertex(Y-d/2, Z*sgn); glVertex(Y+d/2, Z*sgn)
                glEnd()
                    
            glEndList()
        
        self.reset_view()
