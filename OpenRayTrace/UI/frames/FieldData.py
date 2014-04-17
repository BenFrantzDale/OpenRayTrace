import wx

class FieldData(wx.MDIChildFrame):
    def __init__(self, parent):
        wx.MDIChildFrame.__init__(self, id=wx.NewId(), 
                                  parent=parent, 
                                  title='Field Data', 
                                  size=wx.Size(100,100),
                                  pos=wx.Point(100,100),
                                  style=wx.DEFAULT_FRAME_STYLE)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)
