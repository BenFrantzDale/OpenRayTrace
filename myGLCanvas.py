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
from wxPython.glcanvas import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import cmath
from Numeric import *
import math

          
class myGLCanvas(wxGLCanvas):
    def __init__(self, parent):
        wxGLCanvas.__init__(self,parent,-1)
                
        self.init = False
        
        EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        EVT_SIZE(self,self.OnSize)
        EVT_PAINT(self,self.OnPaint)        
        #EVT_IDLE(self,self.OnIdle)
        EVT_LEFT_DOWN(self,self.OnMouseDown)
        EVT_LEFT_UP(self,self.OnMouseUp)
        EVT_MIDDLE_DOWN(self,self.OnMouseDown)
        EVT_MIDDLE_UP(self,self.OnMouseUp)
        EVT_RIGHT_DOWN(self,self.OnMouseDown)
        EVT_RIGHT_UP(self,self.OnMouseUp)
        EVT_MOTION(self, self.OnMouseMotion)
        
        self.K = 1.0
        self.rotatable = True
        self.centered = True
        self.x = 0
        self.y = 0
        

    def OnEraseBackground(self, event):
        self.SetCurrent()  
        pass # Do nothing, to avoid flashing on MSW.
    
    def OnSize(self, event = NULL):
        self.SetCurrent()  
        size = self.GetClientSize()
        
        (self.WIDTH,self.HEIGHT) = size

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()    
        
        if(self.centered):            
            glOrtho(-1.1*self.K/2.0,1.1*self.K/2.0, -1.1*self.K * self.HEIGHT/self.WIDTH/2,1.1*self.K*self.HEIGHT/self.WIDTH/2,-self.K,self.K)
        else:
            glOrtho(-.1*self.K,1.1*self.K, -1.1*self.K * self.HEIGHT/self.WIDTH/2,1.1*self.K*self.HEIGHT/self.WIDTH/2,-self.K,self.K)
        
        glMatrixMode(GL_MODELVIEW)

        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, self.WIDTH, self.HEIGHT)        
        glFlush()
        self.Refresh(False)
        
            
    def OnPaint(self, event=NULL):
        self.SetCurrent()  
        dc = wxPaintDC(self)
        self.SetCurrent()

        if not self.init:            
            self.InitGL()
            self.init = True
        self.DrawGL()
        self.SetCurrent()  
    
    def Rotateable(self,r):
        self.rotatable = r
    
##    def OnIdle(self,evt):
##        self.SetCurrent()  
##        self.Refresh(False) 

    def OnMouseMotion(self, evt):
        self.SetCurrent()  
        if evt.Dragging():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()

            if evt.MiddleIsDown() and self.rotatable:
                                
                self.yspin = float(self.x - self.lastx)
                self.xspin = float(self.y - self.lasty)


                #glMatrixMode(GL_PROJECTION)
                #glLoadIdentity()        

                glMatrixMode(GL_MODELVIEW);
                mat = glGetDoublev(GL_MODELVIEW_MATRIX);
                glLoadIdentity();
                t = self.K/2
                glTranslatef(-t,
                             0.0,
                             0.0);
                glMultMatrixd(mat);
                self.Refresh(False)


                glMatrixMode(GL_MODELVIEW)
                mat = glGetFloatv(GL_MODELVIEW_MATRIX)
                glLoadIdentity()
                glRotated(self.yspin, 0.0, 1.0, 0.0)
                glRotated(self.xspin, 1.0, 0.0, 0.0)
                glMultMatrixd(mat)                
                self.Refresh(False)

                glMatrixMode(GL_MODELVIEW);
                mat = glGetDoublev(GL_MODELVIEW_MATRIX);
                glLoadIdentity();
                glTranslatef(t ,
                             0.0,
                             0.0);
                glMultMatrixd(mat);
                self.Refresh(False)

                
            if evt.LeftIsDown():

                
##                self.distance -=  20  * (self.y - self.lasty)/float(self.WIDTH)
####                
                self.d =  1 + (self.y - self.lasty)/100.0;#/float(self.WIDTH)
                #print self.distance

                glMatrixMode(GL_MODELVIEW)
                mat = glGetFloatv(GL_MODELVIEW_MATRIX)
                glLoadIdentity()
                #glTranslatef(-self.d,0,0)
                glScalef(self.d,
                         self.d,
                         self.d);
                #glTranslatef(self.K/2,0,0)
                glMultMatrixd(mat)                
                self.Refresh(False)
                
                #glLoadIdentity();
####
####                self.Refresh(False)
##
##
##
##                
####                glMatrixMode(GL_PROJECTION)         
####                if(self.lastx - self.x > 0):
####                    d = 0.1
####                else:
####                    d = -0.1
####                
####                print d
####                glTranslatef(0.0,0.0,d)                
####                self.Refresh(False)
##                
##                glPushMatrix()         
##                glMatrixMode(GL_PROJECTION)
##                           
##                glLoadIdentity()
##                glOrtho(0,0,self.WIDTH,self.HEIGHT,0,1)
##                
##                glMatrixMode(MODELVIEW)
##                glLoadIdentity()
##                #gluPerspective(45, float(self.WIDTH)/float(self.HEIGHT), 0, 10.0)
##
##                gluLookAt(0.0, 0.0 ,self.distance,
##                          0.,0.,0.,
##                          0.,1.,0.)
##
##                glMatrixMode(GL_MODELVIEW);
##                glFlush()
##                self.Refresh(False)
##                glPopMatrix()

            if evt.RightIsDown():                    
                glMatrixMode(GL_MODELVIEW);
                mat = glGetDoublev(GL_MODELVIEW_MATRIX);
                glLoadIdentity();
                glTranslatef(1.2*self.K * (self.x - self.lastx)/self.WIDTH,                             
                             1.1/2.0*self.K * (self.lasty-self.y)/self.WIDTH,
                             0.0);
                glMultMatrixd(mat);
                self.Refresh(False)
                
    def OnMouseDown(self, evt):
        self.SetCurrent()  
        self.x,self.y = evt.GetPosition()
        self.CaptureMouse()

    def OnMouseUp(self, evt):
        self.SetCurrent()  
        self.lastx = self.x
        self.lasty = self.y
        self.ReleaseMouse()

    
    def set_k(self,k):
        self.SetCurrent()  
        self.K = k
        self.reset_view()
        
        
    def reset_view(self):        
        self.SetCurrent()  
        size = self.GetClientSize()
        (self.WIDTH,self.HEIGHT) = size
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                
        if(self.centered):            
            glOrtho(-1.1*self.K/2.0,1.1*self.K/2.0, -1.1*self.K * self.HEIGHT/self.WIDTH/2,1.1*self.K*self.HEIGHT/self.WIDTH/2,-self.K,self.K)
        else:
            glOrtho(-.1*self.K,1.1*self.K, -1.1*self.K * self.HEIGHT/self.WIDTH/2,1.1*self.K*self.HEIGHT/self.WIDTH/2,-self.K,self.K)

        #glOrtho(-.1*self.K,1.1*self.K,-1.1*self.K * self.HEIGHT/self.WIDTH/2,1.1*self.K*self.HEIGHT/self.WIDTH/2,-self.K,self.K)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.GetContext():
            self.SetCurrent()
            glViewport(0, 0, self.WIDTH, self.HEIGHT)        
        glFlush()
        self.Refresh(False)
