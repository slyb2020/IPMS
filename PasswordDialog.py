import wx
import os
from DBOperation import GetAllPasswords
from ID_DEFINE import *

class PasswordDialog(wx.Dialog):
    def __init__(self, parent, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "操作员登录对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(300, 60))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(panel, label='请输入您的登录密码：'), 0, wx.TOP, 5)
        self.pswTXT = wx.TextCtrl(panel, size=(100, 25), style=wx.TE_PASSWORD)
        hbox.Add(self.pswTXT, 1, wx.LEFT | wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.EXPAND)
        panel.SetSizer(vbox)
        # panel.SetBackgroundColour(wx.Colour(234,219,212))
        sizer.Add(panel, 0, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)
        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(bitmapDir+"/ok4.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确定", size=(120, 35))
        btn_ok.SetDefault()
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取消", size=(120, 35))
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_ok, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_cancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.tryTimes=4

    def OnOk(self, event):
        psw = self.pswTXT.GetValue()
        if psw not in self.parent.pswList:
            self.tryTimes -= 1
            if self.tryTimes>0:
                self.pswTXT.SetValue('')
                self.pswTXT.SetFocus()
                dlg = wx.MessageDialog(self, '您输入的密码错误，您还有%d次机会重新输入！'%self.tryTimes,
                                       '信息提示',
                                       wx.OK | wx.ICON_INFORMATION
                                       # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
                dlg.ShowModal()
                dlg.Destroy()
                return
        event.Skip()

    def OnCancel(self, event):
        # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
        event.Skip()
