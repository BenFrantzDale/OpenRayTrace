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


from myGLCanvas import *

import cmath
#from Numeric import *
import math



class myCanvas(myGLCanvas):
    def __init__(self,parent):
        myGLCanvas.__init__(self,parent)

        self.WIDTH, self.HEIGHT = 400, 300
        
        #self.gl_list    = []
        self.lens_list = []
        self.ray_list  = []              
        self.color = [0,0,0]

    def InitGL(self):
        self.glSetCurrent()          
        glViewport(0, 0, self.WIDTH, self.HEIGHT)  #setup the view port

        glClearDepth (0.0) #don't really know
        glDisable (GL_DEPTH_TEST)  #disable the gl_depth_test
         
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glEnable (GL_LINE_SMOOTH);

        glEnable (GL_BLEND);

        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE);

            
        self.reset_view()                
        self.reset_view()
        self.Refresh(False)

    def set_list(self,l):
        self.glSetCurrent()    
        self.gl_list = l
                                    
    def set_lens_list(self,l):
        self.glSetCurrent()  
        self.lens_list = l
        
    def set_ray_list(self,l):
        self.glSetCurrent()  
        self.ray_list = l
        
        
    def set_bg_color(self,color):
        self.glSetCurrent()  
        self.color = color
        
    def DrawGL(self):
        self.glSetCurrent()  
        glClearColor(self.color[0],self.color[1],self.color[2], 0.0)
        glClear(GL_COLOR_BUFFER_BIT)
                        
        glMatrixMode(GL_MODELVIEW)
    
        #print self.lens_list
        [glCallList(self.lens_list[i]) for i in range(len(self.lens_list))]
        [glCallList(self.ray_list[i]) for i in range(len(self.ray_list))]        
            
        glFlush()
        self.SwapBuffers() 
    
    def glSetCurrent(self):
        try:
        
            self.SetCurrent()
        except:
            pass
