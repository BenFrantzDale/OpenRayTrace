#OpenRayTrace.UI.frames.Image

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
from OpenRayTrace.ray_trace import *

import math
import numpy as np
import random
from numpy.linalg import norm



class Image(wx.MDIChildFrame):
    wxID = wx.NewId()
    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=self.wxID,
                                  name='Image', parent=prnt, pos=wx.Point(348, 145),
                                  size=wx.Size(1200, 854), style=wx.DEFAULT_FRAME_STYLE,
              title='Image Trace')
        self._init_utils()
        self.SetClientSize(wx.Size(1192, 820))
        self.Bind(EVT_CLOSE, self.OnClose)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.can = myCanvas(self)
        self.Show()
        self.can.glSetCurrent()
        self.can.set_bg_color([0.0,0.0,0.0])
        self.rays = 10
        self.__listsInitialized = False
        self.can.glSetCurrent()
        self.__initializeLists()

    def __initializeLists(self):
        if self.__listsInitialized: return
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)        
        random.seed()
        self.can.Rotateable(False)
        self.__listsInitialized = True
        
    def clear_list(self):
        self.can.glSetCurrent()
        self.__initializeLists()
        glDeleteLists(self.glRayListStart,self.rays)                
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)
        self.can.DrawGL()
        
    def draw_image(self,img,height,t,n,c,t_cum,h):
        self.can.glSetCurrent()          
        self.clear_list()
        
        (rows,cols) = img.shape                
        width = height * cols / rows                
        
        img_ypos = height /(rows-1) * np.array([(i - (rows-1.0)/2.0) for i in range(rows)])        
        img_zpos = width / (cols-1) * np.array([(i - (cols-1.0)/2.0) for i in range(cols)])
            
        cell_width = width/(cols-1.0)
        cell_height = height/(rows-1.0)        
                       
        rays_per_cell = 20
        cnt = self.glRayListStart    
        max_y = -1E8
        min_y = 1E8
        max_z = -1E8
        min_z = 1E8
        
        ylch = []
        zlch = []
        clch = []

        glNewList(cnt, GL_COMPILE)
        for i in range(rows):           
            for j in range(cols):                
                if img[i,j] != 0:
                    for k in range(rays_per_cell):                                                                                            
                        z_launch = random.uniform(img_zpos[j] - cell_width/2.0,img_zpos[j] + cell_width/2.0)
                        y_launch = random.uniform(img_ypos[i] - cell_height/2.0,img_ypos[i] + cell_height/2.0)
                                                                        
                        y_hit = random.uniform(-h[1],h[1])                        
                        zl = np.sqrt(h[1]**2 - y_hit**2)
                        z_hit = random.uniform(-zl,zl)
                                            
                        yy = y_hit - y_launch 
                        zz = z_hit - z_launch 
                        xx2 = t[0]**2
                        Yi = yy / norm([t[0], yy, zz])
                        Zi = zz / norm([t[0], yy, zz])
                        Xi = np.sqrt(1.0 - Yi**2 - Zi**2)
                             
                        x,y,z,X,Y,Z = skew_ray((0,y_launch,z_launch),(Xi,Yi,Zi),t,n,c,t_cum,h)                                                
                        
                        max_y = max(y[-1],max_y)
                        max_z = max(z[-1],max_z)
                        min_y = min(y[-1],min_y)
                        min_z = min(z[-1],min_z)
                        
                        ylch.append(y_launch)
                        zlch.append(z_launch)
                        clch.append([img[i,j],img[i,j],img[i,j]])
                        
                        if len(x) > 2:
                            self.spots(x[-1],y[-1],z[-1],color=[img[i,j],img[i,j],img[i,j]])
                            
                           
        for i in range(len(ylch)):
            self.spots(0, ylch[i], zlch[i] + np.ceil(min_z)*1.5, clch[i])

        cnt +=1
                
        glEndList()

        #print max_y,min_y,max_z,min_z
        self.can.K = math.ceil(2*(max_y - min_y))
        self.can.DrawGL()
        
                    
    def spots(self,x,y,z,color):
        self.can.glSetCurrent()  
        
        #glNewList(ray, GL_COMPILE_AND_EXECUTE)      
        glColor(color[0],color[1],color[2])                
        
        glBegin(GL_POINTS)                  
        #glVertexf(x[len(x)-1],y[len(x)-1],z[len(x)-1])                     
        glVertex(z,y)                     
        glEnd()        
        glFlush()        
        #glEndList()

    def OnClose(self, event): self.Hide()

