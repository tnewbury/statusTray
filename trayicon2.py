#!/usr/bin/env python
import wx
import time
#from subprocess import Popen, PIPE
import subprocess

TRAY_TOOLTIP = 'System Tray Demo'
#TRAY_ICON = 'icon.png'

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    
    def __init__(self, frame):

        self.TRAY_ICON = 'icon.png'
	self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(self.TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_update, self.timer)
        self.timer.Start(100)
        


    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Backup', self.on_backup)
        create_menu_item(menu, 'Restore', self.on_restore)
	create_menu_item(menu, 'Patches', self.on_patches)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
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
	self.set_icon(self.TRAY_ICON)


    def on_backup(self, event):
        cmdOutput = subprocess.Popen(["zenity --warning --text 'Backing up your shit'"],shell=True,stdout=subprocess.PIPE) 
        self.TRAY_ICON = "icon_red.png"
        cmdOutput = subprocess.Popen(["lsyncd -nodaemon -rsync /home/`whoami` /nfs/test/"],shell=True,stdout=subprocess.PIPE)
        self.TRAY_ICON = "icon_green.png"

    def on_restore(self, event):
        cmdOutput = subprocess.Popen(["zenity --warning --text 'Restoring. Youre shit'"],shell=True,stdout=subprocess.PIPE)
        self.TRAY_ICON = "icon.png" 
        cmdOutput = subprocess.Popen(["lsyncd -nodaemon -rsync /nfs/test /home/`whoami`"],shell=True,stdout=subprocess.PIPE)
        self.TRAY_ICON = "icon_green.png"

    def on_patches(self, event):
        #print "apt-get upgrade -s | egrep -o '(^[0-9]+)'"
        cmdOutput = subprocess.check_output(["apt-get upgrade -s | egrep -o '(^[0-9]+)'"],shell=True)
	if len(cmdOutput) >= 3:
            print "Patches to be had"
            self.TRAY_ICON = "icon_red.png"


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
