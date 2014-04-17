import wx

class FieldData(wx.MDIChildFrame):
    def __init__(self, parent):
        wx.Frame.__init__(self, id=wx.NewId(), 
                          parent=parent, 
                          title='Field Data', 
                          size=wx.Size(1,1),
                          pos=wx.Point(100,100),
                          style=wx.DEFAULT_FRAME_STYLE)
        self.Show(True)
