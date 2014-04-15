#Boa:Dialog:wxDialogSaveQuestion

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

def create(parent,fname):
    return wxDialogSaveQuestion(parent,fname)

[wxID_WXDIALOGSAVEQUESTION, wxID_WXDIALOGSAVEQUESTIONBUTTON_CANCEL, 
 wxID_WXDIALOGSAVEQUESTIONBUTTON_NO, wxID_WXDIALOGSAVEQUESTIONBUTTON_YES, 
 wxID_WXDIALOGSAVEQUESTIONSTATICTEXT, 
] = map(lambda _init_ctrls: wxNewId(), range(5))

class wxDialogSaveQuestion(wxDialog):
    def _init_utils(self):
        # generated method, don't edit
        pass

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wxDialog.__init__(self, id=wxID_WXDIALOGSAVEQUESTION,
              name='wxDialogSaveQuestion', parent=prnt, pos=wxPoint(850, 537),
              size=wxSize(431, 155), style=wxDEFAULT_DIALOG_STYLE,
              title='OpenRayTrace')
        self._init_utils()
        self.SetClientSize(wxSize(423, 121))
        self.Center(wxBOTH)

        self.button_yes = wxButton(id=wxID_WXDIALOGSAVEQUESTIONBUTTON_YES,
              label='Yes', name='button_yes', parent=self, pos=wxPoint(48, 80),
              size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.button_yes, wxID_WXDIALOGSAVEQUESTIONBUTTON_YES,
              self.OnButton_yesButton)

        self.button_no = wxButton(id=wxID_WXDIALOGSAVEQUESTIONBUTTON_NO,
              label='No', name='button_no', parent=self, pos=wxPoint(176, 80),
              size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.button_no, wxID_WXDIALOGSAVEQUESTIONBUTTON_NO,
              self.OnButton_noButton)

        self.button_cancel = wxButton(id=wxID_WXDIALOGSAVEQUESTIONBUTTON_CANCEL,
              label='Cancel', name='button_cancel', parent=self,
              pos=wxPoint(304, 80), size=wxSize(75, 23), style=0)
        EVT_BUTTON(self.button_cancel, wxID_WXDIALOGSAVEQUESTIONBUTTON_CANCEL,
              self.OnButton_cancelButton)

        self.staticText = wxStaticText(id=wxID_WXDIALOGSAVEQUESTIONSTATICTEXT,
              label='Do you want to save the changes to', name='staticText',
              parent=self, pos=wxPoint(48, 40), size=wxSize(172, 13), style=0)

    def __init__(self, parent,filename = ''):
        self._init_ctrls(parent)
        self.staticText.SetLabel('Do you want to save the changes to ' + filename+ '?')
        
        
    def OnButton_yesButton(self, event):
        self.Hide()
        event.Skip()
        self.SetReturnCode(0)

    def OnButton_noButton(self, event):
        self.Hide()
        event.Skip()
        self.SetReturnCode(1)

    def OnButton_cancelButton(self, event):
        self.Hide()
        event.Skip()
        self.SetReturnCode(2)
        
