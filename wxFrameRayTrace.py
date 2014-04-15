#Boa:Frame:wxFrameRayTrace

from GridCustTable import *
from wx import *
from wxgrid import *
from myCanvas import *
from lens import *
import os, string
from cmath import *
from math  import *

WIDTH=640.0
HEIGHT=480.0

FLENGTH = 0
POWER = 1
CURVATURE = 2
RADIUS = 3
THICKNESS = 4
APERATURE_RADIUS = 5
GLASS = 6


def create(parent):
    return wxFrameRayTrace(parent)

[wxID_WXFRAMERAYTRACE, wxID_WXFRAMERAYTRACEBUTTON_QUIT, 
 wxID_WXFRAMERAYTRACECHECKBOX_AUTOFOCUS, wxID_WXFRAMERAYTRACEGRID1, 
 wxID_WXFRAMERAYTRACERADIOBUTTON_CONST_POWER, 
 wxID_WXFRAMERAYTRACERADIOBUTTON_CONST_RADIUS, 
 wxID_WXFRAMERAYTRACESTATICTEXT_PARAXIAL_FOCUS, 
 wxID_WXFRAMERAYTRACESTATICTEXT_PF, 
] = map(lambda _init_ctrls: wx.NewId(), range(8))

class wxFrameRayTrace(wxFrame):
    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxFrame.__init__(self, id=wxID_WXFRAMERAYTRACE, name='wxFrameRayTrace',
              parent=prnt, pos=wx.Point(501, 238), size=wx.Size(1032, 814),
              style=wxMAXIMIZE_BOX | wxMINIMIZE_BOX | wxRESIZE_BORDER | wxSYSTEM_MENU | wxSTAY_ON_TOP | wxDEFAULT_FRAME_STYLE,
              title='PyRayTrace')
        self._init_utils()
        self.SetClientSize(wx.Size(1024, 780))
        self.Center(wxBOTH)
        EVT_SIZE(self, self.OnWxframeopenmodalSize)

        self.button_Quit = wxButton(id=wxID_WXFRAMERAYTRACEBUTTON_QUIT,
              label='Quit', name='button_Quit', parent=self, pos=wx.Point(880,
              0), size=wx.Size(144, 48), style=0)
        EVT_BUTTON(self.button_Quit, wxID_WXFRAMERAYTRACEBUTTON_QUIT,
              self.OnButton_quitButton)

        self.grid1 = wxGrid(id=wxID_WXFRAMERAYTRACEGRID1, name='grid1',
              parent=self, pos=wx.Point(0, 536), size=wx.Size(1024, 240),
              style=0)
        EVT_GRID_CELL_CHANGE(self.grid1, self.OnGrid1GridCellChange)

        self.radioButton_const_power = wxRadioButton(id=wxID_WXFRAMERAYTRACERADIOBUTTON_CONST_POWER,
              label='Const Power/F-length', name='radioButton_const_power',
              parent=self, pos=wx.Point(848, 264), size=wx.Size(79, 13), style=0)
        self.radioButton_const_power.SetValue(True)
        EVT_RADIOBUTTON(self.radioButton_const_power,
              wxID_WXFRAMERAYTRACERADIOBUTTON_CONST_POWER,
              self.OnRadiobutton_const_powerRadiobutton)

        self.radioButton_const_radius = wxRadioButton(id=wxID_WXFRAMERAYTRACERADIOBUTTON_CONST_RADIUS,
              label='Const Radius', name='radioButton_const_radius',
              parent=self, pos=wx.Point(848, 288), size=wx.Size(79, 13), style=0)
        self.radioButton_const_radius.SetValue(False)
        EVT_RADIOBUTTON(self.radioButton_const_radius,
              wxID_WXFRAMERAYTRACERADIOBUTTON_CONST_RADIUS,
              self.OnRadiobutton_const_radiusRadiobutton)

        self.staticText_pf = wxStaticText(id=wxID_WXFRAMERAYTRACESTATICTEXT_PF,
              label='Paraxial Focus', name='staticText_pf', parent=self,
              pos=wx.Point(848, 312), size=wx.Size(69, 13), style=0)

        self.staticText_paraxial_focus = wxStaticText(id=wxID_WXFRAMERAYTRACESTATICTEXT_PARAXIAL_FOCUS,
              label='', name='staticText_paraxial_focus', parent=self,
              pos=wx.Point(928, 312), size=wx.Size(0, 13), style=0)

        self.checkBox_autofocus = wxCheckBox(id=wxID_WXFRAMERAYTRACECHECKBOX_AUTOFOCUS,
              label='Autofocus (paraxial)', name='checkBox_autofocus',
              parent=self, pos=wx.Point(848, 336), size=wx.Size(120, 13),
              style=0)
        self.checkBox_autofocus.SetValue(False)

    def __init__(self, parent):
        self._init_ctrls(parent)
                
        self.can = myCanvas(self)
        self.can.SetSize((WIDTH,HEIGHT))
        
        self.rows = 40
        col_label = ['f-length  ','power    ','curvature    ','radius   ','thickness    ','aperature radius ','glass    ']
        self.grid1.CreateGrid(self.rows,len(col_label))
        [self.grid1.SetColLabelValue(i,col_label[i]) for i in range(len(col_label))]
        self.grid1.SetDefaultCellAlignment(wxALIGN_CENTRE,wxALIGN_CENTRE)
        self.grid1.AutoSizeRow(True)
        self.grid1.AutoSizeColumns(True)
                

        for row in range(self.rows):
            for col in range(len(col_label)):
                self.grid1.SetCellEditor(row, col, apply(wxGridCellFloatEditor,[]))

            


        self.glListStart = glGenLists(self.rows + 1) 

        self.n = []
        self.c = []
        self.t = []
        
        self.rays = 10
        self.glRayListStart = glGenLists(self.rays) 
              
            
        self.hold_power = self.radioButton_const_power.GetValue()        
        self.hold_radius = self.radioButton_const_radius.GetValue()        

        self.Layout()
        self.Centre()
        
    def OnWxframeopenmodalSize(self, event):
        self.Layout()
        self.Centre()

    def OnButton_quitButton(self, event):        
        self.Destroy()

                

    def OnGrid1GridCellChange(self, event):
        r = event.GetRow()
        c = event.GetCol() 
        val = float(self.grid1.GetCellValue(r,c))
        
        if(type(val) == type(1.1)):                        
            draw = self.fill_in_values(r,c,val)            
            self.update_display()                            


            #compute paraxial focus
            y = 0.0
            u = 1.0
            l = self.paraxial_ray(y,u)
            self.staticText_paraxial_focus.SetLabel(str(l))
            
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
            Up  = [0 for i in range(self.rays)]
            LAp = [0 for i in range(self.rays)]
            Hp  = [0 for i in range(self.rays)]
            cnt = 0
            
            if((draw == True) and (len(self.t) > 1)):                                
                rayList = range(self.glRayListStart, self.glRayListStart + self.rays)
                                
                for i in range(-self.rays/2+1, self.rays/2):
                    #go to aperature radius
                    
                    Yi = (i/(self.rays/2.0)) * atan(self.h[1]/self.t[0])                    
                    Zi = 0.0                
                    Xi =  pow(1.0 - Yi*Yi - Zi*Zi, 0.5)
                    (x[i],y[i],z[i],X[i],Y[i],Z[i]) = self.skew_ray((0,0,0),(Xi,Yi,Zi))                                


                    self.draw_ray(x[i],y[i],z[i],self.glRayListStart + cnt)
                    cnt+=1
                
                    Hp[i] = -y[i][len(y[i])-1]
                    Up[i] = asin(Y[i][len(Y[i])-1])
                    if(Up[i] != 0):
                        LAp[i] = -Hp[i]/tan(Up[i])
                self.can.set_ray_list(rayList)
                
                #print Up, LAp, Hp
                
        else:
            print 'you must enter a number!!!!'
        
        event.Skip()

    def paraxial_ray(self,yi,ui):
        u = []
        y = []
                
        u.append(ui)
        y.append(yi)        
                
        #print self.n,self.c,self.t
        #self.n.append(1.0)
        for i in range(len(self.t)-1):
            y.append(y[i] + u[i] * self.t[i])                        
            N = self.n[i]
            Np = self.n[i+1]            
            u.append(N*u[i]/Np - self.c[i+1]*y[i+1]*(Np - N)/Np)
            

        #print u,y
        l = -y[len(y)-1]/u[len(u)-1]
        return l
    
    
    
    def draw_ray(self,x,y,z,ray):                                    
        
        glNewList(ray, GL_COMPILE)      
        glColorf(0.0,1.0,1.0)                
        glBegin(GL_LINE_STRIP)
        
        for i in range(len(x)):
            glVertexf(x[i] + self.t_cum[i],y[i],z[i]) 
            
        glEnd()        
        glEndList()
            
        
        
        #return (x[i],y[i],z[i],X[i],Y[i],Z[i])
    

                    
    def skew_ray(self,(xi,yi,zi),(Xi,Yi,Zi)):
        x = []
        y = []
        z = []
        E = []
        g = []
        X = []
        Y = []
        Z = []
        Ep = []
        
        #we must know two coords
        x.append(xi)
        y.append(yi)
        z.append(zi)
        
        #we must know atleast two directions
        X.append(Xi)
        Y.append(Yi)
        Z.append(Zi)
        
        i = 0        

        self.c.append(0)
        self.n.append(1)
        for i in range(len(self.t)):
            #print self.n,self.r
            if(len(self.t) !=0):                            
                #print ' i = ',i,self.t[i]
                e  = self.t[i]*X[i] - (x[i]*X[i] + y[i]*Y[i] +z[i]*Z[i])
                Mx = x[i] + e*X[i] - self.t[i]
                M2 = x[i]*x[i] + y[i]*y[i] + z[i]*z[i] -e*e +self.t[i] * self.t[i] - 2*self.t[i] * x[i]
                                
                A = X[i]*X[i]
                B = (M2*self.c[i+1] - 2*Mx)*self.c[i+1]
                if(A > B):
                    E.append(pow(A - B,.5))
                else:
                    E.append(pow(A + B,.5))
                                                
                L  = e + (M2*self.c[i+1] - 2*Mx)/(X[i]+E[i])
                
                x.append(x[i] + L*X[i] - self.t[i])
                y.append(y[i] + L*Y[i])
                z.append(z[i] + L*Z[i])
                
                A = 1
                B = (self.n[i]/self.n[i+1]) * (self.n[i]/self.n[i+1])*(1 - E[i]*E[i])
                if(A > B):
                    Ep.append(pow(A - B,0.5))
                else:
                    print 'TIR'
                    Ep.append(pow(A + B,0.5))
                
                
                g.append(Ep[i] - (self.n[i]/self.n[i+1]) * E[i])
                X.append((self.n[i]/self.n[i+1]) *X[i] - g[i]*x[i+1]*self.c[i+1] + g[i])
                Y.append((self.n[i]/self.n[i+1]) *Y[i] - g[i]*y[i+1]*self.c[i+1])
                Z.append((self.n[i]/self.n[i+1]) *Z[i] - g[i]*z[i+1]*self.c[i+1])
        
        self.t_cum.append(self.t_cum[len(self.t_cum)-1])                

##            print 'e = ',e
##            print 'Mx = ',Mx
##            print 'M2 = ',M2
##            print 'E = ',E
##            print 'L = ',L
##            print 'x = ' ,x
##            print 'y = ',y
##            print 'z = ',z
##            print 'Ep = ',Ep
##            print 'g = ',g
##            print 'X = ',X
##            print 'Y = ',Y
##            print 'Z = ',Z
##            print 'c = ',self.c
##            print 't = ',self.t
##            print 'n = ',self.n
        return (x,y,z,X,Y,Z)

    

    def draw_surface(self,c,t,h,n):        
        
        if(c!=0):
            r = 1/c
        else:
            r = 1000000

##        glBegin(GL_LINES) 
##        glVertexf(t,h,0)
##        glVertexf(t,-h,0)
##        glEnd()
                        
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
                                    

        glBegin(GL_LINE_STRIP)    

        for i in range(n):                    

            glVertex3f(x[i],y[i],0)            

        glEnd()
      
        glBegin(GL_LINE_STRIP)    

        for i in range(n):                    

            glVertex3f(x[i],-y[i],0)            

        glEnd()
              
        return (x[i],y[i])
    
    
    
    
    
    
    
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
                    
        if(c == FLENGTH): #focal length changed
            self.grid1.SetCellValue(r,POWER,str(1.0/val)) #set power            
            if (self.grid1.GetCellValue(r+1,APERATURE_RADIUS) == ''):
                self.grid1.SetCellValue(r+1,APERATURE_RADIUS,str(1.0))
            if (self.grid1.GetCellValue(r+1,GLASS) == ''):
                self.grid1.SetCellValue(r+1,GLASS,str(1))            
            if (self.grid1.GetCellValue(r+1,THICKNESS) == ''):
                self.grid1.SetCellValue(r+1,THICKNESS,str(0))                             
            self.update_radius(r)            
                
        if(c == POWER): #power has changed    
            self.grid1.SetCellValue(r,FLENGTH,str(1.0/val))
            
            if (self.grid1.GetCellValue(r+1,APERATURE_RADIUS) == ''):
                self.grid1.SetCellValue(r+1,APERATURE_RADIUS,str(1.0))
            if (self.grid1.GetCellValue(r+1,GLASS) == ''):
                self.grid1.SetCellValue(r+1,GLASS,str(1))            
            if (self.grid1.GetCellValue(r+1,THICKNESS) == ''):
                self.grid1.SetCellValue(r+1,THICKNESS,str(0))                 
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
            
            if(self.grid1.GetCellValue(r,POWER) == ''):
                self.radioButton_const_radius.SetValue(True)
                self.OnRadiobutton_const_radiusRadiobutton()
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
        
        return True

    def update_display(self):
        thickness = 0                
                
        z = [0 for i in range(self.rows)]
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
                (self.grid1.GetCellValue(i,CURVATURE)        != '') |
                (self.grid1.GetCellValue(i,APERATURE_RADIUS) != '') ):                                
            
        
                self.c.append(float(self.grid1.GetCellValue(i,CURVATURE))) 
                
                self.h.append(float(self.grid1.GetCellValue(i,APERATURE_RADIUS)))
                surf.append(i)    
                    
                self.n.append(float(self.grid1.GetCellValue(i,GLASS)))
            
            
            if(self.grid1.GetCellValue(i,THICKNESS) != ''):
                t1 += (float(self.grid1.GetCellValue(i,THICKNESS))) 
                self.t.append(float(self.grid1.GetCellValue(i,THICKNESS)))
                self.t_cum.append(t1)

                                
        l = range(1,self.rows)
        

        for i in range(len(self.t)):                
            #draw the data
            glDeleteLists(self.glListStart + surf[i], 1) #delete the list
                                           
            glNewList(self.glListStart + surf[i], GL_COMPILE)        
            glColorf(1.0,1.0,1.0)                                   
            if(i == 0):
                glBegin(GL_LINES)
                glVertexf(0,0,0)
                glVertexf(t1,0,0)
                glEnd()        
            
            glColorf(1.0,1.0,0.0)                                   
            z[i] = self.draw_surface(self.c[i],self.t_cum[i],self.h[i],10)
                
            if(i > 0):                        
                if(self.n[i-1] != 1):
                    glBegin(GL_LINES)
    
                    glVertex3f(float(z[i-1][0]),float(z[i-1][1]),0)
                    glVertex3f(float(z[i][0])  ,float(z[i][1]),0)

                    glVertex3f(float(z[i-1][0]),-float(z[i-1][1]),0)
                    glVertex3f(float(z[i][0]),-float(z[i][1]),0)

                    glEnd()                        
                        
            glEndList()        
        self.can.set_lens_list(l)

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

            rad = ((2*n+2*pow((n*n - phi*n*t),.5))*(n-1))/(2*n*phi)
            
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

    def OnRadiobutton_const_powerRadiobutton(self, event=None):
        self.hold_power = True
        self.hold_radius = False
 #       event.Skip()

    def OnRadiobutton_const_radiusRadiobutton(self, event=None):
        self.hold_power = False
        self.hold_radius = True
#        event.Skip()

