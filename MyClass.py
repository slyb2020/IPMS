import wx
import images
from ID_DEFINE import *
from MyLog import MyLogCtrl
import wx.lib.agw.foldpanelbar as fpb
from SystemIntroductionPanel import SystemIntroductionPanel
from six import BytesIO
import wx.lib.agw.aquabutton as AB
from OrderManagementPanel import OrderManagementPanel, CreateNewOrderDialog
import time

def GetCollapsedIconData():
    return \
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x8eIDAT8\x8d\xa5\x93-n\xe4@\x10\x85?g\x03\n6lh)\xc4\xd2\x12\xc3\x81\
\xd6\xa2I\x90\x154\xb9\x81\x8f1G\xc8\x11\x16\x86\xcd\xa0\x99F\xb3A\x91\xa1\
\xc9J&\x96L"5lX\xcc\x0bl\xf7v\xb2\x7fZ\xa5\x98\xebU\xbdz\xf5\\\x9deW\x9f\xf8\
H\\\xbfO|{y\x9dT\x15P\x04\x01\x01UPUD\x84\xdb/7YZ\x9f\xa5\n\xce\x97aRU\x8a\
\xdc`\xacA\x00\x04P\xf0!0\xf6\x81\xa0\xf0p\xff9\xfb\x85\xe0|\x19&T)K\x8b\x18\
\xf9\xa3\xe4\xbe\xf3\x8c^#\xc9\xd5\n\xa8*\xc5?\x9a\x01\x8a\xd2b\r\x1cN\xc3\
\x14\t\xce\x97a\xb2F0Ks\xd58\xaa\xc6\xc5\xa6\xf7\xdfya\xe7\xbdR\x13M2\xf9\
\xf9qKQ\x1fi\xf6-\x00~T\xfac\x1dq#\x82,\xe5q\x05\x91D\xba@\xefj\xba1\xf0\xdc\
zzW\xcff&\xb8,\x89\xa8@Q\xd6\xaaf\xdfRm,\xee\xb1BDxr#\xae\xf5|\xddo\xd6\xe2H\
\x18\x15\x84\xa0q@]\xe54\x8d\xa3\xedf\x05M\xe3\xd8Uy\xc4\x15\x8d\xf5\xd7\x8b\
~\x82\x0fh\x0e"\xb0\xad,\xee\xb8c\xbb\x18\xe7\x8e;6\xa5\x89\x04\xde\xff\x1c\
\x16\xef\xe0p\xfa>\x19\x11\xca\x8d\x8d\xe0\x93\x1b\x01\xd8m\xf3(;x\xa5\xef=\
\xb7w\xf3\x1d$\x7f\xc1\xe0\xbd\xa7\xeb\xa0(,"Kc\x12\xc1+\xfd\xe8\tI\xee\xed)\
\xbf\xbcN\xc1{D\x04k\x05#\x12\xfd\xf2a\xde[\x81\x87\xbb\xdf\x9cr\x1a\x87\xd3\
0)\xba>\x83\xd5\xb97o\xe0\xaf\x04\xff\x13?\x00\xd2\xfb\xa9`z\xac\x80w\x00\
\x00\x00\x00IEND\xaeB`\x82'


def GetCollapsedIconBitmap():
    return wx.Bitmap(GetCollapsedIconImage())


def GetCollapsedIconImage():
    stream = BytesIO(GetCollapsedIconData())
    return wx.Image(stream)


def GetExpandedIconData():
    return \
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x9fIDAT8\x8d\x95\x93\xa1\x8e\xdc0\x14EO\xb2\xc4\xd0\xd2\x12\xb7(mI\
\xa4%V\xd1lQT4[4-\x9a\xfe\xc1\xc2|\xc6\xc2~BY\x83:A3E\xd3\xa0*\xa4\xd2\x90H!\
\x95\x0c\r\r\x1fK\x81g\xb2\x99\x84\xb4\x0fY\xd6\xbb\xc7\xf7>=\'Iz\xc3\xbcv\
\xfbn\xb8\x9c\x15 \xe7\xf3\xc7\x0fw\xc9\xbc7\x99\x03\x0e\xfbn0\x99F+\x85R\
\x80RH\x10\x82\x08\xde\x05\x1ef\x90+\xc0\xe1\xd8\ryn\xd0Z-\\A\xb4\xd2\xf7\
\x9e\xfbwoF\xc8\x088\x1c\xbbae\xb3\xe8y&\x9a\xdf\xf5\xbd\xe7\xfem\x84\xa4\
\x97\xccYf\x16\x8d\xdb\xb2a]\xfeX\x18\xc9s\xc3\xe1\x18\xe7\x94\x12cb\xcc\xb5\
\xfa\xb1l8\xf5\x01\xe7\x84\xc7\xb2Y@\xb2\xcc0\x02\xb4\x9a\x88%\xbe\xdc\xb4\
\x9e\xb6Zs\xaa74\xadg[6\x88<\xb7]\xc6\x14\x1dL\x86\xe6\x83\xa0\x81\xba\xda\
\x10\x02x/\xd4\xd5\x06\r\x840!\x9c\x1fM\x92\xf4\x86\x9f\xbf\xfe\x0c\xd6\x9ae\
\xd6u\x8d \xf4\xf5\x165\x9b\x8f\x04\xe1\xc5\xcb\xdb$\x05\x90\xa97@\x04lQas\
\xcd*7\x14\xdb\x9aY\xcb\xb8\\\xe9E\x10|\xbc\xf2^\xb0E\x85\xc95_\x9f\n\xaa/\
\x05\x10\x81\xce\xc9\xa8\xf6><G\xd8\xed\xbbA)X\xd9\x0c\x01\x9a\xc6Q\x14\xd9h\
[\x04\xda\xd6c\xadFkE\xf0\xc2\xab\xd7\xb7\xc9\x08\x00\xf8\xf6\xbd\x1b\x8cQ\
\xd8|\xb9\x0f\xd3\x9a\x8a\xc7\x08\x00\x9f?\xdd%\xde\x07\xda\x93\xc3{\x19C\
\x8a\x9c\x03\x0b8\x17\xe8\x9d\xbf\x02.>\x13\xc0n\xff{PJ\xc5\xfdP\x11""<\xbc\
\xff\x87\xdf\xf8\xbf\xf5\x17FF\xaf\x8f\x8b\xd3\xe6K\x00\x00\x00\x00IEND\xaeB\
`\x82'


def GetExpandedIconBitmap():
    return wx.Bitmap(GetExpandedIconImage())


def GetExpandedIconImage():
    stream = BytesIO(GetExpandedIconData())
    return wx.Image(stream)


def CreateBackgroundBitmap():
    mem_dc = wx.MemoryDC()
    bmp = wx.Bitmap(200, 300)
    mem_dc.SelectObject(bmp)
    mem_dc.Clear()
    # colour the menu face with background colour
    top = wx.Colour("blue")
    bottom = wx.Colour("light blue")
    filRect = wx.Rect(0, 0, 200, 300)
    mem_dc.GradientFillConcentric(filRect, top, bottom, wx.Point(100, 150))
    mem_dc.SelectObject(wx.NullBitmap)
    return bmp


class MainPanel(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(1024, 768), style=wx.TAB_TRAVERSAL):
        wx.Panel.__init__(self, parent, id, pos, size, style)
        self.parent = parent
        self.Freeze()
        il = wx.ImageList(16, 16)
        self.idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.idx2 = il.Add(images.GridBG.GetBitmap())
        self.idx3 = il.Add(images.Smiles.GetBitmap())
        self.idx4 = il.Add(images._rt_undo.GetBitmap())
        self.idx5 = il.Add(images._rt_save.GetBitmap())
        self.idx6 = il.Add(images._rt_redo.GetBitmap())

        self._leftWindow1 = wx.adv.SashLayoutWindow(self, ID_WINDOW_LEFT, wx.DefaultPosition,
                                                    wx.Size(200, 1000), wx.NO_BORDER |
                                                    wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        # will occupy the space not used by the Layout Algorithm
        self.CreateBottomWindow()
        self.log = MyLogCtrl(self.bottomWindow, -1, "")
        self.work_zone_Panel = WorkZonePanel(self, self.parent, self.log)
        self.Thaw()
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.ReCreateFoldPanel(0)
        self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=ID_WINDOW_LEFT,
                  id2=ID_WINDOW_BOTTOM)  # BOTTOM和LEFT顺序不能换，要想更改哪个先分，只需更改上面窗口定义的顺序
        self._pnl.Bind(fpb.EVT_CAPTIONBAR, self.OnPressCaption)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNoteBookPageChanged)

    def CreateBottomWindow(self):
        self.bottomWindow = wx.adv.SashLayoutWindow(self, ID_WINDOW_BOTTOM, style=wx.NO_BORDER | wx.adv.SW_3D)
        self.bottomWindow.SetDefaultSize((1000, 200))
        self.bottomWindow.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
        self.bottomWindow.SetAlignment(wx.adv.LAYOUT_BOTTOM)
        # win.SetBackgroundColour(wx.Colour(0, 0, 255))
        self.bottomWindow.SetSashVisible(wx.adv.SASH_TOP, True)
        self.bottomWindow.SetExtraBorderSize(5)

    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.work_zone_Panel)
        event.Skip()

    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return
        eID = event.GetId()
        if eID == ID_WINDOW_LEFT:
            self._leftWindow1.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eID == ID_WINDOW_BOTTOM:
            self.bottomWindow.SetDefaultSize((1000, event.GetDragRect().height))
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.work_zone_Panel)
        self.work_zone_Panel.Refresh()

    def ReCreateFoldPanel(self, fpb_flags, state=0):
        # delete earlier panel
        self._leftWindow1.Freeze()
        self._leftWindow1.DestroyChildren()
        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1, -1), agwStyle=fpb_flags | fpb.FPB_COLLAPSE_TO_BOTTOM)
        Images = wx.ImageList(16, 16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())

        if self.parent.operatorCharacter in ["技术员", "技术主管", "技术部长", "下单员", "经理"]:
            item = self._pnl.AddFoldPanel("订单操作面板", collapsed=False,
                                          foldIcons=Images)
            item.SetLabel("订单操作面板")
            panel = wx.Panel(item, -1, size=(300, 700))
            vbox = wx.BoxSizer(wx.VERTICAL)
            if self.parent.operatorCharacter == "下单员":
                bitmap = wx.Bitmap(bitmapDir + "/aquabutton.png",
                                   wx.BITMAP_TYPE_PNG)
                self.newOrderBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  新建订单", size=(100, 50))
                self.newOrderBTN.Bind(wx.EVT_BUTTON, self.OnCreateNewOrderBTN)
                self.newOrderBTN.SetForegroundColour(wx.BLACK)
                # self.editOrderBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  批量排产", size=(100, 50))
                # self.editOrderBTN.SetForegroundColour(wx.BLACK)
                static = wx.StaticLine(panel, -1)
                vbox.Add(self.newOrderBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
                # vbox.Add(self.editOrderBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
                vbox.Add(static, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            if self.parent.operatorCharacter in ["下单员", "技术员", "技术主管", "技术部长", "经理"]:
                value = "草稿订单"
                if self.parent.operatorCharacter == "下单员":
                    value = "草稿订单"
                self.orderTypeCOMBO = wx.ComboBox(panel, value=value, choices=["草稿订单", "在产订单", "完工订单", "废弃订单"])
                self.orderTypeCOMBO.Bind(wx.EVT_COMBOBOX, self.OnOrderTypeCOMBOChanged)
                vbox.Add(self.orderTypeCOMBO, 0, wx.EXPAND)
            self.orderInfoPanel = wx.Panel(panel, size=(-1, 500))
            vbox.Add(self.orderInfoPanel, 1, wx.EXPAND)
            panel.SetSizer(vbox)
            # self.ReCreateOrderInfoPanel()
            self._pnl.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 0)
            if self.parent.operatorCharacter in ["下单员", "技术员", "技术主管", "技术部长", '经理']:
                item.Expand()
            else:
                item.Collapse()

        if self.parent.operatorCharacter in ["采购员"]:
            item = self._pnl.AddFoldPanel("原材料价格操作面板", collapsed=False,
                                          foldIcons=Images)
            item.SetLabel("原材料价格操作面板")
            panel = wx.Panel(item, -1, size=(300, 700))
            vbox = wx.BoxSizer(wx.VERTICAL)
            if self.parent.operatorCharacter == "采购员":
                bitmap = wx.Bitmap(bitmapDir + "/aquabutton.png",
                                   wx.BITMAP_TYPE_PNG)
                self.inputTodayPriceBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  录入今日原材料价格", size=(100, 50))
                self.inputTodayPriceBTN.Bind(wx.EVT_BUTTON, self.OnInputTodayPriceBTN)
                self.inputTodayPriceBTN.SetForegroundColour(wx.BLACK)
                # self.editOrderBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "  批量排产", size=(100, 50))
                # self.editOrderBTN.SetForegroundColour(wx.BLACK)
                static = wx.StaticLine(panel, -1)
                vbox.Add(self.inputTodayPriceBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
                # vbox.Add(self.editOrderBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
                vbox.Add(static, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
            panel.SetSizer(vbox)
            # self.ReCreateOrderInfoPanel()
            self._pnl.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 0)
            if self.parent.operatorCharacter in ['采购员']:
                item.Expand()
            else:
                item.Collapse()

        self._leftWindow1.Thaw()

    def OnInputTodayPriceBTN(self, event):
        dlg = InputTodayPriceDialog(self, self.log)
        dlg.CenterOnScreen()
        dlg.ShowModal()
        dlg.Destroy()
        self.work_zone_Panel.orderManagementPanel.ReCreate()

    def OnOrderTypeCOMBOChanged(self, event):
        type = self.orderTypeCOMBO.GetValue()[:2]
        self.work_zone_Panel.orderManagementPanel.type = type
        self.work_zone_Panel.orderManagementPanel.ReCreate()

    def ReCreateOrderInfoPanel(self):
        self.orderInfoPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticBox(self.orderInfoPanel, label="订单详细信息", size=(-1, 1200))
        vbox.Add(title, 1, wx.EXPAND)
        self.orderInfoPanel.SetSizer(vbox)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        hhbox = wx.BoxSizer()
        hhbox.Add((5, -1))
        hhbox.Add(wx.StaticText(title, label="总面积:", size=(70, -1)), 0, wx.TOP, 5)
        self.orderTotalSquireTXT = wx.TextCtrl(title, size=(40, -1))
        hhbox.Add(self.orderTotalSquireTXT, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1, 5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5, -1))
        hhbox.Add(wx.StaticText(title, label="子订单数:", size=(70, -1)), 0, wx.TOP, 5)
        self.subOrderAmountTXT = wx.TextCtrl(title, size=(40, -1))
        hhbox.Add(self.subOrderAmountTXT, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1, 5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5, -1))
        hhbox.Add(wx.StaticText(title, label="总墙板数:", size=(70, -1)), 0, wx.TOP, 5)
        self.orderTotalPanelAmountTXT = wx.TextCtrl(title, size=(40, -1))
        hhbox.Add(self.orderTotalPanelAmountTXT, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1, 5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5, -1))
        hhbox.Add(wx.StaticText(title, label="总天花板数:", size=(70, -1)), 0, wx.TOP, 5)
        self.orderTotalCeilingAmountTXT = wx.TextCtrl(title, size=(40, -1))
        hhbox.Add(self.orderTotalCeilingAmountTXT, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1, 5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5, -1))
        hhbox.Add(wx.StaticText(title, label="总构件数:", size=(70, -1)), 0, wx.TOP, 5)
        self.orderTotalConstructionAmountTXT = wx.TextCtrl(title, size=(40, -1))
        hhbox.Add(self.orderTotalConstructionAmountTXT, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1, 5))
        hhbox = wx.BoxSizer()
        hhbox.Add((5, -1))
        bitmap = wx.Bitmap(os.path.normpath(bitmapDir + "/lbnews.png"), wx.BITMAP_TYPE_PNG)
        # self.addSubOrderBTN = GB.GradientButton(title,-1, bitmap,'追加子订单',size=(-1,40))
        self.addSubOrderBTN = wx.Button(title, label='追加子订单', size=(-1, 40))
        self.addSubOrderBTN.Bind(wx.EVT_BUTTON, self.OnAddSubOrderBTN)
        hhbox.Add(self.addSubOrderBTN, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        # vbox.Add((-1,5))
        # hhbox = wx.BoxSizer()
        # hhbox.Add((5,-1))
        # hhbox.Add(wx.StaticText(title,label="订单状态:",size=(70,-1)),0,wx.TOP,5)
        # self.orderStateTXT=wx.TextCtrl(title,size=(40,-1),style=wx.TE_READONLY)
        # self.orderStateTXT.SetValue(self.work_zone_Panel.orderManagmentPanel.data[7])
        # hhbox.Add(self.orderStateTXT,1,wx.RIGHT,5)
        # vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1, 10))
        vbox.Add(wx.StaticLine(title, style=wx.HORIZONTAL), 0, wx.EXPAND)
        vbox.Add((-1, 10))
        self.orderDetailNotebook = wx.Notebook(title, -1, size=(21, 800), style=
        wx.BK_DEFAULT
                                               # wx.BK_TOP
                                               # wx.BK_BOTTOM
                                               # wx.BK_LEFT
                                               # wx.BK_RIGHT
                                               # | wx.NB_MULTILINE
                                               , name="OrderDetail")
        il = wx.ImageList(16, 16)
        idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.total_page_num = 0
        self.orderDetailNotebook.AssignImageList(il)
        red = wx.Bitmap(os.path.normpath(bitmapDir + "/red.png"), wx.BITMAP_TYPE_PNG)
        blue = wx.Bitmap(os.path.normpath(bitmapDir + "/blue.png"), wx.BITMAP_TYPE_PNG)
        green = wx.Bitmap(os.path.normpath(bitmapDir + "/green.png"), wx.BITMAP_TYPE_PNG)
        idx2 = il.Add(images.GridBG.GetBitmap())
        idx3 = il.Add(images.Smiles.GetBitmap())
        idx4 = il.Add(images._rt_undo.GetBitmap())
        idx5 = il.Add(images._rt_save.GetBitmap())
        idx6 = il.Add(images._rt_redo.GetBitmap())
        idx7 = il.Add(red)
        idx8 = il.Add(green)
        idx9 = il.Add(blue)
        vbox.Add(self.orderDetailNotebook, 1, wx.EXPAND)
        self.currentOrderID = self.work_zone_Panel.manufactureManagementPanel.data[0]
        self.currentOrderSubOrderIDStr = self.work_zone_Panel.manufactureManagementPanel.data[8]
        self.currentOrderSubOrderStateStr = self.work_zone_Panel.manufactureManagementPanel.data[9]
        self.subOrderPanel = []
        self.suborderTotalSquireTXT = []
        self.suborderTotalPanelAmountTXT = []
        self.suborderTotalCeilingAmountTXT = []
        self.suborderTotalConstructionAmountTXT = []
        self.suborderStateTXT = []
        self.subOrderNameList = self.currentOrderSubOrderIDStr.split(',')
        self.subOrderStateList = self.currentOrderSubOrderStateStr.split(',')
        if len(self.subOrderStateList) != len(self.subOrderNameList):
            wx.MessageBox("子订单状态异常——子订单数不匹配，请进行数据检查！")
        subOrderAmount = len(self.subOrderNameList)
        # subOrderNum=GetSubOrderAmount(self.work_zone_Panel.orderManagmentPanel.data[0])#根据订单号，读取子订单数量
        for i in range(subOrderAmount):
            subPanel = wx.Panel(self.orderDetailNotebook, size=(100, 500))
            self.subOrderPanel.append(subPanel)
            self.orderDetailNotebook.AddPage(self.subOrderPanel[i], "%s#" % self.subOrderNameList[i])
            # okimage = wx.Bitmap(os.path.normpath(bitmapDir + "/ok3.png"), wx.BITMAP_TYPE_PNG)
            self.orderDetailNotebook.SetSelection(0)
            vvbox = wx.BoxSizer(wx.VERTICAL)
            hhbox = wx.BoxSizer()
            hhbox.Add((5, -1))
            hhbox.Add(wx.StaticText(self.subOrderPanel[i], label="子订单面积:", size=(70, -1)), 0, wx.TOP, 5)
            suborderTotalSquireTXT = wx.TextCtrl(self.subOrderPanel[i], size=(40, -1))
            self.suborderTotalSquireTXT.append(suborderTotalSquireTXT)
            hhbox.Add(self.suborderTotalSquireTXT[i], 1, wx.RIGHT, 5)
            vvbox.Add(hhbox, 0, wx.EXPAND)

            vvbox.Add((-1, 5))
            hhbox = wx.BoxSizer()
            hhbox.Add((5, -1))
            hhbox.Add(wx.StaticText(self.subOrderPanel[i], label="子订单墙板数:", size=(70, -1)), 0, wx.TOP, 5)
            suborderTotalPanelAmountTXT = wx.TextCtrl(self.subOrderPanel[i], size=(40, -1))
            self.suborderTotalPanelAmountTXT.append(suborderTotalPanelAmountTXT)
            hhbox.Add(self.suborderTotalPanelAmountTXT[i], 1, wx.RIGHT, 5)
            vvbox.Add(hhbox, 0, wx.EXPAND)

            vbox.Add((-1, 5))
            hhbox = wx.BoxSizer()
            hhbox.Add((5, -1))
            hhbox.Add(wx.StaticText(self.subOrderPanel[i], label="子订单天花板数:", size=(70, -1)), 0, wx.TOP, 5)
            suborderTotalCeilingAmountTXT = wx.TextCtrl(self.subOrderPanel[i], size=(40, -1))
            self.suborderTotalCeilingAmountTXT.append(suborderTotalCeilingAmountTXT)
            hhbox.Add(self.suborderTotalCeilingAmountTXT[i], 1, wx.RIGHT, 5)
            vvbox.Add(hhbox, 0, wx.EXPAND)

            vvbox.Add((-1, 5))
            hhbox = wx.BoxSizer()
            hhbox.Add((5, -1))
            hhbox.Add(wx.StaticText(self.subOrderPanel[i], label="子订单构件数:", size=(70, -1)), 0, wx.TOP, 5)
            suborderTotalConstructionAmountTXT = wx.TextCtrl(self.subOrderPanel[i], size=(40, -1))
            self.suborderTotalConstructionAmountTXT.append(suborderTotalConstructionAmountTXT)
            hhbox.Add(self.suborderTotalConstructionAmountTXT[i], 1, wx.RIGHT, 5)
            vvbox.Add(hhbox, 0, wx.EXPAND)

            vvbox.Add((-1, 5))
            hhbox = wx.BoxSizer()
            hhbox.Add((5, -1))
            hhbox.Add(wx.StaticText(self.subOrderPanel[i], label="子订单状态:", size=(70, -1)), 0, wx.TOP, 5)
            suborderStateTXT = wx.TextCtrl(self.subOrderPanel[i], size=(40, -1), style=wx.TE_READONLY)
            self.suborderStateTXT.append(suborderStateTXT)
            self.suborderStateTXT[i].SetValue(self.subOrderStateList[i])
            hhbox.Add(self.suborderStateTXT[i], 1, wx.RIGHT, 5)
            vvbox.Add(hhbox, 0, wx.EXPAND)
            vvbox.Add((-1, 10))
            vvbox.Add(wx.StaticLine(self.subOrderPanel[i], style=wx.HORIZONTAL), 0, wx.EXPAND)
            if self.subOrderStateList[i] == "接单":
                self.orderDetailNotebook.SetPageImage(i, idx7)
                self.specificOrderProductionBTN = wx.Button(self.subOrderPanel[i], label="子订单排产", size=(-1, 40),
                                                            name='子订单排产%d' % (i + 1))
                self.specificOrderProductionBTN.Bind(wx.EVT_BUTTON, self.OnSpecificOrderProductionBTN)
                vvbox.Add(self.specificOrderProductionBTN, 0, wx.EXPAND | wx.ALL, 5)
            elif self.subOrderStateList[i] == "已排产":
                self.orderDetailNotebook.SetPageImage(i, idx8)
                self.specificOrderPrintScheduleBTN = wx.Button(self.subOrderPanel[i], label="打印子订单任务单", size=(-1, 40),
                                                               name='子订单打印任务单%d' % (i + 1))
                self.specificOrderPrintScheduleBTN.Bind(wx.EVT_BUTTON, self.OnPrintScheduleBTN)
                vvbox.Add(self.specificOrderPrintScheduleBTN, 0, wx.EXPAND | wx.ALL, 5)
                self.glueSchedulePrintBTN = wx.Button(self.subOrderPanel[i], label="打印子订单胶水单", size=(-1, 40),
                                                      name='子订单打印胶水单%d' % (i + 1))
                self.glueSchedulePrintBTN.Bind(wx.EVT_BUTTON, self.OnGlueSchedulePrintBTN)
                vvbox.Add(self.glueSchedulePrintBTN, 0, wx.EXPAND | wx.ALL, 5)
                self.packageBTN = wx.Button(self.subOrderPanel[i], label="子订单打包", size=(-1, 40),
                                            name='子订单产品打包%d' % (i + 1))
                self.packageBTN.Bind(wx.EVT_BUTTON, self.OnPackageBTN)
                vvbox.Add(self.packageBTN, 0, wx.EXPAND | wx.ALL, 5)
            self.subOrderPanel[i].SetSizer(vvbox)

        title.SetSizer(vbox)
        self.orderInfoPanel.Layout()

    def OnGlueSchedulePrintBTN(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        suborderNumber = name[-1]
        message = "系统正在处理胶水单数据，请稍候..."
        busy = PBI.PyBusyInfo(message, parent=None, title="系统正忙",
                              icon=images.Smiles.GetBitmap())

        wx.Yield()
        self.productionSchedule = ProductionScheduleAlgorithm(self.log,
                                                              self.work_zone_Panel.manufactureManagementPanel.data[0],
                                                              suborderNumber)
        if self.productionSchedule.wrongNumber == 0:
            filename = scheduleDir + '%s/%s/GlueNoSheet.pdf' % (
                self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
            if not os.path.exists(filename):
                event.Skip()
                MakeGlueNoSheetTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber,
                                        filename,
                                        self.productionSchedule.panelList)  # 这些数据在ProductionScheduleAlgorithm.py文件中
            filename = scheduleDir + '%s/%s/GlueLabelSheet.pdf' % (
                self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
            if not os.path.exists(filename):
                event.Skip()
                MakeGlueLabelSheetTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber,
                                           filename,
                                           self.productionSchedule.panelList)  # 这些数据在ProductionScheduleAlgorithm.py文件中
            del busy
            dlg = GlueSheetManagementDailog(self, self.log, self.work_zone_Panel.manufactureManagementPanel.data[0],
                                            suborderNumber)
            dlg.CenterOnScreen()
            dlg.ShowModal()
            dlg.Destroy()
        else:
            del busy
            self.productionSchedule.missList = list(set(self.productionSchedule.missList))
            self.productionSchedule.wrongNumber = len(self.productionSchedule.missList)
            wx.MessageBox("缺少如下%s张图纸：\r\n%s,\r\n  无法完成排产，请补全图纸后再试！" % (
                self.productionSchedule.wrongNumber, str(self.productionSchedule.missList)), "提示信息")

    def OnAddSubOrderBTN(self, event):
        wildcard = "Excel文件 (*.xlsx)|*.xlsx|" \
                   "Excel文件 (*.xls)|*.xls|" \
                   "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="请选择Excel文件",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE |
                  wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                  wx.FD_PREVIEW
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.excelFileName = dlg.GetPaths()[0]
            temp = self.excelFileName.split('.')[-1]
            if temp == 'xls':
                xls2xlsx(self.excelFileName)
                self.excelFileName += 'x'
            orderID = GetOrderIDFromExcelFile(self.excelFileName)
            subOrderList = GetSubOrderIDListFromExcelFile(self.excelFileName)
            # print("orderID=",orderID,subOrderList,self.subOrderNameList)
            error = False
            for newSubOrder in subOrderList:
                if newSubOrder in self.subOrderNameList:
                    wx.MessageBox("%s订单已包含 %s# 子订单的数据，无法重复导入，请检查后重试！" % (self.currentOrderID, newSubOrder), "信息提示窗口")
                    error = True
            if not error:
                # dlg2 = AddSubOrderFromExcelDialog(self, orderID)
                dlg2 = ImportOrderFromExcelDialog(self, orderID, insertMode=True)
                dlg2.CenterOnScreen()
                if dlg2.ShowModal() == wx.ID_OK:
                    # InsertNewOrderRecord(self.log, 1, self.newOrderID)
                    # CreateNewOrderSheet(self.log, 1, self.newOrderID)
                    _, boardList = GetAllOrderList(self.log, 1)
                    self.work_zone_Panel.manufactureManagementPanel.dataArray = np.array(boardList)
                    self.work_zone_Panel.manufactureManagementPanel.orderGrid.ReCreate()
                dlg2.Destroy()
        dlg.Destroy()
        self.currentOrderID = self.work_zone_Panel.manufactureManagementPanel.data[0]
        self.currentOrderSubOrderIDStr = self.work_zone_Panel.manufactureManagementPanel.data[8]
        self.currentOrderSubOrderStateStr = self.work_zone_Panel.manufactureManagementPanel.data[9]
        self.ReCreateOrderInfoPanel()
        self.work_zone_Panel.manufactureManagementPanel.ReCreateOrderDetailTree()

    def OnPackageBTN(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        suborderNumber = name[-1]
        dbName = "%s" % self.currentOrderID
        _, dbNameList = GetPackageListFromDB(self.log, WHICHDB)
        if dbName not in dbNameList:
            CreatePackageSheetForOrder(self.log, WHICHDB, dbName)
        dlg = PackageDialog(self, self.log, self.work_zone_Panel.manufactureManagementPanel.data, suborderNumber)
        dlg.CenterOnScreen()
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()

    def OnPrintScheduleBTN(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        suborderNumber = name[-1]
        dlg = ProductionScheduleDialog(self, self.log, self.work_zone_Panel.manufactureManagementPanel.data[0],
                                       suborderNumber)
        dlg.CenterOnScreen()
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()

    def OnSpecificOrderProductionBTN(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        suborderNumber = name[-1]
        dlg = wx.MessageDialog(self, '将对 %s# 子订单进行排产操作，此操作不可逆，是否继续?' % suborderNumber,
                               '信息提示',
                               wx.OK | wx.CANCEL | wx.ICON_INFORMATION
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
            self.productionSchedule = ProductionScheduleAlgorithm(self.log,
                                                                  self.work_zone_Panel.manufactureManagementPanel.data[
                                                                      0], suborderNumber)
            if self.productionSchedule.wrongNumber == 0:
                _, self.pageRowNum = GetPropertySchedulePageRowNumber(self.log, 1)
                if self.work_zone_Panel.manufactureManagementPanel.data[0] == None:
                    dirName = scheduleDir + '%s/' % self.work_zone_Panel.manufactureManagementPanel.data[0]
                else:
                    dirName = scheduleDir + '%s/' % self.work_zone_Panel.manufactureManagementPanel.data[0] + '%s/' % (
                        int(suborderNumber))
                if not os.path.exists(dirName):
                    os.makedirs(dirName)
                filename = scheduleDir + '%s/%s/CutSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakeCutScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber,
                                        filename,
                                        self.productionSchedule.cuttingScheduleList,
                                        PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                filename = scheduleDir + '%s/%s/VerticalCutSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakeHorizontalCutScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0],
                                                  suborderNumber, filename,
                                                  self.productionSchedule.horizontalCuttingScheduleList,
                                                  PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                filename = scheduleDir + '%s/%s/MaterialSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakeMaterialScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber,
                                             filename,
                                             self.productionSchedule.horizontalCuttingScheduleList,
                                             self.productionSchedule.cuttingScheduleList,
                                             PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                filename = scheduleDir + '%s/%s/BendingSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakeBendingScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber,
                                            filename,
                                            self.productionSchedule.bendingScheduleList,
                                            PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                filename = scheduleDir + '%s/%s/S2FormingSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakeS2FormingScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber,
                                              filename,
                                              self.productionSchedule.S2FormingScheduleList,
                                              PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                filename = scheduleDir + '%s/%s/CeilingFormingSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakeCeilingFormingScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0],
                                                   suborderNumber, filename,
                                                   self.productionSchedule.ceilingFormingScheduleList,
                                                   PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                filename = scheduleDir + '%s/%s/CeilingFormingSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakeCeilingFormingScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0],
                                                   suborderNumber, filename,
                                                   self.productionSchedule.ceilingFormingScheduleList,
                                                   PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                filename = scheduleDir + '%s/%s/PRPressSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakePRPressScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber,
                                            filename,
                                            self.productionSchedule.prScheduleList,
                                            PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                filename = scheduleDir + '%s/%s/VacuumSchedule.pdf' % (
                    self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber)
                MakeVacuumScheduleTemplate(self.work_zone_Panel.manufactureManagementPanel.data[0], suborderNumber,
                                           filename,
                                           self.productionSchedule.vacuumScheduleList,
                                           PAGEROWNUMBER=self.pageRowNum)  # 这些数据在ProductionScheduleAlgorithm.py文件中
                self.subOrderStateList[int(suborderNumber) - 1] = "已排产"  # 这个之前应该增加一个数据库更新操作
                suborderState = str(self.subOrderStateList[0])
                for state in self.subOrderStateList[1:]:
                    suborderState += ','
                    suborderState += state
                self.work_zone_Panel.manufactureManagementPanel.data[9] = suborderState
                UpdateSubOrderStateInDB(self.log, 1, self.work_zone_Panel.manufactureManagementPanel.data[0],
                                        suborderState)
                self.work_zone_Panel.manufactureManagementPanel.orderGrid.ReCreate()
                self.ReCreateOrderInfoPanel()
                dlg = ProductionScheduleDialog(self, self.log, self.work_zone_Panel.manufactureManagementPanel.data[0],
                                               suborderNumber)
                dlg.CenterOnScreen()
                if dlg.ShowModal() == wx.ID_OK:
                    pass
                dlg.Destroy()
            else:
                self.productionSchedule.missList = list(set(self.productionSchedule.missList))
                self.productionSchedule.wrongNumber = len(self.productionSchedule.missList)
                wx.MessageBox("缺少如下%s张图纸：\r\n%s,\r\n  无法完成排产，请补全图纸后再试！" % (
                    self.productionSchedule.wrongNumber, str(self.productionSchedule.missList)), "提示信息")
        else:
            dlg.Destroy()

    def OnCreateNewOrderBTN(self, event):
        dlg = CreateNewOrderDialog(self, self.log)
        dlg.CenterOnScreen()
        dlg.ShowModal()
        dlg.Destroy()
        self.work_zone_Panel.orderManagementPanel.ReCreate()

    def OnImportOrderDataBTN(self, event):
        from DBOperation import GetTableListFromDB
        _, dbNameList = GetTableListFromDB(None, 1)
        if len(dbNameList) > 0:
            nameList = []
            for name in dbNameList:
                if name.isdigit():
                    nameList.append(int(name))
            self.newOrderID = max(nameList) + 1
        else:
            self.newOrderID = 1
        from NewOrderInquireDialog import NewOrderInquiredDialog
        dlg = NewOrderInquiredDialog(self, self.newOrderID)
        dlg.CenterOnScreen()
        value = dlg.ShowModal()
        dlg.Destroy()
        if value == wx.ID_OK:
            wildcard = "Excel文件 (*.xlsx)|*.xlsx|" \
                       "Excel文件 (*.xls)|*.xls|" \
                       "All files (*.*)|*.*"
            dlg = wx.FileDialog(
                self, message="请选择Excel文件",
                defaultDir=os.getcwd(),
                defaultFile="",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_MULTIPLE |
                      wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                      wx.FD_PREVIEW
            )
            if dlg.ShowModal() == wx.ID_OK:
                self.excelFileName = dlg.GetPaths()[0]
                temp = self.excelFileName.split('.')[-1]
                if temp == 'xls':
                    xls2xlsx(self.excelFileName)
                    self.excelFileName += 'x'
                dlg.Destroy()
                orderID = GetOrderIDFromExcelFile(self.excelFileName)
                _, orderInfor = GetOrderByOrderID(self.log, 1, orderID)
                if orderInfor != None:
                    wx.MessageBox("此订单已存在，请修改Excel文件中的订单编号，然后重试！", "错误提示：")
                else:
                    dlg = ImportOrderFromExcelDialog(self, self.newOrderID)
                    dlg.CenterOnScreen()
                    if dlg.ShowModal() == wx.ID_OK:
                        # InsertNewOrderRecord(self.log, 1, self.newOrderID)
                        # CreateNewOrderSheet(self.log, 1, self.newOrderID)
                        _, boardList = GetAllOrderList(self.log, 1)
                        self.work_zone_Panel.manufactureManagementPanel.dataArray = np.array(boardList)
                        self.work_zone_Panel.manufactureManagementPanel.orderGrid.ReCreate()
                    dlg.Destroy()
            else:
                dlg.Destroy()
                # _, boardList = GetAllOrderList(self.log, 1)
                # self.work_zone_Panel.orderManagmentPanel.dataArray = np.array(boardList)
                # self.work_zone_Panel.orderManagmentPanel.orderGrid.ReCreate()
                # # XLSGridFrame(None,paths[0])
        else:
            from NewOrderInquireDialog import NewOrderMainDialog
            dlg = NewOrderMainDialog(self, self.newOrderID)
            dlg.CenterOnScreen()
            if dlg.ShowModal() == wx.ID_OK:
                pass
                # InsertNewOrderRecord(self.log,1,self.newOrderID)
                # CreateNewOrderSheet(self.log,1,self.newOrderID)
                # _, boardList = GetAllOrderList(self.log, 1)
                # self.work_zone_Panel.orderManagmentPanel.dataArray = np.array(boardList)
                # self.work_zone_Panel.orderManagmentPanel.orderGrid.ReCreate()
            dlg.Destroy()

    def OnPressCaption(self, event):
        for i in range(0, self._pnl.GetCount()):
            item = self._pnl.GetFoldPanel(i)
            self._pnl.Collapse(item)
        event.Skip()

    def OnNoteBookPageChanged(self, event):
        obj = event.GetEventObject()
        if obj.GetName() == 'MainNoteBook':
            page = obj.GetSelection()
            pageName = self.work_zone_Panel.notebook.GetPageText(page)
            if pageName == "订单管理":
                pass
                # self.work_zone_Panel.orderManagementPanel.ReCreate()
            elif pageName == "图纸管理":
                self.work_zone_Panel.bluePrintManagementPanel.ReCreate()
            elif pageName == "生产管理":
                self.work_zone_Panel.manufactureManagementPanel.ReCreate()
            elif pageName == "基材管理":
                self.work_zone_Panel.boardManagementPanel.ReCreate()
            Title = ["", "订单操作面板", "原材料价格操作面板", "基材操作面板", "图纸操作面板", "生产管理面板"]
            for i in range(0, self._pnl.GetCount()):
                item = self._pnl.GetFoldPanel(i)
                self._pnl.Collapse(item)
                # print(item.GetItemPos())
                if item.GetLabel() == Title[page]:
                    self._pnl.Expand(item)
        event.Skip()


class WorkZonePanel(wx.Panel):
    def __init__(self, parent, master, log):
        wx.Panel.__init__(self, parent, -1)
        self.Freeze()
        self.parent = parent
        self.master = master
        self.log = log
        self.notebook = wx.Notebook(self, -1, size=(21, 21), style=
        wx.BK_DEFAULT
                                    # wx.BK_TOP
                                    # wx.BK_BOTTOM
                                    # wx.BK_LEFT
                                    # wx.BK_RIGHT
                                    # | wx.NB_MULTILINE
                                    , name="MainNoteBook")
        self.notebook.Freeze()
        il = wx.ImageList(16, 16)
        idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.total_page_num = 0
        self.notebook.AssignImageList(il)
        idx2 = il.Add(images.GridBG.GetBitmap())
        idx3 = il.Add(images.Smiles.GetBitmap())
        idx4 = il.Add(images._rt_undo.GetBitmap())
        idx5 = il.Add(images._rt_save.GetBitmap())
        idx6 = il.Add(images._rt_redo.GetBitmap())
        hbox = wx.BoxSizer()
        hbox.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(hbox)
        self.systemIntroductionPanel = SystemIntroductionPanel(self.notebook)
        self.notebook.AddPage(self.systemIntroductionPanel, "系统介绍")

        if self.master.operatorCharacter in ["技术员", "技术主管", "技术部长", "下单员", "经理", "财务人员", "采购员"]:
            if self.master.operatorCharacter in ["技术员", "技术主管", "技术部长"]:
                self.orderManagementPanel = OrderManagementPanel(self.notebook, self.master, self.log,
                                                                 character=self.master.operatorCharacter, type="草稿")
            else:
                self.orderManagementPanel = OrderManagementPanel(self.notebook, self.master, self.log,
                                                                 character=self.master.operatorCharacter)
            self.notebook.AddPage(self.orderManagementPanel, "订单管理")
        # if self.master.operatorCharacter in ["采购员", "经理"]:
        #     self.meterialPriceManagementPanel = MeterialPriceManagementPanel(self.notebook, self.log)
        #     self.notebook.AddPage(self.meterialPriceManagementPanel, "原材料价格管理")

        # if self.master.operatorCharacter in ["技术员","经理"]:
        #     self.boardManagementPanel = BoardManagementPanel(self.notebook, self, self.log)
        #     self.notebook.AddPage(self.boardManagementPanel, "基材管理")
        # if self.master.operatorCharacter in ["技术员","经理"]:
        #     self.bluePrintManagementPanel = BluePrintManagementPanel(self.notebook, self, self.log)
        #     self.notebook.AddPage(self.bluePrintManagementPanel, "图纸管理")
        # if self.master.operatorCharacter in ["技术员","经理"]:
        #     self.manufactureManagementPanel = ManufactureManagementPanel(self.notebook, self.master, self.log)
        #     self.notebook.AddPage(self.manufactureManagementPanel, "生产管理")
        # self.orderManagementPanel.ReCreate()
        self.notebook.SetSelection(1)
        # if self.master.operatorCharacter == '下单员':
        #     self.notebook.SetSelection(1)
        # elif self.master.operatorCharacter in ["技术员","管理员"]:
        #     self.manufactureManagementPanel.ReCreate()
        #     self.notebook.SetSelection(4)
        self.Thaw()
        self.notebook.Thaw()
