#Boa:MDIChild:wxMDIChildFrame_spot_diagram
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
from myCanvas import *
#import math
from ray_trace import *
from Numeric import *


def create(parent):
    return wxMDIChildFrame_spot_diagram(parent)

[wxID_WXMDICHILDFRAME_SPOT_DIAGRAM] = map(lambda _init_ctrls: wxNewId(), range(1))

class wxMDIChildFrame_spot_diagram(wx.MDIChildFrame):
    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=wxID_WXMDICHILDFRAME_SPOT_DIAGRAM,
              name='wxMDIChildFrame_spot_diagram', parent=prnt, pos=wx.Point(368,
              368), size=wx.Size(991, 713), style=wx.DEFAULT_FRAME_STYLE,
              title='Spot Diagram')
        self._init_utils()
        self.SetClientSize(wx.Size(983, 679))
        self.Bind(EVT_CLOSE,self.OnWxmdichildframe_spot_diagramClose)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.can = myCanvas(self)
        self.Show()
        self.can.glSetCurrent()
        self.can.set_bg_color([0.0,0.0,0.0])


        self.rays = 5
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)
        
        self.y_ave = 0.0
        self.can.Rotateable(False)
        

    
            
    def comp_rays(self,Yi,Zi,pos,t,n,c,t_cum,h):        
        (xi,yi,zi) = pos                        
        xs = []
        ys = []
        zs = []
        Xs = []
        Ys = []
        Zs = []
        
        cnt = 0
        for j in Yi:
            for k in Zi:                       
                i = pow(1.0 - j*j - k*k,0.5)                
                (x,y,z,X,Y,Z) = skew_ray((xi,yi,zi),(i,j,k),t,n,c,t_cum,h)
##                self.GetParent().ogl.draw_ray(x,y,z,cnt,t_cum,color = [0.0,1.0,0.0])
                cnt+=1
                if(len(x) > len(t)):
                    xs.append(x[len(x)-1])
                    ys.append(y[len(y)-1])
                    zs.append(z[len(z)-1])    
                    Xs.append(X[len(X)-1])                
                    Ys.append(Y[len(Y)-1])                
                    Zs.append(Z[len(Z)-1])                
                    
        return (array(xs),array(ys),array(zs),array(Xs),array(Ys),array(Zs))
        
    def clear_list(self):
        self.can.glSetCurrent()
        glDeleteLists(self.glRayListStart,self.rays)                
        self.glRayListStart = glGenLists(self.rays)
        self.rayList = range(self.glRayListStart,self.glRayListStart+self.rays)        
        self.can.set_ray_list(self.rayList)
        self.can.DrawGL()
        
    def draw_spots(self, t, n, c, t_cum, h,object_height):
        self.can.glSetCurrent()                      
        self.clear_list()    
        
        angles = 20
        cnt = self.glRayListStart    
        
        #precalc ray locations
        pos = array([0.0,.7071,1.0])
        pos = -object_height * pos
        z_launch = 0
        
        y_hit = array([i for i in range(-angles,angles+1)],Float32) * h[1]/angles
        z_hit = y_hit
        offset_y = 0
        max_y = []
        min_y = []
        max_z = []
        min_z = []
        width_y = []
        width_z = []
        
        x = []
        y = []
        z = []
        X = []
        Y = []
        Z = []
        original_t = t[len(t)-1]
        t_temp = t
        
        #for jj in range(-2,3):
            #delta = 0.5 * jj            
        #t_temp[len(t)-1] = original_t + delta
        #print t_temp,t,delta
            
        for i in range(len(pos)):
            y_launch = pos[i]
            yy = y_hit - y_launch 
            zz = z_hit - z_launch 
            xx2 = t[0]*t[0]
            den = (pow(zz*zz + yy*yy + xx2,0.5)) 
            Yi = yy / den
            Zi = zz / den
                                                            
                
            (xs,ys,zs,Xs,Ys,Zs) = self.comp_rays(Yi,Zi,(0.0,y_launch,0.0),t_temp,n,c,t_cum,h)                
            
            x.append(xs)                
            y.append(ys)
            z.append(zs)
            X.append(Xs)
            Y.append(Ys)
            Z.append(Zs)
                            
            if(len(y[i]) > 0 and len(z[i]) > 0):
                max_y.append(max(y[i]))
                min_y.append(min(y[i]))                            
                width_y.append(max_y[len(max_y)-1] - min_y[len(min_y)-1])
            
                max_z.append(max(z[i]))
                min_z.append(min(z[i]))
                width_z.append(max_z[len(max_z)-1] - min_z[len(min_z)-1])
            
            #print max_y,min_y,max_z,min_z
        
        max_height = max(array(width_y))
        max_width  = max(array(width_z))
        offset_y   = max_width * 2 * (-1 + array(range(len(max_y)))) - ((array(max_y) + array(min_y))/2)
        offset_z   = 0.0#max_width * 2 #* (-1 + array(range(len(pos)))) - ((array(max_z) + array(min_z))/2)

        
        for i in range(len(max_y)): 
            glNewList(cnt, GL_COMPILE_AND_EXECUTE)
            if(len(z[i]) >  len(max_y)):
                self.spots(z[i] + offset_z , y[i] + offset_y[i], color = [1.0,1.0,1.0])   
            glEndList()
            cnt += 1

##        max_y = []
##        min_y = []
##        max_z = []
##        min_z = []
##        width_y = []
##        width_z = []
    
        self.can.set_k(6*(max_height-min(array(min_y))))
        self.can.DrawGL()
        #self.Refresh(False)           
        
    
    def spots(self,x,y,color):
        self.can.glSetCurrent()                  
        glColorf(color[0],color[1],color[2])                
        
        glBegin(GL_POINTS)        
        [glVertexf(x[i],y[i]) for i in range(len(x))]
        glEnd()        
        glFlush()
        
        

    def OnWxmdichildframe_spot_diagramClose(self, event):
        self.Hide()
    