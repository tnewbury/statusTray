#!/usr/bin/env python
import wx
import time
#from subprocess import Popen, PIPE
import subprocess
import re


TRAY_TOOLTIP = 'Backup/patch system'
#TRAY_ICON = 'icon.png'

def create_menu_item(menu, label, func, iconpath):
    item = wx.MenuItem(menu, -1, label)
    item.SetBitmap(wx.Bitmap(iconpath))
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    
    def __init__(self, frame):

        self.checkpatches = 0
        self.TRAY_ICON = 'icon.png'
	self.patchicon = 'gtick.png'
        self.backupicon = 'gtick.png'
        self.restoreicon = 'gtick.png'
        self.healthscore = 3

        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(self.TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update, self.timer)
        self.timer.Start(500)
        cmdOutput = subprocess.check_output(["cat /proc/version"],shell=True)
        result = re.search('Hat|Ubuntu',cmdOutput)
        if result.group(0) == 'Hat':
            self.lversion = 0
	else:
            self.lversion = 1

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, '&Backup', self.on_backup, self.backupicon)
        create_menu_item(menu, '&Restore', self.on_restore, self.restoreicon)
	create_menu_item(menu, '&Patched', self.on_patches, self.patchicon)
        menu.AppendSeparator()
        create_menu_item(menu, 'E&xit', self.on_exit, 'rcross.png')
	return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print 'Tray icon was left-clicked.'
        
    def on_update(self, event):
        #if self.TRAY_ICON == "icon.png":
        #    self.TRAY_ICON = "icon_red.png"
        #else:
        #    self.TRAY_ICON = "icon.png"
	self.checkpatches += 1
        if self.checkpatches == 3600:
                self.on_patches(wx.EVT_TASKBAR_LEFT_DOWN)
        if self.healthscore >= 3:
                self.TRAY_ICON = "icon_green.png"
        else:
                self.TRAY_ICON = "icon_red.png"
        self.set_icon(self.TRAY_ICON)


    def on_backup(self, event):
        cmdOutput = subprocess.Popen(["zenity --warning --text 'Backing up your shit'"],shell=True,stdout=subprocess.PIPE) 
        self.TRAY_ICON = "icon_red.png"
        self.backupicon = "gup.png"
        self.healthscore -= 1
        cmdOutput = subprocess.Popen(["lsyncd -nodaemon -rsync /home/`whoami`/ /nfs/test/"],shell=True,stdout=subprocess.PIPE)
        self.TRAY_ICON = "icon_green.png"
        self.backupicon = "gtick.png"
        self.healthscore += 1

    def on_restore(self, event):
        cmdOutput = subprocess.Popen(["zenity --warning --text 'Restoring. Youre shit'"],shell=True,stdout=subprocess.PIPE)
        self.TRAY_ICON = "icon.png"
        self.restoreicon = "gdown.png"
        self.healthscore -= 1 
        cmdOutput = subprocess.Popen(["lsyncd -nodaemon -rsync /nfs/test /home/`whoami`"],shell=True,stdout=subprocess.PIPE)
        self.TRAY_ICON = "icon_green.png"
        self.restoreicon = "gtick.png"
        self.healthscore += 1

    def on_patches(self, event):
        #print "apt-get upgrade -s | egrep -o '(^[0-9]+)'"
        if self.lversion == 1:
            cmdOutput = subprocess.check_output(["apt-get upgrade -s | wc -l"],shell=True)
	    if cmdOutput >= 10:
                print "Patches to be had"
                #self.TRAY_ICON = "icon_red.png"
                self.patchicon = "rcross.png"
                self.healthscore -= 1
            else:
                #self.TRAY_ICON = "icon_green.png"
                self.patchicon = "gtick.png"
                self.healthscore = 3
                
        if self.lversion == 0:
            cmdOutput = subprocess.check_output(["yum check-update | wc -l"],shell=True)
            if cmdOutput >= 2:
                print "Patches to be had"
                #self.TRAY_ICON = "icon_red.png"
                self.patchicon = "rcross.png"
                self.healthscore -= 1
            else:
                #self.TRAY_ICON = "icon_green.png"
                self.patchicon = "gtick.png"
                self.healthscore = 3

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
