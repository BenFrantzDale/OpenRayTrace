import wx

class FieldData(wx.MDIChildFrame):
    def __init__(self, parent):
        wx.MDIChildFrame.__init__(self, id=wx.NewId(), 
                                  parent=parent, 
                                  title='Field Data', 
                                  size=wx.Size(100,100),
                                  pos=wx.Point(100,100),
                                  style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1) 
        basicLabel = wx.StaticText(panel, -1, "Basic Control:")
        basicText = wx.TextCtrl(panel, -1, "I've entered some text!", size=(175, -1))
        basicText.SetInsertionPoint(0)

        pwdLabel = wx.StaticText(panel, -1, "Password:")
        pwdText = wx.TextCtrl(panel, -1, "password", size=(175, -1),style=wx.TE_PASSWORD)
        sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        sizer.AddMany([basicLabel, basicText, pwdLabel, pwdText])
        panel.SetSizer(sizer)
        self.Show(True)
