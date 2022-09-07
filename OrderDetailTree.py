import wx
from math import *
from ID_DEFINE import *
import string
import images
import xml.etree.ElementTree as ET
import os
import cv2
from ImportOrderDialog import InputNewOrderDialog
from DBOperation import GetOrderDetailRecord,InsertOrderDetailRecord
import numpy as np

class OrderDetailTree(wx.Panel):
    def __init__(self, parent, master,log, orderID,structure,size=wx.DefaultSize, ):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1, size=size, style=wx.BORDER_THEME)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.master = master
        self.log = log
        self.orderID = orderID
        # self.dataList = structureList[1]
        subOrderList,deckOrderList,zoneOrderList,roomOrderList=structure
        # datasetList = [
        #     ["ImageNet", [["2017", []], ["2018", []]]],
        #     ["FasionMNIST", [["2007", []], ["2012", []]]],
        #     ["MNIST", [["2007", []], ["2012", []]]],
        #     ["猫狗大战", []],
        # ]

        tID = wx.NewIdRef()
        self.tree = wx.TreeCtrl(self, tID, wx.DefaultPosition, size,
                               wx.TR_HAS_BUTTONS
                               | wx.TR_EDIT_LABELS
                               # | wx.TR_MULTIPLE
                               # | wx.TR_HIDE_ROOT
                               )
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        smileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        # smileidx    = il.Add(images.Smiles.GetBitmap())
        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot('订单%s'%self.orderID)
        self.tree.SetItemData(self.root, "根")
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
        # subOrderList=['1','2','3']
        # deckOrderList=[
        #     [1],
        #     [1,2],
        #     [1,2,3],
        # ]
        # zoneOrderList=[
        #     [
        #         [1,2,3]
        #     ],
        #     [
        #         [1,2,3],
        #         [1,2,3],
        #     ],
        #     [
        #         [1,2,3],
        #         [1,2,3],
        #         [1,2,3]
        #     ],
        # ]
        # roomOrderList=[
        #     [
        #         [
        #             [1,],[1,2],[1,2,3]
        #         ]
        #     ],
        #     [
        #         [
        #             [1,2,3],[1,2,3],[1,2,3]
        #         ],
        #         [
        #             [1,2,3],[1,2,3],[1,2,3]
        #         ],
        #     ],
        #     [
        #         [
        #             [1,2,3],[1,2,3],[1,2,3]
        #         ],
        #         [
        #             [1,2,3],[1,2,3],[1,2,3]
        #         ],
        #         [
        #             [1,2,3],[1,2,3],[1,2,3]
        #         ]
        #     ],
        # ]

        for subOrderNum, subOrder in enumerate(subOrderList):
            sub = self.tree.AppendItem(self.root, "子订单"+subOrder)
            self.tree.SetItemData(sub, "子订单_"+str(subOrder))
            self.tree.SetItemImage(sub, fldridx, wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(sub, fldropenidx, wx.TreeItemIcon_Expanded)
            for deckOrderNum, deckOrder in enumerate(deckOrderList[subOrderNum]):
                deck = self.tree.AppendItem(sub, "甲板" + str(deckOrder))
                self.tree.SetItemData(deck, "甲板订单_"+str(subOrder)+'_'+str(deckOrder))
                self.tree.SetItemImage(deck, fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(deck, fldropenidx, wx.TreeItemIcon_Expanded)
                for zoneOrderNum, zoneOrder in enumerate(zoneOrderList[subOrderNum][deckOrderNum]):
                    zone = self.tree.AppendItem(deck,"区域" + str(zoneOrder))
                    self.tree.SetItemData(zone, "区域订单_"+str(subOrder)+'_'+str(deckOrder)+'_'+str(zoneOrder))
                    self.tree.SetItemImage(zone, fldridx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(zone, fldropenidx, wx.TreeItemIcon_Expanded)
                    for roomOrderNum,roomOrder in enumerate(roomOrderList[subOrderNum][deckOrderNum][zoneOrderNum]):
                        room = self.tree.AppendItem(zone, "房间" + str(roomOrder))
                        self.tree.SetItemData(room, "房间订单_"+str(subOrder)+'_'+str(deckOrder)+'_'+str(zoneOrder)+'_'+str(roomOrder))
                        self.tree.SetItemImage(room, fldridx, wx.TreeItemIcon_Normal)
                        self.tree.SetItemImage(room, fldropenidx, wx.TreeItemIcon_Expanded)
        self.tree.ExpandAll()
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

    def OnLeftDown(self,event):
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)
        try:
            itemData = self.tree.GetItemData(item)
        except:
            event.Skip()
            return
        if itemData == "根":
            self.master.showRange=[]
            self.master.ReCreteOrderDetailGridPanel()
        else:
            self.master.showRange = itemData.split("_")
            self.master.ReCreteOrderDetailGridPanel()
            # if dataList[0]=='子订单':
            #     subOrderID=dataList[1]
            # elif dataList[0]=='甲板订单':
            #     subOrderID=dataList[1]
            #     deckOrderID=dataList[2]
            # elif dataList[0]=='区域订单':
            #     subOrderID=dataList[1]
            #     deckOrderID=dataList[2]
            #     zoneOrderID=dataList[3]
            # elif dataList[0]=='房间订单':
            #     subOrderID=dataList[1]
            #     deckOrderID=dataList[2]
            #     zoneOrderID=dataList[3]
            #     roomOrderID=dataList[4]
        event.Skip()

    def OnRightDown(self, event):
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item:
            self.tree.SelectItem(item)
            # if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewIdRef()
            self.popupID2 = wx.NewIdRef()
            self.popupID3 = wx.NewIdRef()
            self.popupID4 = wx.NewIdRef()
            self.popupID5 = wx.NewIdRef()
            self.popupID6 = wx.NewIdRef()
            self.popupID7 = wx.NewIdRef()
            self.popupID8 = wx.NewIdRef()
            self.popupID9 = wx.NewIdRef()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
            self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
            self.Bind(wx.EVT_MENU, self.OnPopupEight, id=self.popupID8)
            self.Bind(wx.EVT_MENU, self.OnPopupNine, id=self.popupID9)

            menu = wx.Menu()
            item1 = wx.MenuItem(menu, self.popupID1,"新建子订单")
            item1.Enable(False)
            menu.Append(item1)
            item2 = wx.MenuItem(menu, self.popupID2,"新建甲板订单")
            item2.Enable(False)
            menu.Append(item2)
            item3 = wx.MenuItem(menu, self.popupID3,"新建区域订单")
            item3.Enable(False)
            menu.Append(item3)
            item4 = wx.MenuItem(menu, self.popupID4,"新建房间订单")
            item4.Enable(False)
            menu.Append(item4)
            item5 = wx.MenuItem(menu, self.popupID5,"新建零件订单")
            item5.Enable(False)
            menu.Append(item5)
            if self.tree.GetItemData(item) == '根':
                item1.Enable(True)
            elif self.tree.GetItemData(item) == '子订单':
                item2.Enable(True)
            elif self.tree.GetItemData(item) == '区域订单':
                item3.Enable(True)
            elif self.tree.GetItemData(item) == '房间订单':
                item4.Enable(True)
            else:
                item5.Enable(True)


            # Popup the menu.  If an item is selected then its handler
            # will be called before PopupMenu returns.
            self.PopupMenu(menu)
            menu.Destroy()

    def TreeDataTransform(self,orderDetailData):
        orderTreeData = np.array(orderDetailData)
        subOrderIDList = list(orderTreeData[:,2])#提出所有子订单号组成列表
        subOrderIDList = set(subOrderIDList)#得到所有不重复的子订单号
        result=[]
        for keyword in subOrderIDList:
            temp = []
            for subOrder in orderDetailData:
                if str(subOrder[2])==str(keyword):
                    temp.append(subOrder)
            result.append([keyword,temp])#把订单按子订单分好
        for subOrderIndex,subOrder in enumerate(result):
            # subOrderKeyword = subOrder[0]
            deckOrderInThisSubOrderList = subOrder[1]
            deckOrderArray = np.array(deckOrderInThisSubOrderList)
            deckIDList = list(deckOrderArray[:,3])
            deckIDList = set(deckIDList)
            deckOrderList = []
            for keyword in deckIDList:
                temp = []
                for deckOrderIndex,deckOrder in enumerate(deckOrderInThisSubOrderList):
                    if str(deckOrder[3]) == str(keyword):
                        temp.append(deckOrder)
                deckOrderList.append([keyword,temp])
            result[subOrderIndex][1]=deckOrderList

        for subOrderIndex,subOrder in enumerate(result):
            deckOrderInThisSubList = subOrder[1]
            for zoneOrderIndex,zoneOrderInThisDeck in enumerate(deckOrderInThisSubList):
                zoneOrderInThisDeckList=zoneOrderInThisDeck[1]
                zoneOrderArray = np.array(zoneOrderInThisDeckList)
                zoneIDList = list(zoneOrderArray[:,4])
                zoneIDList = set(zoneIDList)
                zoneOrderList = []
                for keyword in zoneIDList:
                    temp = []
                    for zoneOrder in zoneOrderInThisDeckList:
                        if str(zoneOrder[4]) == str(keyword):
                            temp.append(zoneOrder)
                    zoneOrderList.append([keyword,temp])
                result[subOrderIndex][1][zoneOrderIndex][1]=zoneOrderList

        for subOrderIndex,subOrder in enumerate(result):
            deckOrderInThisSubList = subOrder[1]
            for zoneOrderIndex,zoneOrderInThisDeck in enumerate(deckOrderInThisSubList):
                zoneOrderInThisDeckList=zoneOrderInThisDeck[1]
                for roomOrderIndex,roomOrderInThisZone in enumerate(zoneOrderInThisDeckList):
                    roomOrderInThisZoneList = roomOrderInThisZone[1]
                    roomOrderArray = np.array(roomOrderInThisZoneList)
                    roomIDList = list(roomOrderArray[:,5])
                    roomIDList = set(roomIDList)
                    roomOrderList = []
                    for keyword in roomIDList:
                        temp = []
                        for roomOrder in roomOrderInThisZoneList:
                            if str(roomOrder[5]) == str(keyword):
                                temp.append(roomOrder)
                        roomOrderList.append([keyword,temp])
                result[subOrderIndex][1][zoneOrderIndex][1][roomOrderIndex][1]=roomOrderList
        return result

    def OnPopupOne(self, event):
        self.log.WriteText("Popup one\n")
        dlg = InputNewOrderDialog(self,self.orderID)
        if dlg.ShowModal()==wx.ID_OK:
            InsertOrderDetailRecord(self.log,1,1)
            dlg.Destroy()
            _, orderDetailData = GetOrderDetailRecord(self.log, 1, self.orderID)
            self.dataList = TreeDataTransform(self.orderDetailData)
            self.ReCreateTree()

    def OnPopupTwo(self, event):
        self.log.WriteText("Popup two\n")

    def OnPopupThree(self, event):
        self.log.WriteText("Popup three\n")

    def OnPopupFour(self, event):
        self.log.WriteText("Popup four\n")

    def OnPopupFive(self, event):
        self.log.WriteText("Popup five\n")

    def OnPopupSix(self, event):
        self.log.WriteText("Popup six\n")

    def OnPopupSeven(self, event):
        self.log.WriteText("Popup seven\n")

    def OnPopupEight(self, event):
        self.log.WriteText("Popup eight\n")

    def OnPopupNine(self, event):
        self.log.WriteText("Popup nine\n")

    def OnSize(self, event):
        w, h = self.GetClientSize()
        self.tree.SetSize(0, 0, w, h)

    def OnBeginEdit(self, event):
        event.Veto()

    def OnEndEdit(self, event):
        event.Veto()

    def ReCreateTree(self):
        self.tree.Destroy()
        tID = wx.NewIdRef()
        self.tree = wx.TreeCtrl(self, tID, wx.DefaultPosition,size=wx.DefaultSize,style=
                               wx.TR_HAS_BUTTONS
                               | wx.TR_EDIT_LABELS
                               # | wx.TR_MULTIPLE
                               # | wx.TR_HIDE_ROOT
                               )
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        smileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_OTHER, isz))
        # smileidx    = il.Add(images.Smiles.GetBitmap())
        self.tree.SetImageList(il)
        self.il = il
        self.root = self.tree.AddRoot('订单%s'%self.orderID)
        self.tree.SetItemData(self.root, "根")
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
        subOrderTreePass = True if len(self.dataList)==1 else False
        for subOrderList in self.dataList:
            if not subOrderTreePass:
                sub = self.tree.AppendItem(self.root, subOrderList[0])
                self.tree.SetItemData(sub, "子订单")
                self.tree.SetItemImage(sub, fldridx, wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(sub, fldropenidx, wx.TreeItemIcon_Expanded)
            else:
                sub = self.root
            deckOrderTreePass = True if len(subOrderList[1])==1 else False
            for deckOrderList in subOrderList[1]:
                if not deckOrderTreePass:
                    deck = self.tree.AppendItem(sub, deckOrderList[0])
                    self.tree.SetItemData(deck, "甲板订单")
                    self.tree.SetItemImage(deck, fldridx, wx.TreeItemIcon_Normal)
                    self.tree.SetItemImage(deck, fldropenidx, wx.TreeItemIcon_Expanded)
                else:
                    deck = sub
                zoneOrderTreePass = True if len(deckOrderList[1])==1 else False
                for zoneOrderList in deckOrderList[1]:
                    if not zoneOrderTreePass:
                        zone = self.tree.AppendItem(deck, zoneOrderList[0])
                        self.tree.SetItemData(zone, "区域订单")
                        self.tree.SetItemImage(zone, fileidx, wx.TreeItemIcon_Normal)
                        self.tree.SetItemImage(zone, smileidx, wx.TreeItemIcon_Selected)
                    else:
                        zone = deck
                    roomOrderTreePass = True if len(zoneOrderList[1])==1 else False
                    for roomOrderList in zoneOrderList[1]:
                        if not roomOrderTreePass:
                            room = self.tree.AppendItem(zone, roomOrderList[0])
                            self.tree.SetItemData(room, "房间订单")
                            self.tree.SetItemImage(room, fileidx, wx.TreeItemIcon_Normal)
                            self.tree.SetItemImage(room, smileidx, wx.TreeItemIcon_Selected)
                        else:
                            room = zone
                        for componentList in roomOrderList[1]:
                            item = self.tree.AppendItem(zone, componentList[6])
                            self.tree.SetItemData(item, "零件订单")
                            self.tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)
                            self.tree.SetItemImage(item, smileidx, wx.TreeItemIcon_Selected)

        self.tree.ExpandAll()
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.tree,1,wx.EXPAND)
        self.SetSizer(vbox)
        self.Layout()
        # self.tree.Refresh()
