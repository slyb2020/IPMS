# _*_ coding: UTF-8 _*_
# ----------------------------------------------------------------------------
# Name:         Main.py
# Purpose:      Testing lots of stuff, controls, window types, etc.
#
# Author:       Robin Dunn
#
# Created:      A long time ago, in a galaxy far, far away...
# Copyright:    (c) 1999-2020 by Total Control Software
# Licence:      wxWindows license
# Tags:         phoenix-port, py3-port
# ----------------------------------------------------------------------------
import wx.lib.agw.flatmenu as FM
import wx.lib.mixins.inspection
from wx.adv import SplashScreen as SplashScreen
from wx.lib.agw.artmanager import ArtManager, DCSaver
from wx.lib.agw.fmresources import ControlFocus, ControlPressed
from wx.lib.agw.fmresources import FM_OPT_SHOW_TOOLBAR

from BackgoundPanel import BackgroundPanel
from DBOperation import GetEnterpriseInfo, GetStaffInfoWithPassword
from MyClass import *
from PasswordDialog import PasswordDialog
from SetupPropertyDialog import SetupPropertyDialog
from DBOperation import GetAllPasswords
from ID_DEFINE import *
import time

# VERSION_STRING = "20220313A7"
VERSION_STRING = "221208"


def switchRGBtoBGR(colour):
    return wx.Colour(colour.Blue(), colour.Green(), colour.Red())


class FM_MyRenderer(FM.FMRenderer):
    def __init__(self):
        FM.FMRenderer.__init__(self)

    def DrawMenuButton(self, dc, rect, state):
        self.DrawButton(dc, rect, state)

    def DrawMenuBarButton(self, dc, rect, state):
        self.DrawButton(dc, rect, state)

    def DrawButton(self, dc, rect, state, colour=None):
        if state == ControlFocus:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        elif state == ControlPressed:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().HighlightBackgroundColour())
        else:  # ControlNormal, ControlDisabled, default
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRoundedRectangle(rect.x, rect.y, rect.width, rect.height, 4)

    def DrawMenuBarBackground(self, dc, rect):
        vertical = ArtManager.Get().GetMBVerticalGradient()
        dcsaver = DCSaver(dc)
        # fill with gradient
        startColour = self.menuBarFaceColour
        endColour = ArtManager.Get().LightColour(startColour, 90)
        dc.SetPen(wx.Pen(endColour))
        dc.SetBrush(wx.Brush(endColour))
        dc.DrawRectangle(rect)

    def DrawToolBarBg(self, dc, rect):
        if not ArtManager.Get().GetRaiseToolbar():
            return
        # fill with gradient
        startColour = self.menuBarFaceColour()
        dc.SetPen(wx.Pen(startColour))
        dc.SetBrush(wx.Brush(startColour))
        dc.DrawRectangle(0, 0, rect.GetWidth(), rect.GetHeight())


class FlatMenuFrame(wx.Frame):
    def __init__(self, parent):
        # ?????????????????????????????????????????????wx.MAXIMIZE
        wx.Frame.__init__(self, parent, size=(1800, 1000), style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetIcon(images.Mondrian.GetIcon())
        self.enterpriseName = enterpriseName
        self.SetTitle("%s????????????????????????   Version??????1.%s" % (self.enterpriseName, VERSION_STRING))
        self.check_in_flag = False
        self.timer_count = 0
        # self.mouse_position = wx.Point()
        self.pswList = []
        self.infoList = []
        self.operatorID = ''
        self.operatorName = ''
        self.folderState = ''
        _, self.pswList,self.infoList = GetAllPasswords(None,WHICHDB)

        self.operator_role = 0
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # Create a main panel and place some controls on it
        self.mainPANEL = BackgroundPanel(self)
        # from MyClass import MainPanel
        # if self.check_in_flag:
        #     self.mainPANEL = MainPanel(self, wx.ID_ANY)
        # else:
        #     self.mainPANEL = BackgroundPanel(self)
        from MyStatusBar import MyStatusBar
        self.statusbar = MyStatusBar(self)
        self.SetStatusBar(self.statusbar)
        self.CreateMenu()
        self.ConnectEvents()
        mainSizer.Add(self._mb, 0, wx.EXPAND)
        mainSizer.Add(self.mainPANEL, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        mainSizer.Layout()
        ArtManager.Get().SetMBVerticalGradient(True)
        ArtManager.Get().SetRaiseToolbar(False)
        self._mb.Refresh()
        self.CenterOnScreen()
        self._mb.GetRendererManager().SetTheme(FM.StyleVista)
        self.check_in_flag = False

    def UpdateMainUI(self):
        self.Freeze()
        self._mb.Destroy()
        try:
            self.mainPANEL.Destroy()
        except:
            pass
        self.CreateMenu()
        if self.check_in_flag:
            self.mainPANEL = MainPanel(self, wx.ID_ANY)
        else:
            self.mainPANEL = BackgroundPanel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self._mb, 0, wx.EXPAND)
        mainSizer.Add(self.mainPANEL, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Thaw()

    def CreateMenu(self):
        # Create the menubar
        self._mb = FM.FlatMenuBar(self, wx.ID_ANY, 48, 5, options=FM_OPT_SHOW_TOOLBAR)
        fileMenu = FM.FlatMenu()
        fileMenuOut = FM.FlatMenu()
        setupMenu = FM.FlatMenu()
        helpMenu = FM.FlatMenu()
        subMenuExit = FM.FlatMenu()
        self.newMyTheme = self._mb.GetRendererManager().AddRenderer(FM_MyRenderer())
        new_file_bmp = wx.Bitmap("d:/IPMS/dist/bitmaps/filenew.png", wx.BITMAP_TYPE_PNG)
        view1Bmp = wx.Bitmap("d:/IPMS/dist/bitmaps/sunling3.png", wx.BITMAP_TYPE_PNG)
        view3Bmp = wx.Bitmap("d:/IPMS/dist/bitmaps/lbadd.png", wx.BITMAP_TYPE_PNG)
        view2Bmp = wx.Bitmap("d:/IPMS/dist/bitmaps/lbcharge.png", wx.BITMAP_TYPE_PNG)
        view4Bmp = wx.Bitmap("d:/IPMS/dist/bitmaps/filesave.png", wx.BITMAP_TYPE_PNG)
        contractBmp = wx.Bitmap("d:/IPMS/dist/bitmaps/33.png", wx.BITMAP_TYPE_PNG)
        order1Bmp = wx.Bitmap("d:/IPMS/dist/bitmaps/opened.png", wx.BITMAP_TYPE_PNG)
        order2Bmp = wx.Bitmap("d:/IPMS/dist/bitmaps/locked.png", wx.BITMAP_TYPE_PNG)
        order3Bmp = wx.Bitmap("d:/IPMS/dist/bitmaps/order3.png", wx.BITMAP_TYPE_PNG)
        propertyBmp = wx.Bitmap("d:/IPMS/dist/bitmaps/property.png", wx.BITMAP_TYPE_PNG)

        # Set an icon to the exit/help/transparency menu item
        exitImg = wx.Bitmap("d:/IPMS/dist/bitmaps/exit-16.png", wx.BITMAP_TYPE_PNG)
        helpImg = wx.Bitmap("d:/IPMS/dist/bitmaps/help-16.png", wx.BITMAP_TYPE_PNG)
        ghostBmp = wx.Bitmap("d:/IPMS/dist/bitmaps/field-16.png", wx.BITMAP_TYPE_PNG)

        # Create the menu items
        item = FM.FlatMenuItem(fileMenu, MENU_CHECK_IN, "&R ????????????...\tCtrl+R", "????????????", wx.ITEM_NORMAL)
        fileMenuOut.AppendItem(item)
        item = FM.FlatMenuItem(fileMenu, MENU_CHECK_OUT, "&R ??????...\tCtrl+R", "????????????", wx.ITEM_NORMAL)
        fileMenu.AppendItem(item)

        item = FM.FlatMenuItem(setupMenu, MENU_SETUP_PROPERTY, "&O ??????????????????...\tCtrl+O", "??????????????????", wx.ITEM_NORMAL)
        setupMenu.AppendItem(item)

        if self.check_in_flag:
            self._mb.AddTool(MENU_NEW_FILE, u"????????????", view1Bmp)
            self._mb.AddTool(MENU_CHECK_OUT, u"??????...", order2Bmp)
            self._mb.AddTool(MENU_SETUP_PROPERTY, u"??????????????????", propertyBmp)
        else:
            self._mb.AddTool(MENU_CHECK_IN, u"&R ????????????...\tCtrl+R", order1Bmp)
        self._mb.AddSeparator()  # Separator

        self._mb.AddRadioTool(wx.ID_ANY, "View Details", view3Bmp)
        self._mb.AddRadioTool(wx.ID_ANY, "View Details", view4Bmp)
        self._mb.AddRadioTool(wx.ID_ANY, "View Multicolumn", contractBmp)
        self._mb.AddRadioTool(wx.ID_ANY, "View Multicolumn", order1Bmp)
        self._mb.AddRadioTool(wx.ID_ANY, "View Multicolumn", order2Bmp)
        self._mb.AddRadioTool(wx.ID_ANY, "View Multicolumn", order3Bmp)

        # Add non-toolbar item
        item = FM.FlatMenuItem(subMenuExit, wx.ID_EXIT, "E&xit\tAlt+X", "Exit demo", wx.ITEM_NORMAL, None, exitImg)
        subMenuExit.AppendItem(item)
        fileMenu.AppendSeparator()
        item = FM.FlatMenuItem(subMenuExit, wx.ID_EXIT, "E&xit\tAlt+Q", "Exit demo", wx.ITEM_NORMAL, None, exitImg)
        fileMenu.AppendItem(item)
        fileMenuOut.AppendItem(item)

        item = FM.FlatMenuItem(helpMenu, MENU_HELP, "&A??????\tCtrl+H", "??????...", wx.ITEM_NORMAL, None, helpImg)
        helpMenu.AppendItem(item)

        fileMenu.SetBackgroundBitmap(CreateBackgroundBitmap())

        # Add menu to the menu bar
        if self.check_in_flag:
            self._mb.Append(fileMenu, "&F ??????")
            self._mb.Append(setupMenu, "&O ??????????????????")
            self._mb.Append(helpMenu, "&H ??????")
        else:
            self._mb.Append(fileMenuOut, "&F ??????")
            self._mb.Append(helpMenu, "&H ??????")

    def ConnectEvents(self):
        # Attach menu events to some handlers
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnAbout, id=MENU_HELP)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnCheckIn, id=MENU_CHECK_IN)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnSetupProperty, id=MENU_SETUP_PROPERTY)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnCheckOut, id=MENU_CHECK_OUT)

    def OnSetupProperty(self, event):
        if self.operatorCharacter == '????????????':
            dlg = SetupPropertyDialog(self, self.mainPANEL.log)
            dlg.CenterOnScreen()
            dlg.ShowModal()
            dlg.Destroy()
        else:
            wx.MessageBox("????????????????????????????????????!","????????????")

    def OnCheckOut(self, event):
        # self.mainPANEL.work_zone_Panel.orderManagementPanel.orderUpdateCheckThread.Stop()
        self.check_in_flag = False
        self.operatorName = ""
        self.statusbar.SetStatusText("???????????????%s ?????????  " % self.operatorName, 2)
        self.UpdateMainUI()

    def OnCheckIn(self, event):
        password = ''
        dlg = PasswordDialog(self)
        dlg.CenterOnScreen()
        if dlg.ShowModal() == wx.ID_OK:
            password = dlg.pswTXT.GetValue()
        dlg.Destroy()
        if password != '' and password in self.pswList:
            staffInfo = self.infoList[self.pswList.index(password)]
            if staffInfo[5] == "??????":
                self.operatorCharacter = staffInfo[2]
                self.operatorName = staffInfo[3]
                self.operatorID = staffInfo[4]
                self.check_in_flag = True
                self.statusbar.SetStatusText(
                    "??????????????? %s->%s->%s->%s ?????????  " % (staffInfo[0], staffInfo[1], staffInfo[2], self.operatorName), 2)
                self.UpdateMainUI()
            else:
                dlg = wx.MessageDialog(self, '???????????????????????????????????????', "????????????",
                                       wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
        else:
            dlg = wx.MessageDialog(self, '????????????????????????????????????', "????????????",
                                   wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def UpdateMenuState(self):
        self._mb.FindMenuItem(MENU_CHECK_IN).Enable(not self.check_in_flag)
        self._mb.FindMenuItem(MENU_CHECK_OUT).Enable(self.check_in_flag)

    def OnSize(self, event):
        self._mgr.Update()
        self.Layout()

    def OnQuit(self, event):
        self.Destroy()

    def OnAbout(self, event):
        msg = "%s ????????????????????????\n\n" % self.enterpriseName + \
              "???????????????????????? ???????????? 2021??????2029\n\n" + \
              "\n" + \
              "????????????????????????:\n\n" + \
              "slyb@tju.edu.cn\n\n" + \
              "????????? 0." + VERSION_STRING
        dlg = wx.MessageDialog(self, msg, "??????",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class MySplashScreen(SplashScreen):
    def __init__(self):
        bmp = wx.Image("d:/IPMS/dist/bitmaps/BackgroundPIC.jpg").ConvertToBitmap()
        SplashScreen.__init__(self, bmp,
                              wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                              3000, None, -1)   #3000???????????????EVT_CLOSE????????????Splash??????
        wx.Yield()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        global  enterpriseName
        _, enterpriseName = GetEnterpriseInfo(None, WHICHDB)
        self.fc = wx.CallLater(10, self.ShowMain)   #self.fc??????wx.CallLater???????????????10???????????????

    def OnClose(self, evt):
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()

    def ShowMain(self):
        self.frame = FlatMenuFrame(None)
        self.frame.Show()
        if self.fc.IsRunning():#??????CallLater???????????????????????????splashScreen??????????????????????????????SplashScreen?????????????????????
            self.Raise()
        wx.CallAfter(self.frame.OnCheckIn, None)  #????????????????????????????????????????????????OnCheckIn??????


class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        splash = MySplashScreen()
        splash.Show()

        return True


def main():
    app = MyApp(False)
    app.MainLoop()


if __name__ == '__main__':
    __name__ = 'Main'
    main()
