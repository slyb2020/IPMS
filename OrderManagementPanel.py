import copy
import threading
from operator import itemgetter
import json
import numpy as np
import pandas as pd

import wx
import wx.grid as gridlib
import wx.lib.agw.pybusyinfo as PBI
from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel

import images
from DBOperation import GetAllOrderAllInfo, GetAllOrderList, GetOrderDetailRecord, InsertNewOrder, \
    UpdateDraftOrderInfoByID, GetTechDrawingDataByID, UpdateTechCheckStateByID, GetDraftComponentInfoByID, \
    UpdateDraftCheckInfoByID, UpdateDraftOrderStateInDB, \
    UpdatePurchchaseCheckStateByID, UpdateFinancingCheckStateByID, UpdateManagerCheckStateByID, UpdateOrderSquareByID, \
    GetExchagneRateInDB, UpdateOrderAnnotationTriggerList, GetOrderAnnotationTriggerList,\
    UpdateOrderOperatorCheckStateByID, GetStaffInfo, GetDraftOrderDetail, \
    GetPriceDateListFromDB, GetPriceDicFromDB, UpdateDraftOrderInDB,UpdateOrderAnnotation,GetOrderAnnotation
from DateTimeConvert import *
from MakePdfReport import *
from OrderDetailTree import OrderDetailTree
from SetupPropertyDialog import *

from ProductionScheduleDialog import PDFViewerPanel

from BluePrintManagementPanel import BluePrintShowPanel


class OrderDetailGrid(gridlib.Grid):
    def __init__(self, parent, master, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.master = master
        self.moveTo = None
        if not self.master.showRange:
            self.data = np.array(self.master.orderDetailData)[:, 2:]
            self.titleList = orderDetailLabelList[2:]
            self.colSizeList = orderDetailColSizeList[2:]
        elif self.master.showRange[0] == "子订单":
            self.data = []
            for data in self.master.orderDetailData:
                if str(data[2]) == str(self.master.showRange[1]):
                    self.data.append(data)
            self.data = np.array(self.data)[:, 3:]
            self.titleList = orderDetailLabelList[3:]
            self.colSizeList = orderDetailColSizeList[3:]
        elif self.master.showRange[0] == "甲板订单":
            self.data = []
            for data in self.master.orderDetailData:
                if str(data[2]) == str(self.master.showRange[1]) and str(data[3]) == str(self.master.showRange[2]):
                    self.data.append(data)
            self.data = np.array(self.data)[:, 4:]
            self.titleList = orderDetailLabelList[4:]
            self.colSizeList = orderDetailColSizeList[4:]
        elif self.master.showRange[0] == "区域订单":
            self.data = []
            for data in self.master.orderDetailData:
                if str(data[2]) == str(self.master.showRange[1]) and str(data[3]) == str(
                        self.master.showRange[2]) and str(data[4]) == str(self.master.showRange[3]):
                    self.data.append(data)
            self.data = np.array(self.data)[:, 5:]
            self.titleList = orderDetailLabelList[5:]
            self.colSizeList = orderDetailColSizeList[5:]
        elif self.master.showRange[0] == "房间订单":
            self.data = []
            for data in self.master.orderDetailData:
                if str(data[2]) == str(self.master.showRange[1]) and str(data[3]) == str(
                        self.master.showRange[2]) and str(data[4]) == str(self.master.showRange[3]) and str(
                    data[5]) == str(self.master.showRange[4]):
                    self.data.append(data)
            self.data = np.array(self.data)[:, 6:]
            self.titleList = orderDetailLabelList[6:]
            self.colSizeList = orderDetailColSizeList[6:]

        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.CreateGrid(self.data.shape[0], self.data.shape[1])  # , gridlib.Grid.SelectRows)
        for i in range(self.data.shape[1]):
            self.SetColLabelSize(25)
            self.SetColSize(i, self.colSizeList[i])
            self.SetColLabelValue(i, self.titleList[i])
        for rowNum, row in enumerate(self.data):
            self.SetRowLabelSize(40)
            self.SetRowLabelValue(rowNum, str(rowNum + 1))
            for colNum, col in enumerate(row):
                self.SetCellAlignment(rowNum, colNum, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.SetCellValue(rowNum, colNum, str(col))
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)

    def OnCellLeftClick(self, event):
        row = event.GetRow()
        self.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.SelectRow(row)

    def OnCellRightClick(self, evt):
        evt.Skip()

    def OnCellLeftDClick(self, event):
        row = event.GetRow()
        col = event.GetCol()
        self.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.SelectRow(row)
        if self.GetColLabelValue(col) == "图纸":
            bluePrintName = self.GetCellValue(row, col)

    def OnCellRightDClick(self, evt):
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        evt.Skip()

    def OnLabelRightClick(self, evt):
        evt.Skip()

    def OnLabelLeftDClick(self, evt):
        evt.Skip()

    def OnLabelRightDClick(self, evt):
        evt.Skip()

    def OnGridColSort(self, evt):
        self.log.write("OnGridColSort: %s %s" % (evt.GetCol(), self.GetSortingColumn()))
        self.SetSortingColumn(evt.GetCol())

    def OnRowSize(self, evt):
        evt.Skip()

    def OnColSize(self, evt):
        evt.Skip()

    def OnRangeSelect(self, evt):
        evt.Skip()

    def OnCellChange(self, evt):
        evt.Skip()

    def OnIdle(self, evt):
        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()

    def OnSelectCell(self, evt):
        evt.Skip()

    def OnEditorShown(self, evt):
        evt.Skip()

    def OnEditorCreated(self, evt):
        evt.Skip


class OrderGrid(gridlib.Grid):
    def __init__(self, parent, master, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.Freeze()
        self.log = log
        self.master = master
        self.moveTo = None

        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.CreateGrid(self.master.dataArray.shape[0],
                        len(self.master.colLabelValueList))  # , gridlib.Grid.SelectRows)
        self.EnableEditing(False)

        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)

        self.SetRowLabelSize(50)
        self.SetColLabelSize(25)

        for i, title in enumerate(self.master.colLabelValueList):
            self.SetColLabelValue(i, title)
        for i, width in enumerate(self.master.colWidthList):
            self.SetColSize(i, width)

        for i, order in enumerate(self.master.dataArray):
            self.SetRowSize(i, 25)
            for j, item in enumerate(order[:-3]):  # z最后一列位子订单列表，不再grid上显示
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
                self.SetCellValue(i, j, str(item))
                if j == 0:
                    if int(order[0]) < 2:
                        self.SetCellBackgroundColour(i, j, wx.RED)
                    elif int(order[0]) < 5:
                        self.SetCellBackgroundColour(i, j, wx.YELLOW)
                elif j >= 9:
                    if item == "未审核":
                        self.SetCellBackgroundColour(i, j, wx.Colour(250, 180, 180))
                    elif item == "审核通过":
                        self.SetCellBackgroundColour(i, j, wx.GREEN)
                    else:
                        self.SetCellBackgroundColour(i, j, wx.YELLOW)

        # self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        # self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        # self.Bind(gridlib.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        # self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)
        self.Thaw()

    def ReCreate(self):
        self.ClearGrid()
        self.EnableEditing(False)
        if self.GetNumberRows() < self.master.dataArray.shape[0]:
            self.InsertRows(0, self.master.dataArray.shape[0] - self.GetNumberRows())
        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)

        self.SetRowLabelSize(50)
        self.SetColLabelSize(25)

        for i, title in enumerate(self.master.colLabelValueList):
            self.SetColLabelValue(i, title)
        for i, width in enumerate(self.master.colWidthList):
            self.SetColSize(i, width)
        for i, order in enumerate(self.master.dataArray):
            self.SetRowSize(i, 25)
            for j, item in enumerate(order[:-3]):  # z最后一列位子订单列表，不再grid上显示
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
                self.SetCellValue(i, j, str(item))
                if j == 0:
                    if int(order[0]) < 2:
                        self.SetCellBackgroundColour(i, j, wx.RED)
                    elif int(order[0]) < 5:
                        self.SetCellBackgroundColour(i, j, wx.YELLOW)
                elif j >= 9:
                    if item == "未审核":
                        self.SetCellBackgroundColour(i, j, wx.Colour(250, 180, 180))
                    elif item == "审核通过":
                        self.SetCellBackgroundColour(i, j, wx.GREEN)
                    else:
                        self.SetCellBackgroundColour(i, j, wx.YELLOW)

    def OnIdle(self, evt):
        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()


class OrderUpdateCheckThread(threading.Thread):
    def __init__(self, parent, log):
        super(OrderUpdateCheckThread, self).__init__()
        self.parent = parent
        self.log = log
        self.setDaemon(True)  # 设置为守护线程， 即子线程是守护进程，主线程结束子线程也随之结束。
        self.dataList = None
        self.staffInfo = None
        self.draftOrderDic = None

    def run(self):
        while 1:
            _, draftOrderDic = GetDraftOrderDetail(self.log, WHICHDB)
            if self.draftOrderDic != draftOrderDic:
                self.draftOrderDic = draftOrderDic
                self.parent.draftOrderDic = draftOrderDic
            _, dataList = GetAllOrderAllInfo(self.log, WHICHDB, self.parent.type)
            if self.dataList != dataList:
                self.dataList = dataList
                self.parent.dataList = dataList
                # try:
                #     self.parent.orderGrid.ReCreate()
                # except:
                #     pass
                try:
                    wx.CallAfter(self.parent.ReCreate)
                except:
                    pass
            _, staffInfo = GetStaffInfo(self.log, WHICHDB)
            if self.staffInfo != staffInfo:
                self.staffInfo = staffInfo
                self.parent.staffInfo = staffInfo
                try:
                    wx.CallAfter(self.parent.ReCreate)
                except:
                    pass
            if not self.parent.priceDataDic:
                priceDateLatest = GetPriceDateListFromDB(self.log, WHICHDB)[0]
                self.parent.priceDataDic = GetPriceDicFromDB(self.log, WHICHDB, priceDateLatest)
            if not self.parent.exChangeRateDic:
                self.parent.exChangeRateDic = GetExchagneRateInDB(self.log, WHICHDB)
            wx.Sleep(0.1)


class OrderManagementPanel(wx.Panel):
    def __init__(self, parent, master, log, character, type="草稿"):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.master = master
        self.log = log
        self.type = type
        self.character = character
        self.dataList = []
        self.staffInfo = []
        self.draftOrderDic = []
        self.priceDataDic = []
        self.exChangeRateDic = None
        self.exchangeRate = None
        self.orderUpdateCheckThread = OrderUpdateCheckThread(self, self.log)
        self.orderUpdateCheckThread.start()

    def ReCreate(self):
        if not self.staffInfo or not self.dataList:
            try:
                # self.orderGrid.ClearGrid()
                self.orderGrid.DeleteRows(0,self.orderGrid.GetNumberRows())
            except:
                pass
            return
        # self.Freeze()
        try:
            self.DestroyChildren()
        except:
            pass
        self.busy = False
        self.showRange = []
        if self.type == "草稿":
            self.colLabelValueList = ["剩余时间", "订单编号", "订单名称", "总价", "产品数量", "投标日期", "下单日期", "下单员", "订单状态", "技术部审核",
                                      "采购部审核", "财务部审核", "订单部审核", "经理审核"]
            self.colWidthList = [60, 60, 80, 80, 80, 80, 80, 80, 80, 70, 70, 70, 70, 70]
        elif self.type == "在产":
            self.colLabelValueList = ["剩余时间", "订单编号", "订单名称", "总价", "产品数量", "订单交货日期", "下单时间", "下单员", "订单状态"]
            self.colWidthList = [60, 60, 80, 70, 60, 85, 85, 85, 60]
        elif self.type == "完工":
            self.colLabelValueList = ["序号", "订单编号", "订单名称", "总价", "产品数量", "订单交货日期", "下单时间", "下单员", "订单状态"]
            self.colWidthList = [60, 60, 80, 70, 60, 85, 85, 85, 60]
        elif self.type == "废弃":
            self.colLabelValueList = ["序号", "订单编号", "订单名称", "总价", "产品数量", "投标日期", "下单日期", "下单员", "订单状态", "技术部审核",
                                      "采购审核", "财务审核", "订单部审核", "经理审核"]
            self.colWidthList =  [60, 60, 80, 80, 80, 80, 80, 80, 80, 70, 70, 70, 70, 70]
        self.orderDetailData = []
        orderList = []
        for index, record in enumerate(self.dataList):  # 这个循环是把要在grid中显示的数据排序，对齐，内容规整好
            record = list(record)
            if self.type in ["草稿","废弃"]:
                if self.type == "草稿":
                    startDay = datetime.date.today()
                    if record[4]:
                        temp = record[4].split('-')
                        endDay = datetime.date(year=int(temp[0]), month=int(temp[1]), day=int(temp[2]))
                        record.insert(0, (endDay - startDay).days)
                elif self.type == "废弃":
                    record.insert(0, index+1)
                record[1] = "%05d" % int(record[1])
                if record[3] == "" or record[3] == None:
                    record[3] = "暂无报价"
                if record[4] == '0':
                    record[4] = ""
                for staffInfo in self.staffInfo:
                    if staffInfo[4] == record[7]:
                        record[7] = staffInfo[3]
                        break
                for i in range(5):
                    if self.type in ["草稿", "废弃"]:
                        if record[9 + i] == 'N':
                            record[9 + i] = "未审核"
                        elif record[9 + i] == 'Y':
                            record[9 + i] = "审核通过"
                        else:
                            record[9 + i] = "正在审核"
            elif self.type == '在产':
                startDay = datetime.date.today()
                if record[4]:
                    temp = record[4].split('-')
                    endDay = datetime.date(year=int(temp[0]), month=int(temp[1]), day=int(temp[2]))
                    record.insert(0, (endDay - startDay).days)
                else:
                    record.insert(0, 0)
            elif self.type == '完工':
                record.insert(0, index+1)
            orderList.append(record)
        orderList.sort(key=itemgetter(0), reverse=False)

        self.dataArray = np.array(orderList)
        self.data = []
        self.orderIDSearch = ''
        self.orderStateSearch = ''
        self.productNameSearch = ''
        self.operatorSearch = ''
        hbox = wx.BoxSizer()
        size = (1000, -1)
        if self.type in ["草稿", "废弃"]:
            size = (1100, -1)
        elif self.type in ["在产", "完工"]:
            size = (710, -1)
        try:
            self.leftPanel = wx.Panel(self, size=size)
            hbox.Add(self.leftPanel, 0, wx.EXPAND)
            self.rightPanel = wx.Panel(self, style=wx.BORDER_THEME)
            hbox.Add(self.rightPanel, 1, wx.EXPAND)
            self.SetSizer(hbox)
            vvbox = wx.BoxSizer(wx.VERTICAL)
            self.orderGrid = OrderGrid(self.leftPanel, self, self.log)
            vvbox.Add(self.orderGrid, 1, wx.EXPAND)
            hhbox = wx.BoxSizer()
            searchPanel = wx.Panel(self.leftPanel, size=(-1, 30), style=wx.BORDER_DOUBLE)
            vvbox.Add(searchPanel, 0, wx.EXPAND)
            hhbox = wx.BoxSizer()
            self.searchResetBTN = wx.Button(searchPanel, label='Rest', size=(48, -1))
            # self.searchResetBTN.Bind(wx.EVT_BUTTON, self.OnResetSearchItem)
            hhbox.Add(self.searchResetBTN, 0, wx.EXPAND)
            self.orderIDSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[0], -1),
                                                 style=wx.TE_PROCESS_ENTER)
            # self.orderIDSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnOrderIDSearch)
            hhbox.Add(self.orderIDSearchCtrl, 0, wx.EXPAND)
            self.customerNameSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[1], -1))
            # self.customerNameSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnOrderStateSearch)
            hhbox.Add(self.customerNameSearchCtrl, 0, wx.EXPAND)
            ##################################奇怪，这段代码会极大地拖慢程序运行速度###############################################
            # self.productNameSearchCtrl = wx.ComboBox(searchPanel, choices=['A1', 'B0', 'B1', 'B5', 'B7'],
            #                                          size=(self.colWidthList[2], -1))
            # self.productNameSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnProductNameSearch)
            # hhbox.Add(self.productNameSearchCtrl, 0, wx.EXPAND)
            ################################################################################################################
            hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[2], -1)),0,wx.EXPAND)
            self.productAmountSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[3], -1))
            hhbox.Add(self.productAmountSearchCtrl, 0, wx.EXPAND)
            self.deliverDateSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[4], -1))
            hhbox.Add(self.deliverDateSearchCtrl, 0, wx.EXPAND)
            self.orderDateSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[5], -1))
            hhbox.Add(self.orderDateSearchCtrl, 0, wx.EXPAND)
            hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[6], -1)),0,wx.EXPAND)
            hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[7], -1)),0,wx.EXPAND)
            hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[8], -1)),0,wx.EXPAND)
            if self.type in ["草稿","废弃"]:
                hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[9], -1)),0,wx.EXPAND)
                hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[10], -1)),0,wx.EXPAND)
                hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[11], -1)),0,wx.EXPAND)
                hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[12], -1)),0,wx.EXPAND)
                hhbox.Add(wx.TextCtrl(searchPanel, size=(self.colWidthList[13], -1)),0,wx.EXPAND)
            # self.operatorSearchCtrl = wx.ComboBox(searchPanel, choices=["1803089"], size=(self.colWidthList[6], -1))
            # self.operatorSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnOperatorSearch)
            # hhbox.Add(self.operatorSearchCtrl, 0, wx.EXPAND)
            # self.orderStateSearchCtrl = wx.ComboBox(searchPanel, choices=["接单", "排产", "下料", "加工", "打包", "发货"],
            #                                         size=(self.colWidthList[7], -1))
            # self.orderStateSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnOrderStateSearch)
            # hhbox.Add(self.orderStateSearchCtrl, 0, wx.EXPAND)

            searchPanel.SetSizer(hhbox)
            self.leftPanel.SetSizer(vvbox)
            self.orderGrid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
            self.Layout()
        except:
            pass
        # self.Thaw()

    def ReCreateOrderDetailTree(self):
        self.orderDetailTreePanel.DestroyChildren()
        _, self.orderDetailData = GetOrderDetailRecord(self.log, 1, self.data[0])
        if len(self.orderDetailData) == 0:
            self.treeStructure = []
        else:
            self.treeStructure = self.TreeDataTransform()
        self.orderDetailTree = OrderDetailTree(self.orderDetailTreePanel, self, self.log, self.data[0],
                                               self.treeStructure)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.orderDetailTree, 1, wx.EXPAND)
        self.orderDetailTreePanel.SetSizer(vbox)
        self.orderDetailTreePanel.Layout()

    def ReCreateOrderEditPanel(self):
        self.orderEditPanel.Freeze()
        self.orderEditPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.draftOrderEditPanel = DraftOrderPanel(self.orderEditPanel, self, self.log, size=(600, 600), mode="EDIT",
                                                   ID=self.data[1], character=self.character)
        vbox.Add(self.draftOrderEditPanel, 1, wx.EXPAND)
        # line = wx.StaticLine(self.orderEditPanel, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        # sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)
        #
        # btnsizer = wx.BoxSizer()
        # bitmap1 = wx.Bitmap("D:/IPMS/dist/bitmaps/ok3.png", wx.BITMAP_TYPE_PNG)
        # bitmap2 = wx.Bitmap("D:/IPMS/dist/bitmaps/cancel1.png", wx.BITMAP_TYPE_PNG)
        # bitmap3 = wx.Bitmap("D:/IPMS/dist/bitmaps/33.png", wx.BITMAP_TYPE_PNG)
        # btn_ok = wx.Button(self.orderEditPanel, wx.ID_OK, "确 认 修 改", size=(200, 50))
        # btn_ok.Bind(wx.EVT_BUTTON,self.OnDraftOrderEditOkBTN)
        # btn_ok.SetBitmap(bitmap1, wx.LEFT)
        # btnsizer.Add(btn_ok, 0)
        # btnsizer.Add((40, -1), 0)
        # sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        # self.orderEditPanel.SetSizer(sizer)
        # sizer.Fit(self.orderEditPanel)
        self.orderEditPanel.SetSizer(vbox)
        self.orderEditPanel.Layout()
        self.orderEditPanel.Thaw()

    def ReCreateTechCheckPanel(self):
        self.orderTechCheckPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.techCheckInfoPanel = DraftOrderPanel(self.orderTechCheckPanel, self, self.log, size=(300, 600), mode="USE",
                                                  ID=self.data[1], character=self.character)
        vbox.Add(self.techCheckInfoPanel, 1, wx.EXPAND)
        self.orderTechCheckPanel.SetSizer(vbox)
        self.orderTechCheckPanel.Layout()

    def ReCreatePurchaseCheckPanel(self):
        self.orderPurchaseCheckPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.purchaseCheckInfoPanel = DraftOrderPanel(self.orderPurchaseCheckPanel, self, self.log, size=(300, 600),
                                                      mode="USE", ID=self.data[1], character=self.character)
        vbox.Add(self.purchaseCheckInfoPanel, 1, wx.EXPAND)
        self.orderPurchaseCheckPanel.SetSizer(vbox)
        self.orderPurchaseCheckPanel.Layout()

    def ReCreateFinancialCheckPanel(self):
        self.orderFinancialCheckPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.financialCheckInfoPanel = DraftOrderPanel(self.orderFinancialCheckPanel, self, self.log, size=(300, 600),
                                                       mode="USE", ID=self.data[1], character=self.character)
        vbox.Add(self.financialCheckInfoPanel, 1, wx.EXPAND)
        self.orderFinancialCheckPanel.SetSizer(vbox)
        self.orderFinancialCheckPanel.Layout()

    def ReCreateManagerCheckPanel(self):
        self.orderManagerCheckPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.managerCheckInfoPanel = DraftOrderPanel(self.orderManagerCheckPanel, self, self.log, size=(300, 600),
                                                     mode="USE", ID=self.data[1], character=self.character)
        vbox.Add(self.managerCheckInfoPanel, 1, wx.EXPAND)
        self.orderManagerCheckPanel.SetSizer(vbox)
        self.orderManagerCheckPanel.Layout()

    def OnCellLeftClick(self, event):
        row = event.GetRow()
        self.orderGrid.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.orderGrid.SelectRow(row)
        self.data = self.dataArray[row]
        if self.type == "草稿":
            self.ReCreateRightPanel()
            if self.character in ["订单管理员","项目经理"]:
                self.ReCreateOrderEditPanel()
            if self.character in ["技术员","技术主管","技术部长"]:
                self.ReCreateTechCheckPanel()
            if self.character in ["采购员"]:
                self.ReCreatePurchaseCheckPanel()
            if self.character in ["财务人员"]:
                self.ReCreateFinancialCheckPanel()
            if self.character in ["副总经理","经理"]:
                self.ReCreateManagerCheckPanel()
        elif self.type in orderWorkingStateList:
            if not self.busy:
                # self.ReCreateMiddlePanel(self.type, self.editState)
                self.ReCreateRightPanel()
                _, self.orderDetailData = GetOrderDetailRecord(self.log, 1, self.data[0])
                if len(self.orderDetailData) == 0:
                    self.treeStructure = []
                else:
                    self.treeStructure = self.TreeDataTransform()
                self.ReCreateOrderDetailTree()
        event.Skip()

    def TreeDataTransform(self):
        orderTreeData = np.array(self.orderDetailData)
        subOrderIDList = list(orderTreeData[:, 2])  # 提出所有子订单号组成列表
        subOrderIDList = list(set(subOrderIDList))  # 得到所有不重复的子订单号
        subOrderIDList.sort()
        result = copy.deepcopy(subOrderIDList)
        for subNum, subOrderID in enumerate(result):
            deckOrderIDList = []
            for data in orderTreeData:
                if str(data[2]) == str(subOrderID):
                    deckOrderIDList.append(data[3])
            deckOrderIDList = list(set(deckOrderIDList))
            deckOrderIDList.sort()
            result[subNum] = deckOrderIDList
        deckOrderIDList = result
        result = copy.deepcopy(deckOrderIDList)
        for subNum, subOrderID in enumerate(result):
            for deckNum, deckOrderID in enumerate(subOrderID):
                zoneOrderIDList = []
                for data in orderTreeData:
                    if str(data[2]) == str(subOrderIDList[subNum]) and str(data[3]) == str(deckOrderID):
                        zoneOrderIDList.append(data[4])
                zoneOrderIDList = list(set(zoneOrderIDList))
                zoneOrderIDList.sort()
                result[subNum][deckNum] = zoneOrderIDList
        zoneOrderIDList = result
        result = copy.deepcopy(zoneOrderIDList)
        for subNum, subOrderID in enumerate(result):
            for deckNum, deckOrderID in enumerate(subOrderID):
                for zoneNum, zoneOrderID in enumerate(deckOrderID):
                    roomOrderIDList = []
                    for data in orderTreeData:
                        if str(data[2]) == str(subOrderIDList[subNum]) and str(data[3]) == str(
                                deckOrderIDList[subNum][deckNum]) and str(data[4]) == str(zoneOrderID):
                            roomOrderIDList.append(data[5])
                    roomOrderIDList = list(set(roomOrderIDList))
                    roomOrderIDList.sort()
                    result[subNum][deckNum][zoneNum] = roomOrderIDList
        roomOrderIDList = result
        return subOrderIDList, deckOrderIDList, zoneOrderIDList, roomOrderIDList

    def ReCreateRightPanel(self):
        self.rightPanel.Freeze()
        self.rightPanel.DestroyChildren()
        self.notebook = wx.Notebook(self.rightPanel, -1, size=(21, 21), style=
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
        hbox = wx.BoxSizer()
        hbox.Add(self.notebook, 1, wx.EXPAND)
        self.rightPanel.SetSizer(hbox)
        self.rightPanel.Layout()
        if self.type in orderWorkingStateList:
            self.orderDetailPanel = wx.Panel(self.notebook)
            self.notebook.AddPage(self.orderDetailPanel, "订单详情")
            self.orderExcelPanel = wx.Panel(self.notebook)
            self.notebook.AddPage(self.orderExcelPanel, "订单原始Excel")
            hbox = wx.BoxSizer()
            self.orderDetailTreePanel = wx.Panel(self.orderDetailPanel, size=(260, -1))
            self.orderDetailGridPanel = wx.Panel(self.orderDetailPanel, size=(100, -1), style=wx.BORDER_THEME)
            hbox.Add(self.orderDetailTreePanel, 0, wx.EXPAND)
            hbox.Add(self.orderDetailGridPanel, 1, wx.EXPAND)
            self.orderDetailPanel.SetSizer(hbox)
            self.orderDetailPanel.Layout()
        elif self.type == "草稿":
            if self.master.operatorCharacter in ["项目经理",'订单管理员']:
                self.orderEditPanel = wx.Panel(self.notebook, size=(260, -1))
                self.notebook.AddPage(self.orderEditPanel, "订单部审核")
                self.ReCreateOrderEditPanel()
            if self.master.operatorCharacter in ["技术员","技术主管","技术部长"]:
                self.orderTechCheckPanel = wx.Panel(self.notebook, size=(260, -1))
                self.notebook.AddPage(self.orderTechCheckPanel, "技术部审核")
            if self.master.operatorCharacter == '采购员':
                self.orderPurchaseCheckPanel = wx.Panel(self.notebook, size=(260, -1))
                self.notebook.AddPage(self.orderPurchaseCheckPanel, "采购部审核")
            # self.orderFinancialCheckPanel = wx.Panel(self.notebook,size=(260,-1))
            # self.notebook.AddPage(self.orderFinancialCheckPanel, "财务部审核")
            if self.master.operatorCharacter in ["副总经理","经理"]:
                self.orderManagerCheckPanel = wx.Panel(self.notebook, size=(260, -1))
                self.notebook.AddPage(self.orderManagerCheckPanel, "经理审核")
        self.rightPanel.Thaw()

    # def OnDraftOrderEditOkBTN(self,event):
    #     d = self.draftOrderEditPanel.pg.GetPropertyValues(inc_attributes=True)
    #     dic = {}
    #     for k, v in d.items():
    #         dic[k] = v
    #
    #     # operatorID = self.parent.parent.operatorID
    #     for key in dic.keys():
    #         if dic[key]=="" and '*' in key:
    #             wx.MessageBox("%s不能为空，请重新输入！"%key)
    #             return
    #     code = UpdateDraftOrderInfoByID(self.log,WHICHDB,dic,self.data[1])
    #     if code>0:
    #         wx.MessageBox("更新成功！")
    #     else:
    #         wx.MessageBox("更新失败！")
    #     self.ReCreate()
    #
    # def OnDraftOrderEditCancelBTN(self,event):
    #     self.ReCreate()

    def ReCreteOrderDetailGridPanel(self):
        self.orderDetailGridPanel.Freeze()
        self.orderDetailGridPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.orderDetailGrid = OrderDetailGrid(self.orderDetailGridPanel, self, self.log)
        vbox.Add(self.orderDetailGrid, 1, wx.EXPAND)
        self.orderDetailGridPanel.SetSizer(vbox)
        self.orderDetailGridPanel.Layout()
        self.orderDetailGridPanel.Thaw()

    def OnOrderStateSearch(self, event):
        self.orderStateSearch = self.orderStateSearchCtrl.GetValue()
        self.ReSearch()

    def OnOperatorSearch(self, event):
        self.operatorSearch = self.operatorSearchCtrl.GetValue()
        self.ReSearch()

    def OnOrderIDSearch(self, event):
        self.orderIDSearch = self.orderIDSearchCtrl.GetValue()
        self.ReSearch()

    def OnProductNameSearch(self, event):
        self.productNameSearch = self.productNameSearchCtrl.GetValue()
        self.ReSearch()

    def ReSearch(self):
        _, orderList = GetAllOrderList(self.log, 1)
        self.dataArray = np.array(orderList)
        if self.productNameSearch != '':
            orderList = []
            for order in self.dataArray:
                if order[2] == self.productNameSearch:
                    orderList.append(order)
            self.dataArray = np.array(orderList)
        if self.orderIDSearch != '':
            orderList = []
            for order in self.dataArray:
                if str(order[0]) == self.orderIDSearch:
                    orderList.append(order)
            self.dataArray = np.array(orderList)
        if self.operatorSearch != '':
            orderList = []
            for order in self.dataArray:
                if str(order[6]) == self.operatorSearch:
                    orderList.append(order)
            self.dataArray = np.array(orderList)
        if self.orderStateSearch != '':
            orderList = []
            for order in self.dataArray:
                if str(order[7]) == self.orderStateSearch:
                    orderList.append(order)
            self.dataArray = np.array(orderList)
        self.orderGrid.ReCreate()

    def OnResetSearchItem(self, event):
        self.orderIDSearch = ''
        self.orderIDSearchCtrl.SetValue('')
        self.productNameSearch = ''
        self.productNameSearchCtrl.SetValue('')
        self.productAmountSearchCtrl.SetValue('')
        self.deliverDateSearchCtrl.SetValue('')
        self.orderDateSearchCtrl.SetValue('')
        self.operatorSearch = ''
        self.operatorSearchCtrl.SetValue('')
        self.orderStateSearch = ''
        self.orderStateSearchCtrl.SetValue('')
        self.ReSearch()


class DraftOrderPanel(wx.Panel):
    def __init__(self, parent, master, log, size, mode="NEW", ID=None, character="技术员"):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=size)
        self.master = master
        self.log = log
        self.ID = ID
        self.mode = mode
        self.character = character
        self.priceDataDic = []
        self.ReCreate()

    def ReCreate(self):
        self.orderName = ""
        self.customerName = ""
        self.customerInfo = ""
        self.contactsName = ""
        self.phoneNumber = ""
        self.email = ""
        self.bidMode = BIDMODE[0]
        self.bidMethod = BIDMETHOD[0]
        self.draftOrderType = 0
        self.techDrawingName1 = ""
        self.techDrawingName2 = ""
        self.techDrawingName3 = ""
        self.techDrawingName4 = ""
        self.secureProtocolName = ""
        self.bidDocName = ""
        self.techRequireDocName = ""
        self.makeOrderDate = wx.DateTime.Now()
        self.bidDate = pydate2wxdate(datetime.date.today() + datetime.timedelta(days=7))
        if self.ID != None:
            self.ID = int(self.ID)
        if self.mode == "NEW":
            pass
        else:
            while 1:
                dic = None
                for item in self.master.draftOrderDic:
                    if item["Index"] == self.ID:
                        dic = item
                        break
                if dic:
                    break
            self.makeOrderDate = str2wxdate(dic["下单时间"])
            self.bidDate = str2wxdate(dic["投标时间"])
            self.orderName = dic["订单名称"]
            self.customerName = dic["客户名称"]
            self.customerInfo = dic["客户公司信息"]
            self.contactsName = dic["联系人"]
            self.phoneNumber = dic["联系人电话"]
            self.email = dic["联系人邮箱"]
            self.draftOrderType = int(dic['草稿订单类别'])
            self.bidMode = dic["投标方式"]
            self.bidMethod = dic["投标格式"]
            self.techDrawingName1 = dic["客户原始技术图纸名1"]
            self.techDrawingName2 = dic["客户原始技术图纸名2"]
            self.techDrawingName3 = dic["客户原始技术图纸名3"]
            self.techDrawingName4 = dic["客户原始技术图纸名4"]
            self.techCheckState = dic['设计审核状态']
            self.orderOperatorCheckState = dic['订单部审核状态']
            self.managerCheckState = dic['经理审核状态']
            self.techDrawingName1 = self.techDrawingName1.strip("/")
            if self.techDrawingName2 == None:
                self.techDrawingName2 = ""
            else:
                self.techDrawingName2 = self.techDrawingName2.strip("/")
            if self.techDrawingName3 == None:
                self.techDrawingName3 = ""
            else:
                self.techDrawingName3 = self.techDrawingName3.strip("/")
            if self.techDrawingName4 == None:
                self.techDrawingName4 = ""
            else:
                self.techDrawingName4 = self.techDrawingName4.strip("/")
        self.Freeze()
        self.DestroyChildren()
        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel,
                                                style=wxpg.PG_SPLITTER_AUTO_CENTER |
                                                      wxpg.PG_AUTO_SORT |
                                                      wxpg.PG_TOOLBAR)

        # Show help as tooltips
        pg.ExtraStyle |= wxpg.PG_EX_HELP_AS_TOOLTIPS

        # pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        # pg.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
        # pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        # pg.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )

        if not getattr(sys, '_PropGridEditorsRegistered', False):
            pg.RegisterEditor(TrivialPropertyEditor)
            pg.RegisterEditor(SampleMultiButtonEditor)
            pg.RegisterEditor(TechDrawingButtonEditor)
            pg.RegisterEditor(LargeImageEditor)
            # ensure we only do it once
            sys._PropGridEditorsRegistered = True

        #
        # Add properties
        #
        # NOTE: in this example the property names are used as variable names
        # in one of the tests, so they need to be valid python identifiers.
        #
        draftOrderTypeList = ['简单报价', '详细报价']
        pg.AddPage("订单部录入信息")
        pg.Append(wxpg.PropertyCategory("1 - 订单基本信息"))
        pg.Append(wxpg.StringProperty("1.订单名称 *", value=self.orderName))
        # pg.Append( wxpg.StringProperty("2.草稿订单类别",value=self.draftOrderType) )
        pg.Append(wxpg.EnumProperty("2.草稿订单类别", "2.草稿订单类别",
                                    draftOrderTypeList,
                                    [0, 1],
                                    self.draftOrderType))
        pg.Append(wxpg.StringProperty("3.客户单位名称", value=self.customerName))
        pg.Append(wxpg.StringProperty("4.客户公司信息", value=self.customerInfo))
        pg.Append(wxpg.StringProperty("5.联系人姓名 *", value=self.contactsName))
        pg.Append(wxpg.StringProperty("6.联系人电话", value=self.phoneNumber))
        pg.Append(wxpg.StringProperty("7.联系人email *", value=self.email))
        pg.Append(wxpg.DateProperty("8.下单日期", value=self.makeOrderDate))

        pg.Append(wxpg.PropertyCategory("2 - 询价文件"))

        pg.Append(wxpg.DateProperty("1.投标日期", value=self.bidDate))
        # pg.Append( wxpg.EnumProperty("2.投标方式","2.投标方式",
        #                              BIDMODE,
        #                              [0,1,2],
        #                              BIDMODE.index(self.bidMode)) )
        # pg.Append( wxpg.EnumProperty("3.投标格式","3.投标格式",
        #                              BIDMETHOD,
        #                              [0,1],
        #                              BIDMETHOD.index(self.bidMethod)) )

        pg.Append(wxpg.PropertyCategory("3 - 附件"))
        if self.mode in ["NEW", "EDIT"]:
            pg.Append(wxpg.FileProperty("1.产品清单或图纸文件", value=self.techDrawingName1))
            pg.Append(wxpg.FileProperty("2.产品清单或图纸文件", value=self.techDrawingName2))
            pg.Append(wxpg.FileProperty("3.产品清单或图纸文件", value=self.techDrawingName3))
            pg.Append(wxpg.FileProperty("4.产品清单或图纸文件", value=self.techDrawingName4))

            pg.SetPropertyAttribute("1.产品清单或图纸文件", wxpg.PG_FILE_SHOW_FULL_PATH, 0)
            pg.SetPropertyAttribute("2.产品清单或图纸文件", wxpg.PG_FILE_SHOW_FULL_PATH, 0)
            pg.SetPropertyAttribute("3.产品清单或图纸文件", wxpg.PG_FILE_SHOW_FULL_PATH, 0)
            pg.SetPropertyAttribute("4.产品清单或图纸文件", wxpg.PG_FILE_SHOW_FULL_PATH, 0)
            # pg.SetPropertyAttribute( "1.图纸文件 *", wxpg.PG_FILE_INITIAL_PATH,
            #                          r"C:\Program Files\Internet Explorer" )
            pg.SetPropertyAttribute("1.投标日期", wxpg.PG_DATE_PICKER_STYLE,
                                    wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
            topsizer.Add(pg, 1, wx.EXPAND)
            if self.character in ["项目经理",'订单管理员']:
                if self.ID != None:
                    rowsizer = wx.BoxSizer(wx.HORIZONTAL)
                    but = wx.Button(panel, -1, "保存修改", size=(-1, 35))
                    but.Bind(wx.EVT_BUTTON, self.OnDraftOrderEditOkBTN)
                    rowsizer.Add(but, 1)
                    but = wx.Button(panel, -1, "取消修改", size=(-1, 35))
                    but.Bind(wx.EVT_BUTTON, self.OnDraftOrderEditCancelBTN)
                    rowsizer.Add(but, 1)
                    topsizer.Add(rowsizer, 0, wx.EXPAND)
                    rowsizer = wx.BoxSizer(wx.HORIZONTAL)
                    but = wx.Button(panel, -1, "订单废弃", size=(-1, 35))
                    but.Bind(wx.EVT_BUTTON, self.OnDraftOrderAbandonBTN)
                    rowsizer.Add(but, 1)
                    but = wx.Button(panel, -1, "订单投产", size=(-1, 35))
                    # but.Bind(wx.EVT_BUTTON, self.OnDraftOrderEditCancelBTN)
                    rowsizer.Add(but, 1)
                    topsizer.Add(rowsizer, 0, wx.EXPAND)
                    rowsizer = wx.BoxSizer(wx.HORIZONTAL)
                    if self.orderOperatorCheckState == 'Y' and self.managerCheckState == 'Y':
                        temp = "生成报价单"
                    else:
                        temp = "进行订单部审核"
                    but = wx.Button(panel, -1, temp, size=(-1, 35), name=temp)
                    but.Bind(wx.EVT_BUTTON, self.OnDraftOrderCreateQuotationBTN)
                    rowsizer.Add(but, 1)
                    topsizer.Add(rowsizer, 0, wx.EXPAND)
                    # btnsizer = wx.BoxSizer()
                    # bitmap1 = wx.Bitmap("D:/IPMS/dist/bitmaps/ok3.png", wx.BITMAP_TYPE_PNG)
                    # bitmap2 = wx.Bitmap("D:/IPMS/dist/bitmaps/cancel1.png", wx.BITMAP_TYPE_PNG)
                    # bitmap3 = wx.Bitmap("D:/IPMS/dist/bitmaps/33.png", wx.BITMAP_TYPE_PNG)
                    # btn_ok = wx.Button(self.orderEditPanel, wx.ID_OK, "确 认 修 改", size=(200, 50))
                    # btn_ok.Bind(wx.EVT_BUTTON,self.OnDraftOrderEditOkBTN)
                    # btn_ok.SetBitmap(bitmap1, wx.LEFT)
                    # btnsizer.Add(btn_ok, 0)
                    # btnsizer.Add((40, -1), 0)
                    # sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
                    # self.orderEditPanel.SetSizer(sizer)
                    # sizer.Fit(self.orderEditPanel)
        else:
            techDrawingName1 = self.techDrawingName1.split("/")[-1]
            techDrawingName1 = "%d." % self.ID + techDrawingName1
            techDrawingName2 = self.techDrawingName2.split("/")[-1]
            if techDrawingName2 != "":
                techDrawingName2 = "%d." % self.ID + techDrawingName2
            techDrawingName3 = self.techDrawingName3.split("/")[-1]
            if techDrawingName3 != "":
                techDrawingName3 = "%d." % self.ID + techDrawingName3
            techDrawingName4 = self.techDrawingName4.split("/")[-1]
            if techDrawingName4 != "":
                techDrawingName4 = "%d." % self.ID + techDrawingName4
            pg.Append(wxpg.LongStringProperty("1.产品清单或图纸文件", value=techDrawingName1))
            pg.SetPropertyEditor("1.产品清单或图纸文件", "TechDrawingButtonEditor")
            pg.Append(wxpg.LongStringProperty("2.产品清单或图纸文件", value=techDrawingName2))
            pg.SetPropertyEditor("2.产品清单或图纸文件", "TechDrawingButtonEditor")
            pg.Append(wxpg.LongStringProperty("3.产品清单或图纸文件", value=techDrawingName3))
            pg.SetPropertyEditor("3.产品清单或图纸文件", "TechDrawingButtonEditor")
            pg.Append(wxpg.LongStringProperty("4.产品清单或图纸文件", value=techDrawingName4))
            pg.SetPropertyEditor("4.产品清单或图纸文件", "TechDrawingButtonEditor")
            topsizer.Add(pg, 1, wx.EXPAND)
            rowsizer = wx.BoxSizer(wx.HORIZONTAL)
            if self.character in ["技术员","技术主管","技术部长"]:
                but = wx.Button(panel, -1, "开始技术部审核", size=(-1, 35))
                but.Bind(wx.EVT_BUTTON, self.OnStartTechCheck)
                rowsizer.Add(but, 1)
                # but = wx.Button(panel,-1,"完成设计审核",size=(-1,35))
                # but.Bind( wx.EVT_BUTTON, self.OnFinishTechCheck)
                # rowsizer.Add(but,1)
            elif self.character == "采购员":
                but = wx.Button(panel, -1, "开始采购部审核", size=(-1, 35))
                but.Bind(wx.EVT_BUTTON, self.OnStartPurchaseCheck)
                rowsizer.Add(but, 1)
                but = wx.Button(panel, -1, "完成采购部审核", size=(-1, 35))
                but.Bind(wx.EVT_BUTTON, self.OnFinishPurchaseCheck)
                rowsizer.Add(but, 1)
            elif self.character == "财务":
                but = wx.Button(panel, -1, "开始财务部审核", size=(-1, 35))
                but.Bind(wx.EVT_BUTTON, self.OnStartFinancialCheck)
                rowsizer.Add(but, 1)
                but = wx.Button(panel, -1, "完成财务部审核", size=(-1, 35))
                but.Bind(wx.EVT_BUTTON, self.OnFinishFinancialCheck)
                rowsizer.Add(but, 1)
            elif self.character in ["经理","副总经理"]:
                but = wx.Button(panel, -1, "开始经理审核", size=(-1, 35))
                but.Bind(wx.EVT_BUTTON, self.OnStartManagerCheck)
                # rowsizer.Add(but,1)
                # but = wx.Button(panel,-1,"完成经理审核",size=(-1,35))
                # but.Bind( wx.EVT_BUTTON, self.OnFinishManagerCheck)
                rowsizer.Add(but, 1)
            topsizer.Add(rowsizer, 0, wx.EXPAND)

        # pg.AddPage( "技术部审核信息" )
        # pg.Append( wxpg.PropertyCategory("1 - 订单基本信息2") )
        # sp = pg.Append( wxpg.StringProperty('StringProperty_as_Password', value='ABadPassword') )
        # sp.SetAttribute('Hint', 'This is a hint')
        # sp.SetAttribute('Password', True)
        #
        # pg.Append( wxpg.IntProperty("Int", value=100) )
        # self.fprop = pg.Append( wxpg.FloatProperty("Float", value=123.456) )
        # pg.Append( wxpg.BoolProperty("Bool", value=True) )
        # boolprop = pg.Append( wxpg.BoolProperty("Bool_with_Checkbox", value=True) )
        # pg.SetPropertyAttribute(
        #     "Bool_with_Checkbox",    # You can find the property by name,
        #     #boolprop,               # or give the property object itself.
        #     "UseCheckbox", True)     # The attribute name and value
        #
        # pg.Append( wxpg.PropertyCategory("2 - 询价文件2") )
        # _,minNum=GetPropertyVerticalCuttingParameter(self.log,1)
        # pg.Append( wxpg.IntProperty("启动纵切最小板材数",value=minNum) )
        # pg.SetPropertyEditor("启动纵切最小板材数","SpinCtrl")
        # _,pageRowNum=GetPropertySchedulePageRowNumber(self.log,1)
        # pg.Append( wxpg.IntProperty("任务单每页行数",value=pageRowNum) )
        # pg.SetPropertyEditor("任务单每页行数","SpinCtrl")
        # pg.Append( DirsProperty("墙角板型号列表",value=['2SG','2SD','2SE','2SH']) )
        #
        # pg.Append( wxpg.PropertyCategory("3 - 附件") )
        # pg.Append( wxpg.LongStringProperty("LongString",
        #     value="This is a\nmulti-line string\nwith\ttabs\nmixed\tin."))
        # pg.Append( wxpg.ArrayStringProperty("ArrayString",value=['A','B','C']) )
        #
        # pg.Append( wxpg.EnumProperty("Enum","Enum",
        #                              ['wxPython Rules',
        #                               'wxPython Rocks',
        #                               'wxPython Is The Best'],
        #                              [10,11,12],
        #                              0) )
        # pg.Append( wxpg.EditEnumProperty("EditEnum","EditEnumProperty",
        #                                  ['A','B','C'],
        #                                  [0,1,2],
        #                                  "Text Not in List") )
        #
        # pg.Append( wxpg.DateProperty("Date",value=wx.DateTime.Now()) )
        # pg.Append( wxpg.FontProperty("Font",value=panel.GetFont()) )
        # pg.Append( wxpg.ColourProperty("Colour",
        #                                value=panel.GetBackgroundColour()) )
        # pg.Append( wxpg.SystemColourProperty("SystemColour") )
        # pg.Append( wxpg.ImageFileProperty("ImageFile") )
        # pg.Append( wxpg.MultiChoiceProperty("MultiChoice",
        #             choices=['wxWidgets','QT','GTK+']) )
        #
        # pg.Append( wxpg.PropertyCategory("4 - 财务部审核信息2") )
        # #pg.Append( wxpg.PointProperty("Point",value=panel.GetPosition()) )
        # pg.Append( SizeProperty("Size", value=panel.GetSize()) )
        # #pg.Append( wxpg.FontDataProperty("FontData") )
        # pg.Append( wxpg.IntProperty("IntWithSpin",value=256) )
        # pg.SetPropertyEditor("IntWithSpin","SpinCtrl")
        #
        # pg.Append( wxpg.PropertyCategory("5 - 经理审核信息2") )
        # pg.Append( IntProperty2("IntProperty2", value=1024) )
        #
        # pg.Append( PyObjectProperty("PyObjectProperty") )
        #
        # pg.Append( DirsProperty("Dirs1",value=['C:/Lib','C:/Bin']) )
        # pg.Append( DirsProperty("Dirs2",value=['/lib','/bin']) )
        #
        # # Test another type of delimiter
        # pg.SetPropertyAttribute("Dirs2", "Delimiter", '"')
        #
        # # SampleMultiButtonEditor
        # pg.Append( wxpg.LongStringProperty("MultipleButtons") )
        # pg.SetPropertyEditor("MultipleButtons", "SampleMultiButtonEditor")
        # pg.Append( SingleChoiceProperty("SingleChoiceProperty") )
        #
        # # Custom editor samples
        # prop = pg.Append( wxpg.StringProperty("StringWithCustomEditor",
        #                                       value="test value") )
        # pg.SetPropertyEditor(prop, "TrivialPropertyEditor")
        #
        # pg.Append( wxpg.ImageFileProperty("ImageFileWithLargeEditor") )
        # pg.SetPropertyEditor("ImageFileWithLargeEditor", "LargeImageEditor")

        # rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        # but = wx.Button(panel,-1,"GetPropertyValues(as_strings=True)")
        # but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues2 )
        # rowsizer.Add(but,1)
        # but = wx.Button(panel,-1,"AutoFill")
        # but.Bind( wx.EVT_BUTTON, self.OnAutoFill )
        # rowsizer.Add(but,1)
        # topsizer.Add(rowsizer,0,wx.EXPAND)
        # rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        # but = wx.Button(panel,-1,"Delete")
        # but.Bind( wx.EVT_BUTTON, self.OnDeleteProperty )
        # rowsizer.Add(but,1)
        # but = wx.Button(panel,-1,"Run Tests")
        # but.Bind( wx.EVT_BUTTON, self.RunTests )
        # rowsizer.Add(but,1)
        # topsizer.Add(rowsizer,0,wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        self.Thaw()

    def OnDraftOrderAbandonBTN(self, event):
        dlg = wx.MessageDialog(self, "您确定要废弃此订单吗？", "信息提示", style=wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            if UpdateDraftOrderStateInDB(self.log, WHICHDB, self.ID, "废弃") == 0:
                # self.master.ReCreate()
                wx.MessageBox("订单已成功废弃，系统稍后将刷新显示！", "信息提示")
            else:
                wx.MessageBox("订单废弃操作失败！", "信息提示")
        dlg.Destroy()

    def OnDraftOrderCreateQuotationBTN(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        if self.techCheckState != "Y":
            wx.MessageBox("订单没有完成技术审核，无法进行订单部审核，请稍后再试！", "信息提示")
            return

        busy = PBI.PyBusyInfo("正在从云端数据库读取订单数据，请稍候！", parent=None, title="系统忙提示",
                              icon=images.Smiles.GetBitmap())

        wx.Yield()
        # self.priceDateLatest = GetPriceDateListFromDB(self.log, WHICHDB)[0]
        # self.priceDataDic = GetPriceDicFromDB(self.log, WHICHDB, self.priceDateLatest)
        while self.priceDataDic==[]:
            self.priceDataDic = self.master.priceDataDic
        dlg = QuotationSheetDialog(self, self.master, self.log, self.ID, self.character, name, self.orderName)
        dlg.CenterOnScreen()
        del busy
        dlg.ShowModal()
        dlg.Destroy()
        # self.master.dataList = []
        # self.master.ReCreate()

    def OnDraftOrderEditOkBTN(self, event):
        d = self.pg.GetPropertyValues(inc_attributes=True)
        dic = {}
        for k, v in d.items():
            if "产品清单或图纸文件" in k:
                temp = str(v)
                v = temp.replace('\\','/')
            dic[k] = v
        # operatorID = self.parent.parent.operatorID

        for key in dic.keys():
            if key == "1.产品清单或图纸文件" and dic[key] == "" and dic['2.草稿订单类别'] == '详细报价':
                wx.MessageBox("%s不能为空，请重新输入！" % key)
                return
            if dic[key] == "" and '*' in key:
                wx.MessageBox("%s不能为空，请重新输入！" % key)
                return
        busy = PBI.PyBusyInfo("正在数据保存到云端数据库，请稍候！", parent=None, title="系统忙提示",
                              icon=images.Smiles.GetBitmap())

        wx.Yield()
        code = UpdateDraftOrderInfoByID(self.log, WHICHDB, dic, self.ID)
        del busy
        if code >= 0:
            wx.MessageBox("更新成功！","信息提示")
        else:
            wx.MessageBox("更新失败！","信息提示")

    def OnDraftOrderEditCancelBTN(self, event):
        self.ReCreate()

    def OnStartManagerCheck(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        if self.techCheckState != "Y":
            wx.MessageBox("订单没有完成技术审核，无法进行经理审核，请稍后再试！", "信息提示")
            return
        busy = PBI.PyBusyInfo("正在从云端数据库读取订单数据，请稍候！", parent=None, title="系统忙提示",
                              icon=images.Smiles.GetBitmap())

        wx.Yield()

        self.priceDateLatest = GetPriceDateListFromDB(self.log, WHICHDB)[0]
        self.priceDataDic = GetPriceDicFromDB(self.log, WHICHDB, self.priceDateLatest)
        dlg = QuotationSheetDialog(self, self.master, self.log, self.ID, self.character, name, self.orderName)
        dlg.CenterOnScreen()
        del busy
        dlg.ShowModal()
        dlg.Destroy()
        # self.master.dataList = []
        # self.master.ReCreate()

    def OnFinishManagerCheck(self, event):
        pass

    def OnStartFinancialCheck(self, event):
        self.draftCheckFrame = DraftCheckFrame(self, self.log, self.ID, character=self.character)
        self.draftCheckFrame.Show(True)
        self.draftCheckFrame.CenterOnScreen()

    def OnFinishFinancialCheck(self, event):
        pass

    def OnStartPurchaseCheck(self, event):
        self.draftCheckFrame = DraftCheckFrame(self, self.log, self.ID, character=self.character)
        self.draftCheckFrame.Show(True)
        self.draftCheckFrame.CenterOnScreen()

    def OnFinishPurchaseCheck(self, event):
        pass

    def OnStartTechCheck(self, event):
        if self.techCheckState == 'Y':
            dlg = wx.MessageDialog(self, "此订单已完成技术部审核，如果您继续执行审核操作会导致之前的操作全部重置！\r\n请确认是否继续执行审核操作？", "信息提示",
                                   style=wx.YES_NO)
            if dlg.ShowModal() == wx.ID_NO:
                return
            dlg.Destroy()
        if self.techCheckState != 'I':
            UpdateTechCheckStateByID(self.log, WHICHDB, self.ID, "I")
            UpdatePurchchaseCheckStateByID(self.log, WHICHDB, self.ID, 'N')
            UpdateFinancingCheckStateByID(self.log, WHICHDB, self.ID, 'N')
            UpdateManagerCheckStateByID(self.log, WHICHDB, self.ID, 'N')
            UpdateOrderOperatorCheckStateByID(self.log, WHICHDB, self.ID, 'N', None, None)
            UpdateManagerCheckStateByID(self.log, WHICHDB, self.ID, 'N')
        # self.techCheckFrame = wx.MessageDialog(self,"测试进行中")
        # self.techCheckFrame.ShowModal()
        message = "正在读取订单数据，请稍候。。。"
        busy = PBI.PyBusyInfo(message, parent=None, title="系统忙提示",
                              icon=images.Smiles.GetBitmap())
        wx.Yield()
        self.techCheckDialog = TechCheckDialog(self.master, self.log, self.ID, character=self.character)
        self.techCheckDialog.CenterOnScreen()
        del busy
        if self.techCheckDialog.ShowModal() == wx.ID_OK:
            UpdateTechCheckStateByID(self.log, WHICHDB, self.ID, "Y")
            UpdatePurchchaseCheckStateByID(self.log, WHICHDB, self.ID, 'Y')
            UpdateFinancingCheckStateByID(self.log, WHICHDB, self.ID, 'Y')
            self.master.dataList = []
            # self.master.ReCreate()

    def OnFinishTechCheck(self, event):
        UpdateTechCheckStateByID(self.log, WHICHDB, self.ID, "Y")
        # self.master.ReCreate()


class WallPanelOtherCheckGrid(gridlib.Grid):
    def __init__(self, parent, log, type, id, character):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.type = type
        self.id = id
        self.character = character
        if self.type == "WALL":
            data = GetDraftComponentInfoByID(self.log, WHICHDB, self.id)
        self.data = []
        for dic in data:
            temp = []
            for section in WallCheckEnableSectionDic[self.character]:
                temp.append(dic[section])
            self.data.append(temp)
        self.SetDefaultRowSize(30)
        self.colLabels = OtherCheckTitleDict[self.type]
        self.colWidths = OtherCheckColWidthDict[self.type]
        self.CreateGrid(len(self.data), len(self.colLabels))  # , gridlib.Grid.SelectRows)
        self.SetRowLabelSize(80)
        self.SetColLabelSize(60)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        # self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChanged)
        font = self.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        attr = gridlib.GridCellAttr()
        attr.SetFont(font)
        attr.SetBackgroundColour(wx.LIGHT_GREY)
        attr.SetReadOnly(True)
        attr.SetAlignment(wx.RIGHT, -1)

        for i, title in enumerate(self.colLabels):
            self.SetColSize(i, self.colWidths[i])
            self.SetColLabelValue(i, title)
        for i, row in enumerate(self.data):
            for j, col in enumerate(row):
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                # self.SetCellFont(i, j, wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                self.SetCellValue(i, j, col)
                if j == 8:
                    self.SetCellEditor(i, j, gridlib.GridCellFloatEditor(-1, 2))
                # self.SetCellBackgroundColour(i, j, wx.BLUE)
        for j in range(len(self.colLabels)):
            self.SetCellAlignment(len(self.data), j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            if j != 8:
                self.SetColAttr(j, attr)
        # attr.IncRef()

    def OnCellChanged(self, event):
        row = event.GetRow()
        col = event.GetCol()
        event.Skip()
        a = float(self.GetCellValue(row, col - 1))
        b = float(self.GetCellValue(row, col))
        self.SetCellValue(row, col + 1, str(a * b))
    # def OnLeftDClick(self, evt):
    #     if self.CanEnableCellControl():
    #         self.EnableCellEditControl()


class WallPanelTechCheckGrid(gridlib.Grid):
    def __init__(self, parent, log, type, id):
        gridlib.Grid.__init__(self, parent, -1)
        self.log = log
        self.type = type
        self.id = id
        data=[]
        if self.type in ["WALL", 'CEILING', "INTERIORDOOR", "FIREDOOR",'WETUNIT']:
            data = GetDraftComponentInfoByID(self.log, WHICHDB, self.id, self.type)
        self.data = []
        for dic in data:
            temp = []
            for section in WallCheckEnableSectionList:
                if section == '潮湿' or section == '加强':
                    if dic[section] == '1' or dic[section]=="Y":
                        dic[section]=True
                    else:
                        dic[section] = False
                temp.append(dic[section])
            self.data.append(temp)
        self.SetDefaultRowSize(30)
        self.table = WallPanelCheckDataTable(log, self.type, self.data)
        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(self.table, True)

        font = self.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        attr = gridlib.GridCellAttr()
        attr.SetFont(font)
        # attr.SetBackgroundColour(wx.LIGHT_GREY)
        attr.SetReadOnly(True)
        attr.SetAlignment(wx.RIGHT, -1)
        self.SetColAttr(4, attr)
        if self.type in ["WALL","CEILING"]:
            self.SetColAttr(5, attr)
        if self.type == "CEILING":
            self.SetColAttr(2, attr)
        if self.type == "FIREDOOR":
            self.SetColAttr(3, attr)
        if self.type == "WETUNIT":
            self.SetColAttr(1, attr)
            self.SetColAttr(2, attr)
            self.SetColAttr(3, attr)
        self.SetRowLabelSize(80)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(False)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.colLabels = CheckTitleDict[self.type]
        self.colWidths = CheckColWidthDict[self.type]
        for i, title in enumerate(self.colLabels):
            self.SetColSize(i, self.colWidths[i])
        for i, row in enumerate(self.data):
            for j, col in enumerate(row):
                # self.SetCellBackgroundColour(i, j, wx.BLUE)
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                # self.SetCellFont(i, j, wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        for j in range(len(self.colLabels)):
            self.SetCellAlignment(len(self.colLabels), j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

    def OnCellChange(self, evt):
        thickDic = {"F": '25', 'A': '50', 'G': '25', 'D': '50'}
        ceilingLengthDic = {"TNF-C46":'600',"TNF-C55":'≤3000',"TNF-C64":'≤3000',"TNF-C65":'≤3000',"TNF-C68":'≤3000',"TNF-C70":'≤3000',
                           "TNF-C71":'≤3000',"TNF-C72":'≤3000',"TNF-C73":'≤3000'}
        # ceilingWidthDic = {"TNF-C46":'70',"TNF-C55":'50',"TNF-C64":'40',"TNF-C65":'50',"TNF-C68":'50',"TNF-C70":'50',
        #                    "TNF-C71":'50',"TNF-C72":'50',"TNF-C73":'50'}
        interiorDoorHeightDic = {"TNF-A60ZF-S001":'2100',"TNF-A60BF-A60-01":'2100',"TNF-SA60BF-A60-01":'2200',
                                 "TNF-B15BF-001":'2200',"TNF-SB15BF-S001":'2200',"TNF-B15ZF-HNR-01":'2000',
                                 "TNF-B15ZF-01":'2100'}
        interiorDoorWidthDic = {"TNF-A60ZF-S001":'1000',"TNF-A60BF-A60-01":'1000',"TNF-SA60BF-A60-01":'2100',
                                 "TNF-B15BF-001":'1100',"TNF-SB15BF-S001":'2000',"TNF-B15ZF-HNR-01":'1000',
                                 "TNF-B15ZF-01":'1050'}
        col = evt.GetCol()
        row = evt.GetRow()
        if self.type=="WALL":
            if col == 0:
                lastChar = self.GetCellValue(row, col)[-1]
                self.table.SetTypeName(1,WallSurfaceDict[self.GetCellValue(row, 0)])
                self.SetCellValue(row, 4, thickDic[lastChar])
                self.SetCellValue(row,5,"m2")
        elif self.type=="CEILING":
            if col == 0:
                self.SetCellValue(row,2,ceilingLengthDic[self.GetCellValue(row, 0)])
                self.SetCellValue(row,4,CellingEnableThickDict[self.GetCellValue(row, 0)])
                self.SetCellValue(row,5,"m2")
                self.table.SetTypeName(1,CellingEnableSurfaceDict[self.GetCellValue(row, 0)])
                if self.GetCellValue(row,1) not in CellingEnableSurfaceDict[self.GetCellValue(row, 0)]:
                    self.SetCellValue(row,1,CellingEnableSurfaceDict[self.GetCellValue(row, 0)][0])
                self.table.SetTypeName(3,CellingEnableWidthDict[self.GetCellValue(row, 0)])
                if self.GetCellValue(row,3) not in CellingEnableWidthDict[self.GetCellValue(row, 0)]:
                    self.SetCellValue(row, 3, CellingEnableWidthDict[self.GetCellValue(row, 0)][0])
            # if col == 3:
            #     if self.GetCellValue(row,col) not in CellingEnableThicknessDict[self.GetCellValue(row,0)]:
            #         self.SetCellBackgroundColour(row,col,wx.RED)
            #         # self.SetCellValue(row,col,CellingEnableThicknessDict[self.GetCellValue(row,0)][0])
            #         wx.MessageBox("输入数据不合理，请重新输入","系统提示")
            #     else:
            #         self.SetCellBackgroundColour(row,col,wx.WHITE)
        elif self.type=="INTERIORDOOR":
            if col == 0:
                self.SetCellValue(row,2,interiorDoorHeightDic[self.GetCellValue(row, 0)])
                self.SetCellValue(row,3,interiorDoorWidthDic[self.GetCellValue(row, 0)])
                self.SetCellValue(row,4,"PCS")
                # self.table.SetTypeName(1, interiorDoorEnableSurfaceDict[self.GetCellValue(row, 0)])
            # if col == 3:
            #     if self.GetCellValue(row,col) not in CellingEnableThicknessDict[self.GetCellValue(row,0)]:
            #         self.SetCellBackgroundColour(row,col,wx.RED)
            #         # self.SetCellValue(row,col,CellingEnableThicknessDict[self.GetCellValue(row,0)][0])
            #         wx.MessageBox("输入数据不合理，请重新输入","系统提示")
            #     else:
            #         self.SetCellBackgroundColour(row,col,wx.WHITE)
        elif self.type=="FIREDOOR":
            if col == 0:
                self.table.SetTypeName(2,FireDoorEnableHeightDict[self.GetCellValue(row, 0)])
                self.table.SetTypeName(3,FireDoorEnableWidthDict[self.GetCellValue(row, 0)])
                if self.GetCellValue(row, 0) == "检修门(HB6 Inspection Door)":
                    self.SetCellValue(row,2,"≤1800")
                    self.SetCellValue(row,3,'≤800')
                    self.SetCellValue(row,4,'25')
                self.SetCellValue(row,5,"PCS")
            if col == 2:
                if self.GetCellValue(row, 0) == "检修口(Hatch)":
                    self.SetCellValue(row, 3, self.GetCellValue(row, 2))
                    self.SetCellValue(row, 4, "")
                else:
                    self.SetCellValue(row, 3, "≤1800")
                    self.SetCellValue(row, 4, "25")
        elif self.type=="WETUNIT":
            if col == 0:
                self.SetCellValue(row,5,"PCS")
        evt.Skip()

    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()


class DraftCheckFrame(wx.Frame):
    def __init__(self, parent, log, id, character):
        self.parent = parent
        self.log = log
        self.id = id
        self.character = character
        wx.Frame.__init__(
            self, parent, -1, "%s审核窗口 —— %05d" % (self.character[:-1], self.id), size=(1510, 800)
        )
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.Freeze()
        self.notebook = wx.Notebook(self, -1, size=(21, 21), style=
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
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.notebook, 1, wx.EXPAND)
        hhbox = wx.BoxSizer()
        saveBTN = wx.Button(self, -1, "保存", size=(100, 45))
        saveBTN.SetDefault()
        saveBTN.Bind(wx.EVT_BUTTON, self.OnSaveBTN)
        hhbox.Add(saveBTN, 1, wx.ALL, 10)
        saveExitBTN = wx.Button(self, -1, "保存并退出", size=(100, 45))
        saveExitBTN.Bind(wx.EVT_BUTTON, self.OnSaveExitBTN)
        hhbox.Add(saveExitBTN, 1, wx.ALL, 10)
        cancelBTN = wx.Button(self, -1, "取消", size=(100, 45))
        cancelBTN.Bind(wx.EVT_BUTTON, self.OnCancelBTN)
        hhbox.Add(cancelBTN, 1, wx.ALL, 10)
        vbox.Add(hhbox, 0, wx.EXPAND)
        self.SetSizer(vbox)
        self.Layout()
        self.wallCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.wallCheckPanel, "TNF Wall Panel")
        self.ceilingCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.ceilingCheckPanel, "TNF Ceiling Panel")
        self.interiorDoorCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.interiorDoorCheckPanel, "TNF Interior Door")
        self.wetUnitCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.wetUnitCheckPanel, "TNF Wet Unit")
        self.Thaw()

        # p = wx.Panel(self, -1, style=0)
        hbox = wx.BoxSizer()
        # if self.character=="技术员":
        #     self.wallPanelCheckGrid = WallPanelTechCheckGrid(self.wallCheckPanel, self.log, type="WALL", id=self.id)
        #     hbox.Add(self.wallPanelCheckGrid, 1, wx.EXPAND)
        # if self.character == "采购员":
        #     self.wallPanelCheckGrid = WallPanelOtherCheckGrid(self.wallCheckPanel, self.log, type="WALL", id=self.id,
        #                                                       character="采购员")
        #     hbox.Add(self.wallPanelCheckGrid, 1, wx.EXPAND)
        self.wallCheckPanel.SetSizer(hbox)
        self.wallCheckPanel.Layout()

    def OnSaveExitBTN(self, evt):
        error = self.Save()
        if not error:
            self.Close()
        evt.Skip()

    def OnCancelBTN(self, evt):
        del self.wallPanelCheckGrid
        self.Close()
        evt.Skip()

    def OnSaveBTN(self, evt):
        self.wallPanelCheckGrid.Destroy()
        self.Save()
        evt.Skip()

    def Save(self):
        # rowNum = self.wallPanelCheckGrid.table.GetNumberRows()
        # colNum = self.wallPanelCheckGrid.table.GetNumberCols()
        # data=[]
        # error=False
        # for i in range(rowNum-1):
        #     temp = ["WALL"]
        #     for j in range(colNum):
        #         temp.append(self.wallPanelCheckGrid.table.GetValue(i,j))
        #     data.append(temp)
        # self.wallDataDicList = self.MakeDicListData(data,"WALL")
        # for row,dics in enumerate(self.wallDataDicList):
        #     for col,section in enumerate(WallCheckEnableSectionList):
        #         if dics[section] == '':
        #             self.wallPanelCheckGrid.SetCellBackgroundColour(row,col,wx.Colour(255,200,200))
        #             self.wallPanelCheckGrid.Refresh()
        #             wx.MessageBox("'%s'字段不能为空！"%section,"信息提示")
        #             return True
        #         else:
        #             self.wallPanelCheckGrid.SetCellBackgroundColour(row,col,wx.Colour(255,255,255))
        #             self.wallPanelCheckGrid.Refresh()
        # UpdateDrafCheckInfoByID(self.log,WHICHDB,self.id,self.wallDataDicList)
        return False

    def MakeDicListData(self, data, type):
        dicList = []
        if type == "WALL":
            sectionList = copy.deepcopy(WallCheckEnableSectionList)
            sectionList.insert(0, "类别")
            dicList = [dict(zip(sectionList, row)) for row in data]
        return dicList


class TechCheckDialog(wx.Dialog):
    def __init__(self, parent, log, id, character):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.log = log
        self.id = id
        self.character = character
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "技术部审核对话框", pos=wx.DefaultPosition, size=(1350, 800))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self, size=(1350, 750))
        sizer.Add(self.panel, 1, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap("D:/IPMS/dist/bitmaps/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap("D:/IPMS/dist/bitmaps/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap("D:/IPMS/dist/bitmaps/33.png", wx.BITMAP_TYPE_PNG)
        btnSave = wx.Button(self, -1, "保存技术部审核数据", size=(200, 50))
        btnSave.SetBitmap(bitmap3, wx.LEFT)
        btnSave.Bind(wx.EVT_BUTTON, self.OnSaveBTN)
        btnSaveAndExit = wx.Button(self, wx.ID_OK, "完成技术部审核并退出", size=(200, 50))
        btnSaveAndExit.Bind(wx.EVT_BUTTON, self.OnSaveExitBTN)
        btnSaveAndExit.SetBitmap(bitmap1, wx.LEFT)
        btnCancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 50))
        btnCancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btnSave, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btnSaveAndExit, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btnCancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.ReCreate()

    def ReCreate(self):
        self.panel.Freeze()
        self.notebook = wx.Notebook(self.panel, -1, size=(21, 21), style=
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
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(vbox)
        self.panel.Layout()
        self.wallCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.wallCheckPanel, "TNF Wall Panel")
        self.ceilingCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.ceilingCheckPanel, "TNF Ceiling Panel")
        self.interiorDoorCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.interiorDoorCheckPanel, "TNF Interior Door")
        self.fireDoorCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.fireDoorCheckPanel, "TNF Hatch")
        self.wetUnitCheckPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.wetUnitCheckPanel, "TNF Wet Unit")
        self.panel.Thaw()

        hbox = wx.BoxSizer()
        self.wallPanelCheckGrid = WallPanelTechCheckGrid(self.wallCheckPanel, self.log, type="WALL", id=self.id)
        hbox.Add(self.wallPanelCheckGrid, 1, wx.EXPAND)
        self.wallCheckPanel.SetSizer(hbox)
        self.wallCheckPanel.Layout()
        hbox = wx.BoxSizer()
        self.ceilingPanelCheckGrid = WallPanelTechCheckGrid(self.ceilingCheckPanel, self.log, type="CEILING", id=self.id)
        hbox.Add(self.ceilingPanelCheckGrid, 1, wx.EXPAND)
        self.ceilingCheckPanel.SetSizer(hbox)
        self.ceilingCheckPanel.Layout()
        hbox = wx.BoxSizer()
        self.interiorDoorCheckGrid = WallPanelTechCheckGrid(self.interiorDoorCheckPanel, self.log, type="INTERIORDOOR", id=self.id)
        hbox.Add(self.interiorDoorCheckGrid, 1, wx.EXPAND)
        self.interiorDoorCheckPanel.SetSizer(hbox)
        self.interiorDoorCheckPanel.Layout()
        hbox = wx.BoxSizer()
        self.fireDoorCheckGrid = WallPanelTechCheckGrid(self.fireDoorCheckPanel, self.log, type="FIREDOOR", id=self.id)
        hbox.Add(self.fireDoorCheckGrid, 1, wx.EXPAND)
        self.fireDoorCheckPanel.SetSizer(hbox)
        self.fireDoorCheckPanel.Layout()
        hbox = wx.BoxSizer()
        self.wetUnitCheckGrid = WallPanelTechCheckGrid(self.wetUnitCheckPanel, self.log, type="WETUNIT", id=self.id)
        hbox.Add(self.wetUnitCheckGrid, 1, wx.EXPAND)
        self.wetUnitCheckPanel.SetSizer(hbox)
        self.wetUnitCheckPanel.Layout()

    def OnSaveExitBTN(self, evt):
        error = self.Save()
        if not error:
            evt.Skip()

    def OnSaveBTN(self, evt):
        self.Save()
        evt.Skip()

    def Save(self):
        data = []
        error = False
        rowNum = self.wallPanelCheckGrid.table.GetNumberRows()
        colNum = self.wallPanelCheckGrid.table.GetNumberCols()
        square = 0
        for i in range(rowNum - 1):
            temp = ["WALL"]
            if self.wallPanelCheckGrid.table.GetValue(i, 6):
                square += float(self.wallPanelCheckGrid.table.GetValue(i, 6))
            for j in range(colNum):
                res = self.wallPanelCheckGrid.table.GetValue(i, j)
                if j in [7,8]:#这里的7，8两列分别对应潮湿和加强的两列数据
                    res = 'Y' if res else 'N'
                temp.append(res)
            data.append(temp)
        self.wallDataDicList = []
        wallDataDicList = self.MakeDicListData(data, "WALL")
        for row, dics in enumerate(wallDataDicList):
            if dics['数量'] != 0:
                for col, section in enumerate(WallCheckEnableSectionList):
                    if dics[section] == '':  # 这说明有字段输入值为空
                        if section == '单位':
                            dics[col]=='m2'
                        elif section != "产品描述" and section != '数量':  # 如果为空的字段不是产品描述的话
                            self.notebook.SetSelection(0)  # 调到墙板页面，因为这是检查的是墙板数据
                            self.wallPanelCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 200, 200))
                            self.wallPanelCheckGrid.Refresh()
                            wx.MessageBox("'%s'字段不能为空！" % section, "信息提示")
                            return True
                    else:
                        self.wallPanelCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 255, 255))
                        self.wallPanelCheckGrid.Refresh()
                self.wallDataDicList.append(dics)

        rowNum = self.ceilingPanelCheckGrid.table.GetNumberRows()
        colNum = self.ceilingPanelCheckGrid.table.GetNumberCols()
        data = []
        for i in range(rowNum - 1):
            temp = ["CEILING"]
            square += float(self.ceilingPanelCheckGrid.table.GetValue(i, 6))
            for j in range(colNum):
                temp.append(self.ceilingPanelCheckGrid.table.GetValue(i, j))
            data.append(temp)
        self.ceilingDataDicList = []
        ceilingDataDicList = self.MakeDicListData(data, "CEILING")
        for row, dics in enumerate(ceilingDataDicList):
            if dics["数量"]!=0:
                for col, section in enumerate(CeilingCheckEnableSectionList):
                    if dics[section] == '':
                        if section != "产品描述" and section != '数量':
                            self.notebook.SetSelection(1)
                            self.ceilingPanelCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 200, 200))
                            self.ceilingPanelCheckGrid.Refresh()
                            wx.MessageBox("'%s'字段不能为空！" % section, "信息提示")
                            return True
                    else:
                        self.ceilingPanelCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 255, 255))
                        self.ceilingPanelCheckGrid.Refresh()
                self.ceilingDataDicList.append(dics)

        rowNum = self.interiorDoorCheckGrid.table.GetNumberRows()
        colNum = self.interiorDoorCheckGrid.table.GetNumberCols()
        data = []
        for i in range(rowNum - 1):
            temp = ["INTERIORDOOR"]
            # square += float(self.interiorDoorPanelCheckGrid.table.GetValue(i, 5))
            for j in range(colNum):
                temp.append(self.interiorDoorCheckGrid.table.GetValue(i, j))
            data.append(temp)
        self.interiorDoorDataDicList = []
        interiorDoorDataDicList = self.MakeDicListData(data, "INTERIORDOOR")
        for row, dics in enumerate(interiorDoorDataDicList):
            if dics['数量']!=0:
                for col, section in enumerate(InteriorDoorCheckEnableSectionList):
                    if dics[section] == '':
                        if section == '单位':
                            dics[col]='PCS'
                        elif section != "产品描述" and section != '数量':
                            self.notebook.SetSelection(2)
                            self.interiorDoorCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 200, 200))
                            self.interiorDoorCheckGrid.Refresh()
                            wx.MessageBox("'%s'字段不能为空！" % section, "信息提示")
                            return True
                    else:
                        self.interiorDoorCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 255, 255))
                        self.interiorDoorCheckGrid.Refresh()
                self.interiorDoorDataDicList.append(dics)

        rowNum = self.fireDoorCheckGrid.table.GetNumberRows()
        colNum = self.fireDoorCheckGrid.table.GetNumberCols()
        data = []
        for i in range(rowNum - 1):
            temp = ["FIREDOOR"]
            # square += float(self.interiorDoorPanelCheckGrid.table.GetValue(i, 5))
            for j in range(colNum):
                temp.append(self.fireDoorCheckGrid.table.GetValue(i, j))
            data.append(temp)
        self.fireDoorDataDicList = []
        fireDoorDataDicList = self.MakeDicListData(data, "FIREDOOR")
        for row, dics in enumerate(fireDoorDataDicList):
            if dics['数量']!=0:
                for col, section in enumerate(FireDoorCheckEnableSectionList):
                    if dics[section] == '':
                        if section != "产品描述" and section!="产品厚度" and section != '数量':
                            self.notebook.SetSelection(3)
                            self.fireDoorCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 200, 200))
                            self.fireDoorCheckGrid.Refresh()
                            wx.MessageBox("'%s'字段不能为空！" % section, "信息提示")
                            return True
                    else:
                        self.fireDoorCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 255, 255))
                        self.fireDoorCheckGrid.Refresh()
                self.fireDoorDataDicList.append(dics)

        rowNum = self.wetUnitCheckGrid.table.GetNumberRows()
        colNum = self.wetUnitCheckGrid.table.GetNumberCols()
        data = []
        for i in range(rowNum - 1):
            temp = ["WETUNIT"]
            # square += float(self.interiorDoorPanelCheckGrid.table.GetValue(i, 5))
            for j in range(colNum):
                temp.append(self.wetUnitCheckGrid.table.GetValue(i, j))
            data.append(temp)
        self.wetUnitDataDicList = []
        wetUnitDataDicList = self.MakeDicListData(data, "WETUNIT")
        for row, dics in enumerate(wetUnitDataDicList):
            if dics["数量"]!=0:
                for col, section in enumerate(WetUnitCheckEnableSectionList):
                    if dics[section] == '':
                        if section != "产品描述" and section!="产品表面材料" and section!="产品长度" and section!="产品宽度" and section!="产品厚度" and section != '数量':
                            self.notebook.SetSelection(4)
                            self.wetUnitCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 200, 200))
                            self.wetUnitCheckGrid.Refresh()
                            wx.MessageBox("'%s'字段不能为空！" % section, "信息提示")
                            return True
                    else:
                        self.wetUnitCheckGrid.SetCellBackgroundColour(row, col, wx.Colour(255, 255, 255))
                        self.wetUnitCheckGrid.Refresh()
                self.wetUnitDataDicList.append(dics)
        self.wallDataDicList = self.wallDataDicList + self.ceilingDataDicList + self.interiorDoorDataDicList + self.fireDoorDataDicList + self.wetUnitDataDicList
        UpdateDraftCheckInfoByID(self.log, WHICHDB, self.id, self.wallDataDicList)
        UpdateOrderSquareByID(self.log, WHICHDB, self.id, square)
        return False

    def MakeDicListData(self, data, type):
        dicList = []
        if type in ["WALL", 'CEILING','INTERIORDOOR','FIREDOOR','WETUNIT']:
            if type == "WALL":
                sectionList = copy.deepcopy(WallCheckEnableSectionList)
            elif type == "CEILING":
                sectionList = copy.deepcopy(CeilingCheckEnableSectionList)
            elif type == "INTERIORDOOR":
                sectionList = copy.deepcopy(InteriorDoorCheckEnableSectionList)
            elif type == "FIREDOOR":
                sectionList = copy.deepcopy(FireDoorCheckEnableSectionList)
            elif type == "WETUNIT":
                sectionList = copy.deepcopy(WetUnitCheckEnableSectionList)
            sectionList.insert(0, "类别")
            dicList = [dict(zip(sectionList, row)) for row in data]
        return dicList


class WallPanelCheckDataTable(gridlib.GridTableBase):
    def __init__(self, log, type, data):
        gridlib.GridTableBase.__init__(self)
        self.log = log
        self.type = type

        self.colLabels = CheckTitleDict[self.type]

        if self.type == 'WALL':
            self.dataTypes = [
                gridlib.GRID_VALUE_CHOICE + ':TNF-4SF,TNF-4SA,TNF-3SF,TNF-3SA,TNF-2SF,TNF-2SA,TNF-2SG,TNF-2SD',
                # gridlib.GRID_VALUE_CHOICE + ':B15 Lining,B15 HNR,B15 Partition',
                gridlib.GRID_VALUE_CHOICE + ':CP/G,GP/G,S.S/G,S.S/S.S',
                gridlib.GRID_VALUE_CHOICE + ':≤2500',
                gridlib.GRID_VALUE_CHOICE + ':≤600,>600',
                gridlib.GRID_VALUE_STRING,
                gridlib.GRID_VALUE_CHOICE + ':m2',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_BOOL,
                gridlib.GRID_VALUE_BOOL,
                gridlib.GRID_VALUE_FLOAT + ':6,2',
            ]
        elif self.type == 'CEILING':
            self.dataTypes = [
                gridlib.GRID_VALUE_CHOICE + ':TNF-C46,TNF-C55,TNF-C64,TNF-C65,TNF-C68,TNF-C70,TNF-C71,TNF-C72,TNF-C73',
                # gridlib.GRID_VALUE_CHOICE + ':B15',
                gridlib.GRID_VALUE_CHOICE + ':PVC,S.S(304),PVC/G,S.S(304)/G',
                gridlib.GRID_VALUE_CHOICE + ':≤3000,600',
                gridlib.GRID_VALUE_CHOICE + ':600,300,275',
                gridlib.GRID_VALUE_CHOICE + ':40,50,70,100',
                gridlib.GRID_VALUE_CHOICE + ':m2',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_STRING,
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
            ]
        elif self.type == 'INTERIORDOOR':
            temp = []
            for row in data:
                row = row[:4]+row[5:]
                temp.append(row)
            data=temp
            self.dataTypes = [
                gridlib.GRID_VALUE_CHOICE + ':TNF-A60ZF-S001,TNF-A60BF-A60-01,TNF-SA60BF-A60-01,TNF-B15BF-001,TNF-SB15BF-S001,TNF-B15ZF-HNR-01,TNF-B15ZF-01',
                # gridlib.GRID_VALUE_CHOICE + ':TNF-A60ZF-S001, TNF-A60BF-A60-01, TNF-B15BF-001',
                gridlib.GRID_VALUE_CHOICE + ':painted/G,S.S(304)/G',
                gridlib.GRID_VALUE_CHOICE + ':2000,2100,2200',
                gridlib.GRID_VALUE_CHOICE + ':1000,1050,1100,2100',
                gridlib.GRID_VALUE_CHOICE + ':PCS',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_CHOICE + ':40,50,70,100',
                gridlib.GRID_VALUE_STRING,
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
            ]
        elif self.type == 'FIREDOOR':
            self.dataTypes = [
                gridlib.GRID_VALUE_CHOICE + ':检修口(Hatch),检修门(HB6 Inspection Door)',
                # gridlib.GRID_VALUE_CHOICE + ':TNF-A60ZF-S001, TNF-A60BF-A60-01, TNF-B15BF-001',
                gridlib.GRID_VALUE_CHOICE + ':PVC,S.S(304)',
                gridlib.GRID_VALUE_CHOICE + ':≤300,400-600,>600,MAX 18000',
                gridlib.GRID_VALUE_CHOICE + ':≤300,400-600,>600,MAX 800',
                gridlib.GRID_VALUE_CHOICE + ':25',
                gridlib.GRID_VALUE_CHOICE + ':PCS',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_STRING,
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
            ]
        elif self.type == 'WETUNIT':
            self.dataTypes = [
                gridlib.GRID_VALUE_CHOICE + ':TYPE-1-L/1-R',
                # gridlib.GRID_VALUE_CHOICE + ':TNF-A60ZF-S001, TNF-A60BF-A60-01, TNF-B15BF-001',
                gridlib.GRID_VALUE_CHOICE + ':PVC,S.S(304)',
                gridlib.GRID_VALUE_CHOICE + ':≤300,400-600,>600,MAX 18000',
                gridlib.GRID_VALUE_CHOICE + ':≤300,400-600,>600,MAX 800',
                gridlib.GRID_VALUE_CHOICE + ':25',
                gridlib.GRID_VALUE_CHOICE + ':PCS',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_STRING,
                gridlib.GRID_VALUE_FLOAT + ':6,2',
                gridlib.GRID_VALUE_FLOAT + ':6,2',
            ]
        self.data = data

    # --------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        return len(self.data) + 1

    def GetNumberCols(self):
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)

                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,  # The table
                                               gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED,  # what we did to it
                                               1  # how many
                                               )

                self.GetView().ProcessTableMessage(msg)

        innerSetValue(row, col, value)

    # --------------------------------------------------
    # Some optional methods

    # Called when the grid needs to display labels
    def GetColLabelValue(self, col):
        return self.colLabels[col]

    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    def SetTypeName(self, col,list):
        temp=':'
        for item in list:
            temp += '%s,'%item
        self.dataTypes[col] = gridlib.GRID_VALUE_CHOICE + temp
    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)


class CreateNewOrderDialog(wx.Dialog):
    def __init__(self, parent, log, charactor, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.log = log
        self.charactor = charactor
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "新建订单对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.propertyPanel = DraftOrderPanel(self, self.parent.work_zone_Panel.orderManagementPanel, self.log,
                                             size=(600, 600), character=self.charactor)
        sizer.Add(self.propertyPanel, 1, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap("D:/IPMS/dist/bitmaps/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap("D:/IPMS/dist/bitmaps/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap("D:/IPMS/dist/bitmaps/33.png", wx.BITMAP_TYPE_PNG)
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

        btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)

    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()

    def OnOk(self, event):
        d = self.propertyPanel.pg.GetPropertyValues(inc_attributes=True)
        self.propertyDic = {}
        for k, v in d.items():
            if "产品清单或图纸文件" in k:
                temp = str(v)
                v = temp.replace('\\','/')
            self.propertyDic[k] = v

        operatorID = self.parent.parent.operatorID
        for key in self.propertyDic.keys():
            if self.propertyDic[key] == "" and '*' in key:
                wx.MessageBox("%s不能为空，请重新输入！" % key)
                return
            if self.propertyDic[key] == 1 and key == '2.草稿订单类别' and self.propertyDic['1.产品清单或图纸文件'] == '':
                wx.MessageBox("%s不能为空，请重新输入！" % key)
                return
        startDate = wxdate2pydate(self.propertyDic["8.下单日期"])
        endDate = wxdate2pydate(self.propertyDic["1.投标日期"])
        delta = (endDate - startDate).days
        if delta < 5:
            wx.MessageBox("投标日期与下单日期太近，请修改后再试！")
            return
        result = InsertNewOrder(self.log, WHICHDB, self.propertyDic, operatorID)
        if result<0:
            wx.MessageBox("存储出错，请检查后重试！","系统提示")
        else:
            wx.MessageBox("操作成功！")
        event.Skip()


class TechDrawingButtonEditor(wxpg.PGTextCtrlEditor):
    def __init__(self):
        wxpg.PGTextCtrlEditor.__init__(self)
        self.fileData = []

    def LoadFileData(self):
        message = "正在从数据库中读取数据，请稍候..."
        busy = PBI.PyBusyInfo(message, parent=None, title="系统忙。。。",
                              icon=images.Smiles.GetBitmap())
        wx.Yield()
        self.fileData = GetTechDrawingDataByID(None, WHICHDB, self.id,self.fileName)
        del busy

    def CreateControls(self, propGrid, property, pos, sz):
        tempList = property.GetValue().split('.')
        self.fileType = tempList[-1]
        self.fileName=""
        for i in tempList[1:-1]:
            self.fileName += i
            self.fileName += '.'
        self.fileName += tempList[-1]
        self.id = tempList[0]
        # self.fileData = GetTechDrawingDataByID(None,WHICHDB,self.id)
        # Create and populate buttons-subwindow
        buttons = wxpg.PGMultiButton(propGrid, sz)
        # Add two regular buttons
        buttons.AddButton("...")
        buttons.AddButton("A")
        # Add a bitmap button
        buttons.AddBitmapButton(wx.ArtProvider.GetBitmap(wx.ART_FOLDER))

        # Create the 'primary' editor control (textctrl in this case)
        wnd = super(TechDrawingButtonEditor, self).CreateControls(
            propGrid,
            property,
            pos,
            buttons.GetPrimarySize())
        wnd = wnd.GetPrimary()
        # Finally, move buttons-subwindow to correct position and make sure
        # returned wxPGWindowList contains our custom button list.
        buttons.Finalize(propGrid, pos)

        # We must maintain a reference to any editor objects we created
        # ourselves. Otherwise they might be freed prematurely. Also,
        # we need it in OnEvent() below, because in Python we cannot "cast"
        # result of wxPropertyGrid.GetEditorControlSecondary() into
        # PGMultiButton instance.
        self.buttons = buttons

        return wxpg.PGWindowList(wnd, buttons)

    def OnEvent(self, propGrid, prop, ctrl, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            buttons = self.buttons
            evtId = event.GetId()
            if evtId == buttons.GetButtonId(0):
                # Do something when the first button is pressed
                wx.LogDebug("First button pressed")
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(1):
                # Do something when the second button is pressed
                if self.fileType == "pdf":
                    self.LoadFileData()
                    with open("temp.pdf", 'wb') as fp:
                        fp.write(self.fileData)
                        fp.close()
                    dlg = wx.Dialog(None, title="技术图纸", size=(1800, 1000))
                    BluePrintShowPanel(dlg, None, "temp.pdf")
                    dlg.CenterOnScreen()
                    dlg.ShowModal()
                    dlg.Destroy()
                else:
                    wx.MessageBox("文件不是pdf格式，无法在系统中打开。请在Windows中使用专门的编辑软件查看文件内容！","系统提示")
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(2):
                # Do something when the third button is pressed
                self.LoadFileData()
                dlg = wx.DirDialog(None, "Choose a directory:",
                                   style=wx.DD_DEFAULT_STYLE
                                   # | wx.DD_DIR_MUST_EXIST
                                   # | wx.DD_CHANGE_DIR
                                   )

                # If the user selects OK, then we process the dialog's data.
                # This is done by getting the path data from the dialog - BEFORE
                # we destroy it.
                if dlg.ShowModal() == wx.ID_OK:
                    with open(dlg.GetPath() + "\\" + self.fileName, 'wb') as fp:
                        fp.write(self.fileData)
                        fp.close
                    wx.MessageBox("技术图纸已存储于%s" % (dlg.GetPath() + "\\" + self.fileName), "信息提示")
                # Only destroy a dialog after you're done with it.
                dlg.Destroy()
                return False  # Return false since value did not change

        return super(TechDrawingButtonEditor, self).OnEvent(propGrid, prop, ctrl, event)


class QuotationSheetDialog(wx.Dialog):
    def __init__(self, parent, master, log, id, character, name="进行订单部审核",orderName=''):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.master = master
        self.orderName = orderName
        self.log = log
        self.id = id
        self.character = character
        self.priceDataDic = self.parent.priceDataDic
        self.name = name
        self.quotationRange = "国内报价"
        quotationDate = None
        exchangeDate = None
        self.quotationDate = None
        self.exchangeDate = None
        self.currencyName = '人民币'
        self.exchangeRateDic = {}
        for record in self.parent.master.dataList:
            if record[0]==self.id:
                quotationDate = record[-3] if record[-3]!='None' and record[-3]!='' else str(datetime.date.today())
                exchangeDate = record[-2] if record[-2]!='None' and record[-2]!=''else str(datetime.date.today())
                quotationDate = quotationDate.split('-')
                self.quotationDate = datetime.date(int(quotationDate[0]), int(quotationDate[1]), int(quotationDate[2]))
                exchangeDate = exchangeDate.split('-')
                self.exchangeDate = datetime.date(int(exchangeDate[0]), int(exchangeDate[1]), int(exchangeDate[2]))
                self.currencyName = record[-1] if record[-1] else '人民币'
                break
        # quotationDate, exchangeDate = GetQuotationDateAndExchangeDateFromDB(self.log, WHICHDB, self.id)
        if not quotationDate:
            self.quotationDate = datetime.date.today() - datetime.timedelta(1)
        # else:
        #     quotationDate = quotationDate.split('-')
        #     self.quotationDate = datetime.date(int(quotationDate[0]), int(quotationDate[1]), int(quotationDate[2]))
        if not self.exchangeDate:
            self.exchangeDate = datetime.date.today() - datetime.timedelta(1)
        # else:
        #     exchangeDate = exchangeDate.split('-')
        #     self.exchangeDate = datetime.date(int(exchangeDate[0]), int(exchangeDate[1]), int(exchangeDate[2]))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        if self.character in ["项目经理",'订单管理员']:
            title = "订单部审核对话框"
        elif self.character in ['经理','副总经理']:
            title = "经理审核对话框"
        self.Create(parent, -1, title, pos=wx.DefaultPosition, size=(1900, 900))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.controlPanel = wx.Panel(self, size=(1900, 50))
        sizer.Add(self.controlPanel, 0, wx.EXPAND)
        self.gridPanel = wx.Panel(self, size=(1900, 750))
        sizer.Add(self.gridPanel, 1, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap("D:/IPMS/dist/bitmaps/pdf.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap("D:/IPMS/dist/bitmaps/excel.png", wx.BITMAP_TYPE_PNG)
        # bitmap3 = wx.Bitmap("D:/IPMS/dist/bitmaps/33.png", wx.BITMAP_TYPE_PNG)
        if self.character in ["项目经理",'订单管理员'] and self.name == "生成报价单":
            createPdfQuotationSheetBTN = wx.Button(self, -1, "生成pdf报价单", size=(200, 50))
            createPdfQuotationSheetBTN.SetBitmap(bitmap1, wx.LEFT)
            createPdfQuotationSheetBTN.Bind(wx.EVT_BUTTON, self.OnCreatePdfQuotationSheetBTN)
            btnsizer.Add((40, -1), 0)
            btnsizer.Add(createPdfQuotationSheetBTN, 0)
            createExcelQuotationSheetBTN = wx.Button(self, -1, "生成Excel报价单", size=(200, 50))
            createExcelQuotationSheetBTN.SetBitmap(bitmap2, wx.LEFT)
            createExcelQuotationSheetBTN.Bind(wx.EVT_BUTTON, self.OnCreateExcelQuotationSheetBTN)
            btnsizer.Add((40, -1), 0)
            btnsizer.Add(createExcelQuotationSheetBTN, 0)
        if self.character in ["项目经理",'订单管理员']:
            label = "完成订单部审核并退出"
        else:
            label = "完成经理审核并退出"
        btnSaveAndExit = wx.Button(self, wx.ID_OK, label, size=(200, 50))
        if self.name == '生成报价单':
            btnSaveAndExit.Show(False)
        btnSaveAndExit.Bind(wx.EVT_BUTTON, self.OnSaveExitBTN)
        # btnSaveAndExit.SetBitmap(bitmap1, wx.LEFT)
        btnCancel = wx.Button(self, wx.ID_CANCEL, "返  回", size=(200, 50))
        # btnCancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btnSaveAndExit, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btnCancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.CreateControlPanel()
        self.editAnnotationdlg = EditAnnotationDialog(self,self.log,self.id)
        self.editAnnotationdlg.CenterOnScreen()
        self.CreateGrid()
        # self.ReCreateGrid()
    def OnCreateExcelQuotationSheetBTN(self, event):
        filename = quotationSheetDir + '报价单%05d.xlsx' % self.id
        totalRowNumber = 8+12 + len(self.quotationSheetGrid.dataWall)+6 + len(self.quotationSheetGrid.dataCeiling)+6\
                     + len(self.quotationSheetGrid.dataInteriorDoor) + 6 + len(self.quotationSheetGrid.dataFireDoor)\
                     + 6 + len(self.quotationSheetGrid.dataWetUnit) + 6
        dataExcel = []
        for row in range(totalRowNumber):
            rowData = []
            for col in range(13):
                rowData.append(self.quotationSheetGrid.GetCellValue(row,col))
            dataExcel.append(rowData)
        dataExcel = np.array(dataExcel)
        data_df = pd.DataFrame(dataExcel)
        data_df.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J','K','L','M']
        data_df.index = [i+1 for i in range(totalRowNumber)]
        writer = pd.ExcelWriter(filename)
        data_df.to_excel(writer)
        writer.save()
        wx.MessageBox("Excel格式报价单：%s已生成，\r\n您可以使用Excel进行查看和编辑."%filename,"信息提示窗口")

    def OnCreatePdfQuotationSheetBTN(self, event):
        annotation = self.quotationSheetGrid.GetAnnotation()
        # UpdateOrderAnnotation(self.log, WHICHDB, self.id, annotation)
        filename = quotationSheetDir + '报价单%05d.pdf' % self.id
        # self.log.WriteText("here1" + filename)
        dataWall = self.quotationSheetGrid.GetWallData()
        dataCeiling = self.quotationSheetGrid.GetCeilingData()
        dataInteriorDoor = self.quotationSheetGrid.GetInteriorDoorData()
        dataFireDoor = self.quotationSheetGrid.GetFireDoorData()
        dataWetUnit = self.quotationSheetGrid.GetWetUnitData()
        # dataNoteText = self.quotationSheetGrid.GetNoteText()
        # print(dataNoteText)
        dataNoteText = annotation
        MakeQuotationSheetTemplate(filename, dataWall, dataCeiling, dataInteriorDoor,dataFireDoor,dataWetUnit,dataNoteText,log=self.log, currencyName=self.currencyName)
        dlg = QuotationSheetViewDialog(self, self.log, filename)
        dlg.CenterOnScreen()
        dlg.ShowModal()
        dlg.Close()
        # self.Close()

    def OnSaveExitBTN(self, event):
        sumupPrice = float(self.quotationSheetGrid.wallSumupPricesRMB) + float(self.quotationSheetGrid.ceilingSumupPricesRMB)\
                     + float(self.quotationSheetGrid.interiorDoorSumupPricesRMB)+float(self.quotationSheetGrid.fireDoorSumupPricesRMB)\
                     + float(self.quotationSheetGrid.wetUnitSumupPricesRMB)
        # annotation = self.quotationSheetGrid.GetAnnotation()
        if self.character in ["项目经理",'订单管理员','副总经理']:
            dicList = self.quotationSheetGrid.dataWall + self.quotationSheetGrid.dataCeiling + self.quotationSheetGrid.dataInteriorDoor\
                      + self.quotationSheetGrid.dataFireDoor + self.quotationSheetGrid.dataWetUnit
            UpdateDraftOrderInDB(self.log, WHICHDB, self.id, dicList)
            # UpdateOrderAnnotation(self.log,WHICHDB,self.id,annotation)
            # temp = GetOrderAnnotation(self.log,WHICHDB,self.id)
            # ann=["","",""]
            # for i,item in enumerate(temp[:3]):
            #     ann[i]=item
            # print(ann)
            if self.character in ["项目经理",'订单管理员']:
                UpdateOrderOperatorCheckStateByID(self.log, WHICHDB, self.id, 'Y', str(self.quotationDate),
                                                  str(self.exchangeDate), self.currencyName, str(sumupPrice))
            elif self.character in ["副总经理"]:
                UpdateManagerCheckStateByID(self.log, WHICHDB, self.id, 'Y', self.quotationDate, self.exchangeDate)
        self.Close()

    def CreateControlPanel(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add((20, -1))
        hhbox.Add(wx.StaticText(self.controlPanel, label="请选择报价日期："), 0, wx.TOP, 15)
        self.quotationDateCtrl = wx.adv.DatePickerCtrlGeneric(self.controlPanel, size=(135, -1),
                                                              style=wx.adv.DP_DROPDOWN
                                                                    | wx.adv.DP_SHOWCENTURY
                                                                    | wx.adv.DP_ALLOWNONE)
        self.quotationDateCtrl.SetValue(self.quotationDate)
        hhbox.Add(self.quotationDateCtrl, 0, wx.TOP, 10)
        hhbox.Add((10, -1))
        hhbox.Add(wx.StaticLine(self.controlPanel, style=wx.VERTICAL), 0, wx.EXPAND)
        hhbox.Add((10, -1))
        hhbox.Add(wx.StaticText(self.controlPanel, label="请选择汇率日期："), 0, wx.TOP, 15)
        self.exchangeDateCtrl = wx.adv.DatePickerCtrlGeneric(self.controlPanel, size=(135, -1),
                                                             style=wx.adv.DP_DROPDOWN
                                                                   | wx.adv.DP_SHOWCENTURY
                                                                   | wx.adv.DP_ALLOWNONE)
        self.exchangeDateCtrl.SetValue(self.exchangeDate)
        hhbox.Add(self.exchangeDateCtrl, 0, wx.TOP, 10)
        hhbox.Add((10, -1))
        hhbox.Add(wx.StaticText(self.controlPanel, label="报价币种："), 0, wx.TOP, 15)
        if self.currencyName != "人民币":
            self.exchangeDateCtrl.Enable(True)
        else:
            self.exchangeDateCtrl.Enable(False)
        self.currencyNameCOMBO = wx.ComboBox(self.controlPanel, value=self.currencyName, size=(100, -1),choices=["人民币",'美元','英镑','欧元','日元','卢布'])
        self.currencyNameCOMBO.Bind(wx.EVT_COMBOBOX, self.OnCurrencyNameChanged)
        hhbox.Add(self.currencyNameCOMBO,0,wx.TOP,10)
        hhbox.Add((10,-1))
        self.exchangeRateTXT = wx.TextCtrl(self.controlPanel, size=(80,-1), style=wx.TE_READONLY)
        for i in range(10):
            if not self.parent.master.exChangeRateDic:
                wx.Sleep(1)
            else:
                break
        self.exchangeRate=None
        if self.parent.master.exChangeRateDic:
            for item in self.parent.master.exChangeRateDic:
                if self.exchangeDate == item['日期']:
                    self.exchangeRateDic = item
                    self.exchangeRate = self.exchangeRateDic[self.currencyName]
                    break
        if not self.exchangeRate:
            self.exchangeRateDic = self.parent.master.exChangeRateDic[-1]
            self.exchangeRate = self.exchangeRateDic[self.currencyName]
            #这块儿应加入把新值插入汇率数据库的操作
        self.exchangeRateTXT.SetValue(self.exchangeRate)
        hhbox.Add(self.exchangeRateTXT, 0, wx.TOP,10)
        hhbox.Add((10, -1))
        hhbox.Add(wx.StaticLine(self.controlPanel, style=wx.VERTICAL), 0, wx.EXPAND)
        hhbox.Add((10, -1))
        self.quotationRangeCtrl = wx.ComboBox(self.controlPanel,value=self.quotationRange,size=(135, -1),choices=['国内报价','国外报价'])
        self.quotationRangeCtrl.Bind(wx.EVT_COMBOBOX,self.OnQuotationRangeChanged)
        hhbox.Add(self.quotationRangeCtrl, 0, wx.TOP, 10)
        hhbox.Add((10, -1))
        hhbox.Add(wx.StaticLine(self.controlPanel, style=wx.VERTICAL), 0, wx.EXPAND)
        hhbox.Add((10, -1))
        self.addNoteButton = wx.Button(self.controlPanel,label="编辑格式备注",size=(135,30))
        self.addNoteButton.SetBackgroundColour(wx.Colour(100,255,100))
        self.addNoteButton.Bind(wx.EVT_BUTTON, self.OnAddNoteButton)
        hhbox.Add(self.addNoteButton,0, wx.TOP, 10)
        # hhbox.Add((10, -1))
        # self.addNoteButton1 = wx.Button(self.controlPanel,label="编辑自定义备注1",size=(135,30))
        # self.addNoteButton1.Bind(wx.EVT_BUTTON, self.OnAddNoteButton1)
        # hhbox.Add(self.addNoteButton1,0, wx.TOP, 10)
        # hhbox.Add((10, -1))
        # self.addNoteButton2 = wx.Button(self.controlPanel,label="编辑自定义备注2",size=(135,30))
        # self.addNoteButton2.Bind(wx.EVT_BUTTON, self.OnAddNoteButton2)
        # hhbox.Add(self.addNoteButton2,0, wx.TOP, 10)
        # hhbox.Add((10, -1))
        # self.addNoteButton3 = wx.Button(self.controlPanel,label="编辑自定义备注3",size=(135,30))
        # self.addNoteButton3.Bind(wx.EVT_BUTTON, self.OnAddNoteButton3)
        # hhbox.Add(self.addNoteButton3,0, wx.TOP, 10)
        vbox.Add(hhbox, 1, wx.EXPAND)
        self.controlPanel.SetSizer(vbox)
        self.quotationDateCtrl.Bind(wx.adv.EVT_DATE_CHANGED, self.OnQuotationDateChanged)
        self.exchangeDateCtrl.Bind(wx.adv.EVT_DATE_CHANGED, self.OnExchangeRatDateChanged)
        if self.name == "生成报价单":
            self.quotationDateCtrl.Enable(False)
            self.exchangeDateCtrl.Enable(False)

    def OnAddNoteButton(self,event):
        if self.editAnnotationdlg.ShowModal() == wx.ID_OK:
            self.quotationSheetGrid.RefreshAnnotation()
        self.editAnnotationdlg.Close()

    def OnAddNoteButton1(self,event):
        dlg = wx.TextEntryDialog(
            self, '请输入备注的中/英文信息',
            '信息输入', '')
        dlg.SetValue(self.quotationSheetGrid.annotationList[0])
        if dlg.ShowModal() == wx.ID_OK:
            self.quotationSheetGrid.SetNoteValue(0,dlg.GetValue())
        dlg.Destroy()

    def OnAddNoteButton2(self,event):
        dlg = wx.TextEntryDialog(
            self, '请输入备注的中/英文信息',
            '信息输入', '')
        dlg.SetValue(self.quotationSheetGrid.annotationList[1])
        if dlg.ShowModal() == wx.ID_OK:
            self.quotationSheetGrid.SetNoteValue(1,dlg.GetValue())
        dlg.Destroy()

    def OnAddNoteButton3(self,event):
        dlg = wx.TextEntryDialog(
            self, '请输入备注的中/英文信息',
            '信息输入', '')
        dlg.SetValue(self.quotationSheetGrid.annotationList[2])
        if dlg.ShowModal() == wx.ID_OK:
            self.quotationSheetGrid.SetNoteValue(2,dlg.GetValue())
        dlg.Destroy()

    def OnCurrencyNameChanged(self,event):
        if self.currencyName != self.currencyNameCOMBO.GetValue():
            self.currencyName = self.currencyNameCOMBO.GetValue()
            if self.currencyName != "人民币" and self.name !='生成报价单':
                self.exchangeDateCtrl.Enable(True)
            else:
                self.exchangeDateCtrl.Enable(False)
            self.exchangeRate = self.exchangeRateDic[self.currencyName]
            self.exchangeRateTXT.SetValue(str(self.exchangeRate))
            self.quotationSheetGrid.exchangeRate = self.exchangeRate
            self.quotationSheetGrid.currencyName = self.currencyName
            self.quotationSheetGrid.ReCreate()

    def OnExchangeRatDateChanged(self, event):
        if event.GetDate() != self.exchangeDate:
            self.exchangeDate = event.GetDate()
            self.exchangeDate = wxdate2pydate(self.exchangeDate)
            self.parent.master.exchangeRate = None
            for item in self.parent.master.exChangeRateDic:
                if str(self.exchangeDate) == item['日期']:
                    self.parent.master.exchangeRate = item[self.currencyName]
                    break
            if not self.parent.master.exchangeRate:
                self.parent.master.exchangeRate = self.parent.master.exChangeRateDic[-1][self.currencyName]
                # 这块儿应加入把新值插入汇率数据库的操作
            self.exchangeRateTXT.SetValue(self.parent.master.exchangeRate)
            self.quotationSheetGrid.exchangeRate = self.parent.master.exchangeRate
            self.quotationSheetGrid.ReCreate()

    def OnQuotationDateChanged(self, event):
        if event.GetDate() != self.quotationDate:
            self.quotationDate = event.GetDate()
            self.quotationDate = wxdate2pydate(self.quotationDate)
            self.quotationSheetGrid.SetCellValue(1,2,str(self.quotationDate))
        event.Skip()

    def OnQuotationRangeChanged(self, event):
        if self.quotationRange!=self.quotationRangeCtrl.GetValue():
            self.quotationRange = self.quotationRangeCtrl.GetValue()
            self.quotationSheetGrid.quotationRange = self.quotationRange
            self.quotationSheetGrid.ReCreate()
        event.Skip()

    def ReCreateGrid(self):
        self.gridPanel.Freeze()
        self.gridPanel.DestroyChildren()
        self.quotationRange = self.quotationRangeCtrl.GetValue()
        hbox = wx.BoxSizer()
        self.quotationSheetGrid = QuotationSheetGrid(self.gridPanel, self.master, self.editAnnotationdlg, self.log, self.id, self.priceDataDic, self.quotationDate,
                                                     self.exchangeDate,self.quotationRange, self.name, self.currencyName, self.exchangeRate, self.orderName)
        hbox.Add(self.quotationSheetGrid, 1, wx.EXPAND)
        self.gridPanel.SetSizer(hbox)
        self.gridPanel.Layout()
        self.gridPanel.Thaw()

    def CreateGrid(self):
        self.gridPanel.Freeze()
        self.quotationRange = self.quotationRangeCtrl.GetValue()
        hbox = wx.BoxSizer()
        self.quotationSheetGrid = QuotationSheetGrid(self.gridPanel, self.master, self.editAnnotationdlg, self.log, self.id, self.priceDataDic, self.quotationDate,
                                                     self.exchangeDate,self.quotationRange, self.name, self.currencyName, self.exchangeRate, self.orderName)
        hbox.Add(self.quotationSheetGrid, 1, wx.EXPAND)
        self.gridPanel.SetSizer(hbox)
        self.gridPanel.Layout()
        self.gridPanel.Thaw()


class QuotationSheetGrid(gridlib.Grid):
    def __init__(self, parent, master,annotationDlg, log, id, priceDataDic, quotationDate, exchangeRateDate,quotationRange,name,currencyName='人民币',exchangeRate=100,orderName=''):
        gridlib.Grid.__init__(self, parent, -1)
        self.master = master
        self.orderName = orderName
        self.id = id
        self.annotationDlg = annotationDlg
        self.log = log
        self.name = name
        self.moveTo = None
        self.priceDataDic = priceDataDic
        self.quotationDate = quotationDate
        self.exchangeRateDate = exchangeRateDate
        self.quotationRange = quotationRange
        self.currencyName = currencyName
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        temp = GetOrderAnnotation(self.log, WHICHDB, self.id)
        self.annotationList = ["", "", ""]
        for i, item in enumerate(temp[:3]):
            self.annotationList[i] = item
        self.dataWall = GetDraftComponentInfoByID(self.log, WHICHDB, self.id, "WALL")
        self.dataCeiling = GetDraftComponentInfoByID(self.log, WHICHDB, self.id, "CEILING")
        self.dataInteriorDoor = GetDraftComponentInfoByID(self.log, WHICHDB, self.id, "INTERIORDOOR")
        self.dataFireDoor = GetDraftComponentInfoByID(self.log, WHICHDB, self.id, "FIREDOOR")
        self.dataWetUnit = GetDraftComponentInfoByID(self.log, WHICHDB, self.id, "WETUNIT")
        self.wallUnitPrice = [0] * len(self.dataWall)
        self.wallTotalPrice = [0] * len(self.dataWall)
        self.exchangeRate = exchangeRate
        self.wallRowNumList=[]
        self.wallSumupPricesRMB = 0.0
        self.ceilingRowNumList=[]
        self.ceilingSumupPricesRMB = 0.0
        self.interiorDoorRowNumList=[]
        self.interiorDoorSumupPricesRMB = 0.0
        self.fireDoorRowNumList=[]
        self.fireDoorSumupPricesRMB = 0.0
        self.wetUnitRowNumList=[]
        self.wetUnitSumupPricesRMB = 0.0
        for i, dic in enumerate(self.dataWall):
            if dic['单价'] != None:
                self.wallUnitPrice[i] = float(dic['单价'])
            if dic['总价'] == None:
                self.wallTotalPrice[i] = self.wallUnitPrice[i] * float(dic['数量'])
            else:
                self.wallTotalPrice[i] = float(dic['总价'])
        self.ceilingUnitPrice = [0] * len(self.dataCeiling)
        self.ceilingTotalPrice = [0] * len(self.dataCeiling)
        for i, dic in enumerate(self.dataCeiling):
            if dic['单价'] != None:
                self.ceilingUnitPrice[i] = float(dic['单价'])
            if dic['总价'] == None:
                self.ceilingTotalPrice[i] = self.ceilingUnitPrice[i] * float(dic['数量'])
            else:
                self.ceilingTotalPrice[i] = float(dic['总价'])
        self.interiorDoorUnitPrice = [0] * len(self.dataInteriorDoor)
        self.interiorDoorTotalPrice = [0] * len(self.dataInteriorDoor)
        for i, dic in enumerate(self.dataInteriorDoor):
            if dic['单价'] != None:
                self.interiorDoorUnitPrice[i] = float(dic['单价'])
            if dic['总价'] == None:
                self.interiorDoorTotalPrice[i] = self.interiorDoorUnitPrice[i] * float(dic['数量'])
            else:
                self.interiorDoorTotalPrice[i] = float(dic['总价'])
        self.fireDoorUnitPrice = [0] * len(self.dataFireDoor)
        self.fireDoorTotalPrice = [0] * len(self.dataFireDoor)
        for i, dic in enumerate(self.dataFireDoor):
            if dic['单价'] != None:
                self.fireDoorUnitPrice[i] = float(dic['单价'])
            if dic['总价'] == None:
                self.fireDoorTotalPrice[i] = self.fireDoorUnitPrice[i] * float(dic['数量'])
            else:
                self.fireDoorTotalPrice[i] = float(dic['总价'])
        self.wetUnitUnitPrice = [0] * len(self.dataWetUnit)
        self.wetUnitTotalPrice = [0] * len(self.dataWetUnit)
        for i, dic in enumerate(self.dataWetUnit):
            if dic['单价'] != None:
                self.wetUnitUnitPrice[i] = float(dic['单价'])
            if dic['总价'] == None:
                self.wetUnitTotalPrice[i] = self.fireDoorUnitPrice[i] * float(dic['数量'])
            else:
                self.wetUnitTotalPrice[i] = float(dic['总价'])
        self.Freeze()
        self.CreateGrid(8+12 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6, 22)  # , gridlib.Grid.SelectRows)
        self.EnableEditing(True)
        self.SetRowLabelSize(50)
        self.SetColLabelSize(25)
        self.SetColSize(0, 50)
        self.SetColSize(1, 170)
        self.SetColSize(3, 100)
        self.SetColSize(4, 135)
        self.SetColSize(5, 100)
        self.SetColSize(6, 100)
        self.SetColSize(7, 40)
        self.SetColSize(8, 60)
        self.SetColSize(9, 80)
        self.SetColSize(10, 70)
        self.SetColSize(11, 100)
        self.SetColSize(12, 100)
        self.SetColSize(13, 40)
        self.SetColSize(14, 105)
        self.SetColSize(21, 105)
        for i in range(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6):
            for j in range(22):
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)

        # self.productLaborUnitPrice = 20.11
        # self.scrapRate = 0.03
        # self.overheadRate = 0.26
        # self.profitRate = 0.15
        # self.marginNT = 0.2
        # self.marginDK = 0
        # self.agentRate = 0
        # exchangeRate = self.master.exchangeRate
        colNum = 21 if self.name=='生成报价单' else 20
        for i in range(colNum):
            attr = gridlib.GridCellAttr()
            # attr.SetFont(font)
            # attr.SetBackgroundColour(wx.LIGHT_GREY)
            attr.SetReadOnly(True)
            attr.SetAlignment(wx.CENTER, -1)
            self.SetColAttr(i, attr)
        # attr.IncRef()

        self.ReCreate()
        self.Thaw()
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChanged)

    def GetAnnotation(self):
        value=[]
        for i in range(12):
            temp = self.GetCellValue(8 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 + i,1)
            if len(temp)>0:
                value.append(temp)
        return value

    # def GetNoteValue(self,number):
    #     value = self.GetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 3 + number, 1)
    #     return value
    #
    def SetNoteValue(self,number, info):
        self.annotationList[number]=info
        self.SetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 3 + number, 1, info)

    def OnCellChanged(self, evt):
        col = evt.GetCol()
        row = evt.GetRow()
        if row in self.wallRowNumList:
            price = self.GetCellValue(row,col)
            try:
                price = int(price)
            except:
                price=0
                self.SetCellValue(row,col,'')
            error=True
            for i in range(6):
                temp = self.GetCellValue(row,14+i)
                if temp:
                    temp = temp.split('-')
                    left = int(temp[0])
                    right = int(temp[1])
                else:
                    left = 0
                    right =0
                if price>=left and price<=right:
                    error=False
                    break
            if error:
                self.SetCellBackgroundColour(row,col,wx.Colour(200,100,0))
            else:
                self.SetCellBackgroundColour(row,col,wx.WHITE)
            if self.GetCellValue(row,col):
                price = price * 1.3 if self.GetCellValue(11 + i, 10) == 'Y' else price
                price = price + 15 if self.GetCellValue(11 + i, 8) == "Y" else price
                price = price + 20 if self.GetCellValue(11 + i, 9) == "Y" else price
                unitPriceUS = price/self.exchangeRate*100
                totalPriceUS = float(self.GetCellValue(row,6))*unitPriceUS
                self.SetCellValue(row, 11, "%6.2f"%unitPriceUS)
                self.SetCellValue(row, 12, "%6.2f"%totalPriceUS)
                self.wallSumupPrices = 0.0
                self.wallSumupPricesRMB = 0.0
                for i in range(len(self.dataWall)):
                    try:
                        price = float(self.GetCellValue(11 + i, 20))
                    except:
                        price = 0.0
                    price = price * 1.3 if self.GetCellValue(11 + i, 10) == 'Y' else price
                    price = price + 15 if self.GetCellValue(11 + i, 8) == "Y" else price
                    price = price + 20 if self.GetCellValue(11 + i, 9) == "Y" else price
                    totalPriceRMB = float(self.GetCellValue(row, 6)) * price
                    self.wallSumupPricesRMB += totalPriceRMB
                    temp = self.GetCellValue(11+i,20)
                    temp = float(temp) if temp else 0
                    self.dataWall[i]["实际报价"]=str(temp)
                    temp = self.GetCellValue(11+i,11)
                    temp = float(temp) if temp else 0
                    self.dataWall[i]["单价"]=str(temp)
                    temp = self.GetCellValue(11+i,12)
                    temp = float(temp) if temp else 0
                    self.dataWall[i]["总价"]=str(temp)
                    self.wallSumupPrices += temp
                self.SetCellValue(11+len(self.dataWall),12,format(self.wallSumupPrices,','))
        elif row in self.ceilingRowNumList:
            price = self.GetCellValue(row,col)
            try:
                price = int(price)
            except:
                price=0
                self.SetCellValue(row,col,'')
            error=True
            for i in range(6):
                temp = self.GetCellValue(row,14+i)
                if temp:
                    temp = temp.split('-')
                    left = int(temp[0])
                    right = int(temp[1])
                else:
                    left = 0
                    right = 0
                if price>=left and price<=right:
                    error=False
                    break
            if error:
                self.SetCellBackgroundColour(row,col,wx.Colour(200,100,0))
            else:
                self.SetCellBackgroundColour(row,col,wx.WHITE)
            if self.GetCellValue(row,col):
                unitPriceUS = price/self.exchangeRate*100
                totalPriceUS = float(self.GetCellValue(row,6))*unitPriceUS
                self.SetCellValue(row, 11, "%6.2f"%unitPriceUS)
                self.SetCellValue(row, 12, "%6.2f"%totalPriceUS)
                self.ceilingSumupPrices = 0.0
                self.ceilingSumupPricesRMB = 0.0
                for i in range(len(self.dataCeiling)):
                    try:
                        price = float(self.GetCellValue(11 + len(self.dataWall) + 6 + i, 20))
                    except:
                        price = 0.0
                    totalPriceRMB = float(self.GetCellValue(11 + len(self.dataWall) + 6 + i, 6)) * price
                    self.ceilingSumupPricesRMB += totalPriceRMB
                    temp = self.GetCellValue(11 + len(self.dataWall) + 6 + i,20)
                    temp = float(temp) if temp else 0
                    self.dataCeiling[i]["实际报价"]=str(temp)
                    temp = self.GetCellValue(11 + len(self.dataWall) + 6 + i,11)
                    temp = float(temp) if temp else 0
                    self.dataCeiling[i]["单价"]=str(temp)
                    temp = self.GetCellValue(11 + len(self.dataWall) + 6 + i,12)
                    temp = float(temp) if temp else 0
                    self.dataCeiling[i]["总价"]=str(temp)
                    self.ceilingSumupPrices += temp
                self.SetCellValue(11+len(self.dataWall)+6+len(self.dataCeiling),12,format(self.ceilingSumupPrices,','))
        elif row in self.interiorDoorRowNumList:
            price = self.GetCellValue(row,col)
            try:
                price = int(price)
            except:
                price=0
                self.SetCellValue(row,col,'')
            error=True
            for i in range(6):
                temp = self.GetCellValue(row,14+i)
                if temp:
                    temp = temp.split('-')
                    left = int(temp[0])
                    right = int(temp[1])
                else:
                    left = 0
                    right = 0
                if price>=left and price<=right:
                    error=False
                    break
            if error:
                self.SetCellBackgroundColour(row,col,wx.Colour(200,100,0))
            else:
                self.SetCellBackgroundColour(row,col,wx.WHITE)
            if self.GetCellValue(row,col):
                unitPriceUS = price/self.exchangeRate*100
                totalPriceUS = float(self.GetCellValue(row,6))*unitPriceUS
                self.SetCellValue(row, 11, "%6.2f"%unitPriceUS)
                self.SetCellValue(row, 12, "%6.2f"%totalPriceUS)
                self.interiorDoorSumupPrices = 0.0
                self.interiorDoorSumupPricesRMB = 0.0
                for i in range(len(self.dataInteriorDoor)):
                    try:
                        price = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + i, 20))
                    except:
                        price = 0.0
                    totalPriceRMB = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + i, 6)) * price
                    self.interiorDoorSumupPricesRMB += totalPriceRMB
                    temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + i,20)
                    temp = float(temp) if temp else 0
                    self.dataInteriorDoor[i]["实际报价"]=str(temp)
                    temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + i,11)
                    temp = float(temp) if temp else 0
                    self.dataInteriorDoor[i]["单价"]=str(temp)
                    temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + i,12)
                    temp = float(temp) if temp else 0
                    self.dataInteriorDoor[i]["总价"]=str(temp)
                    self.interiorDoorSumupPrices += temp
                self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + len(self.dataInteriorDoor),12,format(self.interiorDoorSumupPrices,','))
        elif row in self.fireDoorRowNumList:
            price = self.GetCellValue(row,col)
            try:
                price = int(price)
            except:
                price=0
                self.SetCellValue(row,col,'')
            error=True
            for i in range(6):
                temp = self.GetCellValue(row,14+i)
                if temp:
                    temp = temp.split('-')
                    left = int(temp[0])
                    right = int(temp[1])
                else:
                    left = 0
                    right = 0
                if price>=left and price<=right:
                    error=False
                    break
            if error:
                self.SetCellBackgroundColour(row,col,wx.Colour(200,100,0))
            else:
                self.SetCellBackgroundColour(row,col,wx.WHITE)
            if self.GetCellValue(row,col):
                unitPriceUS = price/self.exchangeRate*100
                totalPriceUS = float(self.GetCellValue(row,6))*unitPriceUS
                self.SetCellValue(row, 11, "%6.2f"%unitPriceUS)
                self.SetCellValue(row, 12, "%6.2f"%totalPriceUS)
                self.fireDoorSumupPrices = 0.0
                self.fireDoorSumupPricesRMB = 0.0
                for i in range(len(self.dataFireDoor)):
                    try:
                        price = float(self.GetCellValue(11  + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor) + 18 + i, 20))
                    except:
                        price = 0.0
                    totalPriceRMB = float(self.GetCellValue(11  + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor) + 18 + i, 6)) * price
                    self.fireDoorSumupPricesRMB += totalPriceRMB
                    temp = self.GetCellValue(11  + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor) + 18 + i,20)
                    temp = float(temp) if temp else 0
                    self.dataFireDoor[i]["实际报价"]=str(temp)
                    temp = self.GetCellValue(11 + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor) + 18 + i,11)
                    temp = float(temp) if temp else 0
                    self.dataFireDoor[i]["单价"]=str(temp)
                    temp = self.GetCellValue(11  + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor) + 18 + i,12)
                    temp = float(temp) if temp else 0
                    self.dataFireDoor[i]["总价"]=str(temp)
                    self.fireDoorSumupPrices += temp
                self.SetCellValue(11 + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor) + len(self.dataFireDoor) + 18,12,format(self.fireDoorSumupPrices,','))
        elif row in self.wetUnitRowNumList:
            price = self.GetCellValue(row,col)
            try:
                price = int(price)
            except:
                price=0
                self.SetCellValue(row,col,'')
            error=True
            for i in range(6):
                temp = self.GetCellValue(row,14+i)
                if temp:
                    temp = temp.split('-')
                    left = int(temp[0])
                    right = int(temp[1])
                else:
                    left = 0
                    right = 0
                if price>=left and price<=right:
                    error=False
                    break
            if error:
                self.SetCellBackgroundColour(row,col,wx.Colour(200,100,0))
            else:
                self.SetCellBackgroundColour(row,col,wx.WHITE)
            if self.GetCellValue(row,col):
                unitPriceUS = price/self.exchangeRate*100
                totalPriceUS = float(self.GetCellValue(row,6))*unitPriceUS
                self.SetCellValue(row, 11, "%6.2f"%unitPriceUS)
                self.SetCellValue(row, 12, "%6.2f"%totalPriceUS)
                self.wetUnitSumupPrices = 0.0
                self.wetUnitSumupPricesRMB = 0.0
                for i in range(len(self.dataWetUnit)):
                    try:
                        price = float(self.GetCellValue(11  + len(self.dataWall) + 6 + len(self.dataCeiling) +6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 20))
                    except:
                        price = 0.0
                    totalPriceRMB = float(self.GetCellValue(11  + len(self.dataWall) + 6 + len(self.dataCeiling) +6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 6)) * price
                    self.wetUnitSumupPricesRMB += totalPriceRMB
                    temp = self.GetCellValue(11  + len(self.dataWall) + 6 + len(self.dataCeiling) +6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i,20)
                    temp = float(temp) if temp else 0
                    self.dataWetUnit[i]["实际报价"]=str(temp)
                    temp = self.GetCellValue(11  + len(self.dataWall) + 6 + len(self.dataCeiling) +6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i,11)
                    temp = float(temp) if temp else 0
                    self.dataWetUnit[i]["单价"]=str(temp)
                    temp = self.GetCellValue(11  + len(self.dataWall) + 6 + len(self.dataCeiling) +6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i,12)
                    temp = float(temp) if temp else 0
                    self.dataWetUnit[i]["总价"]=str(temp)
                    self.wetUnitSumupPrices += temp
                self.SetCellValue(11  + len(self.dataWall) + 6 + len(self.dataCeiling) +6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit),12,format(self.wetUnitSumupPrices,','))
        evt.Skip()

    def GetWallData(self):
        dataWall = []
        if len(self.dataWall)>0:
            for row in range(len(self.dataWall) + 1):
                rowList = []
                for col in range(13):
                    rowList.append(self.GetCellValue(row + 11, col))
                dataWall.append(rowList)
        return dataWall

    def GetCeilingData(self):
        dataCeiling = []
        if len(self.dataCeiling)>0:
            for row in range(len(self.dataCeiling) + 1):
                rowList = []
                for col in range(13):
                    rowList.append(self.GetCellValue(row + 11 + len(self.dataWall) + 6, col))
                dataCeiling.append(rowList)
        return dataCeiling

    def GetInteriorDoorData(self):
        dataInteriorDoor = []
        if len(self.dataInteriorDoor)>0:
            for row in self.interiorDoorRowNumList:
                rowList = []
                for col in range(13):
                    rowList.append(self.GetCellValue(row, col))
                dataInteriorDoor.append(rowList)
            #下面的代码是把合计那一行也取出来
            rowList = []
            for col in range(13):
                rowList.append(self.GetCellValue(self.interiorDoorRowNumList[-1]+1, col))
            dataInteriorDoor.append(rowList)
        return dataInteriorDoor

    def GetFireDoorData(self):
        dataFireDoor = []
        if len(self.dataFireDoor)>0:
            for row in self.fireDoorRowNumList:
                rowList = []
                for col in range(13):
                    rowList.append(self.GetCellValue(row, col))
                dataFireDoor.append(rowList)
            #下面的代码是把合计那一行也取出来
            rowList = []
            for col in range(13):
                rowList.append(self.GetCellValue(self.fireDoorRowNumList[-1]+1, col))
            dataFireDoor.append(rowList)
        return dataFireDoor

    def GetWetUnitData(self):
        dataWetUnit = []
        if len(self.dataWetUnit)>0:
            for row in self.wetUnitRowNumList:
                rowList = []
                for col in range(13):
                    rowList.append(self.GetCellValue(row, col))
                dataWetUnit.append(rowList)
            #下面的代码是把合计那一行也取出来
            rowList = []
            for col in range(13):
                rowList.append(self.GetCellValue(self.wetUnitRowNumList[-1]+1, col))
            dataWetUnit.append(rowList)
        return dataWetUnit

    def GetNoteText(self):
        dataNoteText = []
        number=0
        for i in range(3):
            temp = self.GetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 3 + i,1)
            if len(temp)>0:
                rowList = "%s, "%str(number+10)+temp
                number += 1
                dataNoteText.append(rowList)
        #下面的代码是把合计那一行也取出来
        return dataNoteText

    def ReCreate(self):
        # _, self.allProductMeterialUnitPriceList = GetAllProductMeterialUnitPriceInDB(self.log, WHICHDB)
        quotationDate = str(self.quotationDate)
        # _, self.allMeterialUnitPriceList = GetAllMeterialUnitPriceByIdInDB(self.log, WHICHDB, quotationDate)
        self.exchangeRate = float(self.exchangeRate)
        self.ClearGrid()
        self.SetCellValue(0, 0, "INEXA TNF")
        # self.SetCellValue(0, 12+2, "Currency rate")
        # self.SetCellValue(0, 13+2, "%.2f" % self.exchangeRate)
        # self.SetCellValue(0, 14+2, "USD-CNY")
        # self.SetCellValue(0, 15+2, str(self.exchangeRateDate))
        #
        self.SetCellValue(1, 0, "Date: ")
        self.SetCellValue(1, 2, quotationDate)
        # self.SetCellValue(1, 12+2, "OverHead")
        # self.SetCellValue(1, 13+2, "26%")
        # self.SetCellValue(1, 14+2, "Over-head by NT	")
        # self.SetCellSize(1, 14+2, 1, 2)
        #
        self.SetCellValue(2, 0, "Project Name.:")
        self.SetCellValue(2, 2, "%s"%self.orderName)
        # self.SetCellValue(2, 12+2, "crap rate")
        # self.SetCellValue(2, 13+2, "3%")
        # self.SetCellValue(2, 14+2, "All")
        # self.SetCellSize(2, 14+2, 1, 2)
        #
        self.SetCellValue(3, 0, "Inexa Quotation No.: ")
        self.SetCellValue(3, 2, "%06d"%self.id)
        # self.SetCellValue(3, 12+2, "Profile")
        # self.SetCellValue(3, 13+2, "15%")
        # self.SetCellValue(3, 14+2, "All")
        # self.SetCellSize(3, 14+2, 1, 2)
        #
        # self.SetCellValue(4, 12+2, "CM for NT")
        # self.SetCellValue(4, 13+2, "20%")
        # self.SetCellValue(4, 14+2, "Proposed by NT")
        # self.SetCellSize(4, 14+2, 1, 2)
        #
        # self.SetCellValue(5, 12+2, "CM for DK")
        # self.SetCellValue(5, 13+2, "0%")
        # self.SetCellValue(5, 14+2, "TBD by DK office")
        # self.SetCellSize(5, 14+2, 1, 2)
        #
        # self.SetCellValue(6, 12+2, "Agent rate")
        # self.SetCellValue(6, 13+2, "0%")
        # self.SetCellValue(6, 14+2, "TBD by DK office")
        # self.SetCellSize(6, 14+2, 1, 2)

        self.SetCellValue(7, 0, "Re:")
        self.SetCellValue(7, 1, "TNF accommodation system")
        # self.SetCellValue(7, 12+2, "Bussiness type")
        # self.SetCellValue(7, 13+2, "Export")
        # self.SetCellValue(7, 14+2, "Export")
        self.SetCellSize(7, 14+2, 1, 2)

        # #####################################     Wall Panel  ########################################################
        self.SetCellValue(8, 0, "1)TNF Wall Panel")
        self.SetCellValue(9, 0, "编号" if self.currencyName=='人民币' else "Item")
        self.SetCellValue(9, 1, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9, 2, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9, 3, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9, 4, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9, 5, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9, 7, "单位" if self.currencyName=='人民币' else "Unit")
        self.SetCellValue(9, 6, "总计" if self.currencyName=='人民币' else"Total")
        self.SetCellValue(9, 8, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9, 9, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9, 10, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9, 8+3, "单价" if self.currencyName=='人民币' else "Unit Price")
        self.SetCellValue(9, 9+3, "总价" if self.currencyName=='人民币' else "Total Price")
        self.SetCellValue(10, 12+2, "5000平方米")
        self.SetCellValue(10, 13+2, "80000平方米")
        self.SetCellValue(10, 14+2, "10000平方米")
        self.SetCellValue(10, 15+2, "20000平方米")
        self.SetCellValue(10, 16+2, "30000平方米")
        self.SetCellValue(10, 17+2, "40000平方米")
        self.SetCellValue(10, 18+2, "实际报价")
        # self.SetCellValue(9, 19, "0.0%")
        # self.SetCellValue(9, 21, "Inc. over head")

        self.SetCellValue(10, 1, "型号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(10, 2, "表材" if self.currencyName=='人民币' else "surface")
        self.SetCellValue(10, 3, "高度/长度 (mm)" if self.currencyName=='人民币' else "height/length (mm)")
        self.SetCellValue(10, 4, "宽度 (mm)" if self.currencyName=='人民币' else "width (mm)")
        self.SetCellValue(10, 5, "厚度 (mm)" if self.currencyName=='人民币' else "thickness (mm)")
        self.SetCellValue(10, 6, "数量" if self.currencyName=='人民币' else "Quantity")
        self.SetCellValue(10, 8, "潮湿" if self.currencyName=='人民币' else "Wet")
        self.SetCellValue(10, 9, "加强" if self.currencyName=='人民币' else "Strengthen")
        self.SetCellValue(10, 10, "超宽" if self.currencyName=='人民币' else "OverWidth")
        self.SetCellValue(10, 8+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10, 9+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])

        self.SetCellSize(0, 0, 1, 2)
        self.SetCellSize(1, 0, 1, 2)
        self.SetCellSize(2, 0, 1, 2)
        self.SetCellSize(3, 0, 1, 2)
        self.SetCellSize(7, 1, 1, 10)
        self.SetCellSize(8, 0, 1, 2)
        self.SetCellSize(8, 12+2, 1, 2)
        self.SetCellSize(8, 20+2, 2, 1)
        self.SetCellSize(9, 0, 2, 1)
        self.SetCellSize(9, 7, 2, 1)
        wallTotalAmount = 0.0
        wallTatalPriceUSD = 0.0
        self.wallRowNumList = []
        for i, wallDict in enumerate(self.dataWall):
            self.wallRowNumList.append(11+i)
            wallAmount = float(wallDict['数量'])
            wallTotalAmount += wallAmount
            self.SetCellValue(11 + i, 0, str(i + 1))
            self.SetCellValue(11 + i, 1, wallDict['产品名称'])
            # self.SetCellValue(11 + i, 2, wallDict['产品型号'])
            self.SetCellValue(11 + i, 2, wallDict['产品表面材料'])
            self.SetCellValue(11 + i, 3, wallDict['产品长度'])
            self.SetCellValue(11 + i, 4, wallDict['产品宽度'])
            self.SetCellValue(11 + i, 5, wallDict['产品厚度'])
            self.SetCellValue(11 + i, 7, wallDict['单位'])
            self.SetCellValue(11 + i, 6, wallDict['数量'])
            self.SetCellValue(11 + i, 8, "Y" if wallDict['潮湿']=='Y' else "")
            self.SetCellValue(11 + i, 9, "Y" if wallDict['加强']=='Y' else "")
            # self.SetCellValue(11 + i, 11, wallDict['单价'])
            # self.SetCellValue(11 + i, 12, wallDict['总价'])
            ## self.SetCellValue(11 + i, 10, wallDict['超宽'])
            # _,temp = GetProductMeterialUnitPriceInDB(self.log,WHICHDB,wallDict)
            renderer = gridlib.GridCellNumberRenderer()
            self.SetCellRenderer(11+i, 20, renderer)
            price = '' if not wallDict['实际报价'] else wallDict['实际报价']
            self.SetCellValue(11+i,20,price)
            for item in self.priceDataDic:
                if item["产品名称"] == wallDict['产品名称'] \
                        and item["产品表面材料"] == wallDict['产品表面材料'] and item["产品长度"] == wallDict['产品长度'] \
                        and item["报价类别"] == self.quotationRange:
                    if wallDict['产品宽度'] != "≤600":
                        self.SetCellValue(11+i,10,"Y")
                    else:
                        self.SetCellValue(11+i,10,"")
                    self.SetCellValue(11+i,12+2,item['5000平方米'])
                    self.SetCellValue(11+i,13+2,item['8000平方米'])
                    self.SetCellValue(11+i,14+2,item['10000平方米'])
                    self.SetCellValue(11+i,15+2,item['20000平方米'])
                    self.SetCellValue(11+i,16+2,item['30000平方米'])
                    self.SetCellValue(11+i,17+2,item['40000平方米'])
                    break
            error=True
            try:
                price = float(price)
            except:
                price = 0
            for j in range(6):
                temp = self.GetCellValue(11+i,14+j)
                if temp=="":
                    break
                temp = temp.split('-')
                left = int(temp[0])
                right = int(temp[1])
                if price>=left and price<=right:
                    error=False
                    break
            if error:
                self.SetCellBackgroundColour(i+11,20,wx.Colour(200,100,0))
            else:
                self.SetCellBackgroundColour(i+11,20,wx.WHITE)
            price = price*1.3 if self.GetCellValue(11+i,10)=='Y' else price
            price = price+15 if wallDict["潮湿"]=="Y" else price
            price = price+20 if wallDict["加强"]=="Y" else price
            unitPriceUS = price*100 / self.exchangeRate
            totalPriceUS = float(self.GetCellValue(11+i, 6)) * unitPriceUS
            self.SetCellValue(i+11, 11, "%6.2f"%unitPriceUS)
            self.SetCellValue(i+11, 12,"%6.2f"%totalPriceUS)
        sumupPriceUS = 0.0
        self.wallSumupPricesRMB = 0.0
        for i in range(len(self.dataWall)):
            try:
                price = float(self.GetCellValue(11+i,20))
            except:
                price = 0.0
            price = price * 1.3 if self.GetCellValue(11 + i, 10) == 'Y' else price
            price = price + 15 if self.GetCellValue(11 + i, 8) == "Y" else price
            price = price + 20 if self.GetCellValue(11 + i, 9) == "Y" else price
            totalPriceRMB = float(self.GetCellValue(11 + i, 6)) * price
            self.wallSumupPricesRMB += totalPriceRMB
            temp = self.GetCellValue(11 + i, 20)
            temp = float(temp) if temp else 0
            self.dataWall[i]["实际报价"] = str(temp)
            temp = self.GetCellValue(11 + i, 11)
            temp = float(temp) if temp else 0
            self.dataWall[i]["单价"] = str(temp)
            temp = self.GetCellValue(11 + i, 12)
            temp = float(temp) if temp else 0
            self.dataWall[i]["总价"] = str(temp)
            sumupPriceUS += temp
        self.SetCellValue(11 + len(self.dataWall), 6, format(wallTotalAmount,','))
        self.SetCellValue(11 + len(self.dataWall), 7, 'm2')
        temp = format(sumupPriceUS, ',')
        self.SetCellValue(11 + len(self.dataWall), 12, temp)

        ##########################################   Ceiling Panel   ###################################################
        self.SetCellValue(8 + 6 + len(self.dataWall), 0, "2)TNF Ceiling Panel")
        self.SetCellSize(8 + 6 + len(self.dataWall), 0, 1, 2)
        self.SetCellSize(9 + 6 + len(self.dataWall), 0, 2, 1)
        self.SetCellSize(9 + 6 + len(self.dataWall), 7, 2, 1)

        self.SetCellValue(9 + 6 + len(self.dataWall), 0, "编号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(9 + 6 + len(self.dataWall), 1, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall), 2, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall), 3, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall), 4, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall), 5, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall), 7, "单位" if self.currencyName=='人民币' else "Unit")
        self.SetCellValue(9 + 6 + len(self.dataWall), 6, "总计" if self.currencyName=='人民币' else"Total")
        self.SetCellValue(9 + 6 + len(self.dataWall), 8, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall), 9, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall), 10, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall), 8+3, "单价" if self.currencyName=='人民币' else "Unit Price")
        self.SetCellValue(9 + 6 + len(self.dataWall), 9+3, "总价" if self.currencyName=='人民币' else "Total Price")

        self.SetCellValue(10 + 6 + len(self.dataWall), 1, "型号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(10 + 6 + len(self.dataWall), 2, "表材" if self.currencyName=='人民币' else "surface")
        self.SetCellValue(10 + 6 + len(self.dataWall), 3, "高度/长度 (mm)" if self.currencyName=='人民币' else "height/length (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall), 4, "宽度 (mm)" if self.currencyName=='人民币' else "width (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall), 5, "厚度" if self.currencyName=='人民币' else "thickness (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall), 6, "数量" if self.currencyName=='人民币' else "Quantity")
        self.SetCellValue(10 + 6 + len(self.dataWall), 8, "潮湿" if self.currencyName=='人民币' else "Wet")
        self.SetCellValue(10 + 6 + len(self.dataWall), 9, "加强" if self.currencyName=='人民币' else "Strengthen")
        self.SetCellValue(10 + 6 + len(self.dataWall), 10, "超宽" if self.currencyName=='人民币' else "OverWidth")
        self.SetCellValue(10 + 6 + len(self.dataWall), 8+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10 + 6 + len(self.dataWall), 9+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10 + 6 + len(self.dataWall), 12+2, "5000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall), 13+2, "8000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall), 14+2, "10000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall), 15+2, "20000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall), 16+2, "30000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall), 17+2, "40000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall), 18+2, "实际报价")

        ceilingTotalAmount = 0.0
        ceilingTatalPriceUSD = 0.0
        self.ceilingRowNumList = []
        for i, ceilingDict in enumerate(self.dataCeiling):
            self.ceilingRowNumList.append(11+4+len(self.dataWall)+2+i)
            ceilingAmount = float(ceilingDict['数量'])
            ceilingTotalAmount += ceilingAmount
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 0, str(i + 1))
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 1, ceilingDict['产品名称'])
            # self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 2, ceilingDict['产品型号'])
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 2, ceilingDict['产品表面材料'])
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 3, ceilingDict['产品长度'])
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 4, ceilingDict['产品宽度'])
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 5, ceilingDict['产品厚度'])
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 6, ceilingDict['数量'])
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 7, ceilingDict['单位'])

            renderer = gridlib.GridCellNumberRenderer()
            self.SetCellRenderer(11 + 4 + len(self.dataWall) + 2 + i, 20, renderer)
            price = '' if not ceilingDict['实际报价'] else ceilingDict['实际报价']
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 20, price)
            for item in self.priceDataDic:
                if item["产品名称"] == ceilingDict['产品名称'] \
                        and item["产品表面材料"] == ceilingDict['产品表面材料'] and item["产品长度"] == ceilingDict['产品长度'] \
                        and item['产品宽度']== ceilingDict['产品宽度'] and item["报价类别"] == self.quotationRange:
                    # if wallDict['产品宽度'] != "≤600":
                    #     self.SetCellValue(11 + i, 10, "Y")
                    # else:
                    #     self.SetCellValue(11 + i, 10, "")
                    self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 12 + 2, item['5000平方米'])
                    self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 13 + 2, item['8000平方米'])
                    self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 14 + 2, item['10000平方米'])
                    self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 15 + 2, item['20000平方米'])
                    self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 16 + 2, item['30000平方米'])
                    self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 17 + 2, item['40000平方米'])
                    break
            error = True
            try:
                price = float(price)
            except:
                price = 0
            for j in range(6):
                temp = self.GetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 14 + j)
                if temp == "":
                    break
                temp = temp.split('-')
                left = int(temp[0])
                right = int(temp[1])
                if price >= left and price <= right:
                    error = False
                    break
            if error:
                self.SetCellBackgroundColour(11 + len(self.dataWall) + 6 + i, 20, wx.Colour(200, 100, 0))
            else:
                self.SetCellBackgroundColour(11 + len(self.dataWall) + 6 + i, 20, wx.WHITE)
            unitPriceUS = price*100 / self.exchangeRate
            totalPriceUS = float(self.GetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 6)) * unitPriceUS
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 11, "%6.2f"%unitPriceUS)
            self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 12, "%6.2f"%totalPriceUS)
        sumupPriceUS = 0.0
        self.ceilingSumupPricesRMB = 0.0
        for i in range(len(self.dataCeiling)):
            try:
                price = float(self.GetCellValue(11 + 4 + len(self.dataWall) + 2 + i,20))
            except:
                price = 0.0
            totalPriceRMB = float(self.GetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 6)) * price
            self.ceilingSumupPricesRMB += totalPriceRMB
            temp = self.GetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 20)
            temp = float(temp) if temp else 0
            self.dataCeiling[i]["实际报价"] = str(temp)
            temp = self.GetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 11)
            temp = float(temp) if temp else 0
            self.dataCeiling[i]["单价"] = str(temp)
            temp = self.GetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 12)
            temp = float(temp) if temp else 0
            self.dataCeiling[i]["总价"] = str(temp)
            sumupPriceUS += temp
        self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + len(self.dataCeiling), 6, format(ceilingTotalAmount,','))
        self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + len(self.dataCeiling), 7, 'm2')
        self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + len(self.dataCeiling), 12, format(sumupPriceUS, ','))

        #####################################    Interior Door   #######################################################
        self.SetCellValue(8 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 0, "3)TNF Interior Door")
        self.SetCellSize(8 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 0, 1, 2)
        self.SetCellSize(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 0, 2, 1)
        self.SetCellSize(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 7, 2, 1)

        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 0, "编号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 1, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 2, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 3, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 4, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 5, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 7, "单位" if self.currencyName=='人民币' else "Unit")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 6, "总计" if self.currencyName=='人民币' else"Total")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 8, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 9, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 10, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 8+3, "单价" if self.currencyName=='人民币' else "Unit Price")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 9+3, "总价" if self.currencyName=='人民币' else "Total Price")

        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 1, "型号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 2, "表材" if self.currencyName=='人民币' else "surface")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 3, "高度/长度 (mm)" if self.currencyName=='人民币' else "height/length (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 4, "宽度 (mm)" if self.currencyName=='人民币' else "width (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 5, "厚度" if self.currencyName=='人民币' else "thickness (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 6, "数量" if self.currencyName=='人民币' else "Quantity")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 8, "潮湿" if self.currencyName=='人民币' else "Wet")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 9, "加强" if self.currencyName=='人民币' else "Strengthen")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 10, "超宽" if self.currencyName=='人民币' else "OverWidth")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 8+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 9+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 12+2, "5000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 13+2, "8000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 14+2, "10000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 15+2, "20000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 16+2, "30000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 17+2, "40000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6, 18+2, "实际报价")

        interiorDoorTotalAmount = 0.0
        interiorDoorTatalPriceUSD = 0.0
        self.interiorDoorRowNumList = []
        for i, interiorDoorDict in enumerate(self.dataInteriorDoor):
            self.interiorDoorRowNumList.append(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + i)
            interiorDoorAmount = float(interiorDoorDict['数量'])
            interiorDoorTotalAmount += interiorDoorAmount
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 0, str(i + 1))
            self.SetCellValue(11  + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 1, interiorDoorDict['产品名称'])
            # self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 2, ceilingDict['产品型号'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 2, interiorDoorDict['产品表面材料'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 3, interiorDoorDict['产品长度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 4, interiorDoorDict['产品宽度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 5, interiorDoorDict['产品厚度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 6, interiorDoorDict['数量'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 7, interiorDoorDict['单位'])

            renderer = gridlib.GridCellNumberRenderer()
            self.SetCellRenderer(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 20, renderer)
            price = '' if not interiorDoorDict['实际报价'] else interiorDoorDict['实际报价']
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 20, price)
            for item in self.priceDataDic:
                if item["产品名称"] == interiorDoorDict['产品名称'] \
                        and item["产品表面材料"] == interiorDoorDict['产品表面材料'] and item["产品长度"] == interiorDoorDict['产品长度'] \
                        and item['产品宽度']== interiorDoorDict['产品宽度'] and item["报价类别"] == self.quotationRange:
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 12 + 2, item['5000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 13 + 2, item['8000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 14 + 2, item['10000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 15 + 2, item['20000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 16 + 2, item['30000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 17 + 2, item['40000平方米'])
                    break
            error = True
            try:
                price = float(price)
            except:
                price = 0
            for j in range(6):
                temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 14 + j)
                if temp == "":
                    break
                temp = temp.split('-')
                left = int(temp[0])
                right = int(temp[1])
                if price >= left and price <= right:
                    error = False
                    break
            if error:
                self.SetCellBackgroundColour(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 20, wx.Colour(200, 100, 0))
            else:
                self.SetCellBackgroundColour(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 20, wx.WHITE)
            unitPriceUS = price*100 / self.exchangeRate
            totalPriceUS = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 6)) * unitPriceUS
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 11, "%6.2f"%unitPriceUS)
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 12, "%6.2f"%totalPriceUS)
        sumupPriceUS = 0.0
        self.interiorDoorSumupPricesRMB = 0.0
        for i in range(len(self.dataInteriorDoor)):
            try:
                price = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i,20))
            except:
                price = 0.0
            totalPriceRMB = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 6)) * price
            self.interiorDoorSumupPricesRMB += totalPriceRMB
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 20)
            temp = float(temp) if temp else 0
            self.dataInteriorDoor[i]["实际报价"] = str(temp)
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 11)
            temp = float(temp) if temp else 0
            self.dataInteriorDoor[i]["单价"] = str(temp)
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + i, 12)
            temp = float(temp) if temp else 0
            self.dataInteriorDoor[i]["总价"] = str(temp)
            sumupPriceUS += temp
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor), 6, format(interiorDoorTotalAmount,','))
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor), 7, 'PCS')
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor), 12, format(sumupPriceUS, ','))

        # #####################################     Fire Door  #########################################################
        self.SetCellValue(8 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 0, "4)TNF Fire Door")
        self.SetCellSize(8 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 0, 1, 2)
        self.SetCellSize(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 0, 2, 1)
        self.SetCellSize(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 7, 2, 1)

        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 0, "编号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 1, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 2, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 3, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 4, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 5, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 7, "单位" if self.currencyName=='人民币' else "Unit")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 6, "总计" if self.currencyName=='人民币' else"Total")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 8, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 9, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 10, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 8+3, "单价" if self.currencyName=='人民币' else "Unit Price")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 9+3, "总价" if self.currencyName=='人民币' else "Total Price")

        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 1, "型号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 2, "表材" if self.currencyName=='人民币' else "surface")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 3, "高度/长度 (mm)" if self.currencyName=='人民币' else "height/length (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 4, "宽度 (mm)" if self.currencyName=='人民币' else "width (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 5, "厚度" if self.currencyName=='人民币' else "thickness (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 6, "数量" if self.currencyName=='人民币' else "Quantity")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 8, "潮湿" if self.currencyName=='人民币' else "Wet")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 9, "加强" if self.currencyName=='人民币' else "Strengthen")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 10, "超宽" if self.currencyName=='人民币' else "OverWidth")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 8+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 9+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 12+2, "5000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 13+2, "8000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 14+2, "10000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 15+2, "20000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 16+2, "30000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 17+2, "40000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6, 18+2, "实际报价")
        #
        fireDoorTotalAmount = 0.0
        fireDoorTatalPriceUSD = 0.0
        self.fireDoorRowNumList = []
        for i, fireDoorDict in enumerate(self.dataFireDoor):
            self.fireDoorRowNumList.append(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i)
            fireDoorAmount = float(fireDoorDict['数量'])
            fireDoorTotalAmount += fireDoorAmount
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 0, str(i + 1))
            self.SetCellValue(11  + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 1, fireDoorDict['产品名称'])
            # self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 2, ceilingDict['产品型号'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 2, fireDoorDict['产品表面材料'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 3, fireDoorDict['产品长度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 4, fireDoorDict['产品宽度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 5, fireDoorDict['产品厚度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 6, fireDoorDict['数量'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 7, fireDoorDict['单位'])

            renderer = gridlib.GridCellNumberRenderer()
            self.SetCellRenderer(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 20, renderer)
            price = '' if not fireDoorDict['实际报价'] else fireDoorDict['实际报价']
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 20, price)
            for item in self.priceDataDic:
                if item["产品名称"] == fireDoorDict['产品名称'] \
                        and item["产品表面材料"] == fireDoorDict['产品表面材料'] and item["产品长度"] == fireDoorDict['产品长度'] \
                        and item['产品宽度']== fireDoorDict['产品宽度'] and item["报价类别"] == self.quotationRange:
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 12 + 2, item['5000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 13 + 2, item['8000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 14 + 2, item['10000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 15 + 2, item['20000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 16 + 2, item['30000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 17 + 2, item['40000平方米'])
                    break
            error = True
            try:
                price = float(price)
            except:
                price = 0
            for j in range(6):
                temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 +len(self.dataInteriorDoor) +6 + i, 14 + j)
                if temp == "":
                    break
                temp = temp.split('-')
                left = int(temp[0])
                right = int(temp[1])
                if price >= left and price <= right:
                    error = False
                    break
            if error:
                self.SetCellBackgroundColour(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 20, wx.Colour(200, 100, 0))
            else:
                self.SetCellBackgroundColour(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 20, wx.WHITE)
            unitPriceUS = price*100 / self.exchangeRate
            totalPriceUS = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) +6 + i, 6)) * unitPriceUS
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 11, "%6.2f"%unitPriceUS)
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 12, "%6.2f"%totalPriceUS)
        sumupPriceUS = 0.0
        self.fireDoorSumupPricesRMB = 0.0
        for i in range(len(self.dataFireDoor)):
            try:
                price = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i,20))
            except:
                price = 0.0
            totalPriceRMB = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 6)) * price
            self.fireDoorSumupPricesRMB += totalPriceRMB
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 20)
            temp = float(temp) if temp else 0
            self.dataFireDoor[i]["实际报价"] = str(temp)
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 11)
            temp = float(temp) if temp else 0
            self.dataFireDoor[i]["单价"] = str(temp)
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + i, 12)
            temp = float(temp) if temp else 0
            self.dataFireDoor[i]["总价"] = str(temp)
            sumupPriceUS += temp
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor), 6, format(fireDoorTotalAmount,','))
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor), 7, 'PCS')
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 4 + 2 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor), 12, format(sumupPriceUS, ','))

        # #####################################      Wet Unit    #######################################################
        self.SetCellValue(8 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 0, "5)TNF Wet Unit")
        self.SetCellSize(8 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 0, 1, 2)
        self.SetCellSize(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 0, 2, 1)
        self.SetCellSize(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 7, 2, 1)

        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 0, "编号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 1, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 2, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 3, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 4, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 5, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 7, "单位" if self.currencyName=='人民币' else "Unit")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 6, "总计" if self.currencyName=='人民币' else"Total")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 8, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 9, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 10, "产品" if self.currencyName=='人民币' else "Product")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 8+3, "单价" if self.currencyName=='人民币' else "Unit Price")
        self.SetCellValue(9 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 9+3, "总价" if self.currencyName=='人民币' else "Total Price")

        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 1, "型号" if self.currencyName=='人民币' else "Name")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 2, "表材" if self.currencyName=='人民币' else "surface")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 3, "高度/长度 (mm)" if self.currencyName=='人民币' else "height/length (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 4, "宽度 (mm)" if self.currencyName=='人民币' else "width (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 5, "厚度" if self.currencyName=='人民币' else "thickness (mm)")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 6, "数量" if self.currencyName=='人民币' else "Quantity")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 8, "潮湿" if self.currencyName=='人民币' else "Wet")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 9, "加强" if self.currencyName=='人民币' else "Strengthen")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 10, "超宽" if self.currencyName=='人民币' else "OverWidth")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 8+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 9+3, "元" if self.currencyName=='人民币' else "In %s"%CURRENCYDICT[self.currencyName])
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 12+2, "5000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 13+2, "8000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 14+2, "10000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 15+2, "20000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 16+2, "30000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 17+2, "40000平方米")
        self.SetCellValue(10 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6, 18+2, "实际报价")
        #
        wetUnitTotalAmount = 0.0
        wetUnitTatalPriceUSD = 0.0
        self.wetUnitRowNumList = []
        for i, wetUnitDict in enumerate(self.dataWetUnit):
            self.wetUnitRowNumList.append(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i)
            wetUnitAmount = float(wetUnitDict['数量'])
            wetUnitTotalAmount += wetUnitAmount
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 0, str(i + 1))
            self.SetCellValue(11  + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 1, wetUnitDict['产品名称'])
            # self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 2, ceilingDict['产品型号'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 2, wetUnitDict['产品表面材料'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 3, wetUnitDict['产品长度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 4, wetUnitDict['产品宽度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 5, wetUnitDict['产品厚度'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 6, wetUnitDict['数量'])
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 7, wetUnitDict['单位'])

            renderer = gridlib.GridCellNumberRenderer()
            self.SetCellRenderer(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 20, renderer)
            price = '' if not wetUnitDict['实际报价'] else wetUnitDict['实际报价']
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 20, price)
            for item in self.priceDataDic:
                if item["产品名称"] == wetUnitDict['产品名称'] and item["报价类别"] == self.quotationRange:
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 12 + 2, item['5000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 13 + 2, item['8000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 14 + 2, item['10000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 15 + 2, item['20000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 16 + 2, item['30000平方米'])
                    self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 17 + 2, item['40000平方米'])
                    break
            error = True
            try:
                price = float(price)
            except:
                price = 0
            for j in range(6):
                temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 14 + j)
                if temp == "":
                    break
                temp = temp.split('-')
                left = int(temp[0])
                right = int(temp[1])
                if price >= left and price <= right:
                    error = False
                    break
            if error:
                self.SetCellBackgroundColour(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 20, wx.Colour(200, 100, 0))
            else:
                self.SetCellBackgroundColour(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 20, wx.WHITE)
            unitPriceUS = price*100 / self.exchangeRate
            totalPriceUS = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 6)) * unitPriceUS
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 11, "%6.2f"%unitPriceUS)
            self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 12, "%6.2f"%totalPriceUS)
        sumupPriceUS = 0.0
        self.wetUnitSumupPricesRMB = 0.0
        for i in range(len(self.dataWetUnit)):
            try:
                price = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i,20))
            except:
                price = 0.0
            totalPriceRMB = float(self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 6)) * price
            self.wetUnitSumupPricesRMB += totalPriceRMB
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 20)
            temp = float(temp) if temp else 0
            self.dataWetUnit[i]["实际报价"] = str(temp)
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 11)
            temp = float(temp) if temp else 0
            self.dataWetUnit[i]["单价"] = str(temp)
            temp = self.GetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + i, 12)
            temp = float(temp) if temp else 0
            self.dataWetUnit[i]["总价"] = str(temp)
            sumupPriceUS += temp
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit), 6, format(wetUnitTotalAmount,','))
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit), 7, 'PCS')
        self.SetCellValue(11 + 6 + len(self.dataWall) + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit), 12, format(sumupPriceUS, ','))

        #######################################    备注    ##############################################################
        attr = gridlib.GridCellAttr()
        # attr.SetFont(font)
        # attr.SetBackgroundColour(wx.LIGHT_GREY)
        attr.SetReadOnly(False)
        attr.SetAlignment(wx.CENTER, -1)
        self.SetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6- 4, 0, '备注：')
        # self.SetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 3, 0, '10')
        # self.SetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 2, 0, '11.')
        # self.SetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 1, 0, '12.')
        # self.SetAttr(30 - 3 + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor), 1, attr)
        # self.SetAttr(30 - 2 + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor), 1, attr)
        # self.SetAttr(30 - 1 + len(self.dataWall) + len(self.dataCeiling) + len(self.dataInteriorDoor), 1, attr)
        for i in range(12):
            self.SetCellSize(8 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 + i, 1, 1,12)
            self.SetCellAlignment(
                8 + len(self.dataWall) + 6 + len(self.dataCeiling) + 6 + len(self.dataInteriorDoor) + 6 + len(
                    self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 + i, 1, wx.LEFT, wx.CENTER)

        # self.SetCellSize(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 3, 1, 1,12)
        # self.SetCellSize(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 2, 1, 1,12)
        # self.SetCellSize(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 1, 1, 1,12)
        # self.SetCellAlignment(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 3, 1,wx.LEFT,wx.CENTER)
        # self.SetCellAlignment(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 2, 1,wx.LEFT,wx.CENTER)
        # self.SetCellAlignment(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 1, 1,wx.LEFT,wx.CENTER)
        # self.SetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 3, 1, self.annotationList[0])
        # self.SetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 2, 1, self.annotationList[1])
        # self.SetCellValue(11 + len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 - 1, 1, self.annotationList[2])
        self.RefreshAnnotation()

    def RefreshAnnotation(self):
        for i in range(12):
            self.SetCellValue(8+len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 + i, 1 , "")
        annotationList = self.annotationDlg.content.split('\n')[:12]
        for i, annotation in enumerate(annotationList):
            self.SetCellValue(8+len(self.dataWall)+6 + len(self.dataCeiling)+6 + len(self.dataInteriorDoor) + 6 + len(self.dataFireDoor) + 6 + len(self.dataWetUnit) + 6 + i, 1 , annotation)

    def OnIdle(self, evt):
        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()

#这个类保留今后改为成本核算类
# class QuotationSheetGrid(gridlib.Grid):
#     def __init__(self, parent, log, id, quotationDate, exchangeRateDate):
#         gridlib.Grid.__init__(self, parent, -1)
#         self.id = id
#         self.log = log
#         self.moveTo = None
#         self.quotationDate = quotationDate
#         self.exchangeRateDate = exchangeRateDate
#         self.Bind(wx.EVT_IDLE, self.OnIdle)
#         self.dataWall = GetDraftComponentInfoByID(self.log, WHICHDB, self.id, "WALL")
#         self.dataCeiling = GetDraftComponentInfoByID(self.log, WHICHDB, self.id, "CEILING")
#         self.wallUnitPrice = [0] * len(self.dataWall)
#         self.wallTotalPrice = [0] * len(self.dataWall)
#         self.exchangeRate = 6.66
#         for i, dic in enumerate(self.dataWall):
#             if dic['单价'] != None:
#                 self.wallUnitPrice[i] = float(dic['单价'])
#             if dic['总价'] == None:
#                 self.wallTotalPrice[i] = self.wallUnitPrice[i] * float(dic['数量'])
#             else:
#                 self.wallTotalPrice[i] = float(dic['总价'])
#         self.ceilingUnitPrice = [0] * len(self.dataCeiling)
#         self.ceilingTotalPrice = [0] * len(self.dataCeiling)
#         for i, dic in enumerate(self.dataCeiling):
#             if dic['单价'] != None:
#                 self.ceilingUnitPrice[i] = float(dic['单价'])
#             if dic['总价'] == None:
#                 self.ceilingTotalPrice[i] = self.ceilingUnitPrice[i] * float(dic['数量'])
#             else:
#                 self.ceilingTotalPrice[i] = float(dic['总价'])
#         self.Freeze()
#         self.CreateGrid(23 + len(self.dataWall) + len(self.dataCeiling), 22)  # , gridlib.Grid.SelectRows)
#         self.EnableEditing(False)
#         self.SetRowLabelSize(50)
#         self.SetColLabelSize(25)
#         self.SetColSize(0, 50)
#         self.SetColSize(1, 80)
#         self.SetColSize(3, 100)
#         self.SetColSize(4, 135)
#         self.SetColSize(5, 100)
#         self.SetColSize(6, 100)
#         self.SetColSize(7, 40)
#         self.SetColSize(11, 35)
#         self.SetColSize(12, 100)
#         self.SetColSize(14, 105)
#         self.SetColSize(21, 105)
#         for i in range(23 + len(self.dataWall) + len(self.dataCeiling)):
#             for j in range(22):
#                 self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
#         self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
#
#         self.productLaborUnitPrice = 20.11
#         self.scrapRate = 0.03
#         self.overheadRate = 0.26
#         self.profitRate = 0.15
#         self.marginNT = 0.2
#         self.marginDK = 0
#         self.agentRate = 0
#         exchangeRate = GetExchagneRateInDB(self.log, WHICHDB, str(self.exchangeRateDate))
#         if exchangeRate == None:
#             wx.MessageBox("数据库中没有指定日期的美元汇率，请更换日期后重试！", "信息提示")
#         else:
#             self.exchangeRate = float(exchangeRate) / 100. - 0.02
#         _, productLaborAmountList = GetProductLaborUnitPriceInDB(self.log, WHICHDB)
#         if productLaborAmountList == None:
#             wx.MessageBox("数据库中没有指定日期的原材料价格，请更换日期后重试！", "信息提示")
#         else:
#             self.productLaborAmountList = productLaborAmountList
#
#         self.ReCreate()
#         self.Thaw()
#
#     def GetWallData(self):
#         dataWall = []
#         for row in range(len(self.dataWall) + 1):
#             rowList = []
#             for col in range(11):
#                 rowList.append(self.GetCellValue(row + 11, col))
#             dataWall.append(rowList)
#         return dataWall
#
#     def GetCeilingData(self):
#         dataCeiling = []
#         for row in range(len(self.dataCeiling) + 1):
#             rowList = []
#             for col in range(11):
#                 rowList.append(self.GetCellValue(row + 11 + len(self.dataWall) + 6, col))
#             dataCeiling.append(rowList)
#         return dataCeiling
#
#     def ReCreate(self):
#         _, self.allProductMeterialUnitPriceList = GetAllProductMeterialUnitPriceInDB(self.log, WHICHDB)
#         quotationDate = str(self.quotationDate)
#         _, self.allMeterialUnitPriceList = GetAllMeterialUnitPriceByIdInDB(self.log, WHICHDB, quotationDate)
#         self.ClearGrid()
#         self.SetCellValue(0, 0, "INEXA TNF")
#         self.SetCellValue(0, 12, "Currency rate")
#         self.SetCellValue(0, 13, "%.2f" % self.exchangeRate)
#         self.SetCellValue(0, 14, "USD-CNY")
#         self.SetCellValue(0, 15, str(self.exchangeRateDate))
#
#         self.SetCellValue(1, 0, "Date: ")
#         self.SetCellValue(1, 2, quotationDate)
#         self.SetCellValue(1, 12, "OverHead")
#         self.SetCellValue(1, 13, "26%")
#         self.SetCellValue(1, 14, "Over-head by NT	")
#         self.SetCellSize(1, 14, 1, 2)
#
#         self.SetCellValue(2, 0, "Project No.:")
#         self.SetCellValue(2, 2, "Senta 123")
#         self.SetCellValue(2, 12, "crap rate")
#         self.SetCellValue(2, 13, "3%")
#         self.SetCellValue(2, 14, "All")
#         self.SetCellSize(2, 14, 1, 2)
#
#         self.SetCellValue(3, 0, "Inexa Quotation No.: ")
#         self.SetCellValue(3, 2, "Senta 123")
#         self.SetCellValue(3, 12, "Profile")
#         self.SetCellValue(3, 13, "15%")
#         self.SetCellValue(3, 14, "All")
#         self.SetCellSize(3, 14, 1, 2)
#
#         self.SetCellValue(4, 12, "CM for NT")
#         self.SetCellValue(4, 13, "20%")
#         self.SetCellValue(4, 14, "Proposed by NT")
#         self.SetCellSize(4, 14, 1, 2)
#
#         self.SetCellValue(5, 12, "CM for DK")
#         self.SetCellValue(5, 13, "0%")
#         self.SetCellValue(5, 14, "TBD by DK office")
#         self.SetCellSize(5, 14, 1, 2)
#
#         self.SetCellValue(6, 12, "Agent rate")
#         self.SetCellValue(6, 13, "0%")
#         self.SetCellValue(6, 14, "TBD by DK office")
#         self.SetCellSize(6, 14, 1, 2)
#
#         self.SetCellValue(7, 0, "Re:")
#         self.SetCellValue(7, 1, "TNF accommodation system")
#         self.SetCellValue(7, 12, "Bussiness type")
#         self.SetCellValue(7, 13, "Export")
#         self.SetCellValue(7, 14, "Export")
#         self.SetCellSize(7, 14, 1, 2)
#
#         self.SetCellValue(8, 0, "1)TNF Wall Panel")
#         self.SetCellValue(8, 12, "Direct costs")
#         self.SetCellValue(8, 14, "Scrap rate")
#         self.SetCellValue(8, 15, "Over-head")
#         self.SetCellValue(8, 16, "Profile")
#         self.SetCellValue(8, 17, "Margin-NT")
#         self.SetCellValue(8, 18, "Margin-DK")
#         self.SetCellValue(8, 19, "Agent  rate")
#         self.SetCellValue(8, 20, "sales price")
#         self.SetCellValue(8, 21, "Unit sales price")
#
#         self.SetCellValue(9, 0, "Item")
#         self.SetCellValue(9, 1, "Product")
#         self.SetCellValue(9, 2, "Product")
#         self.SetCellValue(9, 3, "Product")
#         self.SetCellValue(9, 4, "Product")
#         self.SetCellValue(9, 5, "Product")
#         self.SetCellValue(9, 6, "Product")
#         self.SetCellValue(9, 7, "Unit")
#         self.SetCellValue(9, 8, "Total")
#         self.SetCellValue(9, 9, "Unit Price")
#         self.SetCellValue(9, 10, "Total Price")
#         self.SetCellValue(9, 12, "Material")
#         self.SetCellValue(9, 13, "Labor")
#         self.SetCellValue(9, 14, "3.0%")
#         self.SetCellValue(9, 15, "26.0%")
#         self.SetCellValue(9, 16, "15.0%")
#         self.SetCellValue(9, 17, "20.0%")
#         self.SetCellValue(9, 18, "0.0%")
#         self.SetCellValue(9, 19, "0.0%")
#         self.SetCellValue(9, 21, "Inc. over head")
#
#         self.SetCellValue(10, 1, "No.")
#         self.SetCellValue(10, 2, "type")
#         self.SetCellValue(10, 3, "surface")
#         self.SetCellValue(10, 4, "height/length (mm)")
#         self.SetCellValue(10, 5, "width (mm)")
#         self.SetCellValue(10, 6, "thickness (mm)")
#         self.SetCellValue(10, 8, "Quantity")
#         self.SetCellValue(10, 9, "In USD")
#         self.SetCellValue(10, 10, "In USD")
#         self.SetCellValue(10, 12, "RMB")
#         self.SetCellValue(10, 13, "RMB")
#         self.SetCellValue(10, 14, "RMB")
#         self.SetCellValue(10, 15, "RMB")
#         self.SetCellValue(10, 16, "RMB")
#         self.SetCellValue(10, 17, "RMB")
#         self.SetCellValue(10, 18, "RMB")
#         self.SetCellValue(10, 19, "RMB")
#         self.SetCellValue(10, 20, "RMB")
#         self.SetCellValue(10, 21, "USD")
#
#         self.SetCellSize(0, 0, 1, 2)
#         self.SetCellSize(1, 0, 1, 2)
#         self.SetCellSize(2, 0, 1, 2)
#         self.SetCellSize(3, 0, 1, 2)
#         self.SetCellSize(7, 1, 1, 10)
#         self.SetCellSize(8, 0, 1, 2)
#         self.SetCellSize(8, 12, 1, 2)
#         self.SetCellSize(8, 20, 2, 1)
#         self.SetCellSize(9, 0, 2, 1)
#         self.SetCellSize(9, 7, 2, 1)
#         wallTotalAmount = 0.0
#         wallTatalPriceUSD = 0.0
#         for i, wallDict in enumerate(self.dataWall):
#             wallAmount = float(wallDict['数量'])
#             wallTotalAmount += wallAmount
#             self.SetCellValue(11 + i, 0, str(i + 1))
#             self.SetCellValue(11 + i, 1, wallDict['产品名称'])
#             self.SetCellValue(11 + i, 2, wallDict['产品型号'])
#             self.SetCellValue(11 + i, 3, wallDict['产品表面材料'])
#             self.SetCellValue(11 + i, 4, wallDict['产品长度'])
#             self.SetCellValue(11 + i, 5, wallDict['产品宽度'])
#             self.SetCellValue(11 + i, 6, wallDict['产品厚度'])
#             self.SetCellValue(11 + i, 7, wallDict['单位'])
#             self.SetCellValue(11 + i, 8, wallDict['数量'])
#             # _,temp = GetProductMeterialUnitPriceInDB(self.log,WHICHDB,wallDict)
#             for item in self.allProductMeterialUnitPriceList:
#                 if item["产品名称"] == wallDict['产品名称'] and item["产品型号"] == wallDict['产品型号'] \
#                         and item["产品表面材料"] == wallDict['产品表面材料'] and item["产品长度"] == wallDict['产品长度'] and item[
#                     "产品宽度"] == wallDict['产品宽度']:
#                     temp = item
#                     break
#             self.meterialFactorX = float(temp['X面材料系数'])
#             self.meterialIdX = int(temp['X面材料id'])
#             self.meterialFactorY = float(temp['Y面材料系数'])
#             self.meterialIdY = int(temp['Y面材料id'])
#             self.meterialFactorGlue = float(temp['胶水系数'])
#             self.meterialIdGlue = int(temp['胶水id'])
#             self.meterialFactorRockWool = float(temp['岩棉系数'])
#             self.meterialIdRockWool = int(temp['岩棉id'])
#             # _,temp2 = GetMeterialUnitPriceByIdInDB(self.log,WHICHDB,'2022-07-14',self.meterialIdX)
#             temp2 = self.allMeterialUnitPriceList[self.meterialIdX]
#             if temp2['单位'] == 'm2':
#                 self.meterialUnitPriceX = float(temp['X面材料系数']) * float(temp2['价格'])
#             else:
#                 self.meterialUnitPriceX = float(temp['X面厚度']) * float(temp2['密度']) * float(temp['X面材料系数']) * float(
#                     temp2['价格']) / 1000
#             if self.meterialFactorY != None:
#                 # _,temp2 = GetMeterialUnitPriceByIdInDB(self.log,WHICHDB,'2022-07-14',self.meterialIdY)
#                 temp2 = self.allMeterialUnitPriceList[self.meterialIdY]
#                 if temp2['单位'] == 'm2':
#                     self.meterialUnitPriceY = float(temp['Y面材料系数']) * float(temp2['价格'])
#                 else:
#                     self.meterialUnitPriceY = float(temp['Y面厚度']) * float(temp2['密度']) * float(temp['Y面材料系数']) * float(
#                         temp2['价格']) / 1000
#             else:
#                 self.meterialUnitPriceY = 0.0
#             if self.meterialFactorY != 0:
#                 # _,temp2 = GetMeterialUnitPriceByIdInDB(self.log,WHICHDB,'2022-07-14',self.meterialIdGlue)
#                 temp2 = self.allMeterialUnitPriceList[self.meterialIdGlue]
#                 self.meterialUnitPriceGlue = float(temp['胶水系数']) * float(temp2['价格']) / 1000000.
#             else:
#                 self.meterialUnitPriceGlue = 0.0
#             # _, temp2 = GetMeterialUnitPriceByIdInDB(self.log, WHICHDB, '2022-07-14', self.meterialIdRockWool)
#             temp2 = self.allMeterialUnitPriceList[self.meterialIdRockWool]
#             self.meterialUnitPriceRockWool = float(temp['SQM Per Piece']) * 150 * float(temp['产品厚度']) * float(
#                 temp['岩棉系数']) * float(temp2['价格']) / 1000000.
#             meterialUnitPrice = self.meterialUnitPriceX + self.meterialUnitPriceY + self.meterialUnitPriceGlue + self.meterialUnitPriceRockWool
#             self.SetCellValue(11 + i, 12, '%.2f' % meterialUnitPrice)
#
#             productLaborAmount = 0
#             for dic in self.productLaborAmountList:
#                 if wallDict['产品名称'] == dic['产品名称'] and wallDict['产品表面材料'] == dic['产品表面材料']:
#                     productLaborAmount = float(dic['每平方所需工时'])
#                     break
#             productLaborUnitPrice = productLaborAmount * self.productLaborUnitPrice
#             self.SetCellValue(11 + i, 13, '%.2f' % productLaborUnitPrice)
#
#             scrapUnitPrice = meterialUnitPrice * (self.scrapRate + 1)
#             self.SetCellValue(11 + i, 14, '%.2f' % scrapUnitPrice)
#
#             overheadUnitPrice = (scrapUnitPrice + productLaborUnitPrice) * (1 + self.overheadRate)
#             self.SetCellValue(11 + i, 15, '%.2f' % overheadUnitPrice)
#
#             profitUnitPrice = overheadUnitPrice * (1 + self.profitRate)
#             self.SetCellValue(11 + i, 16, '%.2f' % profitUnitPrice)
#
#             marginNTUnitPrice = profitUnitPrice * (1 + self.marginNT)
#             self.SetCellValue(11 + i, 17, '%.2f' % marginNTUnitPrice)
#
#             marginDKUnitPrice = marginNTUnitPrice * (1 + self.marginDK)
#             self.SetCellValue(11 + i, 18, '%.2f' % marginDKUnitPrice)
#
#             agentUnitPrice = marginDKUnitPrice * (1 + self.agentRate)
#             self.SetCellValue(11 + i, 19, '%.2f' % agentUnitPrice)
#
#             salesUnitPrice = agentUnitPrice
#             self.SetCellValue(11 + i, 20, '%.2f' % salesUnitPrice)
#
#             salesUnitPriceUSD = salesUnitPrice / self.exchangeRate
#             self.SetCellValue(11 + i, 21, '%.2f' % salesUnitPriceUSD)
#             self.SetCellValue(11 + i, 9, '%.2f' % salesUnitPriceUSD)
#
#             salesPriceUSD = salesUnitPriceUSD * wallAmount
#             self.SetCellValue(11 + i, 10, '%.2f' % salesPriceUSD)
#             wallTatalPriceUSD += salesPriceUSD
#
#         self.SetCellValue(11 + len(self.dataWall), 8, '%.2f' % wallTotalAmount)
#         self.SetCellValue(11 + len(self.dataWall), 10, '%.2f' % wallTatalPriceUSD)
#
#         ##########################################################################################
#         self.SetCellValue(8 + 6 + len(self.dataWall), 0, "2)TNF Ceiling Panel")
#         self.SetCellSize(8 + 6 + len(self.dataWall), 0, 1, 2)
#         self.SetCellValue(8 + 6 + len(self.dataWall), 12, "Direct costs")
#         self.SetCellSize(8 + 6 + len(self.dataWall), 12, 1, 2)
#         self.SetCellValue(8 + 6 + len(self.dataWall), 14, "Scrap rate")
#         self.SetCellValue(8 + 6 + len(self.dataWall), 15, "Over-head")
#         self.SetCellValue(8 + 6 + len(self.dataWall), 16, "Profile")
#         self.SetCellValue(8 + 6 + len(self.dataWall), 17, "Margin-NT")
#         self.SetCellValue(8 + 6 + len(self.dataWall), 18, "Margin-DK")
#         self.SetCellValue(8 + 6 + len(self.dataWall), 19, "Agent  rate")
#         self.SetCellValue(8 + 6 + len(self.dataWall), 20, "sales price")
#         self.SetCellSize(8 + 6 + len(self.dataWall), 20, 2, 1)
#         self.SetCellValue(8 + 6 + len(self.dataWall), 21, "Unit sales price")
#
#         self.SetCellValue(9 + 6 + len(self.dataWall), 0, "Item")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 1, "Product")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 2, "Product")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 3, "Product")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 4, "Product")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 5, "Product")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 6, "Product")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 7, "Unit")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 8, "Total")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 9, "Unit Price")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 10, "Total Price")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 12, "Material")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 13, "Labor")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 14, "3.0%")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 15, "26.0%")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 16, "15.0%")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 17, "20.0%")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 18, "0.0%")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 19, "0.0%")
#         self.SetCellValue(9 + 6 + len(self.dataWall), 21, "Inc. over head")
#
#         self.SetCellValue(10 + 6 + len(self.dataWall), 1, "No.")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 2, "type")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 3, "surface")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 4, "height/length (mm)")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 5, "width (mm)")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 6, "thickness (mm)")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 8, "Quantity")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 9, "In USD")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 10, "In USD")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 12, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 13, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 14, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 15, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 16, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 17, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 18, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 19, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 20, "RMB")
#         self.SetCellValue(10 + 6 + len(self.dataWall), 21, "USD")
#
#         ceilingTotalAmount = 0.0
#         ceilingTatalPriceUSD = 0.0
#         for i, ceilingDict in enumerate(self.dataCeiling):
#             ceilingAmount = float(ceilingDict['数量'])
#             ceilingTotalAmount += ceilingAmount
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 0, str(i + 1))
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 1, ceilingDict['产品名称'])
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 2, ceilingDict['产品型号'])
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 3, ceilingDict['产品表面材料'])
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 4, ceilingDict['产品长度'])
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 5, ceilingDict['产品宽度'])
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 6, ceilingDict['产品厚度'])
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 7, ceilingDict['单位'])
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 8, ceilingDict['数量'])
#             # _,temp = GetProductMeterialUnitPriceInDB(self.log,WHICHDB,ceilingDict)
#             for item in self.allProductMeterialUnitPriceList:
#                 if item["产品名称"] == ceilingDict['产品名称'] and item["产品型号"] == ceilingDict['产品型号'] \
#                         and item["产品表面材料"] == ceilingDict['产品表面材料'] and item["产品长度"] == ceilingDict['产品长度'] and item[
#                     "产品宽度"] == ceilingDict['产品宽度']:
#                     temp = item
#                     break
#             self.meterialFactorX = float(temp['X面材料系数'])
#             self.meterialIdX = int(temp['X面材料id'])
#             if temp['Y面材料系数'] != None:
#                 self.meterialFactorY = float(temp['Y面材料系数'])
#             else:
#                 self.meterialFactorY = 0.0
#             self.meterialIdY = int(temp['Y面材料id'])
#             self.meterialFactorGlue = float(temp['胶水系数'])
#             self.meterialIdGlue = int(temp['胶水id'])
#             self.meterialFactorRockWool = float(temp['岩棉系数'])
#             self.meterialIdRockWool = int(temp['岩棉id'])
#             # _,temp2 = GetMeterialUnitPriceByIdInDB(self.log,WHICHDB,'2022-07-14',self.meterialIdX)
#             temp2 = self.allMeterialUnitPriceList[self.meterialIdX]
#             if temp2['单位'] == 'm2':
#                 self.meterialUnitPriceX = float(temp['X面材料系数']) * float(temp2['价格'])
#             else:
#                 self.meterialUnitPriceX = float(temp['X面厚度']) * float(temp2['密度']) * float(temp['X面材料系数']) * float(
#                     temp2['价格']) / 1000
#             if self.meterialFactorY != 0:
#                 # _,temp2 = GetMeterialUnitPriceByIdInDB(self.log,WHICHDB,'2022-07-14',self.meterialIdY)
#                 temp2 = self.allMeterialUnitPriceList[self.meterialIdY]
#                 if temp2['单位'] == 'm2':
#                     if temp['Y面材料系数'] != None:
#                         self.meterialUnitPriceY = float(temp['Y面材料系数']) * float(temp2['价格'])
#                     else:
#                         self.meterialUnitPriceY = 0.0
#                 else:
#                     if temp['Y面厚度'] != None:
#                         self.meterialUnitPriceY = float(temp['Y面厚度']) * float(temp2['密度']) * float(
#                             temp['Y面材料系数']) * float(temp2['价格']) / 1000
#                     else:
#                         self.meterialUnitPriceY = 0.0
#             else:
#                 self.meterialUnitPriceY = 0.0
#             if self.meterialFactorY != 0:
#                 # _,temp2 = GetMeterialUnitPriceByIdInDB(self.log,WHICHDB,'2022-07-14',self.meterialIdGlue)
#                 temp2 = self.allMeterialUnitPriceList[self.meterialIdGlue]
#                 self.meterialUnitPriceGlue = float(temp['胶水系数']) * float(temp2['价格']) / 1000000.
#             else:
#                 self.meterialUnitPriceGlue = 0.0
#             # _, temp2 = GetMeterialUnitPriceByIdInDB(self.log, WHICHDB, '2022-07-14', self.meterialIdRockWool)
#             temp2 = self.allMeterialUnitPriceList[self.meterialIdRockWool]
#             if ceilingDict['产品名称'] == 'TNF-C46':
#                 self.meterialUnitPriceRockWool = float(temp['SQM Per Piece']) * 8. * float(ceilingDict['产品厚度']) * float(
#                     temp['岩棉系数']) * float(temp2['价格']) / 100000.
#             else:
#                 self.meterialUnitPriceRockWool = float(temp['SQM Per Piece']) * 15. * float(
#                     ceilingDict['产品厚度']) * float(temp['岩棉系数']) * float(temp2['价格']) / 100000.
#
#             meterialUnitPrice = self.meterialUnitPriceX + self.meterialUnitPriceY + self.meterialUnitPriceGlue + self.meterialUnitPriceRockWool
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 12, '%.2f' % meterialUnitPrice)
#
#             productLaborAmount = 0
#             for dic in self.productLaborAmountList:
#                 if ceilingDict['产品名称'] == dic['产品名称'] and ceilingDict['产品表面材料'] == dic['产品表面材料']:
#                     productLaborAmount = float(dic['每平方所需工时'])
#                     break
#             productLaborUnitPrice = productLaborAmount * self.productLaborUnitPrice
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 13, '%.2f' % productLaborUnitPrice)
#
#             scrapUnitPrice = meterialUnitPrice * (self.scrapRate + 1)
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 14, '%.2f' % scrapUnitPrice)
#
#             overheadUnitPrice = (scrapUnitPrice + productLaborUnitPrice) * (1 + self.overheadRate)
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 15, '%.2f' % overheadUnitPrice)
#
#             profitUnitPrice = overheadUnitPrice * (1 + self.profitRate)
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 16, '%.2f' % profitUnitPrice)
#
#             marginNTUnitPrice = profitUnitPrice * (1 + self.marginNT)
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 17, '%.2f' % marginNTUnitPrice)
#
#             marginDKUnitPrice = marginNTUnitPrice * (1 + self.marginDK)
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 18, '%.2f' % marginDKUnitPrice)
#
#             agentUnitPrice = marginDKUnitPrice * (1 + self.agentRate)
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 19, '%.2f' % agentUnitPrice)
#
#             salesUnitPrice = agentUnitPrice
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 20, '%.2f' % salesUnitPrice)
#
#             salesUnitPriceUSD = salesUnitPrice / self.exchangeRate
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 21, '%.2f' % salesUnitPriceUSD)
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 9, '%.2f' % salesUnitPriceUSD)
#
#             salesPriceUSD = salesUnitPriceUSD * ceilingAmount
#             self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + i, 10, '%.2f' % salesPriceUSD)
#             ceilingTatalPriceUSD += salesPriceUSD
#
#         self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + len(self.dataCeiling), 8, '%.2f' % ceilingTotalAmount)
#         self.SetCellValue(11 + 4 + len(self.dataWall) + 2 + len(self.dataCeiling), 10, '%.2f' % ceilingTatalPriceUSD)
#
#         # for i, title in enumerate(self.master.colLabelValueList):
#         #     self.SetColLabelValue(i,title)
#         # for i, width in enumerate(self.master.colWidthList):
#         #     self.SetColSize(i, width)
#         # for i, order in enumerate(self.master.dataArray[:,:7]):
#         #     self.SetRowSize(i, 25)
#         #     for j, item in enumerate(order):
#         #         self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
#         #         self.SetCellValue(i, j, str(item))
#         #         if int(order[0])<2:
#         #             self.SetCellBackgroundColour(i,j,wx.RED)
#         #         elif int(order[0])<5:
#         #             self.SetCellBackgroundColour(i,j,wx.YELLOW)
#
#     def OnIdle(self, evt):
#         if self.moveTo is not None:
#             self.SetGridCursor(self.moveTo[0], self.moveTo[1])
#             self.moveTo = None
#
#         evt.Skip()


class QuotationSheetViewDialog(wx.Dialog):
    def __init__(self, parent, log, filename):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.log = log
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "报价单浏览窗口", pos=wx.DefaultPosition, size=(1400, 1200))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self, size=(1400, 1200))
        self.buttonpanel = pdfButtonPanel(self.panel, wx.ID_ANY,
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.viewer = pdfViewer(self.panel, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
        sizer.Add(self.panel, 1, wx.EXPAND)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.buttonpanel, 0, wx.EXPAND)
        vbox.Add(self.viewer, 1, wx.EXPAND)
        self.panel.SetSizer(vbox)
        self.panel.Layout()
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.viewer.LoadFile(filename)

class EditAnnotationDialog(wx.Dialog):
    def __init__(self, parent, log, id):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.log = log
        self.id = id
        self.language = "中文"
        self.languageList = ["中文", "英文"]
        fileName = "D:\\IPMS\\dist\\config\\中文备注.txt"
        with open(fileName,'r',encoding='utf=8') as file:
            data = file.readlines()
        self.annotationListHZ = []
        for item in data:
            # item = item.strip('\n')
            self.annotationListHZ.append(item)
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        temp = GetOrderAnnotation(self.log, WHICHDB, self.id)
        if not temp:
            temp=["","","","中文"]
        self.annotationAdditonList = ["", "", ""]
        self.language = temp[3]
        for i, item in enumerate(temp[:3]):
            self.annotationAdditonList[i] = item
        self.DeliverList = ["不包含运费", "包含运费", "包含到港口的运费"] if self.language == '中文' else ["EX", "DAP", "CIF"]
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        # self.triggerList=[[1, 60], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0]]
        self.triggerList = GetOrderAnnotationTriggerList(self.log ,WHICHDB, self.id)
        self.Create(parent, -1, "草稿订单 %06d 备注编辑窗口"%self.id, pos=wx.DefaultPosition, size=(1280,700))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self, size=(1280, 600))
        sizer.Add(self.panel, 1, wx.EXPAND)
        sizer.Add(wx.StaticLine(self,size=(60,-1),style=wx.HORIZONTAL),0,wx.EXPAND)
        hbox = wx.BoxSizer()
        hbox.Add((50,-1),0)
        self.customerAnnotationBTN1 = wx.Button(self,-1,label="编辑自定义备注1",size=(100,40))
        self.customerAnnotationBTN1.Bind(wx.EVT_BUTTON,self.OnAddNoteButton1)
        self.customerAnnotationBTN2 = wx.Button(self,-1,label="编辑自定义备注2",size=(100,40))
        self.customerAnnotationBTN2.Bind(wx.EVT_BUTTON,self.OnAddNoteButton2)
        self.customerAnnotationBTN3 = wx.Button(self,-1,label="编辑自定义备注3",size=(100,40))
        self.customerAnnotationBTN3.Bind(wx.EVT_BUTTON,self.OnAddNoteButton3)
        self.languageCombo = wx.ComboBox(self, -1, value=self.language, choices=self.languageList, size=(100, 40))
        self.languageCombo.Bind(wx.EVT_COMBOBOX, self.OnLanguageChanged)
        self.okButton = wx.Button(self, wx.ID_OK,label = "确认",size=(100,40))
        self.okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL,label = "取消", size=(100,40))
        hbox.Add(self.languageCombo,0,wx.TOP,7)
        hbox.Add((30,-1),0)
        hbox.Add(self.customerAnnotationBTN1,1)
        hbox.Add((30,-1),0)
        hbox.Add(self.customerAnnotationBTN2,1)
        hbox.Add((30,-1),0)
        hbox.Add(self.customerAnnotationBTN3,1)
        hbox.Add((30,-1),0)
        hbox.Add(self.okButton,1)
        hbox.Add((30,-1),0)
        hbox.Add(self.cancelButton,1)
        hbox.Add((50,-1),0)
        sizer.Add(hbox,0,wx.EXPAND|wx.TOP|wx.BOTTOM,10)
        self.SetSizer(sizer)
        self.CreatePanel()
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckChanged)
        sizer.Fit(self)

    def CreatePanel(self):
        self.panel.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.annotationTXT = wx.TextCtrl(self.panel,-1,value="",size=(500,260),style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.RefreshAnnotation()
        self.controlPanel = wx.Panel(self.panel,-1,size=(500,340))
        vbox.Add(self.annotationTXT,0,wx.EXPAND|wx.ALL,2)
        vbox.Add(self.controlPanel,0,wx.EXPAND)
        self.panel.SetSizer(vbox)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1,20))
        for i,(triger,value) in enumerate(self.triggerList):
            annotation =  self.annotationListHZ[i].split('xx')[0]
            trigerCheck = wx.CheckBox(self.controlPanel,-1,label=annotation,name="Trigger%d"%i)
            trigerCheck.SetValue(True if triger==1 else False)
            hbox = wx.BoxSizer()
            hbox.Add((20,-1))
            if i==0:
                hbox.Add(trigerCheck, 0, wx.TOP, 3)
                self.expireDayCombo=wx.ComboBox(self.controlPanel,-1,value=str(value),choices=['30','60','90'],size=(60,-1))
                self.expireDayCombo.Bind(wx.EVT_COMBOBOX, self.OnExpireDayChanged)
                hbox.Add(self.expireDayCombo,0,0)
                hbox.Add((5,-1))
                hbox.Add(wx.StaticText(self.controlPanel,-1,"天;"),0,wx.TOP,3)
            elif i==8:
                hbox.Add(trigerCheck, 0, wx.TOP, 3)
                self.deliverCombo=wx.ComboBox(self.controlPanel, -1, value=self.DeliverList[value], choices=self.DeliverList, size=(130, -1))
                self.deliverCombo.Bind(wx.EVT_COMBOBOX, self.OnDeliverChanged)
                hbox.Add(self.deliverCombo, 0, 0)
                hbox.Add((5,-1))
                hbox.Add(wx.StaticText(self.controlPanel,-1,";"),0,wx.TOP,3)
            else:
                hbox.Add(trigerCheck, 0, 0)
            vbox.Add(hbox)
        self.controlPanel.SetSizer(vbox)
        self.panel.Thaw()

    def RefreshAnnotation(self):
        self.fileName = "D:\\IPMS\\dist\\config\\%s备注.txt"%self.language
        with open(self.fileName,'r',encoding='utf=8') as file:
            data = file.readlines()
        self.annotationList= []
        for item in data:
            # item = item.strip('\n')
            self.annotationList.append(item)
        self.content=""
        index = 0
        for i,(triger, value) in enumerate(self.triggerList):
            content=""
            if triger == 1:
                index += 1
                content = "%i. "%index+self.annotationList[i]
                if i == 0:
                    content = content.replace('xx',str(value))
                if i== 8:
                    content = content.replace('xx', self.DeliverList[value])
                self.content+=content
        for annotation in self.annotationAdditonList:
            content = ""
            if annotation:
                index += 1
                content = content = "%i. "%index+annotation+';\n'
                self.content+=content
        self.annotationTXT.SetValue(self.content)

    def OnCheckChanged(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        index = int(name[-1])
        self.triggerList[index][0] = 1 if obj.GetValue() else 0
        self.RefreshAnnotation()
        if index == 0:
            self.expireDayCombo.Enable(obj.GetValue())
        if index == 8:
            self.deliverCombo.Enable(obj.GetValue())

    def OnExpireDayChanged(self, event):
        self.triggerList[0][1] = int(self.expireDayCombo.GetValue())
        self.RefreshAnnotation()

    def OnDeliverChanged(self,event):
        self.triggerList[8][1] = int(self.deliverCombo.GetSelection())
        self.RefreshAnnotation()

    def OnAddNoteButton1(self,event):
        dlg = wx.TextEntryDialog(
            self, '请输入备注的中/英文信息',
            '信息输入', '')
        dlg.SetValue(self.annotationAdditonList[0])
        if dlg.ShowModal() == wx.ID_OK:
            self.annotationAdditonList[0]=dlg.GetValue()
        dlg.Destroy()
        self.RefreshAnnotation()


    def OnAddNoteButton2(self,event):
        dlg = wx.TextEntryDialog(
            self, '请输入备注的中/英文信息',
            '信息输入', '')
        dlg.SetValue(self.annotationAdditonList[1])
        if dlg.ShowModal() == wx.ID_OK:
            self.annotationAdditonList[1]=dlg.GetValue()
        dlg.Destroy()
        self.RefreshAnnotation()

    def OnAddNoteButton3(self,event):
        dlg = wx.TextEntryDialog(
            self, '请输入备注的中/英文信息',
            '信息输入', '')
        dlg.SetValue(self.annotationAdditonList[2])
        if dlg.ShowModal() == wx.ID_OK:
            self.annotationAdditonList[2]=dlg.GetValue()
        dlg.Destroy()
        self.RefreshAnnotation()

    def OnOk(self,event):
        UpdateOrderAnnotationTriggerList(self.log, WHICHDB, self.triggerList, self.id)
        temp = copy.deepcopy(self.annotationAdditonList)
        temp.append(self.language)
        UpdateOrderAnnotation(self.log, WHICHDB, self.id, temp)
        event.Skip()

    def OnLanguageChanged(self,event):
        self.language = self.languageCombo.GetValue()
        self.DeliverList = ["不包含运费", "包含运费", "包含到港口的运费"] if self.language == '中文' else ["EX", "DAP", "CIF"]
        self.deliverCombo.Items=self.DeliverList
        self.deliverCombo.SetValue(self.DeliverList[self.triggerList[8][1]])
        self.RefreshAnnotation()
