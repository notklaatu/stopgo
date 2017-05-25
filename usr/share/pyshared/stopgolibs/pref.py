import wx
import os
import json

class GUIPref(wx.Frame):
    def __init__(self, parent, id, title, size,style):
        self.parent = parent
        self.screenSize = wx.DisplaySize()
        #self.screenSize = [ 786, 768 ]
        self.screenWidth = int(self.screenSize[0] / 3)
        self.screenHeight = int(self.screenSize[1] / 2)
        #fontsy = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()        
        wx.Frame.__init__(self, parent, id, title, size=(500, 400), style=wx.DEFAULT_FRAME_STYLE)

        dosiero = open(os.path.join(os.path.expanduser("~"), '.config', 'stopgo.conf.json'))
        myprefs = json.load(dosiero)

        self.InitUI(myprefs)
        self.Show()


    def InitUI(self,myprefs):

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(8, 2, 9, 9)

        lbl_enc = wx.StaticText(panel, label="Encoder")
        lbl_con = wx.StaticText(panel, label="Container")
        lbl_pro = wx.StaticText(panel, label="Profile")
        lbl_fps = wx.StaticText(panel, label="FPS")
        lbl_bit = wx.StaticText(panel, label="Bitrate")
        lbl_dir = wx.StaticText(panel, label="Default Save")
        
        # empty spacer
        lbl_mt  = wx.StaticText(panel, label="")
        btn_ok  = wx.Button(panel, label="Save")
        btn_no  = wx.Button(panel, label="Cancel")

        enclist = ['ffmpeg']#, 'avconv']
        conlist = ['mp4','mov']
        prolist = ['1080p','720p']
        fpslist = ['25','24','18','12','8']
        bitlist = ['7Mbps','14Mbps','21Mbps']

        self.fld_enc = wx.ComboBox(panel, choices=enclist,
                                   style=wx.CB_READONLY)
        self.fld_con = wx.ComboBox(panel, choices=conlist,
                                   style=wx.CB_READONLY)
        self.fld_pro = wx.ComboBox(panel, choices=prolist,
                                   style=wx.CB_READONLY)
        self.fld_fps = wx.ComboBox(panel, choices=fpslist,
                                   style=wx.CB_READONLY)
        self.fld_bit = wx.ComboBox(panel, choices=bitlist,
                                   style=wx.CB_READONLY)
        self.fld_dir = wx.TextCtrl(panel, value="Desktop")
        self.fld_fst = wx.CheckBox(panel, label="Warn if no project loaded?")

        try:
            self.fld_enc.SetValue(myprefs['encoder'])
            self.fld_con.SetValue(myprefs['container'])
            self.fld_pro.SetValue(myprefs['profile'])
            self.fld_fps.SetValue(myprefs['fps'])
            self.fld_bit.SetValue(myprefs['bitrate'])
            self.fld_dir.SetValue(myprefs['dir'])
            #self.fld_fst.SetValue(myprefs['warn'])

        except:
            pass

        fgs.AddMany([(lbl_enc), (self.fld_enc, 1, wx.EXPAND),
                     (lbl_con), (self.fld_con, 1, wx.EXPAND),
                     (lbl_pro), (self.fld_pro, 1, wx.EXPAND),
                     (lbl_fps), (self.fld_fps, 1, wx.EXPAND),
                     (lbl_bit), (self.fld_bit, 1, wx.EXPAND),
                     (lbl_dir), (self.fld_dir, 1, wx.EXPAND),
                     #(fld_fst), (self.fld_fst, 1, wx.EXPAND),
                     (btn_ok, 1, wx.EXPAND), (lbl_mt),
                     (btn_no, 1, wx.EXPAND) ])

        #fgs.AddGrowableRow(1, 2)
        fgs.AddGrowableCol(1, 2)

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)

        self.Bind( wx.EVT_BUTTON, self.OnOk, btn_ok )
        self.Bind(wx.EVT_BUTTON, self.OnCancel, btn_no)


    def OnOk(self,e):
        pdict = {}
        pdict['encoder']   = self.fld_enc.GetValue()
        pdict['container'] = self.fld_con.GetValue()
        pdict['profile']   = self.fld_pro.GetValue()
        pdict['fps']       = self.fld_fps.GetValue()
        pdict['bitrate']   = self.fld_bit.GetValue()
        pdict['dir']       = self.fld_dir.GetValue()
        #pdict['warn']      = self.fld_fst.GetValue()

        homedir = os.path.expanduser("~")

        with open(os.path.join(homedir, '.config', 'stopgo.conf.json'), 'w') as outfile:
            json.dump(pdict, outfile)

        self.Destroy()

    def OnCancel(self,e):
        self.Destroy()

