#OpenRayTrace.UI.frames.RayData
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




from wx import *
from wx.grid import *
TSC = 0
SC  = 1
CC  = 2
TAC = 3
AC  = 4
TPC = 5
PC  = 6
DC  = 7
TAchC = 8
LchC  = 9
TchC  = 10
S1    = 11
S2    = 12
S3    = 13
S4    = 14
S5    = 15


class RayData(wx.MDIChildFrame):
    wxID = wx.NewId()
    wxID_DATAGRID1 = wx.NewId()

    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=RayData.wxID,
                                  name='RayData', parent=prnt, 
                                  pos=wx.Point(447,260), size=wx.Size(798, 498), 
                                  style=DEFAULT_FRAME_STYLE,
                                  title='Ray Data')
        self._init_utils()
        self.SetClientSize(wx.Size(790, 464))
        EVT_CLOSE(self, lambda event: self.Hide)

        self.grid1 = Grid(id=self.wxID_DATAGRID1, name='grid1',
                          parent=self, pos=wx.Point(0, 0), size=wx.Size(790, 464), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.rows = 40
        self.col_labels = ['TSC  ','SC','CC   ','TAC  ','AC','TPC   ','PC','DC   ','TAchC   ','LchC','TchC  ','S1','S2','S3','S4','S5']
        self.grid1.CreateGrid(self.rows,len(self.col_labels))
        for i, label in enumerate(self.col_labels): 
            self.grid1.SetColLabelValue(i, label) 
        
        #self.grid1.setRowLabelValue(0,'Total')
        
        self.grid1.SetDefaultCellAlignment(ALIGN_CENTRE,ALIGN_CENTRE)
        self.grid1.AutoSizeRow(True)
        self.grid1.AutoSizeColumns(True)
        
    def calc_third_order_abberations(self,y,u,yp,up,N,c):
        self.grid1.AutoSize()
        #print yp,up,y,u
        last = len(N)-1
        
        I = N[last] * (yp[last]*u[last] - y[last]*up[last])        
        h = I / (N[last] * u[last])
        
        delta_N = [0.0,0.008,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        ctsc   = 0
        csc    = 0
        ccc    = 0
        ctac   = 0
        cac    = 0
        ctpc   = 0
        cpc    = 0
        cdc    = 0
        ctachc = 0
        clchc  = 0
        ctchc  = 0
        cs1    = 0
        cs2    = 0
        cs3    = 0
        cs4    = 0
        cs5    = 0
        
        for s in range(last):                        
            i  = c[s+1]*y[s] + u[s]                      
            
            ip = c[s+1]*yp[s] + up[s]
            
            
            dN = N[s]*(N[s+1] - N[s])/(2*N[s+1]*I)
                        
            B  =  dN * y[s]  * (u[s+1] + i)
            Bp =  dN * yp[s] * (up[s+1] + ip)
            
            K  = y[s] * N[s] * (N[s]/N[s+1] - 1) * (i - u[s+1])/(2*u[last]*u[last])
            #print 'sc = ',K*i*i
            
            h  = I/(N[last]*u[last])
            
            tsc  = B*i*i*h
            ctsc += tsc
            
            sc   = -tsc/u[last]
            csc += sc
            
            cc   = B*i*ip*h
            ccc += cc
            
            tac  = B*ip*ip*h
            ctac += tac
            
            ac   = -tac/u[last]
            cac += ac
            
            tpc  = -(N[s] - N[s+1])*c[s+1]*I*h/(2*N[s]*N[s+1])
            ctpc += tpc
            
            pc   = -tpc/u[last]
            cpc += pc
            
            dc   = h*(Bp*i*ip+0.5*(up[s+1]*up[s+1] - up[s]*up[s]))
            cdc += dc
            
            
            tachc = -y[s]*i/(N[last]*u[last])  *  (delta_N[s] - N[s]*delta_N[s+1] / N[s+1])
            ctachc += tachc
            
            lchc  = -tachc/u[last]
            clchc += lchc
            
            tchc =  -y[s]*ip/(N[last]*u[last])  *  (delta_N[s] - N[s]*delta_N[s+1] / N[s+1])
            ctchc += tchc
           
            s1 = -tsc*2*N[last]*u[last]
            cs1 += s1
            
            s2 = -cc*2*N[last]*u[last]
            cs2 += s2
            
            s3 = -tac*2*N[last]*u[last]
            cs3 += s3
            
            s4 = -tpc*2*N[last]*u[last]
            cs4 += s4
            
            s5 = -dc*2*N[last]*u[last]
            cs5 += s5
            
            for label in self.col_labels:
                label = label.strip()
        
                self.grid1.SetCellValue(s+1,
                                        locals()[label],
                                        label.lower())

            
        for label in self.col_labels:
            label = label.strip()
        
            self.grid1.SetCellValue(0,
                                    locals()[label],
                                    'c{}'.format(label.lower()))

