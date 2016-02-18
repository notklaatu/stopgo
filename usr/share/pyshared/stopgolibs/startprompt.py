import wx
import os

class Choice(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize((300, 123))
        self.SetBackgroundColour('#d4d4d4')#windows
        self.SetTitle("No Project")
        self.InitUI()

    def InitUI(self):

        sb = wx.StaticText(self, label='Stop! Open or Create new project first!')
        ic = wx.ArtProvider.GetBitmap( wx.ART_TIP, size=(48,48) )
        icn= wx.StaticBitmap(self,-1,ic,name='Stop')
        lbl_mt = wx.StaticText(self, label="")

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        vbox.Add(lbl_mt,flag=wx.CENTER, border=2)
        vbox.Add(sb,flag=wx.CENTER, border=2)
        vbox.Add(icn,flag=wx.CENTER, border=0)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        OButton = wx.Button(self, label='OK')
        #NButton = wx.Button(self, label='New')

        hbox2.Add(OButton, flag=wx.CENTER, border=2)
        #hbox2.Add(NButton, flag=wx.LEFT, border=5)
     
        vbox.Add(hbox2,flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=2)

        OButton.Bind(wx.EVT_BUTTON,self.OpenBtn)
        #NButton.Bind(wx.EVT_BUTTON,self.NewBtn)

        '''
        pnl = wx.Panel(self)
        pnl.SetBackgroundColour('#19b3b7')
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        sb = wx.StaticText(pnl, label='Stop! Open or Create new project first!')
        ic = wx.ArtProvider.GetBitmap( wx.ART_TIP, size=(48,48) )
        icn= wx.StaticBitmap(pnl,-1,ic,name='Stop')

        vbox.Add(sb,flag=wx.CENTER, border=2)
        vbox.Add(icn,flag=wx.CENTER, border=2)
        vbox.Add(pnl,proportion=1,flag=wx.ALL|wx.EXPAND, border=0)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        OButton = wx.Button(self, label='OK')
        #NButton = wx.Button(self, label='New')

        hbox2.Add(OButton, flag=wx.CENTER, border=2)
        #hbox2.Add(NButton, flag=wx.LEFT, border=5)
     
        vbox.Add(hbox2,flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=2)

        OButton.Bind(wx.EVT_BUTTON,self.OpenBtn)
        #NButton.Bind(wx.EVT_BUTTON,self.NewBtn)
        '''

        self.Show() 
        self.SetFocus()
        self.SetWindowStyle( wx.STAY_ON_TOP )

    def OnClose(self,msg):
        self.Destroy()
        return msg

    def OpenBtn(self,e):
        msg = 'open'
        self.OnClose(msg)

    def NewBtn(self,e):
        msg = 'new'
        self.OnClose(msg)
