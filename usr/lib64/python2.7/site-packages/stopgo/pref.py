import wx
import os
import json
import six

class GUIPref(wx.Frame):
    def __init__(self, parent, id, title, size,style):
        self.parent = parent
        self.screenSize = wx.DisplaySize()
        #self.screenSize = [ 786, 768 ]
        self.screenWidth = int(self.screenSize[0] / 3)
        self.screenHeight = int(self.screenSize[1] / 2)
        #fontsy = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()        
        wx.Frame.__init__(self, parent, id, title, size=(400, 600), style=wx.DEFAULT_FRAME_STYLE)

        try:
            dosiero = open(os.path.join(os.path.expanduser("~"), '.config', 'stopgo.conf.json'))
            myprefs = json.load(dosiero)
        except:
            #print("No config found.") #DEBUG
            pass

        self.InitUI(myprefs)
        self.Show()

    def InitUI(self,myprefs):

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        sizer = wx.GridBagSizer(5, 5)
        btn_ok  = wx.Button(panel, label="Save")
        btn_no  = wx.Button(panel, label="Cancel")

        enclist = ['ffmpeg']#, 'avconv']
        conlist = ['mp4','mov']
        prolist = ['hd1080','hd720']
        fpslist = ['25','24','18','12','8']
        bitlist = ['7M','14M','21M']
        prmlist = ['New project prompt','No prompt']
        
        self.fld_enc = wx.ComboBox(panel, choices=enclist,
                                   style=wx.CB_READONLY)
        self.fld_con = wx.ComboBox(panel, 
                                   choices=conlist, style=wx.CB_READONLY)
        self.fld_pro = wx.ComboBox(panel, 
                                   choices=prolist, style=wx.CB_READONLY)
        self.fld_fps = wx.ComboBox(panel, 
                                   choices=fpslist, style=wx.CB_READONLY)
        self.fld_bit = wx.ComboBox(panel,
                                   choices=bitlist, style=wx.CB_READONLY)
        self.fld_dir = wx.TextCtrl(panel, value="Desktop")
        self.fld_prm = wx.ComboBox(panel,
                                   choices=prmlist, style=wx.CB_READONLY)

        # layout
        lbl_enc = wx.StaticText(panel, label="Encoder")
        sizer.Add(lbl_enc, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)
        sizer.Add(self.fld_enc, pos=(0, 1), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=15)
        
        lbl_con = wx.StaticText(panel, label="Container")
        sizer.Add(lbl_con, pos=(1, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)
        sizer.Add(self.fld_con, pos=(1, 1), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=15)

        lbl_pro = wx.StaticText(panel, label="Profile")
        sizer.Add(lbl_pro, pos=(2, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)
        sizer.Add(self.fld_pro, pos=(2, 1), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=15)

        lbl_fps = wx.StaticText(panel, label="FPS")
        sizer.Add(lbl_fps, pos=(3, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)
        sizer.Add(self.fld_fps, pos=(3, 1), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=15)

        lbl_bit = wx.StaticText(panel, label="Bitrate")
        sizer.Add(lbl_bit, pos=(4, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)
        sizer.Add(self.fld_bit, pos=(4, 1), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=15)

        lbl_dir = wx.StaticText(panel, label="Default save")
        sizer.Add(lbl_dir, pos=(5, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)
        sizer.Add(self.fld_dir, pos=(5, 1), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=15)

        lbl_prm = wx.StaticText(panel, label="Startup")
        sizer.Add(lbl_prm, pos=(6, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)
        sizer.Add(self.fld_prm, pos=(6, 1), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.EXPAND, border=15)

        #sizer.AddGrowableCol(2)

        sizer.Add(btn_ok, pos=(7, 0), flag=wx.TOP|wx.RIGHT|wx.BOTTOM, border=15)
        
        sizer.Add(btn_no, pos=(7, 1), flag=wx.TOP|wx.RIGHT|wx.BOTTOM, border=15)

        prefstr = PrefProbe().PrefGet()
        myprefs = json.dumps(prefstr,sort_keys=True)
        myprefs = json.loads(myprefs)
        self.fld_enc.SetValue(myprefs['encoder'])
        self.fld_con.SetValue(myprefs['container'])
        self.fld_pro.SetValue(myprefs['profile'])
        self.fld_fps.SetValue(myprefs['fps'])
        self.fld_bit.SetValue(myprefs['bitrate'])
        self.fld_dir.SetValue(myprefs['dir'])
        self.fld_prm.SetValue(myprefs['prompt'])
            
        hbox.Add(sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
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
        pdict['prompt']    = self.fld_prm.GetValue()

        homedir = os.path.expanduser("~")

        with open(os.path.join(homedir, '.config', 'stopgo.conf.json'), 'w') as outfile:
            json.dump(pdict, outfile)

        self.Destroy()


    def OnCancel(self,e):
        self.Destroy()

        
class PrefProbe():
    def __init__(self):
        # does path exist
        self.newprefs = {"profile":"hd1080", "container":"mp4", "bitrate":"21M", "fps":"8", "encoder":"ffmpeg", "dir":"Desktop","prompt":"New project prompt"}

        if not os.path.exists(os.path.join(os.path.expanduser("~"), '.config')):
            os.makedirs( os.path.join(os.path.expanduser("~"), '.config'))

        # does config file exist
        if not os.path.isfile(os.path.join(os.path.expanduser("~"),'.config','stopgo.conf.json')):
            self.PrefDef()
        else:
            #it already exists
            self.PrefGet()


    def PrefGet(self):
        myprefs = {}

        try:
            dosiero = open(os.path.join(os.path.expanduser("~"), '.config', 'stopgo.conf.json'), 'r')
            myprefs = json.load(dosiero)

        except:
            self.PrefDef()
            dosiero = open(os.path.join(os.path.expanduser("~"), '.config', 'stopgo.conf.json'), 'r')
            myprefs = json.load(dosiero)

        for nkey in self.newprefs.items():
            #print(type(myprefs))#DEBUG
            if myprefs.get(nkey[0]) == None:
                #print(str(nkey[0]) + str(' not found') ) #DEBUG
                myprefs[nkey[0]] = nkey[1]
                print(myprefs) #DEBUG

        return myprefs

    def PrefDef(self):
        homedir = os.path.expanduser("~/")

        with open(os.path.join(homedir, '.config', 'stopgo.conf.json'), 'w') as outfile:
            json.dump(self.newprefs, outfile)

