#Boa:MDIChild:wxMDIChildFrame_image

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
import math
from ray_trace import *
from Numeric import *
import random
from scipy import *


def create(parent):
    return wxMDIChildFrame_image(parent)

[wxID_WXMDICHILDFRAME_IMAGE] = map(lambda _init_ctrls: wxNewId(), range(1))

class wxMDIChildFrame_image(wxMDIChildFrame):
    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxMDIChildFrame.__init__(self, id=wxID_WXMDICHILDFRAME_IMAGE,
              name='wxMDIChildFrame_image', parent=prnt, pos=wxPoint(348, 145),
              size=wxSize(1200, 854), style=wxDEFAULT_FRAME_STYLE,
              title='Image Trace')
        self._init_utils()
        self.SetClientSize(wxSize(1192, 820))
        EVT_CLOSE(self, self.OnWxmdichildframe_imageClose)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.can = myCanvas(self)
        self.can.SetCurrent()
        self.can.set_bg_color([0.0,0.0,0.0])


        self.rays = 10
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)        
        random.seed()
        self.can.Rotateable(False)
        
        
    def clear_list(self):
        self.can.SetCurrent()
        glDeleteLists(self.glRayListStart,self.rays)                
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)
        self.can.DrawGL()
        
    def draw_image(self,img,height,t,n,c,t_cum,h):
        self.can.SetCurrent()          
        self.clear_list()
        
        (rows,cols) = img.shape                
        width = height * cols / rows                
        
        img_ypos = height /(rows-1) * array([(i - (rows-1.0)/2.0) for i in range(rows)])        
        img_zpos = width / (cols-1) * array([(i - (cols-1.0)/2.0) for i in range(cols)])
            
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
        
        glNewList(cnt,GL_COMPILE)
        for i in range(rows):           
            for j in range(cols):                
                if(img[i,j] != 0):                    
                    for k in range(rays_per_cell):                                                                                            
                        z_launch = random.uniform(img_zpos[j] - cell_width/2.0,img_zpos[j] + cell_width/2.0)
                        y_launch = random.uniform(img_ypos[i] - cell_height/2.0,img_ypos[i] + cell_height/2.0)
                                                                        
                        y_hit = random.uniform(-h[1],h[1])                        
                        zl = pow(h[1]*h[1] - y_hit*y_hit,0.5)                        
                        z_hit = random.uniform(-zl,zl)
                                            
                        yy = y_hit - y_launch 
                        zz = z_hit - z_launch 
                        xx2 = t[0]*t[0]
                        Yi = yy / (pow(zz*zz + yy*yy + xx2,0.5)) 
                        Zi = zz / (pow(zz*zz + yy*yy + xx2,0.5)) 
                        Xi = pow(1.0 - Yi*Yi - Zi*Zi,0.5)           
                             
                        (x,y,z,X,Y,Z) = skew_ray((0,y_launch,z_launch),(Xi,Yi,Zi),t,n,c,t_cum,h)                                                
                        
                        max_y = max(y[len(y)-1],max_y)
                        max_z = max(z[len(z)-1],max_z)
                        min_y = min(y[len(y)-1],min_y)
                        min_z = min(z[len(z)-1],min_z)
                        
                        ylch.append(y_launch)
                        zlch.append(z_launch)
                        clch.append([img[i,j],img[i,j],img[i,j]])
                        
                        if(len(x) > 2):                            
                            self.spots(x[len(x)-1],y[len(y)-1],z[len(z)-1],color=[img[i,j],img[i,j],img[i,j]])
                            
                           
        for i in range(len(ylch)):
            self.spots(0,ylch[i],zlch[i] + ceil(min_z)*1.5 ,clch[i])

        cnt +=1
                
        glEndList()

        #print max_y,min_y,max_z,min_z
        self.can.set_k(math.ceil(2*(max_y-min_y)))
        self.can.DrawGL()
        
                    
    def spots(self,x,y,z,color):
        self.can.SetCurrent()  
        
        #glNewList(ray, GL_COMPILE_AND_EXECUTE)      
        glColorf(color[0],color[1],color[2])                
        
        glBegin(GL_POINTS)                  
        #glVertexf(x[len(x)-1],y[len(x)-1],z[len(x)-1])                     
        glVertexf(z,y)                     
        glEnd()        
        glFlush()        
        #glEndList()

    def OnWxmdichildframe_imageClose(self, event):
        self.Hide()

def transpose(v):
    (a,b) = v.shape
    return array([v[:,i] for i in range(b)])