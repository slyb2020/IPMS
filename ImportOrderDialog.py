import wx
import os
import images
from ExcelOperation import GetSheetNameListFromExcelFileName,ExcelGridShowPanel
from ExcelOperation import GetSheetDataFromExcelFileName
from DBOperation import InsertBatchOrderDataIntoDB,CreateNewOrderSheet,GetOrderDetailRecord,InsertNewOrderRecord,\
    UpdateOrderRecord,GetOrderByOrderID
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')


class InputNewOrderDialog(wx.Dialog):
    def __init__(self, parent, newOrderID, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.newOrderID = newOrderID
        self.parent = parent
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "订单关键信息输入对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(1700, 800))
        mainInformationPanel = wx.Panel(panel,size=(-1,50))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        vbox.Add(mainInformationPanel,0,wx.EXPAND)
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(mainInformationPanel, label='订单号：'), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(mainInformationPanel, size=(50, 25),style=wx.TE_READONLY)
        self.newOrderIDTXT.SetValue('%05s'%str(self.newOrderID))
        hbox.Add(self.newOrderIDTXT, 1, wx.LEFT | wx.RIGHT, 10)
        vbox.Add(hbox,0,wx.EXPAND)
        mainInformationPanel.SetSizer(vbox)
        sizer.Add(panel,1,wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap(bitmapDir+"/33.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 50))
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 50))
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_ok, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_cancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

        # btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        # manualInputBTN.Bind(wx.EVT_BUTTON, self.OnCancel)

    # def OnOk(self, event):
    #     event.Skip()
    #
    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()

class ImportOrderFromExcelDialog(wx.Dialog):
    def __init__(self, parent, newOrderID,insertMode=False, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.newOrderID = newOrderID
        self.parent = parent
        self.insertMode = insertMode
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "订单关键信息输入对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(1700, 800))
        self.mainInformationPanel = wx.Panel(panel,size=(-1,50))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        vbox.Add(self.mainInformationPanel,0,wx.EXPAND)
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(self.mainInformationPanel, label='订单号：'), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(self.mainInformationPanel, size=(50, 25),style=wx.TE_READONLY)
        self.newOrderIDTXT.SetValue('%05d'%self.newOrderID)
        hbox.Add(self.newOrderIDTXT, 0, wx.LEFT | wx.RIGHT, 10)
        self.mainInformationPanel.SetSizer(hbox)

        self.notebook = wx.Notebook(panel, -1, size=(21, 21), style=
                                    # wx.BK_DEFAULT
                                    # wx.BK_TOP
                                    wx.BK_BOTTOM
                                    # wx.BK_LEFT
                                    # wx.BK_RIGHT
                                    # | wx.NB_MULTILINE
                                    )
        il = wx.ImageList(16, 16)
        idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.total_page_num = 0
        self.notebook.AssignImageList(il)
        idx2 = il.Add(images.GridBG.GetBitmap())
        idx3 = il.Add(images.Smiles.GetBitmap())
        idx4 = il.Add(images._rt_undo.GetBitmap())
        idx5 = il.Add(images._rt_save.GetBitmap())
        idx6 = il.Add(images._rt_redo.GetBitmap())
        vbox.Add(self.notebook,1,wx.EXPAND|wx.LEFT|wx.RIGHT,10)
        panel.SetSizer(vbox)
        # panel.SetBackgroundColour(wx.Colour(234,219,212))
        sizer.Add(panel, 0, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap(bitmapDir+"/33.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 50))
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 50))
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_ok, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_cancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

        self.sheetNameList = GetSheetNameListFromExcelFileName(self.parent.excelFileName)
        self.sheetPage=[]
        sheetNameListTemp = []
        for sheetName in self.sheetNameList:
            dataTemp = GetSheetDataFromExcelFileName(self.parent.excelFileName, sheetName)
            if dataTemp.shape[0]>0 and dataTemp.shape[1]>0:
                sheetNameListTemp.append(sheetName)
                sheetPage = ExcelGridShowPanel(self.notebook,self.parent.excelFileName,sheetName)
                self.notebook.AddPage(sheetPage,sheetName)
                self.sheetPage.append(sheetPage)
        self.sheetNameList = sheetNameListTemp

        if len(self.sheetNameList)>0:
            self.newOrderID = self.GetMainOrderID()
            self.newOrderName = self.GetMainOrderName()
            self.subOrderIDList = self.GetSubOrderIDList()
            self.keyDataColPostion = self.GetKeyDataColPosition()
            self.ReCreateMainInformationPanel()
        btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        # manualInputBTN.Bind(wx.EVT_BUTTON, self.OnCancel)

    def OnOk(self, event):
        if self.insertMode:
            _, orderInfor = GetOrderByOrderID(self.parent.log, 1, self.newOrderID)
            subOrderIdStr=orderInfor[8]
            subOrderStateStr = orderInfor[9]
            for i in self.subOrderIDList:
                subOrderIdStr += ','
                subOrderIdStr += str(int(i))
                subOrderStateStr += ',接单'
            UpdateOrderRecord(self.parent.log,1,self.newOrderID,subOrderIdStr,subOrderStateStr)
            self.parent.work_zone_Panel.manufactureManagementPanel.data[8] = subOrderIdStr
            self.parent.work_zone_Panel.manufactureManagementPanel.data[9] = subOrderStateStr
        else:
            InsertNewOrderRecord(self.parent.log,1,self.newOrderID,self.newOrderName,self.subOrderIDList)
            CreateNewOrderSheet(self.parent.log,1,self.newOrderID)
        orderDataList = []
        for pageNum, page in enumerate(self.sheetPage):
            (rowStart,rowEnd) = self.keyDataColPostion[pageNum][0]
            col = self.keyDataColPostion[pageNum][1]
            for data in page.data[rowStart:rowEnd,:]:
                # `子订单号`, `甲板`, `区域`, `房间`, `图纸`, `宽度`, `高度`, `厚度`, `X面颜色`, `Y面颜色`, `Z面颜色`, `V面颜色`, `数量`, `面板代码`
                temp = [0]*16
                temp[10] = None
                temp[11] = None
                for i in range(len(col)):
                    if col[i]>=0:
                        temp[i]=data[col[i]]
                orderDataList.append(temp)
        InsertBatchOrderDataIntoDB(self.parent.log, 1, self.newOrderID, orderDataList)
        event.Skip()

    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))

    def ReCreateMainInformationPanel(self):
        self.mainInformationPanel.DestroyChildren()
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(self.mainInformationPanel, label='订单号：', size=(50,-1)), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(self.mainInformationPanel, size=(60, -1),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.newOrderIDTXT.SetValue('%05d'%self.newOrderID)
        self.newOrderIDTXT.SetBackgroundColour(wx.RED)
        hbox.Add(self.newOrderIDTXT, 0, wx.RIGHT, 20)

        hbox.Add(wx.StaticText(self.mainInformationPanel, label='订单名称：', size=(60,-1)), 0, wx.TOP, 5)
        self.newOrderNameTXT = wx.TextCtrl(self.mainInformationPanel, size=(100, -1),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.newOrderNameTXT.SetBackgroundColour(wx.YELLOW)
        self.newOrderNameTXT.SetValue(self.newOrderName)
        hbox.Add(self.newOrderNameTXT, 0, wx.RIGHT, 20)

        hbox.Add(wx.StaticText(self.mainInformationPanel, label='子订单：', size=(50,-1)), 0, wx.TOP, 5)
        self.subOrderIDCombo = wx.ComboBox(self.mainInformationPanel, size=(80,25),
                                           choices=self.subOrderIDList, style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.subOrderIDCombo.SetBackgroundColour(wx.GREEN)
        self.subOrderIDCombo.SetValue(self.subOrderIDList[0])
        hbox.Add(self.subOrderIDCombo, 0, wx.RIGHT, 20)

        hbox.Add(wx.StaticText(self.mainInformationPanel, label='甲板：', size=(50,-1)), 0, wx.TOP, 5)
        self.deckIDCombo = wx.ComboBox(self.mainInformationPanel, size=(80,25),
                                           choices=self.subOrderIDList, style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.deckIDCombo.SetBackgroundColour(wx.GREEN)
        hbox.Add(self.deckIDCombo, 0, wx.RIGHT, 20)

        hbox.Add(wx.StaticText(self.mainInformationPanel, label='区域：', size=(50,-1)), 0, wx.TOP, 5)
        self.zoneIDCombo = wx.ComboBox(self.mainInformationPanel, size=(80,25),
                                           choices=self.subOrderIDList, style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.zoneIDCombo.Bind(wx.EVT_COMBOBOX, self.OnDeckIDChanged)
        self.zoneIDCombo.SetBackgroundColour(wx.GREEN)
        # self.deckIDCombo.SetValue(self.deckIDList[0])
        hbox.Add(self.zoneIDCombo, 0, wx.RIGHT, 20)

        hbox.Add(wx.StaticText(self.mainInformationPanel, label='房间：', size=(50,-1)), 0, wx.TOP, 5)
        self.roomIDCombo = wx.ComboBox(self.mainInformationPanel, size=(80,25),
                                           choices=self.subOrderIDList, style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.roomIDCombo.Bind(wx.EVT_COMBOBOX, self.OnRoomIDChanged)
        self.roomIDCombo.SetBackgroundColour(wx.GREEN)
        # self.deckIDCombo.SetValue(self.deckIDList[0])
        hbox.Add(self.roomIDCombo, 0, wx.RIGHT, 20)

        self.mainInformationPanel.SetSizer(hbox)
        self.mainInformationPanel.Layout()
        self.currentPageNum = self.notebook.GetSelection()
        deckList = self.GetDeckItemList(self.currentPageNum, self.subOrderIDList[0])
        self.deckIDCombo.SetItems(deckList)
        self.deckIDCombo.SetValue(deckList[0])
        zoneList = self.GetZoneItemList(0, self.subOrderIDList[0],deckList[0])
        self.zoneIDCombo.SetItems(zoneList)
        self.zoneIDCombo.SetValue(zoneList[0])
        roomList = self.GetRoomItemList(0, self.subOrderIDList[0],deckList[0],zoneList[0])
        self.roomIDCombo.SetItems(roomList)
        self.roomIDCombo.SetValue(roomList[0])
        self.ShowSelectionData()

    def OnDeckIDChanged(self, event):
        roomList = self.GetRoomItemList(self.currentPageNum, self.subOrderIDList[0],self.deckIDCombo.GetValue(),self.zoneIDCombo.GetValue())
        self.roomIDCombo.SetItems(roomList)
        self.roomIDCombo.SetValue(roomList[0])
        self.ShowSelectionData()


    def OnRoomIDChanged(self,event):
        self.ShowSelectionData()

    def ShowSelectionData(self):
        subOrderID = self.subOrderIDCombo.GetValue()
        deckID = self.deckIDCombo.GetValue()
        zoneID = self.zoneIDCombo.GetValue()
        roomID = self.roomIDCombo.GetValue()

        for pageNum, page in enumerate(self.sheetPage):
            subOrderCol = self.keyDataColPostion[pageNum][1][0]
            deckCol = self.keyDataColPostion[pageNum][1][1]
            zoneCol = self.keyDataColPostion[pageNum][1][2]
            roomCol = self.keyDataColPostion[pageNum][1][3]
            dataRowStart = self.keyDataColPostion[pageNum][0][0]
            dataRowEnd = self.keyDataColPostion[pageNum][0][1]
            for rowNum, data in enumerate(self.sheetPage[pageNum].data[dataRowStart:dataRowEnd+1,:]):
                for colNum in range(self.sheetPage[pageNum].data.shape[1]):#先清除全部背景
                    self.sheetPage[pageNum].SetCellBackgroundColour(rowNum + dataRowStart, colNum, wx.WHITE)
                if str(data[subOrderCol]) == subOrderID and str(data[deckCol])==deckID and str(data[zoneCol])==zoneID and str(data[roomCol])==roomID:
                    for colNum in range(self.sheetPage[pageNum].data.shape[1]):#再设置满足条件的背景
                        self.sheetPage[pageNum].SetCellBackgroundColour(rowNum+dataRowStart,colNum,wx.Colour(170,240,170))
        self.sheetPage[self.currentPageNum].Refresh()


    def GetMainOrderID(self):
        for i, row in enumerate(self.sheetPage[0].data):
            if "Project" in row:
                row = list(row)
                col = row.index("Project")
                for j,item in enumerate(row[col+1:]):
                    if item:
                        self.sheetPage[0].SetCellBackgroundColour(i,j+col+1,wx.RED)
                        return int(item)
        return -1
    def GetMainOrderName(self):
        for i, row in enumerate(self.sheetPage[0].data):
            if "Project Name" in row:
                row = list(row)
                col = row.index("Project Name")
                for j, item in enumerate(row[col+1:]):
                    if item:
                        self.sheetPage[0].SetCellBackgroundColour(i,j+col+1,wx.YELLOW)
                        return item
        return ""
    def GetSubOrderIDList(self):
        result = []
        for page in self.sheetPage:
            nextPage = False
            for i, row in enumerate(page.data):
                if nextPage:
                    break
                else:
                    if "SubProject" in row:
                        row = list(row)
                        col = row.index("SubProject")
                        for j, item in enumerate(row[col+1:]):
                            if nextPage:
                                break
                            else:
                                if item:
                                    page.SetCellBackgroundColour(i, j + col + 1, wx.GREEN)
                                    result.append(str(item))
                                    nextPage = True
        return result

    def GetKeyDataColPosition(self):#查找子订单号，甲板，区域，房间所在的列号：
        result = []
        for pageNum, page in enumerate(self.sheetPage):
            for i, row in enumerate(page.data):
                if "SProj" in row and "DECK" in row and "AREA" in row and "ROOM" in row:
                    rowNum = i
                    rowData = list(row)
                    suborderColNum = rowData.index("SProj")
                    deckColNum = rowData.index("DECK")
                    areaColNum = rowData.index("AREA")
                    roomColNum = rowData.index("ROOM")
                    drawingNoColNum = rowData.index("Drawing No.")
                    widthColNum = rowData.index("Width")
                    heightColNum = rowData.index("Height")
                    thicknessColNum = rowData.index("Thickness")
                    xColourColNum = rowData.index("X-Colour")
                    yColourColNum = rowData.index("Y-Colour")
                    codeColNum = rowData.index("Code")
                    if "Z-Colour" in rowData:
                        zColourColNum = rowData.index("Z-Colour")
                    else:
                        zColourColNum = -1
                    if "V-Colour" in rowData:
                        vColourColNum = rowData.index("V-Colour")
                    else:
                        vColourColNum = -1
                    amountColNum = rowData.index("Pcs")
                    codeColNum = rowData.index("Code")
                    break
            rowNumStart = None
            for i, row in enumerate(page.data[rowNum+1:]):
                if int(row[suborderColNum])==int(self.subOrderIDList[pageNum]):
                    rowNumStart = i+rowNum+1
                    break
            if rowNumStart!=None:
                for i, row in enumerate(page.data[rowNumStart+1:]):
                    if  row[suborderColNum]==None and row[deckColNum]==None and row[areaColNum]==None and row[roomColNum]==None:
                        break
                rowNumEnd = i + rowNumStart
                result.append([[rowNumStart,rowNumEnd],[suborderColNum,deckColNum,areaColNum,roomColNum,drawingNoColNum,widthColNum,heightColNum,thicknessColNum,xColourColNum,yColourColNum,zColourColNum,vColourColNum,amountColNum,codeColNum]])
            else:
                wx.MessageBox("Excel文件中不包含有效数据，请检查后重试!")
        return result

    def GetDeckItemList(self,pageNum,subOrderID):
        subOrderCol = self.keyDataColPostion[pageNum][1][0]
        deckCol = self.keyDataColPostion[pageNum][1][1]
        dataRowStart = self.keyDataColPostion[pageNum][0][0]
        dataRowEnd = self.keyDataColPostion[pageNum][0][1]
        result= []
        for data in self.sheetPage[pageNum].data[dataRowStart:dataRowEnd+1,:]:
            if str(int(data[subOrderCol])) == str(int(subOrderID)):
                result.append(str(data[deckCol]))
        result = list(set(result))
        result.sort()
        return result

    def GetZoneItemList(self,pageNum,subOrderID,deckID):
        subOrderCol = self.keyDataColPostion[pageNum][1][0]
        deckCol = self.keyDataColPostion[pageNum][1][1]
        zoneCol = self.keyDataColPostion[pageNum][1][2]
        dataRowStart = self.keyDataColPostion[pageNum][0][0]
        dataRowEnd = self.keyDataColPostion[pageNum][0][1]
        result= []
        for data in self.sheetPage[pageNum].data[dataRowStart:dataRowEnd+1,:]:
            if str(int(data[subOrderCol])) == str(int(subOrderID)) and str(int(data[deckCol]))==str(int(deckID)):
                result.append(str(data[zoneCol]))
        result = list(set(result))
        result.sort()
        return result

    def GetRoomItemList(self,pageNum,subOrderID,deckID,zoneID):
        subOrderCol = self.keyDataColPostion[pageNum][1][0]
        deckCol = self.keyDataColPostion[pageNum][1][1]
        zoneCol = self.keyDataColPostion[pageNum][1][2]
        roomCol = self.keyDataColPostion[pageNum][1][3]
        dataRowStart = self.keyDataColPostion[pageNum][0][0]
        dataRowEnd = self.keyDataColPostion[pageNum][0][1]
        result= []
        for data in self.sheetPage[pageNum].data[dataRowStart:dataRowEnd+1,:]:
            if str(int(data[subOrderCol])) == str(int(subOrderID)) and str(int(data[deckCol]))==str(int(deckID)) and str(data[zoneCol])==zoneID:
                result.append(str(data[roomCol]))
        result = list(set(result))
        result.sort()
        return result

