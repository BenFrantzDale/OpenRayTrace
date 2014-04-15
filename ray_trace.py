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
from __future__ import division
import numpy as np

def paraxial_ray(yi,ui,t,n,c):
    """
    Cast a paraixal ray through the system.
    * yi, ui are the ray y position and angle with the optical axis
    * t, n and c are vectors defining the thickness, index, and curvature of the surfaces.
    Return a 3-tuple:
    * ?
    * y, the y values at each surface
    * u, the angle values at each surface.
    """
    yu = np.nan * np.ones((2, len(t)))
    yu[:,0] = yi, ui
    for i in range(len(t)-1):
        n1, n2 = n[i:i+2]
        ABCD = np.array([[1, t[i]],[(n1-n2)/n2, n1/n2]])
        yu[:,i+1] = ABCD.dot(yu[:,i])

    l = -yu[0,-1] / yu[1,-1] if yu[1,-1] else 0
    return l, yu[0], yu[1]
    
def paraxial_ray2(yi,ui,t,n,c):
        u = []
        y = []
                
        u.append(ui)
        y.append(yi)        
                
        for i in range(len(t)-1):
            N = n[i]
            Np = n[i+1]            
            u.append(N*u[i]/Np - c[i+1]*y[i]*(Np - N)/Np)            
            y.append(y[i] + u[i+1] * t[i+1])   

        
        if (u[len(u)-1] != 0):
            l = -y[len(y)-1]/u[len(u)-1]
        else:
            l = 0
            
        return (l,y,u)


def skew_ray((xi,yi,zi),(Xi,Yi,Zi),T,N,C,T_CUM,H,surf = 0):
        """
        Compute the skew ray starting at (xyz) (going toward XYZ?)
        given thickness, index, curvature, and center-position vectors.
        """
        T = list(T)
        N = list(N)
        C = list(C)
        T_CUM = list(T_CUM)
        H = list(H)

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

        c = C
        c.append(0)
        n = N
        n.append(1)
        
        missed_surface = False
        check_aperature = True
        for i in range(surf,len(T)):                        
            e  = T[i]*X[i] - (x[i]*X[i] + y[i]*Y[i] +z[i]*Z[i])
            Mx = x[i] + e*X[i] - T[i]
            M2 = x[i]*x[i] + y[i]*y[i] + z[i]*z[i] -e*e + T[i] * T[i] - 2* T[i] * x[i]
                                
            A = X[i]*X[i]
            B = (M2*c[i+1] - 2*Mx)*c[i+1]
            
            if(A > B):
                E.append(pow(A - B,.5))
            else:
                #print 'Missed the surface'
                missed_surface = True
                E.append(pow(A + B,.5))
                        
            
            if(missed_surface):                
                x.append(x[i])
                y.append(y[i])
                z.append(z[i])
                X.append(X[i])
                Y.append(Y[i])
                Z.append(Z[i])                                
            else:                                    
                L  = e + (M2*c[i+1] - 2*Mx)/(X[i]+E[i])
                                    
                x.append(x[i] + L*X[i] - T[i])
                y.append(y[i] + L*Y[i])
                z.append(z[i] + L*Z[i])               
                
                #print y
                A = 1
                B = (n[i]/n[i+1]) * (n[i]/n[i+1])*(1 - E[i]*E[i])
                
                
                if(A > B):
                    Ep.append(pow(A - B,0.5))
                else:
                    #print 'TIR'
                    Ep.append(pow(A + B,0.5))
                
                
                g.append(Ep[i] - (n[i]/n[i+1]) * E[i])
                X.append((n[i]/n[i+1]) *X[i] - g[i]*x[i+1]*c[i+1] + g[i])
                Y.append((n[i]/n[i+1]) *Y[i] - g[i]*y[i+1]*c[i+1])
                Z.append((n[i]/n[i+1]) *Z[i] - g[i]*z[i+1]*c[i+1])


                
        
        if(check_aperature):            
            done = False
            for i in range(1,len(T)):            
                if(len(T) !=0):                      
                    if(not done):
                        r = pow(y[i]*y[i] + z[i]*z[i],0.5)
                    
                        if(r > H[i]):
                            x = x[0:i+1]
                            y = y[0:i+1]
                            z = z[0:i+1]
                            done = True
                            
        T_CUM.append(T_CUM[len(T_CUM)-1])                

##            print 'e = ',e
##            print 'Mx = ',Mx
##            print 'M2 = ',M2
##            print 'E = ',E
##            print 'L = ',L
##            print 'x = ' ,x
        #print 'y = ',y
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


##def skew_rays_y_axis(pos,y_hit,z_hit,y_launch,z_launch,T,N,C,T_CUM,H,surf = 0):                    
##        for i in range(len(pos)):
##            y_launch = pos[i]
##            yy = y_hit - y_launch 
##            zz = z_hit - z_launch 
##            xx2 = t[0]*t[0]
##            den = (pow(zz*zz + yy*yy + xx2,0.5)) 
##            Yi = yy / den
##            Zi = zz / den
##            Xi = pow(1.0 - Yi*Yi - Zi*Zi,0.5)           
##                             
##            (x,y,z,X,Y,Z) = skew_ray((0,y_launch,z_launch),(Xi,Yi,Zi),t,n,c,t_cum,h)                                                
##                        
