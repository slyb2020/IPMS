#!/usr/bin/env python
# encoding: utf-8
"""
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: ID_DEFINE.py.py
@time: 2019/6/16 15:23
@desc:
"""
import os
import wx

# 需要设置的参数：
# 1.工单存放文件夹
# dirName = 'D:\\IPMS\\dist\\'
# bitmapDir = 'D:\\IPMS\\dist\\bitmaps\\'
# scheduleDir = 'D:\\IPMS\\dist\\工单\\'
# bluePrintDir = 'D:\\IPMS\\dist\\Stena 生产图纸\\'
# quotationSheetDir = 'D:\\IPMS\\dist\\报价单\\'
dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = "D:/IPMS/dist/bitmaps"
scheduleDir = os.path.join(dirName, '工单/')
bluePrintDir = os.path.join(dirName, 'Stena 生产图纸/')
quotationSheetDir = os.path.join(dirName, '报价单/')
# sys.path.append(os.path.split(dirName)[0])

WHICHDB = 3


dbHostName = ["127.0.0.1", '127.0.0.1', '192.168.1.108','123.60.44.240']
dbUserName = ['root', 'root', 'slyb','root']
dbPassword = ['', '', 'Freescalejm60','mysql123']
dbName = ['智能生产管理系统', '智能生产管理系统_调试', '智能生产管理系统_调试', '智能生产管理系统_调试']
orderDBName = ['订单数据库', '订单数据库_调试', '订单数据库_调试', '订单数据库_调试']
packageDBName = ['货盘数据库', '货盘数据库_调试', '货盘数据库_调试', '货盘数据库_调试']
orderCheckDBName = ['订单审核数据库', '订单审核数据库_调试', '订单审核数据库_调试', '订单审核数据库_调试']
orderDetailLabelList = ['Index', '订单号', '子订单', '甲板', '区域', '房间', '图纸', '面板代码', 'X面颜色', 'Y面颜色', '高度', '宽度', '厚度', '数量',
                        'Z面颜色', 'V面颜色', '胶水单号']
orderDetailColSizeList = [30, 40, 50, 35, 35, 50, 70, 80, 60, 60, 40, 40, 40, 40, 50, 50, 70, 70]
orderWorkingStateList = ['接单', '排产', '下料', '加工', '打包', '发货']

# WallCheckEnableSectionList = ['产品名称', '产品型号', '产品表面材料', '产品长度', '产品宽度', '产品厚度', '单位', '数量', '潮湿', '加强']
WallCheckEnableSectionList = ['产品名称', '产品表面材料', '产品长度', '产品宽度', '产品厚度', '单位', '数量', '潮湿', '加强']
CeilingCheckEnableSectionList = ['产品名称', '产品表面材料', '产品长度', '产品宽度', '产品厚度', '单位', '数量']
# WallCheckEnableSectionDic = {
#     "技术员": ['产品名称', '产品型号', '产品表面材料', '产品长度', '产品宽度', '产品厚度', '单位', '数量', '潮湿', '加强'],
#     "采购员": ['产品名称', '产品型号', '产品表面材料', '产品长度', '产品宽度', '产品厚度', '单位', '数量', '单价', '总价', '潮湿', '加强'],
# }
WallCheckEnableSectionDic = {
    "技术员": ['产品名称', '产品表面材料', '产品长度', '产品宽度', '产品厚度', '单位', '数量', '潮湿', '加强'],
    "采购员": ['产品名称', '产品表面材料', '产品长度', '产品宽度', '产品厚度', '单位', '数量', '单价', '总价', '潮湿', '加强'],
}

MeterialCharacterList = ['材料名', '规格', '供应商', '价格', '单位', '备注']
MeterialCharacterWidthList = [180, 180, 200, 160, 100, 100]

BIDMODE = ['wxPython Rules', 'wxPython Rocks', 'wxPython Is The Best']
BIDMETHOD = ['离岸价', '到岸价']

CheckTitleDict = {
    "WALL": ['Product \r\nNo.', 'Product \r\nSurface', 'Product \r\nHeight/Length (mm)',
             'Product \r\nNo.Wdith (mm)', 'Procuct \r\nNo.Thickness (mm)', 'Unit', 'Total \r\nQuantity',
             'Product \r\nWet','Product \r\nStrengthen'],
    "CEILING": ['Product \r\nNo.', 'Product \r\nSurface', 'Product \r\nHeight/Length (mm)',
             'Product \r\nNo.Wdith (mm)', 'Procuct \r\nNo.Thickness (mm)', 'Unit', 'Total \r\nQuantity',
             ]
    }
# CheckTitleDict = {
#     "WALL": ['Product \r\nNo.', 'Product \r\nType', 'Product \r\nSurface', 'Product \r\nHeight/Length (mm)',
#              'Product \r\nNo.Wdith (mm)', 'Procuct \r\nNo.Thickness (mm)', 'Unit', 'Total \r\nQuantity',
#              'Product \r\nDescription'],
#     "CEILING": ['Product \r\nNo.', 'Product \r\nType', 'Product \r\nSurface', 'Product \r\nHeight/Length (mm)',
#              'Product \r\nNo.Wdith (mm)', 'Procuct \r\nNo.Thickness (mm)', 'Unit', 'Total \r\nQuantity',
#              'Product \r\nDescription']
#     }
OtherCheckTitleDict = {
    "WALL": ['Product \r\nNo.', 'Product \r\nSurface', 'Product \r\nHeight/Length (mm)',
             'Procuct \r\nNo.Wdith (mm)', 'Procuct \r\nNo.Thickness (mm)', 'Unit', 'Total \r\nQuantity',
             'Unit \r\nPrice', 'Total \r\nPrice', 'Product \r\nWet'],
    "CEILING": ['Product \r\nNo.', 'Product \r\nSurface', 'Product \r\nHeight/Length (mm)',
             'Procuct \r\nNo.Wdith (mm)', 'Procuct \r\nNo.Thickness (mm)', 'Unit', 'Total \r\nQuantity',
             'Unit \r\nPrice', 'Total \r\nPrice', 'Product \r\nDescription']
    }
# OtherCheckTitleDict = {
#     "WALL": ['Product \r\nNo.', 'Product \r\nType', 'Product \r\nSurface', 'Product \r\nHeight/Length (mm)',
#              'Procuct \r\nNo.Wdith (mm)', 'Procuct \r\nNo.Thickness (mm)', 'Unit', 'Total \r\nQuantity',
#              'Unit \r\nPrice', 'Total \r\nPrice', 'Product \r\nDescription'],
#     "CEILING": ['Product \r\nNo.', 'Product \r\nType', 'Product \r\nSurface', 'Product \r\nHeight/Length (mm)',
#              'Procuct \r\nNo.Wdith (mm)', 'Procuct \r\nNo.Thickness (mm)', 'Unit', 'Total \r\nQuantity',
#              'Unit \r\nPrice', 'Total \r\nPrice', 'Product \r\nDescription']
#     }
CheckColWidthDict = {
    'WALL': [125, 125, 160, 150, 150, 150, 80, 150, 155],
    'CEILING': [125, 125, 160, 150, 150, 150, 80, 150, 155],
    }
OtherCheckColWidthDict = {
    'WALL': [125, 125, 160, 150, 150, 150, 80, 150, 80, 80, 155],
    'CEILING': [125, 125, 160, 150, 150, 150, 80, 150, 80, 80, 155],
    }
# CheckColWidthDict = {
#     'WALL': [125, 125, 160, 150, 150, 150, 80, 150, 155],
#     'CEILING': [125, 125, 160, 150, 150, 150, 80, 150, 155],
#     }
# OtherCheckColWidthDict = {
#     'WALL': [125, 125, 160, 150, 150, 150, 80, 150, 80, 80, 155],
#     'CEILING': [125, 125, 160, 150, 150, 150, 80, 150, 80, 80, 155],
#     }
WALL = 0
CEILING = 1
CONSTRUCTION = 2

MENU_CHECK_IN = wx.NewIdRef()
MENU_CHECK_OUT = wx.NewIdRef()
MENU_STYLE_DEFAULT = wx.NewIdRef()
MENU_STYLE_XP = wx.NewIdRef()
MENU_STYLE_2007 = wx.NewIdRef()
MENU_STYLE_VISTA = wx.NewIdRef()
MENU_STYLE_MY = wx.NewIdRef()
MENU_USE_CUSTOM = wx.NewIdRef()
MENU_LCD_MONITOR = wx.NewIdRef()
MENU_HELP = wx.NewIdRef()
MENU_SETUP_PROPERTY = wx.NewIdRef()
MENU_DISABLE_MENU_ITEM = wx.NewIdRef()
MENU_REMOVE_MENU = wx.NewIdRef()
MENU_TRANSPARENCY = wx.NewIdRef()
MENU_NEW_FILE = 10005
MENU_SAVE = 10006
MENU_OPEN_FILE = 10007
MENU_NEW_FOLDER = 10008
MENU_COPY = 10009
MENU_CUT = 10010
MENU_PASTE = 10011
ID_WINDOW_LEFT = wx.NewId()
ID_WINDOW_BOTTOM = wx.NewId()
