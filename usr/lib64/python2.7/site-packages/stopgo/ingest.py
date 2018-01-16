# -*- coding: utf-8 -*-
import wx
import wx.lib.scrolledpanel
import os
import sqlite3 as sq
from datetime import datetime, date
import time

def Ingest(self):
    openMsg='Choose a image directory'
    wcd = 'All files (*)|*|Image Directory (*)|*'
    dirname = os.path.join(os.path.expanduser('~'),self.myprefs['dir'])
    
    od = wx.DirDialog(self, message=openMsg,
                      style=wx.FD_OPEN|wx.FD_CHANGE_DIR)

    if od.ShowModal() == wx.ID_OK:
        projpath= os.path.join( od.GetPath() )
        print(projpath)
        dbfile = os.path.join ( os.path.dirname(projpath), os.path.basename( od.GetPath())) + '_import_' + str(time.time()).split('.')[0]
        self.imgdir = projpath

        #with open(os.path.join(projpath,dbfile), 'a'):
        #    os.utime(path, None)
        open( dbfile, 'a' ).close()

        self.con = sq.connect(dbfile, isolation_level=None )

        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Project(Id INTEGER PRIMARY KEY, Path TEXT, Name TEXT, [timestamp] timestamp)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Timeline(Id INTEGER PRIMARY KEY, Image TEXT, Blackspot INT)")
        self.cur.execute("INSERT INTO Project(Path, Name, timestamp) VALUES (?,?,?)", ("images", "StopGo Project", datetime.now() ))

        for counter, item in enumerate( sorted(os.listdir(self.imgdir)) ):
            self.cur.execute("INSERT INTO Project(Path, Name, timestamp) VALUES (?,?,?)", ("images", "Default Project", datetime.now() ))
            self.cur.execute("INSERT INTO Project(Path, Name, timestamp) VALUES (?,?,?)", ("images", "Default Project", datetime.now() ))
            self.cur.execute('INSERT INTO Timeline VALUES(?,?,?)', (counter,item,0))

        self.BuildTimeline(dbfile)
