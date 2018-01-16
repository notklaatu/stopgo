import wx
import os
from datetime import date

def OnAboutBox(self):
        
    description = """StopGo helps you create stop motion animation."""

    licence = """StopGo is free software; you can redistribute 
it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation; either version 3 of the License, 
or (at your option) any later version.

StopGo is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
See the GNU General Public License for more details. You should have 
received a copy of the GNU General Public License along with File Hunter; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, 
Suite 330, Boston, MA  VERSION_STRIVERSION_STRIVERSION_STRINVERSION_STRING307  USA"""

    info = wx.AboutDialogInfo()

    info.SetIcon(wx.Icon(os.path.join(os.path.dirname(__file__),'..','..','stopgo','images','makerbox.png'), wx.BITMAP_TYPE_PNG))
    info.SetName('StopGo')
    info.SetVersion('0.8.18')
    info.SetDescription(description)
    info.SetCopyright('(C) 2016 - ' + str(date.today().year) + ' Seth Kenlon')
    info.SetWebSite('http://makerbox.org.nz')
    info.SetLicence(licence)
    info.AddDeveloper('Klaatu, Seth Kenlon, Jess Weichler')

    wx.AboutBox(info)
