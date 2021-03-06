# OpenRayTrace.UI.Frames.Aberrations
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





from OpenRayTrace.UI.myCanvas import *
from OpenRayTrace.ray_trace import *

import wx
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Aberrations(wx.MDIChildFrame):
    wxID = wx.NewId()
    #def _init_utils(self): pass

    def _init_ctrls(self, prnt):
        wx.MDIChildFrame.__init__(self, id=self.wxID,
                                  name='Aberrations', parent=prnt, pos=wx.Point(399,218), 
                                  size=wx.Size(1200, 854), style=wx.DEFAULT_FRAME_STYLE,
                                  title='Aberrations')
        self.SetClientSize(wx.Size(1192, 820))
        self.Center(wx.BOTH)
        EVT_CLOSE(self, self.OnClose)

    def __init__(self, parent):
        self._init_ctrls(parent)                                
        self.can = myCanvas(self)
        self.Show()
        self.can.glSetCurrent()
        self.can.set_bg_color([0.0,0.0,0.0])



        self.rays = 1000
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)        
        
        self.y_ave = 0.0
        self.can.Rotateable(False)
        
    def clear_list(self):
        self.can.glSetCurrent()
        glDeleteLists(self.glRayListStart,self.rays)                
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)
        self.can.DrawGL()
                
    def calc_abr(self,t,n,c,t_cum,h,object_height):               
        self.clear_list()
        
        angles = 20
        
        Hp     = [] # zeros(2*angles+1,Float)
        tanUp  = [] # zeros(2*angles+1,Float)
        r      = [] #zeros(2*angles+1,Float)
        
        ray = self.glRayListStart
                        
        pos = np.array([0.0,0.7071,1.0])
        pos = -object_height * pos
        title = ['On Axis SPA',str(pos[1]) + 'mm SPA ', str(pos[2]) + 'mm SPA ']
        cnt = 0
                
        y_hit = np.array([i*h[1]/angles for i in range(-angles,angles+1)],dtype=float)
        
        for i in range(len(pos)):  
            p    = pos[i]
            cnt += 1
            ray += 1
                                    
            y_launch = pos[i]
            yy = y_hit - y_launch
            den = (pow(yy*yy + t[0]*t[0],0.5)) 
            Yi = yy / den            
            Xi = pow(1 - Yi*Yi,0.5)
            
            
            for j in range(len(Yi)):                
                (x,y,z,X,Y,Z) = skew_ray((0.0,p,0.0),(Xi[j],Yi[j],0.0),t,n,c,t_cum,h)                                
#                self.GetParent().ogl.draw_ray(x,y,z,j,t_cum,color = [0.0,1.0,1.0])
                                
                if(len(y) == len(t) + 1):                                       
                    Hp.append(y[len(y)-1])
                    tanUp.append(tan(arcsin(Y[len(y)-1])))
                    r.append(y[1])
                                                                                            
            if(cnt == 1 and len(Hp) > 0):
                mx = np.max(Hp)
                #print Hp,tanUp      
                LA = []
                for i in range(len(Hp)):
                    if(tanUp[i] != 0.0):
                        LA.append(-1 * np.array(Hp[i])/np.array(tanUp[i]))
                    else:
                        LA.append(0)
                                                
                self.plotxy(LA,np.array(r),(2, 0),'LA',ray, color = (0.8,0.2,0.2))
                ray += 1
                
            ##print r,Hp
            if(len(Hp) > 0):
                self.plotxy(y_hit,np.array(Hp),(0,0),title[cnt-1],ray,color = (0.2,0.8,0.2))
            Hp = []
            tanUp = []
            r = []
            self.can.DrawGL()
            
                        
    
    
    def plotxy(self,x,y, offset, title, ray, color):              
        self.can.glSetCurrent()
        
        mxy = max(y)
        mny = min(y)
        
        mxx = max(x)
        mnx = min(x)                
        
        rngx = mxx - mnx
        rngy = mxy - mny
                
        glNewList(ray, GL_COMPILE)              
        glTranslatef(offset[0],offset[1],0)
        glColorf(*color)
        x_norm = np.array(x)/rngx
        y_norm = np.array(y)/rngy

        mxy = np.max(y_norm)
        mny = np.min(y_norm)
        
        mxx = np.max(x_norm)
        mnx = np.min(x_norm)                
          
                                    
        glBegin(GL_LINE_STRIP)       
        for i in range(len(y)):
            glVertexf(x_norm[i],y_norm[i])                     
        glEnd()        
                
        
        #draw Axes
        glColorf(1.0,1.0,1.0,1.0)                    
        
                
        glBegin(GL_LINES) 
        yc = 0.0 #(mxy+mny)/2.0     
        glVertexf(mnx,yc)
        glVertexf(mxx,yc)                     

        
        if(mny > 0):
            glVertexf(0.0,0.0)    
        else:
            glVertexf(0.0,mny)
        
        glVertexf(0.0,mxy)                            
        glEnd()                
        
        glColorf(1,1,1,1.0)
        glRasterPos3f(x_norm[0] - .01,y_norm[0]-.01,0.0)
        num = '( '+str(x[0])+' , '+str(y[0]) +  ' )'
        [glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12,ord(ii)) for ii in num]        
        
        glRasterPos3f(x_norm[len(x_norm)-1] - .01,y_norm[len(y_norm)-1]-.01,0.0)
        num = '( '+str(x[len(x)-1])+' , '+str(y[len(y)-1]) +  ' )'
        [glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12,ord(ii)) for ii in num]        
        
        glRasterPos3f(x_norm[len(x_norm)-1] - .01,y_norm[len(y_norm)-1]-.05,0.0)
        num = title
        [glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12,ord(ii)) for ii in num]        
                                                                    

        glTranslatef(-offset[0],-offset[1],0)        
        glFlush()
        glEndList()

    def OnClose(self, event): self.Hide()
