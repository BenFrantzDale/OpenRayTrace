import wx

class FieldData(wx.MDIChildFrame):
    def __init__(self, parent):
        wx.MDIChildFrame.__init__(self, id=wx.NewId(), 
                                  parent=parent, 
                                  title='Field Data', 
                                  size=wx.Size(700,500),
                                  pos=wx.Point(100,100),
                                  style=wx.DEFAULT_FRAME_STYLE)
        panel = wx.Panel(self, -1) 
        nfields = 12
        colLabels = ('field', 'x field', 'y field', 'weight')
        defaults = ('', 0, 0, 1.0)
        ncols = len(colLabels)
        widgets = []
        for label in colLabels:
            widgets.append(wx.StaticText(panel, -1, label))
        for rowi in range(nfields):
            widgets.append(wx.CheckBox(panel, -1, str(rowi)))
            for colj in range(1, ncols):
                widgets.append(wx.TextCtrl(panel, -1, str(defaults[colj]), size=(175, -1)))
                widgets[-1].SetInsertionPoint(0)
        sizer = wx.FlexGridSizer(cols=ncols, hgap=6, vgap=6)
        sizer.AddMany(widgets)
        panel.SetSizer(sizer)
        self.Show(True)
