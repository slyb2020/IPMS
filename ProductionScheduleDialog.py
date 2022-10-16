import wx
import os
from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
from ID_DEFINE import *
from MakePdfReport import *
from DBOperation import GetPropertySchedulePageRowNumber,GetOrderPanelRecord,GetGluepageFromGlueNum,GetGlueLabelpageFromGlueNum
# from DataGrid import DataGrid
import numpy as np
import images
import wx.grid as gridlib

class PDFViewerPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        hsizer = wx.BoxSizer( wx.HORIZONTAL )
        vsizer = wx.BoxSizer( wx.VERTICAL )
        self.buttonpanel = pdfButtonPanel(self, wx.ID_ANY,
                                wx.DefaultPosition, wx.DefaultSize, 0)
        vsizer.Add(self.buttonpanel, 0, wx.GROW|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.viewer = pdfViewer( self, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
        vsizer.Add(self.viewer, 1, wx.GROW|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        # loadbutton = wx.Button(self, wx.ID_ANY, "Load PDF file",
        #                         wx.DefaultPosition, wx.DefaultSize, 0 )
        # vsizer.Add(loadbutton, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        hsizer.Add(vsizer, 1, wx.GROW|wx.ALL, 5)
        self.SetSizer(hsizer)
        self.SetAutoLayout(True)

        # introduce buttonpanel and viewer to each other
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel

        # self.Bind(wx.EVT_BUTTON, self.OnLoadButton, loadbutton)

    def OnLoadButton(self, event):
        dlg = wx.FileDialog(self, wildcard="*.pdf")
        if dlg.ShowModal() == wx.ID_OK:
            wx.BeginBusyCursor()
            self.viewer.LoadFile(dlg.GetPath())
            wx.EndBusyCursor()
        dlg.Destroy()

class ProductionScheduleDialog(wx.Dialog):
    def __init__(self, parent, log, orderID, suborderID = None,size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.orderID = orderID
        self.subOrderID = suborderID
        self.parent = parent
        self.log = log
        _, self.pageRowNum = GetPropertySchedulePageRowNumber(self.log,1)
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        if self.subOrderID == None:
            dirName = scheduleDir + '%s/' % self.orderID
        else:
            dirName = scheduleDir + '%s/' % self.orderID + '%s/'%(int(self.subOrderID))
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "排产操作对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(1200, 900))
        hbox = wx.BoxSizer()
        controlPanel = wx.Panel(panel,size=(150,-1))
        hbox.Add(controlPanel,0,wx.EXPAND)
        pdfPanel = wx.Panel(panel,size=(100,-1))
        hbox.Add(pdfPanel,1,wx.EXPAND)
        panel.SetSizer(hbox)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(panel, label='订单编号：'), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(panel, size=(50, 25),style=wx.TE_READONLY)
        self.newOrderIDTXT.SetValue('%05d' % int(self.orderID))
        hbox.Add(self.newOrderIDTXT, 1, wx.LEFT | wx.RIGHT, 10)
        vbox.Add(hbox, 0, wx.EXPAND)
        if self.subOrderID != None:
            vbox.Add((-1, 10))
            hbox = wx.BoxSizer()
            hbox.Add(10, -1)
            hbox.Add(wx.StaticText(panel, label='子订单号：'), 0, wx.TOP, 5)
            self.subOrderIDTXT = wx.TextCtrl(panel, size=(50, 25),style=wx.TE_READONLY)
            self.subOrderIDTXT.SetValue('%03d' %int(self.subOrderID))
            hbox.Add(self.subOrderIDTXT, 1, wx.LEFT | wx.RIGHT, 10)
            vbox.Add(hbox, 0, wx.EXPAND)

        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.materialScheduleButton = wx.Button(controlPanel, label="材料出库单", size=(90, 40))
        self.materialScheduleButton.Bind(wx.EVT_BUTTON, self.OnMaterialScheduleBTN)
        hhbox.Add(self.materialScheduleButton, 1, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.verticalCuttingScheduleButton = wx.Button(controlPanel, label="横剪任务单", size=(90, 40))
        self.verticalCuttingScheduleButton.Bind(wx.EVT_BUTTON, self.OnVerticalCuttingScheduleBTN)
        hhbox.Add(self.verticalCuttingScheduleButton, 1, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.cutScheduleButton = wx.Button(controlPanel, label="剪板机任务单", size=(90, 40))
        self.cutScheduleButton.Bind(wx.EVT_BUTTON, self.OnCutScheduleBTN)
        hhbox.Add(self.cutScheduleButton, 1, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.bendScheduleButton = wx.Button(controlPanel, label="折弯任务单", size=(90, 40))
        self.bendScheduleButton.Bind(wx.EVT_BUTTON, self.OnBendScheduleBTN)
        hhbox.Add(self.bendScheduleButton, 1, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.orticFormingScheduleButton = wx.Button(controlPanel, label="构件成型任务单", size=(90, 40))
        self.orticFormingScheduleButton.Bind(wx.EVT_BUTTON, self.OnFormingScheduleBTN)
        hhbox.Add(self.orticFormingScheduleButton, 1, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.S2FormingScheduleButton = wx.Button(controlPanel, label="2S成型任务单", size=(90, 40))
        self.S2FormingScheduleButton.Bind(wx.EVT_BUTTON, self.OnS2FormingScheduleBTN)
        hhbox.Add(self.S2FormingScheduleButton, 1, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.ceilingFormingScheduleButton = wx.Button(controlPanel, label="天花板成型任务单", size=(90, 40))
        self.ceilingFormingScheduleButton.Bind(wx.EVT_BUTTON, self.OnCeilingFormingScheduleBTN)
        hhbox.Add(self.ceilingFormingScheduleButton, 1, wx.EXPAND|wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))

        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.PRPressScheduleButton = wx.Button(controlPanel, label="热压任务单", size=(90, 40))
        self.PRPressScheduleButton.Bind(wx.EVT_BUTTON, self.OnPRPressScheduleTN)
        hhbox.Add(self.PRPressScheduleButton, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        hhbox.Add((10, -1))
        self.vacuumScheduleButton = wx.Button(controlPanel, label="特制品任务单", size=(90, 40))
        self.vacuumScheduleButton.Bind(wx.EVT_BUTTON, self.OnVacuumScheduleBTN)
        hhbox.Add(self.vacuumScheduleButton, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hhbox,1,wx.EXPAND)
        vbox.Add((-1,5))

        # hhbox = wx.BoxSizer()
        # hhbox.Add((10, -1))
        # self.packageScheduleButton = wx.Button(controlPanel, label="打包任务单", size=(90, 40))
        # self.packageScheduleButton.Bind(wx.EVT_BUTTON, self.OnOpenFileBTN)
        # hhbox.Add(self.packageScheduleButton, 1, wx.EXPAND|wx.ALL, 5)
        # vbox.Add(hhbox,1,wx.EXPAND)


        # vbox.Add((-1,10))
        # self.cutScheduleButton = wx.Button(controlPanel, label="裁切计划", size=(100, 100))
        # self.cutScheduleButton.Bind(wx.EVT_BUTTON, self.OnOpenFileBTN)
        # vbox.Add(self.cutScheduleButton, 0, wx.EXPAND | wx.ALL, 10)
        controlPanel.SetSizer(vbox)
        # panel.SetBackgroundColour(wx.Colour(234,219,212))
        sizer.Add(panel, 0, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)
        vbox=wx.BoxSizer(wx.VERTICAL)
        self.pdfViewerPanel = PDFViewerPanel(pdfPanel,self.log)
        vbox.Add(self.pdfViewerPanel,1,wx.EXPAND)
        pdfPanel.SetSizer(vbox)


        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap(bitmapDir+"/33.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 40))
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 40))
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

    def OnMaterialScheduleBTN(self, event):
        filename = scheduleDir+'%s/%s/MaterialSchedule.pdf'%(self.orderID,int(self.subOrderID))
        if not os.path.exists(filename):
            MakeMaterialScheduleTemplate(self.orderID, self.subOrderID, filename, self.parent.productionSchedule.horizontalCuttingScheduleList,self.parent.productionSchedule.cuttingScheduleList,PAGEROWNUMBER=self.pageRowNum)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnVerticalCuttingScheduleBTN(self, event):
        filename = scheduleDir+'%s/%s/VerticalCutSchedule.pdf'%(self.orderID,int(self.subOrderID))
        if not os.path.exists(filename):
            MakeHorizontalCutScheduleTemplate(self.orderID, self.subOrderID, filename, self.parent.productionSchedule.horizontalCuttingScheduleList,PAGEROWNUMBER=self.pageRowNum)  #这些数据在ProductionScheduleAlgorithm.py文件中
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnCutScheduleBTN(self, event):
        filename = scheduleDir+'%s/%s/CutSchedule.pdf'%(self.orderID,int(self.subOrderID))
        if not os.path.exists(filename):
            MakeCutScheduleTemplate(self.orderID,self.subOrderID,filename,self.parent.productionSchedule.cuttingScheduleList,PAGEROWNUMBER=self.pageRowNum)  #这些数据在ProductionScheduleAlgorithm.py文件中
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnBendScheduleBTN(self, event):
        filename = scheduleDir+'%s/%s/BendingSchedule.pdf'%(self.orderID,int(self.subOrderID))
        if not os.path.exists(filename):
            MakeBendingScheduleTemplate(self.orderID,self.subOrderID,filename,self.parent.productionSchedule.bendingScheduleList,PAGEROWNUMBER=self.pageRowNum)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnS2FormingScheduleBTN(self, event):
        filename = scheduleDir+'%s/%s/S2FormingSchedule.pdf'%(self.orderID,int(self.subOrderID))
        if not os.path.exists(filename):
            MakeS2FormingScheduleTemplate(self.orderID,self.subOrderID,filename,self.parent.productionSchedule.S2FormingScheduleList,PAGEROWNUMBER=self.pageRowNum)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnCeilingFormingScheduleBTN(self, event):
        filename = scheduleDir+'%s/%s/CeilingFormingSchedule.pdf'%(self.orderID,int(self.subOrderID))
        if not os.path.exists(filename):
            MakeCeilingFormingScheduleTemplate(self.orderID,self.subOrderID,filename,self.parent.productionSchedule.ceilingFormingScheduleList,PAGEROWNUMBER=self.pageRowNum)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnPRPressScheduleTN(self, event):
        filename = scheduleDir+'%s/%s/PRPressSchedule.pdf'%(self.orderID,int(self.subOrderID))
        if not os.path.exists(filename):
            MakePRPressScheduleTemplate(self.orderID,self.subOrderID,filename,self.parent.productionSchedule.prScheduleList,PAGEROWNUMBER=self.pageRowNum)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnVacuumScheduleBTN(self, event):
        filename = scheduleDir+'%s/%s/VacuumSchedule.pdf'%(self.orderID,int(self.subOrderID))
        if not os.path.exists(filename):
            MakeVacuumScheduleTemplate(self.orderID,self.subOrderID,filename,self.parent.productionSchedule.vacuumScheduleList,PAGEROWNUMBER=self.pageRowNum)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnFormingScheduleBTN(self, event):
        filename = scheduleDir+'%s/FormingSchedule.pdf'%self.orderID
        if not os.path.exists(filename):
            MakeFormingScheduleTemplate(filename)
        else:
            MakeFormingScheduleTemplate(filename)
        self.pdfViewerPanel.viewer.LoadFile(filename)

    def OnOpenFileBTN(self, event):
        self.pdfViewerPanel.viewer.LoadFile("Excel/Stena 生产图纸 2SA.pdf")

    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()


class GlueSheetManagementDailog(wx.Dialog):
    def __init__(self, parent, log, orderID, suborderID = None,size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.orderID = orderID
        self.subOrderID = suborderID
        self.parent = parent
        self.log = log
        self.filename = scheduleDir + '%s/%s/GlueNoSheet.pdf' % (orderID,suborderID)
        self.labelfilename = scheduleDir + '%s/%s/GlueLabelSheet.pdf' % (orderID,suborderID)
        if self.subOrderID == None:
            dirName = scheduleDir + '%s/' % self.orderID
        else:
            dirName = scheduleDir + '%s/' % self.orderID + '%s/'%(int(self.subOrderID))
        if not os.path.exists(dirName):
            os.makedirs(dirName)
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "面板胶水单/标签管理窗口", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, size=(1600, 900))
        hbox = wx.BoxSizer()
        controlPanel = wx.Panel(panel,size=(835,-1))
        hbox.Add(controlPanel,0,wx.EXPAND)
        self.notebook = wx.Notebook(panel, -1, size=(21, 21), style=
                                    wx.BK_DEFAULT
                                    # wx.BK_TOP
                                    # wx.BK_BOTTOM
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
        hbox.Add(self.notebook, 1, wx.EXPAND)
        gluePanel = wx.Panel(self.notebook,size=(100,-1))
        self.notebook.AddPage(gluePanel,"胶水单")
        glueLabelPanel = wx.Panel(self.notebook,size=(100,-1))
        self.notebook.AddPage(glueLabelPanel,"不干胶标签")
        panel.SetSizer(hbox)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 20))
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        hbox.Add(wx.StaticText(controlPanel, label='订单编号：'), 0, wx.TOP, 5)
        self.newOrderIDTXT = wx.TextCtrl(controlPanel, size=(50, 25),style=wx.TE_READONLY)
        self.newOrderIDTXT.SetValue('%05d' % int(self.orderID))
        hbox.Add(self.newOrderIDTXT, 1, wx.LEFT | wx.RIGHT, 10)
        if self.subOrderID != None:
            hbox.Add(20, -1)
            hbox.Add(wx.StaticText(controlPanel, label='子订单号：'), 0, wx.TOP, 5)
            self.subOrderIDTXT = wx.TextCtrl(controlPanel, size=(50, 25),style=wx.TE_READONLY)
            self.subOrderIDTXT.SetValue('%03d' %int(self.subOrderID))
            hbox.Add(self.subOrderIDTXT, 1, wx.LEFT | wx.RIGHT, 10)
            vbox.Add(hbox, 0, wx.EXPAND)
        _,data = GetOrderPanelRecord(self.log, 1, self.orderID,self.subOrderID)
        data=np.array(data)
        data=data[:,3:]
        titleList = ['甲板', '区域', '房间', '图纸', '面板代码', 'X面颜色', 'Y面颜色', '高度', '宽度', '厚度',
                                '数量', 'Z面颜色', 'V面颜色', '胶水单号']
        colSizeList = [35, 50, 70, 80, 60, 60, 40, 40, 40, 40, 50, 50, 70, 72]
        self.panelsGrid = DataGrid(controlPanel,data,titleList,colSizeList, log=self.log)
        self.panelsGrid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        vbox.Add(self.panelsGrid,1,wx.LEFT|wx.TOP|wx.BOTTOM|wx.EXPAND,10)
        controlPanel.SetSizer(vbox)
        # panel.SetBackgroundColour(wx.Colour(234,219,212))
        sizer.Add(panel, 0, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)
        vbox=wx.BoxSizer(wx.VERTICAL)
        self.gluePDFViewerPanel = PDFViewerPanel(gluePanel, self.log)
        vbox.Add(self.gluePDFViewerPanel, 1, wx.EXPAND)
        gluePanel.SetSizer(vbox)
        self.gluePDFViewerPanel.viewer.LoadFile(self.filename)
        vbox=wx.BoxSizer(wx.VERTICAL)
        self.glueLabelPDFViewerPanel = PDFViewerPanel(glueLabelPanel, self.log)
        vbox.Add(self.glueLabelPDFViewerPanel, 1, wx.EXPAND)
        glueLabelPanel.SetSizer(vbox)
        self.glueLabelPDFViewerPanel.viewer.LoadFile(self.labelfilename)


        # btnsizer = wx.BoxSizer()
        # bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
        # btn_ok = wx.Button(self, wx.ID_OK, "返回", size=(400, 40))
        # btn_ok.SetBitmap(bitmap1, wx.LEFT)
        # btnsizer.Add(btn_ok, 0)
        # sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        # manualInputBTN.Bind(wx.EVT_BUTTON, self.OnCancel)

    def OnCellLeftClick(self, evt):
        row = evt.GetRow()
        evt.Skip()
        glueNum = self.panelsGrid.data[row][-1]
        _, gluePage = GetGluepageFromGlueNum(self.log,1,self.orderID,glueNum)
        self.gluePDFViewerPanel.viewer.GoPage(int(gluePage) - 1)
        _, glueLabelPage = GetGlueLabelpageFromGlueNum(self.log,1,self.orderID,glueNum)
        self.glueLabelPDFViewerPanel.viewer.GoPage(int(glueLabelPage) - 1)

    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()