#OpenRayTrace.UI/frames.ParaxialData
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

[Y,U,I,YP,UP,IP] = range(6)


class ParaxialData(wx.MDIChildFrame):
    wxID = wx.NewId()
    wxID_DATAGRID1 = wx.NewId()

    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MDIChildFrame.__init__(self, id=self.wxID,
                                  name='ParaxialData', parent=prnt,
                                  pos=wx.Point(311, 198), size=wx.Size(1200, 854),
                                  style=DEFAULT_FRAME_STYLE, title='Paraxial Data')
        self._init_utils()
        self.SetClientSize(wx.Size(1192, 820))
        EVT_CLOSE(self, lambda event: self.Hide)

        self.grid1 = Grid(id=self.wxID_DATAGRID1,
                          name='grid1', parent=self, pos=wx.Point(0, 0), 
                          size=wx.Size(1192,820), style=0)
        EVT_GRID_CELL_CHANGE(self.grid1, self.OnGrid1GridCellChange)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.rows = 40
        col_label = ['y','u','i','yp','up','ip']
        self.grid1.CreateGrid(self.rows,len(col_label))
        [self.grid1.SetColLabelValue(i,col_label[i]) for i in range(len(col_label))]                
        
        self.grid1.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        self.grid1.AutoSizeRow(True)
        self.grid1.AutoSizeColumns(True)
    
    def trace(self,y,u,yp,up):        
        (l,y,u) = self.GetParent().lens.paraxial_ray(y,u)
        (l,yp,up) = self.GetParent().lens.paraxial_ray(yp,up)
        
        [self.set_y_u_yp_up(y[i],u[i],yp[i],up[i],i) for i in range(len(y))]
    
    def set_y_u_yp_up(self,y,u,yp,up,row):
        self.grid1.SetCellValue(row,Y,str(y))
        self.grid1.SetCellValue(row,U,str(u))
        self.grid1.SetCellValue(row,YP,str(yp))
        self.grid1.SetCellValue(row,UP,str(up))
        self.grid1.AutoSize()
        
    def OnGrid1GridCellChange(self, event = None):
        self.grid1.AutoSize()                
        if(event != None):
            r = event.GetRow()
            c = event.GetCol() 
        
        y = self.grid1.GetCellValue(0,Y)
        u = self.grid1.GetCellValue(0,U)
        yp = self.grid1.GetCellValue(0,YP)
        up = self.grid1.GetCellValue(0,UP)
        
        if(y != ''):
            y = float(y)
        else:
            y = 0.0
            
        if(u != ''):
            u = float(u)
        else:
            u = 0.0

        if(yp != ''):
            yp = float(yp)
        else:
            yp = 0.0
            
        if(up != ''):
            up = float(up)
        else:
            up = 0.0
                                            
        self.trace(y,u,yp,up)
             
                    
        event.Skip()


    
