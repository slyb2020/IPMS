import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter,legal,A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time,datetime
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from ID_DEFINE import *
from BarCodeGenerator import BarCodeGenerator
from DBOperation import UpdatePanelGluePageInDB,UpdatePanelGlueLabelPageInDB
from reportlab.lib.styles import ParagraphStyle

pdfmetrics.registerFont(TTFont('SimSun', 'D:/IPMS/dist/Font/SimSun.ttf'))  #注册字体
pdfmetrics.registerFont(TTFont('Times', 'D:/IPMS/dist/Font/times.ttf'))  #注册字体


def DrawLine(my_canvas,lineWidth,startX,startY,endX,endY):
    my_canvas.setLineWidth(lineWidth)
    my_canvas.line(startX, startY, endX, endY)


def coord(x, y, height, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

# def simple_table_with_style(filename):
#     doc = SimpleDocTemplate(filename, pagesize=letter)
#     story = []
#
#     data = [['col_{}'.format(x) for x in range(1, 6)],
#             [str(x) for x in range(1, 6)],
#             ['a', 'b', 'c', 'd', 'e']
#             ]
#
#     tblstyle = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.red),
#                            ('TEXTCOLOR', (0, 1), (-1, 1), colors.blue)
#                            ])
#
#     tbl = Table(data)
#     tbl.setStyle(tblstyle)
#     story.append(tbl)
#
#     doc.build(story)

def DrawMaterialSchedule(c,page,pageDivision):
    I = Image(bitmapDir+"/PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
         <b>A pa<font color=red>r</font>a<i>graph</i></b>
         <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
         <para align=center spaceb=3>The <b>ReportLab Left
         <font color=red>Logo</font></b>
         Image</para>''',
                  styleSheet["BodyText"])
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">颜色</font>')
    Title3 = Paragraph('<font name="SimSun">板材厚度(mm)</font>')
    Title4 = Paragraph('<font name="SimSun">板材宽度(mm)</font>')
    Title5 = Paragraph('<font name="SimSun">出库量(米)</font>')
    Title6 = Paragraph('<font name="SimSun">当前库存量(米)</font>')
    Title7 = Paragraph('<font name="SimSun">签名</font>')
    data = [
            [Title1, Title2, Title3, Title4, Title5, Title6, Title7],
        ]
    for record in page:
        data.append(record)

    tableColWidths = [15.0 * mm, 27.5 * mm, 27.5 * mm, 35 * mm, 25.0 * mm, (186.5 - 155.0) * mm, 25.0 * mm]
    tableStyle=[
                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                    ('BOX', (0, 0), (-1, -1), 2, colors.black),
                    # ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
                ]
    exSeper = pageDivision[0]
    for seperation in pageDivision[1:]:
        if seperation>1:
            sepeTemp=('SPAN',(1,exSeper),(1,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(2,exSeper),(2,seperation-1))
            tableStyle.append(sepeTemp)
            exSeper = seperation
    tableStyle.append(('SPAN',(1,exSeper),(1,-1)))
    tableStyle.append(('SPAN',(2,exSeper),(2,-1)))
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    startY=8+(36-len(data))*6.3
    t.drawOn(c, 12.5 * mm, startY * mm)

def MakeMaterialScheduleTemplate(orderID,subOrderID,filename,horizontalData,cuttingData,PAGEROWNUMBER=35):
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for type in horizontalData:
        for record in type:
            length=0
            seperation.append(num)
            for board in record[3]:
                length+=int(board[0])*int(board[1])
            temp=[index,record[0],record[1],record[2],float(length)/1000.,'','']
            data.append(temp)
            num+=1
            index+=1
            if num>PAGEROWNUMBER:
                num = 1
                pages.append(data)
                pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
                seperation=[1]
                data=[]
    # if len(data)>0:
        # pages.append(data)
        # pageDivision.append(seperation)
    for type in cuttingData:
        length=0
        seperation.append(num)
        for board in type:
            length+=int(board[0][3])*int(board[0][4])
        temp=[index,type[0][0][0],type[0][0][1],type[0][0][2],float(length)/1000.]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司原材料出库单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='M'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Plate Outbound Delivery Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawMaterialSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def DrawVerticalCutSchedule(c,record,pageDivision):
    # if pageDivision[0] == pageDivision[1]:
    I = Image("D:\\WorkSpace\\Python\\NanTong_YNKS\\bitmaps\\PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
         <b>A pa<font color=red>r</font>a<i>graph</i></b>
         <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
         <para align=center spaceb=3>The <b>ReportLab Left
         <font color=red>Logo</font></b>
         Image</para>''',
                  styleSheet["BodyText"])
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">原料板材颜色</font>')
    Title3 = Paragraph('<font name="SimSun">原料板材厚度mm</font>')
    Title4 = Paragraph('<font name="SimSun">原料板材宽度mm</font>')
    Title5 = Paragraph('<font name="SimSun">横剪长度mm</font>')
    Title6 = Paragraph('<font name="SimSun">数量</font>')
    title = [Title1, Title2, Title3, Title4, Title5, Title6]
    tableColWidths = [20.0 * mm, 40.0 * mm, 40.0 * mm, 40.0 * mm,30.0 * mm, 20 * mm]
# data = [
#         [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10, Title11, Title12, Title13, Title14],
#         ['0', '9GLAV', '0.56', '1234', '2400', '37', '110', '110', '110', '110', '110', '110', '30','100'],
#         ['1', '9GLAV', '0.56', '1234', '2400', '37', '111', '111', '111', '110', '110', '110', '20','100'],
#         ['2', '9GLAV', '0.56', '1234', '2400', '37', '112', '112', '112', '110', '110', '110', '50','100'],
#     ]
#     data = pages[0]
    data= [title]
    for row in record:
        data.append(row)
    tableStyle=[
               ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
               ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
               ('BOX', (0, 0), (-1, -1), 2, colors.black),
               ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
               ('BACKGROUND', (4, 1), (5, -1), colors.beige),
               ('BACKGROUND', (6, 1), (6, -1), colors.lavender),
               ('LINEABOVE', (0, 1), (-1, 1), 2, colors.black),
               ('LINEBEFORE', (4, 0), (4, -1), 2, colors.black),
               ('LINEBEFORE', (6, 0), (6, -1), 2, colors.black),
               ('LINEBEFORE', (-1, 0), (-1, -1), 2, colors.black),
               ('VALIGN', (1, 1), (5, 6), 'MIDDLE'),
               ('VALIGN', (1, 7), (5, -1), 'MIDDLE'),
               ]
    exSeper = pageDivision[0]
    for seperation in pageDivision[1:]:
        if seperation>1:
            sepeTemp=('SPAN',(1,exSeper),(1,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(2,exSeper),(2,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(3,exSeper),(3,seperation-1))
            tableStyle.append(sepeTemp)
            exSeper = seperation
    tableStyle.append(('SPAN',(1,exSeper),(1,-1)))
    tableStyle.append(('SPAN',(2,exSeper),(2,-1)))
    tableStyle.append(('SPAN',(3,exSeper),(3,-1)))
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    startY=8+(36-len(data))*6.3
    t.drawOn(c, 12.5 * mm, startY * mm)

def MakeHorizontalCutScheduleTemplate(orderID, subOrderID, filename, record=[],PAGEROWNUMBER=35):
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for type in record:
        for board in type:
            seperation.append(num)
            for item in board[-1]:
                temp=[index,board[0],board[1],board[2],item[0],item[1]]
                data.append(temp)
                num+=1
                index+=1
                if num>PAGEROWNUMBER:
                    num = 1
                    pages.append(data)
                    pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
                    seperation=[1]
                    data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司横剪任务单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='H'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/empBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Plate Horizontal Shear Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawVerticalCutSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def DrawCutSchedule(c,record,colNum,pageDivision):
    # if pageDivision[0] == pageDivision[1]:
    I = Image("D:\\WorkSpace\\Python\\NanTong_YNKS\\bitmaps\\PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
         <b>A pa<font color=red>r</font>a<i>graph</i></b>
         <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
         <para align=center spaceb=3>The <b>ReportLab Left
         <font color=red>Logo</font></b>
         Image</para>''',
                  styleSheet["BodyText"])
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">板材颜色</font>')
    Title3 = Paragraph('<font name="SimSun">板厚</font>')
    Title4 = Paragraph('<font name="SimSun">板宽</font>')
    Title5 = Paragraph('<font name="SimSun">横切长</font>')
    Title6 = Paragraph('<font name="SimSun">数量</font>')
    Title7 = Paragraph('<font name="SimSun">纵切1</font>')
    Title8 = Paragraph('<font name="SimSun">纵切2</font>')
    Title9 = Paragraph('<font name="SimSun">纵切3</font>')
    Title10 = Paragraph('<font name="SimSun">纵切4</font>')
    Title11 = Paragraph('<font name="SimSun">纵切5</font>')
    Title12 = Paragraph('<font name="SimSun">纵切6</font>')
    Title13 = Paragraph('<font name="SimSun">纵切7</font>')
    Title14 = Paragraph('<font name="SimSun">纵切8</font>')
    Title15 = Paragraph('<font name="SimSun">纵切9</font>')
    Title16 = Paragraph('<font name="SimSun">纵切10</font>')
    Title17 = Paragraph('<font name="SimSun">纵切11</font>')
    Title18 = Paragraph('<font name="SimSun">纵切12</font>')
    Title19 = Paragraph('<font name="SimSun">纵切13</font>')
    Title20 = Paragraph('<font name="SimSun">纵切14</font>')
    Title21 = Paragraph('<font name="SimSun">数量</font>')
    TitleList = [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10,
                 Title11, Title12, Title13, Title14, Title15, Title16, Title17, Title18, Title19, Title20, Title21]
    colWidth = 13.5*7/colNum
    tableColWidthsList = [12.0 * mm, 19.0 * mm, 12.0 * mm, 12.0 * mm, 16.0 * mm, 12.0 * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm,
                          colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, colWidth * mm, 12.0 * mm]
    title = TitleList[:colNum+6]
    title.append(Title21)
    tableColWidths = tableColWidthsList[:colNum+6]
    tableColWidths.append(tableColWidthsList[-1])
# data = [
#         [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10, Title11, Title12, Title13, Title14],
#         ['0', '9GLAV', '0.56', '1234', '2400', '37', '110', '110', '110', '110', '110', '110', '30','100'],
#         ['1', '9GLAV', '0.56', '1234', '2400', '37', '111', '111', '111', '110', '110', '110', '20','100'],
#         ['2', '9GLAV', '0.56', '1234', '2400', '37', '112', '112', '112', '110', '110', '110', '50','100'],
#     ]
#     data = pages[0]
    data= [title]
    for row in record:
        temp = ['']*(colNum+7)
        for k in range(len(row)-1):
            temp[k]=row[k]
        temp[-1]=row[-1]
        data.append(temp)
    tableStyle=[
               ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
               ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
               ('BOX', (0, 0), (-1, -1), 2, colors.black),
               ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
               ('BACKGROUND', (4, 1), (5, -1), colors.beige),
               ('BACKGROUND', (6, 1), (-1, -1), colors.lavender),
               ('LINEABOVE', (0, 1), (-1, 1), 2, colors.black),
               ('LINEBEFORE', (4, 0), (4, -1), 2, colors.black),
               ('LINEBEFORE', (6, 0), (6, -1), 2, colors.black),
               ('LINEBEFORE', (-1, 0), (-1, -1), 2, colors.black),
               ('VALIGN', (1, 1), (5, 6), 'MIDDLE'),
               ('VALIGN', (1, 7), (5, -1), 'MIDDLE'),
               ]
    exSeper = pageDivision[0]
    for seperation in pageDivision[1:]:
        if seperation>1:
            sepeTemp=('SPAN',(1,exSeper),(1,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(2,exSeper),(2,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(3,exSeper),(3,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(4,exSeper),(4,seperation-1))
            tableStyle.append(sepeTemp)
            sepeTemp=('SPAN',(5,exSeper),(5,seperation-1))
            tableStyle.append(sepeTemp)
            exSeper = seperation
    tableStyle.append(('SPAN',(1,exSeper),(1,-1)))
    tableStyle.append(('SPAN',(2,exSeper),(2,-1)))
    tableStyle.append(('SPAN',(3,exSeper),(3,-1)))
    tableStyle.append(('SPAN',(4,exSeper),(4,-1)))
    tableStyle.append(('SPAN',(5,exSeper),(5,-1)))
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    startY=8+(36-len(data))*6.3
    t.drawOn(c, 12.5 * mm, startY * mm)

def MakeCutScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    num=1
    index = 1
    pages = []
    pageDivision = []
    pageMaxList = []
    data = []
    seperation = []
    pageMaxvCuttingCol=0
    for type in record:
        for board in type:
            seperation.append(num)
            for item in board[1]:
                temp=[index,board[0][0],board[0][1],board[0][2],board[0][3],board[0][4]]
                for vCutting in item[0]:
                    temp.append(vCutting)
                temp.append(item[1])
                data.append(temp)
                if len(item[0])>pageMaxvCuttingCol:
                    pageMaxvCuttingCol=len(item[0])
                num+=1
                index+=1
                if num>PAGEROWNUMBER:
                    num = 1
                    pages.append(data)

                    pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
                    pageMaxList.append(pageMaxvCuttingCol)
                    pageMaxvCuttingCol = 1
                    seperation=[1]
                    data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
        pageMaxList.append(pageMaxvCuttingCol)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司剪板机任务单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='C'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Plate Shear Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawCutSchedule(myCanvas,page,pageMaxList[i],pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def DrawBendingSchedule(c,record,pageDivision):
    # if pageDivision[0] == pageDivision[1]:
    I = Image("D:\\WorkSpace\\Python\\NanTong_YNKS\\bitmaps\\PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
             <b>A pa<font color=red>r</font>a<i>graph</i></b>
             <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
             <para align=center spaceb=3>The <b>ReportLab Left
             <font color=red>Logo</font></b>
             Image</para>''',
                  styleSheet["BodyText"])
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">面板代码</font>')
    Title3 = Paragraph('<font name="SimSun">图纸号</font>')
    Title4 = Paragraph('<font name="SimSun">长度</font>')
    Title5 = Paragraph('<font name="SimSun">宽度</font>')
    Title6 = Paragraph('<font name="SimSun">厚度</font>')
    Title7 = Paragraph('<font name="SimSun">X面颜色</font>')
    Title8 = Paragraph('<font name="SimSun">Y面颜色</font>')
    Title9 = Paragraph('<font name="SimSun">Z面颜色</font>')
    Title10 = Paragraph('<font name="SimSun">V面颜色</font>')
    Title11 = Paragraph('<font name="SimSun">数量</font>')
    Title12 = Paragraph('<font name="SimSun">胶水单号</font>')
    title = [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10,Title11,Title12]
    tableColWidths = [11.5*mm,25.0*mm,25.0*mm,11.5*mm,11.5*mm,11.5*mm,17*mm,17*mm,17*mm,17*mm,11.5*mm,25*mm]
    data = [title]
    for row in record:
        data.append(row)
    tableStyle = [
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # 类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
        # ('BACKGROUND', (2, 1), (2, -1), colors.pink),
        # ('BACKGROUND', (3, 1), (5, -1), colors.beige),
        # ('BACKGROUND', (6, 1), (10, -1), colors.lavender),

        ('LINEABOVE', (0, 1), (-1, 1), 2, colors.black),
        ('LINEBEFORE', (2, 0), (2, -1), 2, colors.black),
        ('LINEBEFORE', (3, 0), (3, -1), 2, colors.black),
        ('LINEBEFORE', (6, 0), (6, -1), 2, colors.black),
        ('LINEBEFORE', (10, 0), (10, -1), 2, colors.black),
        ('LINEBEFORE', (-1, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (1, 1), (5, 6), 'MIDDLE'),
        ('VALIGN', (1, 7), (5, -1), 'MIDDLE'),
    ]
    for i in range(len(record)):
        if i%2 == 1:
           tableStyle.append(('BACKGROUND', (0, i+1), (-1, i+1), colors.lavender))

    t = Table(data, style=tableStyle, colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    startY = 8 + (36 - len(data)) * 6.3
    t.drawOn(c, 8 * mm, startY * mm)

def MakeBendingScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司折弯任务单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='B'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Bending Machine Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakeS2FormingScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司2S成型任务单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='S'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd S2 Forming Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakeCeilingFormingScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司天花板成型任务单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='E'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Ceiling Forming Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakePRPressScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司PR热压任务单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='P'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd PR Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakeVacuumScheduleTemplate(orderID,subOrderID,filename,record=[],PAGEROWNUMBER=35):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None'
    num=1
    index = 1
    pages = []
    pageDivision = []
    data = []
    seperation = []
    for board in record:
        seperation.append(num)
        board=list(board)
        if board[14]=='None':
            board[14]=''
        if board[15]=='None':
            board[15]=''
        temp=[index,board[7],board[6],board[10],board[11],board[12],board[8],board[9],board[14],board[15],board[13]]
        data.append(temp)
        num+=1
        index+=1
        if num>PAGEROWNUMBER:
            num = 1
            pages.append(data)
            pageDivision.append(seperation)#由于每次seperation初始化都自动往里面添加一个[1],所以如果前两行不同的话会出现【1，1】的情况，需要去除重复的1
            seperation=[1]
            data=[]
    if len(data)>0:
        pages.append(data)
        pageDivision.append(seperation)
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    for i,page in enumerate(pages):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司特制品任务单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='V'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Vacuum Schedule")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(200, 31, height, mm))
        myCanvas.drawString(40,685, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 685, '出单日期：%s'%(datetime.date.today()))
        # simple_table_with_style(filename)
        DrawBendingSchedule(myCanvas,page,pageDivision[i])
        myCanvas.drawRightString(width-50, 5, '页码：%s/%s'%(i+1,len(pages)))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
    myCanvas.save()

def MakeGlueNoSheetTemplate(orderID,subOrderID,filename,record=[]):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None','胶水单号'
    num=1
    index = 1
    pages = []
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    page = 0
    for i, board in enumerate(record):
        data=list(board)
        if data[14]=='None':
            data[14]=''
        if data[15]=='None':
            data[15]=''
        page += 1
        myCanvas.setFont("SimSun", 16)
        myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司胶水单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715,
                            width=40, height=40)
        tempCode='G'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Glue Sheet")
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(205, 31, height, mm))
        DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(10, 131, height, mm))
        DrawLine(myCanvas,1,*coord(205, 31, height, mm),*coord(205, 131, height, mm))
        DrawLine(myCanvas,1,*coord(10, 131, height, mm),*coord(205, 131, height, mm))
        myCanvas.drawString(40,680, text="订单编号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 680, '出单日期：%s' % (datetime.date.today()))
        myCanvas.drawString(40,650, text="图纸编号；%s"%(data[6]))
        myCanvas.drawRightString(width - 50, 650, '胶水单号：%s'%(data[16]))
        DrawLine(myCanvas,1,*coord(10, 55, height, mm),*coord(205, 55, height, mm))
        myCanvas.drawString(40,615, text="                X面颜色       Y面颜色       Z面颜色       V面颜色")
        DrawLine(myCanvas,1,*coord(50, 65, height, mm),*coord(205, 65, height, mm))
        DrawLine(myCanvas,1,*coord(50, 55, height, mm),*coord(50, 115, height, mm))
        DrawLine(myCanvas,1,*coord(50+39, 55, height, mm),*coord(50+39, 115, height, mm))
        DrawLine(myCanvas,1,*coord(50+39*2, 55, height, mm),*coord(50+39*2, 115, height, mm))
        DrawLine(myCanvas,1,*coord(50+39*3, 55, height, mm),*coord(50+39*3, 115, height, mm))
        myCanvas.setFont("Times", 22)
        myCanvas.drawString(170,565, text="%s"%(data[8]))
        myCanvas.drawString(170+110,565, text="%s"%(data[9]))
        myCanvas.drawString(170+110*2,565, text="%s"%(data[14]))
        myCanvas.drawString(170+110*3,565, text="%s"%(data[15]))
        DrawLine(myCanvas,1,*coord(10, 90, height, mm),*coord(205, 90, height, mm))
        myCanvas.setFont("SimSun", 16)
        myCanvas.drawString(50,515, text="长(Length)")
        myCanvas.drawString(50+110,515, text="宽(Width)")
        myCanvas.drawString(50+110*2,515, text="厚(Thick)")
        myCanvas.drawString(40+110*3,515, text="数量(Amount)")
        myCanvas.drawString(40+110*4,515, text="重量(Weight)")

        myCanvas.setFont("Times", 20)
        myCanvas.drawString(55,480, text="%s mm"%(data[10]))
        myCanvas.drawString(55+110,480, text="%s mm"%(data[11]))
        myCanvas.drawString(60+110*2,480, text="%s mm"%(data[12]))
        myCanvas.drawString(60+110*3,480, text="%s Pcs."%(data[13]))
        myCanvas.drawString(60+110*4,480, text="%s"%(""))
        DrawLine(myCanvas,1,*coord(10, 115, height, mm),*coord(205, 115, height, mm))
        myCanvas.setFont("SimSun", 16)
        myCanvas.drawString(50,435, text="甲板(Deck): %s"%(data[3]))
        myCanvas.drawString(220,435, text="区域(Zone): %s"%(data[4]))
        myCanvas.drawString(380,435, text="房间(Room): %s"%(data[5]))

        offset = 410
        offset2=145
        DrawLine(myCanvas,1,*coord(0, 10+offset2, height, mm),*coord(220, 10+offset2, height, mm))

        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,735-offset, text="伊纳克赛(南通)精致内饰材料有限公司胶水单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 715-offset,
                            width=40, height=40)
        tempCode='G'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
        BarCodeGenerator(tempCode,"D:/IPMS/dist/bitmaps/tempBarcode.png")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/tempBarcode.png", width-100, height-40,
                            width=100, height=40)
        myCanvas.setFont("Times", 16)
        myCanvas.drawCentredString(width/2,715-offset, text="Inexa (NanTong) Interiors Co.Ltd Glue Sheet")
        DrawLine(myCanvas,1,*coord(10, 31+offset2, height, mm),*coord(205, 31+offset2, height, mm))
        DrawLine(myCanvas,1,*coord(10, 31+offset2, height, mm),*coord(10, 131+offset2, height, mm))
        DrawLine(myCanvas,1,*coord(205, 31+offset2, height, mm),*coord(205, 131+offset2, height, mm))
        DrawLine(myCanvas,1,*coord(10, 131+offset2, height, mm),*coord(205, 131+offset2, height, mm))
        myCanvas.drawString(40,680-offset, text="订单编号；%s-%03d"%(orderID,int(subOrderID)))
        myCanvas.drawRightString(width-50, 680-offset, '出单日期：%s' % (datetime.date.today()))
        myCanvas.drawString(40,650-offset, text="图纸编号；%s"%(data[6]))
        myCanvas.drawRightString(width - 50, 650-offset, '胶水单号：%s'%(data[16]))
        DrawLine(myCanvas,1,*coord(10, 55+offset2, height, mm),*coord(205, 55+offset2, height, mm))
        myCanvas.drawString(40,615-offset, text="                X面颜色       Y面颜色       Z面颜色       V面颜色")
        DrawLine(myCanvas,1,*coord(50, 65+offset2, height, mm),*coord(205, 65+offset2, height, mm))
        DrawLine(myCanvas,1,*coord(50, 55+offset2, height, mm),*coord(50, 115+offset2, height, mm))
        DrawLine(myCanvas,1,*coord(50+39, 55+offset2, height, mm),*coord(50+39, 115+offset2, height, mm))
        DrawLine(myCanvas,1,*coord(50+39*2, 55+offset2, height, mm),*coord(50+39*2, 115+offset2, height, mm))
        DrawLine(myCanvas,1,*coord(50+39*3, 55+offset2, height, mm),*coord(50+39*3, 115+offset2, height, mm))
        myCanvas.setFont("Times", 22)
        myCanvas.drawString(170,565-offset, text="%s"%(data[8]))
        myCanvas.drawString(170+110,565-offset, text="%s"%(data[9]))
        myCanvas.drawString(170+110*2,565-offset, text="%s"%(data[14]))
        myCanvas.drawString(170+110*3,565-offset, text="%s"%(data[15]))
        DrawLine(myCanvas,1,*coord(10, 90+offset2, height, mm),*coord(205, 90+offset2, height, mm))
        myCanvas.setFont("SimSun", 16)
        myCanvas.drawString(50,515-offset, text="长(Length)")
        myCanvas.drawString(50+110,515-offset, text="宽(Width)")
        myCanvas.drawString(50+110*2,515-offset, text="厚(Thick)")
        myCanvas.drawString(40+110*3,515-offset, text="数量(Amount)")
        myCanvas.drawString(40+110*4,515-offset, text="重量(Weight)")

        myCanvas.setFont("Times", 20)
        myCanvas.drawString(55,480-offset, text="%s mm"%(data[10]))
        myCanvas.drawString(55+110,480-offset, text="%s mm"%(data[11]))
        myCanvas.drawString(60+110*2,480-offset, text="%s mm"%(data[12]))
        myCanvas.drawString(60+110*3,480-offset, text="%s Pcs."%(data[13]))
        myCanvas.drawString(60+110*4,480-offset, text="%s"%(""))
        DrawLine(myCanvas,1,*coord(10, 115+offset2, height, mm),*coord(205, 115+offset2, height, mm))
        myCanvas.setFont("SimSun", 16)
        myCanvas.drawString(50,435-offset, text="甲板(Deck): %s"%(data[3]))
        myCanvas.drawString(220,435-offset, text="区域(Zone): %s"%(data[4]))
        myCanvas.drawString(380,435-offset, text="房间(Room): %s"%(data[5]))
        # myCanvas.drawString(40,670-offset, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
        # myCanvas.drawRightString(width-50, 670-offset, '胶水单号：%s'%(data[16]))
        # DrawLine(myCanvas,1,*coord(10, 50+offset2, height, mm),*coord(205, 50+offset2, height, mm))
        myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
        UpdatePanelGluePageInDB(None, 1, orderID, data[16], page)
    myCanvas.save()

def MakeGlueLabelSheetTemplate(orderID,subOrderID,filename,record=[]):
    #1, 64730, '1', '3', '9', 'Corridor', 'A.2SA.0900', '0', 'YC74H', 'YQ73D', '2160', '550', '50', 2, 'None', 'None','胶水单号'
    #23.2mm
    num=0
    width, height = A4
    myCanvas = canvas.Canvas(filename, pagesize=A4)
    page = 1
    offset=68
    gap = 24
    vOffset=20
    myCanvas.setFont("SimSun", 10)
    for board in record:
        data=list(board)
        if data[14]=='None':
            data[14]=''
        if data[15]=='None':
            data[15]=''
        UpdatePanelGlueLabelPageInDB(None, 1, orderID, data[16], page)
        for i in range(int(data[13])):
            DrawLine(myCanvas,1,*coord(0, 2+num*gap, height, mm),*coord(220, 2+num*gap, height, mm))
            myCanvas.drawString(20,798+vOffset-offset*num, text="项目名称(Project): %s"%("Stena W0272"))

            myCanvas.drawString(200,798+vOffset-offset*num, text="订单编号(OrderId): %s-%03d"%(orderID,int(subOrderID)))

            myCanvas.drawString(360,798+vOffset-offset*num, text="图纸号(Drawing No.): %s"%(data[6]))

            # myCanvas.drawCentredString(80, 785, text="%s"%)
            # myCanvas.drawCentredString(260, 785, text="%s-%03d"%(orderID,int(subOrderID)))
            # myCanvas.drawCentredString(430, 785, text="%s"%())
            myCanvas.drawString(20,778+vOffset-offset*num, text="胶水单编号(Glue Note): %s"%(data[-1]))
            myCanvas.drawString(200,778+vOffset-offset*num, text="长度(Length): %s"%(data[10]))
            myCanvas.drawString(320,778+vOffset-offset*num, text="宽度(Width): %s"%(data[11]))
            myCanvas.drawString(440,778+vOffset-offset*num, text="厚度(Thick): %s"%(data[12]))
            # myCanvas.drawCentredString(80, 760, text="%s"%)
            # myCanvas.drawCentredString(160, 760, text="%s"%(data[10]))
            # myCanvas.drawCentredString(200, 760, text="%s"%(data[11]))
            # myCanvas.drawCentredString(300, 760, text="%s"%(data[12]))
            # myCanvas.drawCentredString(400, 760, text="%s"%(data[13]))
            myCanvas.drawString(20,757+vOffset-offset*num, text="颜色(Colour):  X: %s"%(data[8]))
            myCanvas.drawString(200,757+vOffset-offset*num, text="Y: %s"%(data[9]))
            myCanvas.drawString(320,757+vOffset-offset*num, text="Z: %s"%(data[14]))
            myCanvas.drawString(440,757+vOffset-offset*num, text="V: %s"%(data[15]))
            # myCanvas.drawCentredString(500, 760, text="%s//%s//%s//%s"%())

            # myCanvas.drawCentredString(width/2,735, text="伊纳克赛(南通)精致内饰材料有限公司胶水单")
            # myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715,
            #                     width=40, height=40)
            # tempCode='G'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
            # BarCodeGenerator(tempCode)
            # myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40,
            #                     width=100, height=40)
            # myCanvas.drawCentredString(width/2,715, text="Inexa (NanTong) Interiors Co.Ltd Glue Sheet")
            # DrawLine(myCanvas,1,*coord(10, 31, height, mm),*coord(10, 131, height, mm))
            # DrawLine(myCanvas,1,*coord(205, 31, height, mm),*coord(205, 131, height, mm))
            # DrawLine(myCanvas,1,*coord(10, 131, height, mm),*coord(205, 131, height, mm))
            # myCanvas.drawString(40,680, text="订单编号；%s-%03d"%(orderID,int(subOrderID)))
            # myCanvas.drawRightString(width-50, 680, '出单日期：%s' % (datetime.date.today()))
            # myCanvas.drawString(40,650, text="图纸编号；%s"%(data[6]))
            # myCanvas.drawRightString(width - 50, 650, '胶水单号：%s'%(data[16]))
            # DrawLine(myCanvas,1,*coord(10, 55, height, mm),*coord(205, 55, height, mm))
            # myCanvas.drawString(40,615, text="                X面颜色       Y面颜色       Z面颜色       V面颜色")
            # DrawLine(myCanvas,1,*coord(50, 65, height, mm),*coord(205, 65, height, mm))
            # DrawLine(myCanvas,1,*coord(50, 55, height, mm),*coord(50, 115, height, mm))
            # DrawLine(myCanvas,1,*coord(50+39, 55, height, mm),*coord(50+39, 115, height, mm))
            # DrawLine(myCanvas,1,*coord(50+39*2, 55, height, mm),*coord(50+39*2, 115, height, mm))
            # DrawLine(myCanvas,1,*coord(50+39*3, 55, height, mm),*coord(50+39*3, 115, height, mm))
            # myCanvas.setFont("SimSun", 22)
            # myCanvas.drawString(170+110,565, text="%s"%(data[9]))
            # myCanvas.drawString(170+110*2,565, text="%s"%(data[14]))
            # myCanvas.drawString(170+110*3,565, text="%s"%(data[15]))
            # DrawLine(myCanvas,1,*coord(10, 90, height, mm),*coord(205, 90, height, mm))
            # myCanvas.setFont("SimSun", 16)
            # myCanvas.drawString(50,515, text="长(Length)")
            # myCanvas.drawString(50+110,515, text="宽(Width)")
            # myCanvas.drawString(60+110*2,515, text="厚(Thick)")
            # myCanvas.drawString(40+110*3,515, text="数量(Amount)")
            # myCanvas.drawString(40+110*4,515, text="重量(Weight)")
            #
            # myCanvas.setFont("SimSun", 20)
            # myCanvas.drawString(55,480, text="%s mm"%(data[10]))
            # myCanvas.drawString(55+110,480, text="%s mm"%(data[11]))
            # myCanvas.drawString(60+110*2,480, text="%s mm"%(data[12]))
            # myCanvas.drawString(60+110*3,480, text="%s Pcs."%(data[13]))
            # myCanvas.drawString(60+110*4,480, text="%s"%(""))
            # DrawLine(myCanvas,1,*coord(10, 115, height, mm),*coord(205, 115, height, mm))
            # myCanvas.setFont("SimSun", 16)
            # myCanvas.drawString(50,435, text="甲板(Deck): %s"%(data[3]))
            # myCanvas.drawString(220,435, text="区域(Zone): %s"%(data[4]))
            # myCanvas.drawString(380,435, text="房间(Room): %s"%(data[5]))
            #
            # offset = 410
            # offset2=145
            # DrawLine(myCanvas,1,*coord(0, 10+offset2, height, mm),*coord(220, 10+offset2, height, mm))
            #
            # myCanvas.setFont("SimSun", 18)
            # myCanvas.drawCentredString(width/2,735-offset, text="伊纳克赛(南通)精致内饰材料有限公司胶水单")
            # myCanvas.drawImage(bitmapDir+"/logo.jpg", 30, 715-offset,
            #                     width=40, height=40)
            # tempCode='G'+'%05d'%int(orderID)+'-'+'%03d'%int(subOrderID)+'P%03d'%(i+1)
            # BarCodeGenerator(tempCode)
            # myCanvas.drawImage(dirName+"/tempBarcode.png", width-100, height-40-offset-35,
            #                     width=100, height=40)
            # myCanvas.setFont("SimSun", 16)
            # myCanvas.drawCentredString(width/2,715-offset, text="Inexa (NanTong) Interiors Co.Ltd Glue Sheet")
            # DrawLine(myCanvas,1,*coord(10, 31+offset2, height, mm),*coord(205, 31+offset2, height, mm))
            # DrawLine(myCanvas,1,*coord(10, 31+offset2, height, mm),*coord(10, 131+offset2, height, mm))
            # DrawLine(myCanvas,1,*coord(205, 31+offset2, height, mm),*coord(205, 131+offset2, height, mm))
            # DrawLine(myCanvas,1,*coord(10, 131+offset2, height, mm),*coord(205, 131+offset2, height, mm))
            # myCanvas.drawString(40,680-offset, text="订单编号；%s-%03d"%(orderID,int(subOrderID)))
            # myCanvas.drawRightString(width-50, 680-offset, '出单日期：%s' % (datetime.date.today()))
            # myCanvas.drawString(40,650-offset, text="图纸编号；%s"%(data[6]))
            # myCanvas.drawRightString(width - 50, 650-offset, '胶水单号：%s'%(data[16]))
            # DrawLine(myCanvas,1,*coord(10, 55+offset2, height, mm),*coord(205, 55+offset2, height, mm))
            # myCanvas.drawString(40,615-offset, text="                X面颜色       Y面颜色       Z面颜色       V面颜色")
            # DrawLine(myCanvas,1,*coord(50, 65+offset2, height, mm),*coord(205, 65+offset2, height, mm))
            # DrawLine(myCanvas,1,*coord(50, 55+offset2, height, mm),*coord(50, 115+offset2, height, mm))
            # DrawLine(myCanvas,1,*coord(50+39, 55+offset2, height, mm),*coord(50+39, 115+offset2, height, mm))
            # DrawLine(myCanvas,1,*coord(50+39*2, 55+offset2, height, mm),*coord(50+39*2, 115+offset2, height, mm))
            # DrawLine(myCanvas,1,*coord(50+39*3, 55+offset2, height, mm),*coord(50+39*3, 115+offset2, height, mm))
            # myCanvas.setFont("SimSun", 22)
            # myCanvas.drawString(170,565-offset, text="%s"%(data[8]))
            # myCanvas.drawString(170+110,565-offset, text="%s"%(data[9]))
            # myCanvas.drawString(170+110*2,565-offset, text="%s"%(data[14]))
            # myCanvas.drawString(170+110*3,565-offset, text="%s"%(data[15]))
            # DrawLine(myCanvas,1,*coord(10, 90+offset2, height, mm),*coord(205, 90+offset2, height, mm))
            # myCanvas.setFont("SimSun", 16)
            # myCanvas.drawString(50,515-offset, text="长(Length)")
            # myCanvas.drawString(50+110,515-offset, text="宽(Width)")
            # myCanvas.drawString(60+110*2,515-offset, text="厚(Thick)")
            # myCanvas.drawString(40+110*3,515-offset, text="数量(Amount)")
            # myCanvas.drawString(40+110*4,515-offset, text="重量(Weight)")
            #
            # myCanvas.setFont("SimSun", 20)
            # myCanvas.drawString(55,480-offset, text="%s mm"%(data[10]))
            # myCanvas.drawString(55+110,480-offset, text="%s mm"%(data[11]))
            # myCanvas.drawString(60+110*2,480-offset, text="%s mm"%(data[12]))
            # myCanvas.drawString(60+110*3,480-offset, text="%s Pcs."%(data[13]))
            # myCanvas.drawString(60+110*4,480-offset, text="%s"%(""))
            # DrawLine(myCanvas,1,*coord(10, 115+offset2, height, mm),*coord(205, 115+offset2, height, mm))
            # myCanvas.setFont("SimSun", 16)
            # myCanvas.drawString(50,435-offset, text="甲板(Deck): %s"%(data[3]))
            # myCanvas.drawString(220,435-offset, text="区域(Zone): %s"%(data[4]))
            # myCanvas.drawString(380,435-offset, text="房间(Room): %s"%(data[5]))
            # # myCanvas.drawString(40,670-offset, text="订单号；%s-%03d"%(orderID,int(subOrderID)))
            # # myCanvas.drawRightString(width-50, 670-offset, '胶水单号：%s'%(data[16]))
            # # DrawLine(myCanvas,1,*coord(10, 50+offset2, height, mm),*coord(205, 50+offset2, height, mm))
            num += 1
            if num>11:
                DrawLine(myCanvas, 1, *coord(0, 2 + num * gap, height, mm), *coord(220, 2 + num * gap, height, mm))
                num = 0
                page += 1
                myCanvas.showPage()#这句话相当于分页，显示页面即完成当前页面，开始新页面
                myCanvas.setFont("SimSun", 10)
    DrawLine(myCanvas, 1, *coord(0, 2 + num * gap, height, mm), *coord(220, 2 + num * gap, height, mm))
    myCanvas.save()

def DrawFormingSchedule(c):
    Title1 = Paragraph('<font name="SimSun">序号</font>')
    Title2 = Paragraph('<font name="SimSun">胶水单</font>')
    Title3 = Paragraph('<font name="SimSun">图纸</font>')
    Title4 = Paragraph('<font name="SimSun">长度</font>')
    Title5 = Paragraph('<font name="SimSun">宽度</font>')
    Title6 = Paragraph('<font name="SimSun">厚度</font>')
    Title7 = Paragraph('<font name="SimSun">X</font>')
    Title8 = Paragraph('<font name="SimSun">Y</font>')
    Title9 = Paragraph('<font name="SimSun">Z</font>')
    Title10 = Paragraph('<font name="SimSun">V</font>')
    Title11 = Paragraph('<font name="SimSun">数量</font>')
    data = [
            [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10, Title11],
            ['1', '1122', 'N.2SA.0001', '1495','548', '50','79070','Y1058','','','1'],
            ['2', '1122', 'CC64001',    '1495','548', '25','RAL1101','G','','','2'],
            ['3', '1122', 'N.2SA.0001', '1495','548', '100','79070','G','','','3'],
            ['4', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','4'],
            ['5', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','5'],
            ['6', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','23'],
            ['7', '1122', 'CC64001',    '1495','548', '25','79070','G','','','2'],
            ['8', '1122', 'N.2SA.0001', '1495','548', '100','79070','G','','','3'],
            ['9', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','34'],
            ['10', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','2'],
            ['11', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','23'],
            ['12', '1122', 'CC64001',    '1495','548', '25','79070','G','','','56'],
            ['13', '1122', 'N.2SA.0001', '1495','548', '100','79070','G','','','3'],
            ['14', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','34'],
            ['15', '1122', 'N.2SA.0001', '1495','548', '50','79070','G','','','100'],
    ]
    t = Table(data, style=[
                           ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                           ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.khaki),
                           ('BACKGROUND', (3, 1), (5, -1), colors.beige),
                           ('BACKGROUND', (6, 1), (9, -1), colors.pink),
                           # ('SPAN',(0,0),(1,0)),
                           # ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                           # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           # ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                           # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           # ('VALIGN', (3, 0), (3, 0), 'BOTTOM'),
                           # # ('ALIGN', (0, 3), (0, 3), 'CENTER'),
                           # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           # # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           # # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ],colWidths=[12*mm,15.0*mm,25.0*mm,15.0*mm,15.0*mm,12.0*mm,20.0*mm,20.0*mm,20.0*mm,20*mm,22.0*mm])
    # Table(data, colWidths=[1.9 * inch] * 5)
    # t._argW[3] = 1.5 * inch
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    t.drawOn(c, 12.5 * mm, 130 * mm)
def MakeFormingScheduleTemplate(filename,data=[]):
    width, height = letter
    myCanvas = canvas.Canvas(filename, pagesize=letter)
    myCanvas.setFont("SimSun", 18)
    myCanvas.drawCentredString(width/2,730, text="伊纳克赛(南通)精致内饰材料有限公司成型任务单")
    myCanvas.drawImage(bitmapDir+"/python_logo.png", 30, 710,
                        width=40, height=40)
    myCanvas.setFont("Times", 12)
    myCanvas.drawCentredString(width/2,710, text="Inexa (NanTong) Interiors Co.Ltd Forming Schedule")
    DrawLine(myCanvas,1,*coord(10, 33, height, mm),*coord(200, 33, height, mm))
    myCanvas.drawString(40,670, text="订单号；%s"%'64757-001')
    myCanvas.drawRightString(width-50, 670, '出单日期：%s'%(datetime.date.today()))
    # simple_table_with_style(filename)
    DrawFormingSchedule(myCanvas)
    myCanvas.save()

def DrawQuotationSheet(c,record,currencyName):
    styles = getSampleStyleSheet()
    # # Modify the Normal Style
    # styles["Normal"].fontSize = 12
    # styles["Normal"].leading = 14

    # Create a Justify style
    styles.add(ParagraphStyle(name='Center', alignment=1))
    Title1 = Paragraph('<font name="Times">Item</font>',style = styles['Center'])
    Title2 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title3 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title4 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title5 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title6 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title7 = Paragraph('<font name="Times">Total</font>',style = styles['Center'])
    Title8 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    Title9 = Paragraph('<font name="Times">Wet</font>',style = styles['Center'])
    Title10 = Paragraph('<font name="Times">Strengthen</font>',style = styles['Center'])
    Title11 = Paragraph('<font name="Times">OverWidth</font>',style = styles['Center'])
    Title12 = Paragraph('<font name="Times">Unit Price</font>',style = styles['Center'])
    Title13 = Paragraph('<font name="Times">Total Price</font>',style = styles['Center'])
    Title21 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title22 = Paragraph('<font name="Times">Type</font>',style = styles['Center'])
    Title23 = Paragraph('<font name="Times">Surface</font>',style = styles['Center'])
    Title24 = Paragraph('<font name="Times">Height/Length(mm)</font>',style = styles['Center'])
    Title25 = Paragraph('<font name="Times">Width(mm)</font>',style = styles['Center'])
    Title26 = Paragraph('<font name="Times">Thickness(mm)</font>',style = styles['Center'])
    Title27 = Paragraph('<font name="Times">Quantity</font>',style = styles['Center'])
    Title28 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    Title29 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title30 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title31 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title32 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    Title33 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    data = [
        [Title1, Title2, Title3, Title4, Title5, Title6, Title7, Title8, Title9, Title10, Title11, Title12, Title13],
        [Title21, Title22, Title23, Title24, Title25, Title26, Title27, Title28, Title29, Title30, Title31, Title32,Title33,],]
    for item in record:
        data.append(item)
    tableStyle =[
                           ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                           ('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 1), colors.khaki),
                           ('BACKGROUND', (3, 2), (5, -1), colors.beige),
                           ('BACKGROUND', (11, 2), (11, -1), colors.pink),
                           ('BACKGROUND', (12, 2), (12, -1), colors.lavender),
                           ('SPAN',(0,0),(0,1)),
                           ('SPAN',(7,0),(7,1)),
                           ('SPAN',(8,0),(8,1)),
                           ('SPAN',(9,0),(9,1)),
                           ('SPAN',(10,0),(10,1)),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
                           # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           # # ('ALIGN', (0, 3), (0, 3), 'CENTER'),
                           # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           # # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           # # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ]
    tableColWidths = [12*mm,18.0*mm,18.0*mm,35.0*mm,22.0*mm,28.0*mm,20.0*mm,12.0*mm,12.0*mm,22*mm,22*mm,24*mm,25*mm]

    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    startY = 8 + (23 - len(data)) * 6.3
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    t.drawOn(c, 15 * mm, startY * mm)

def DrawQuotationSheetCeiling(c,record,currencyName):
    styles = getSampleStyleSheet()
    # # Modify the Normal Style
    # styles["Normal"].fontSize = 12
    # styles["Normal"].leading = 14

    # Create a Justify style
    styles.add(ParagraphStyle(name='Center', alignment=1))
    Title1 = Paragraph('<font name="Times">Item</font>',style = styles['Center'])
    Title2 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title3 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title4 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title5 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title6 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title7 = Paragraph('<font name="Times">Total</font>',style = styles['Center'])
    Title8 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    # Title9 = Paragraph('<font name="Times">Wet</font>',style = styles['Center'])
    # Title10 = Paragraph('<font name="Times">Strengthen</font>',style = styles['Center'])
    # Title11 = Paragraph('<font name="Times">OverWidth</font>',style = styles['Center'])
    Title12 = Paragraph('<font name="Times">Unit Price</font>',style = styles['Center'])
    Title13 = Paragraph('<font name="Times">Total Price</font>',style = styles['Center'])
    Title21 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title22 = Paragraph('<font name="Times">Type</font>',style = styles['Center'])
    Title23 = Paragraph('<font name="Times">Surface</font>',style = styles['Center'])
    Title24 = Paragraph('<font name="Times">Height/Length(mm)</font>',style = styles['Center'])
    Title25 = Paragraph('<font name="Times">Width(mm)</font>',style = styles['Center'])
    Title26 = Paragraph('<font name="Times">Thickness(mm)</font>',style = styles['Center'])
    Title27 = Paragraph('<font name="Times">Quantity</font>',style = styles['Center'])
    Title28 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    # Title29 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    # Title30 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    # Title31 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title32 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    Title33 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    data = [
        [Title1,  Title2,  Title3,  Title4,  Title5,  Title6,  Title7,  Title8,  Title12,Title13],
        [Title21, Title22, Title23, Title24, Title25, Title26, Title27, Title28, Title32,Title33,],]
    for item in record:
        temp = item[0:8]+item[11:]
        data.append(temp)
    tableStyle =[
                           ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                           ('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 1), colors.khaki),
                           ('BACKGROUND', (3, 2), (5, -1), colors.beige),
                           ('BACKGROUND', (6, 2), (7, -1), colors.pink),
                           ('BACKGROUND', (8, 2), (9, -1), colors.lavender),
                           ('SPAN',(0,0),(0,1)),
                           ('SPAN',(7,0),(7,1)),
                           # ('SPAN',(8,0),(8,1)),
                           # ('SPAN',(9,0),(9,1)),
                           # ('SPAN',(10,0),(10,1)),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
                           # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           # # ('ALIGN', (0, 3), (0, 3), 'CENTER'),
                           # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           # # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           # # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ]
    tableColWidths = [12*mm,25.0*mm,30.0*mm,35.0*mm,25.0*mm,30.0*mm,25.0*mm,25*mm,30*mm,30*mm]

    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    startY = 8 + (23 - len(data)) * 6.3
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    t.drawOn(c, 15 * mm, startY * mm)

def DrawQuotationSheetInteriorDoor(c,record,currencyName):
    styles = getSampleStyleSheet()
    # # Modify the Normal Style
    # styles["Normal"].fontSize = 12
    # styles["Normal"].leading = 14

    # Create a Justify style
    styles.add(ParagraphStyle(name='Center', alignment=1))
    Title1 = Paragraph('<font name="Times">Item</font>',style = styles['Center'])
    Title2 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title3 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title4 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title5 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title6 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title7 = Paragraph('<font name="Times">Total</font>',style = styles['Center'])
    Title8 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    # Title9 = Paragraph('<font name="Times">Wet</font>',style = styles['Center'])
    # Title10 = Paragraph('<font name="Times">Strengthen</font>',style = styles['Center'])
    # Title11 = Paragraph('<font name="Times">OverWidth</font>',style = styles['Center'])
    Title12 = Paragraph('<font name="Times">Unit Price</font>',style = styles['Center'])
    Title13 = Paragraph('<font name="Times">Total Price</font>',style = styles['Center'])
    Title21 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title22 = Paragraph('<font name="Times">Type</font>',style = styles['Center'])
    Title23 = Paragraph('<font name="Times">Surface</font>',style = styles['Center'])
    Title24 = Paragraph('<font name="Times">Height/Length(mm)</font>',style = styles['Center'])
    Title25 = Paragraph('<font name="Times">Width(mm)</font>',style = styles['Center'])
    Title26 = Paragraph('<font name="Times">Thickness(mm)</font>',style = styles['Center'])
    Title27 = Paragraph('<font name="Times">Quantity</font>',style = styles['Center'])
    Title28 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    # Title29 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    # Title30 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    # Title31 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title32 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    Title33 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    data = [
        [Title1,  Title2,  Title3,  Title4, Title5, Title6, Title7,  Title8,  Title12,Title13],
        [Title21, Title22, Title23, Title24, Title25, Title26, Title27, Title28, Title32,Title33,],]
    for item in record:
        temp = item[0:8]+item[11:]
        data.append(temp)
    tableStyle =[
                           ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                           ('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 1), colors.khaki),
                           ('BACKGROUND', (3, 2), (5, -1), colors.beige),
                           # ('BACKGROUND', (6, 2), (7, -1), colors.pink),
                           ('BACKGROUND', (7, 2), (8, -1), colors.lavender),
                           ('SPAN',(0,0),(0,1)),
                           ('SPAN',(7,0),(7,1)),
                           # ('SPAN',(8,0),(8,1)),
                           # ('SPAN',(9,0),(9,1)),
                           # ('SPAN',(10,0),(10,1)),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
                           # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           # # ('ALIGN', (0, 3), (0, 3), 'CENTER'),
                           # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           # # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           # # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ]
    tableColWidths = [12*mm,45.0*mm,35.0*mm,35.0*mm,25.0*mm,0*mm,25.0*mm,25*mm,35*mm,35*mm]

    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    startY = 8 + (23 - len(data)) * 6.3
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    t.drawOn(c, 15 * mm, startY * mm)

def DrawQuotationSheetFireDoor(c,record,currencyName):
    styles = getSampleStyleSheet()
    # # Modify the Normal Style
    # styles["Normal"].fontSize = 12
    # styles["Normal"].leading = 14

    # Create a Justify style
    styles.add(ParagraphStyle(name='Center', alignment=1))
    Title1 = Paragraph('<font name="Times">Item</font>',style = styles['Center'])
    Title2 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title3 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title4 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title5 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title6 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title7 = Paragraph('<font name="Times">Total</font>',style = styles['Center'])
    Title8 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    # Title9 = Paragraph('<font name="Times">Wet</font>',style = styles['Center'])
    # Title10 = Paragraph('<font name="Times">Strengthen</font>',style = styles['Center'])
    # Title11 = Paragraph('<font name="Times">OverWidth</font>',style = styles['Center'])
    Title12 = Paragraph('<font name="Times">Unit Price</font>',style = styles['Center'])
    Title13 = Paragraph('<font name="Times">Total Price</font>',style = styles['Center'])
    Title21 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title22 = Paragraph('<font name="Times">Type</font>',style = styles['Center'])
    Title23 = Paragraph('<font name="Times">Surface</font>',style = styles['Center'])
    Title24 = Paragraph('<font name="Times">Height/Length(mm)</font>',style = styles['Center'])
    Title25 = Paragraph('<font name="Times">Width(mm)</font>',style = styles['Center'])
    Title26 = Paragraph('<font name="Times">Thickness(mm)</font>',style = styles['Center'])
    Title27 = Paragraph('<font name="Times">Quantity</font>',style = styles['Center'])
    Title28 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    # Title29 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    # Title30 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    # Title31 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title32 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    Title33 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    data = [
        [Title1,  Title2,  Title3,  Title4, Title5, Title6, Title7,  Title8,  Title12,Title13],
        [Title21, Title22, Title23, Title24, Title25, Title26, Title27, Title28, Title32,Title33,],]
    for item in record:
        temp = item[0:8]+item[11:]
        if "检修门" in temp[1]:
            temp[1]="HB6 Inspection Door"
        if "检修口" in temp[1]:
            temp[1]="Hatch"
        data.append(temp)
    tableStyle =[
                           ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                           ('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 1), colors.khaki),
                           ('BACKGROUND', (6, 2), (7, -1), colors.beige),
                           # ('BACKGROUND', (6, 2), (7, -1), colors.pink),
                           ('BACKGROUND', (8, 2), (9, -1), colors.lavender),
                           ('SPAN',(0,0),(0,1)),
                           ('SPAN',(7,0),(7,1)),
                           # ('SPAN',(8,0),(8,1)),
                           # ('SPAN',(9,0),(9,1)),
                           # ('SPAN',(10,0),(10,1)),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
                           # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           # # ('ALIGN', (0, 3), (0, 3), 'CENTER'),
                           # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           # # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           # # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ]
    tableColWidths = [12*mm,45.0*mm,22.0*mm,34.0*mm,22.0*mm,28*mm,20.0*mm,20*mm,35*mm,35*mm]

    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    startY = 8 + (23 - len(data)) * 6.3
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    t.drawOn(c, 15 * mm, startY * mm)

def DrawQuotationSheetWetUnit(c,record,currencyName):
    styles = getSampleStyleSheet()
    # # Modify the Normal Style
    # styles["Normal"].fontSize = 12
    # styles["Normal"].leading = 14

    # Create a Justify style
    styles.add(ParagraphStyle(name='Center', alignment=1))
    Title1 = Paragraph('<font name="Times">Item</font>',style = styles['Center'])
    Title2 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title3 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title4 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title5 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title6 = Paragraph('<font name="Times">Product</font>',style = styles['Center'])
    Title7 = Paragraph('<font name="Times">Total</font>',style = styles['Center'])
    Title8 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    # Title9 = Paragraph('<font name="Times">Wet</font>',style = styles['Center'])
    # Title10 = Paragraph('<font name="Times">Strengthen</font>',style = styles['Center'])
    # Title11 = Paragraph('<font name="Times">OverWidth</font>',style = styles['Center'])
    Title12 = Paragraph('<font name="Times">Unit Price</font>',style = styles['Center'])
    Title13 = Paragraph('<font name="Times">Total Price</font>',style = styles['Center'])
    Title21 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title22 = Paragraph('<font name="Times">Type</font>',style = styles['Center'])
    Title23 = Paragraph('<font name="Times">Surface</font>',style = styles['Center'])
    Title24 = Paragraph('<font name="Times">Height/Length(mm)</font>',style = styles['Center'])
    Title25 = Paragraph('<font name="Times">Width(mm)</font>',style = styles['Center'])
    Title26 = Paragraph('<font name="Times">Thickness(mm)</font>',style = styles['Center'])
    Title27 = Paragraph('<font name="Times">Quantity</font>',style = styles['Center'])
    Title28 = Paragraph('<font name="Times">Unit</font>',style = styles['Center'])
    # Title29 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    # Title30 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    # Title31 = Paragraph('<font name="Times"></font>',style = styles['Center'])
    Title32 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    Title33 = Paragraph('<font name="Times">In %s</font>'%CURRENCYDICT[currencyName],style = styles['Center'])
    data = [
        [Title1,  Title2,  Title3,  Title4, Title5, Title6, Title7,  Title8,  Title12,Title13],
        [Title21, Title22, Title23, Title24, Title25, Title26, Title27, Title28, Title32,Title33,],]
    for item in record:
        temp = item[0:8]+item[11:]
        data.append(temp)
    tableStyle =[
                           ('GRID', (0, 0), (-1, -1), 0.5, colors.black),       #   类别，(起始列，起始行）,(结束列，结束行)，线宽，颜色  #GRID是内外都有线   #BOX是只有外框，内部没线
                           ('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 1), colors.khaki),
                           ('BACKGROUND', (6, 2), (7, -1), colors.beige),
                           # ('BACKGROUND', (6, 2), (7, -1), colors.pink),
                           ('BACKGROUND', (8, 2), (9, -1), colors.lavender),
                           ('SPAN',(0,0),(0,1)),
                           ('SPAN',(7,0),(7,1)),
                           # ('SPAN',(8,0),(8,1)),
                           # ('SPAN',(9,0),(9,1)),
                           # ('SPAN',(10,0),(10,1)),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('LINEABOVE', (0, 2), (-1, 2), 1, colors.black),
                           # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           # # ('ALIGN', (0, 3), (0, 3), 'CENTER'),
                           # ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           # ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           # # ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           # ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           # # ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ]
    tableColWidths = [12*mm,45.0*mm,22.0*mm,34.0*mm,22.0*mm,28*mm,20.0*mm,20*mm,35*mm,35*mm]

    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    startY = 8 + (23 - len(data)) * 6.3
    t = Table(data, style=tableStyle,colWidths=tableColWidths)
    t.wrapOn(c, 186.5 * mm, 800 * mm)
    t.drawOn(c, 15 * mm, startY * mm)

def MakeQuotationSheetTemplate(filename,dataWall=[],dataCeiling=[],dataInteriorDoor=[],dataFireDoor=[],dataWetUnit=[],dataNoteText=[],expiry=61,log=None, currencyName='人民币'):
    annotationList=dataNoteText
    gap = 6.3
    num = 31
    width, height =  (297 * mm, 210 * mm)
    pagesize = (297 * mm, 210 * mm)
    myCanvas = canvas.Canvas(filename, pagesize=pagesize)
    indexNum=1
    wallIndexNum=indexNum
    pageWall=int(np.ceil(len(dataWall)/20.))
    lastPageName="WALL"
    pageCeiling = int(np.ceil(len(dataCeiling)/20.))
    if pageCeiling>0:
        indexNum+=1
        lastPageName = "CEILING"
    ceilingIndexNum = indexNum
    pageInteriorDoor = int(np.ceil(len(dataInteriorDoor)/20.))
    if pageInteriorDoor>0:
        indexNum+=1
        lastPageName = "INTERIORDOOR"
    interiorDoorIndexNum = indexNum
    pageFireDoor = int(np.ceil(len(dataFireDoor)/20.))
    if pageFireDoor>0:
        indexNum+=1
        lastPageName = "FIREDOOR"
    fireDoorIndexNum=indexNum
    pageWetUnit = int(np.ceil(len(dataWetUnit)/20.))
    if pageWetUnit>0:
        indexNum+=1
        lastPageName = "WETUNIT"
    wetUnitIndexNum=indexNum
    # 这里的5是备注的那5行文字
    if lastPageName == "WALL":
        leftRows = 20 * pageWall - len(dataWall)
    if lastPageName == "CEILING":
        leftRows = 20 * pageCeiling - len(dataCeiling)
    if lastPageName == "INTERIORDOOR":
        leftRows = 20 * pageInteriorDoor - len(dataInteriorDoor)
    if lastPageName == "FIREDOOR":
        leftRows = 20 * pageFireDoor - len(dataFireDoor)
    if lastPageName == "WETUNIT":
        leftRows = 20 * pageWetUnit - len(dataWetUnit)
    if leftRows>=len(annotationList):
        pageTotal = pageWall + pageCeiling + pageInteriorDoor + pageFireDoor + pageWetUnit
    else:
        pageTotal = pageWall + pageCeiling + pageInteriorDoor + pageFireDoor + pageWetUnit + 1
    for pageNum in range(pageWall):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,550, text="伊纳克赛(南通)精致内饰材料有限公司产品报价单")
        # log.WriteText("here2"+bitmapDir+"logo.jpg")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 530,
                            width=40, height=40)
        # tempCode = 'O' + '%05d' % int(87) + '-' + '%s' % str(datetime.datetime.today())
        # tempCode = 'O' + '%05d' % int(87) + '-' + '%s' % "2022-07-28"
        # log.WriteText("here3"+dirName+"tempBarcode.png")
        # BarCodeGenerator(tempCode,dirName+"tempBarcode.png", log)
        # log.WriteText("overBarGenerator"+dirName+"tempBarcode.png")
        # myCanvas.drawImage(dirName+"tempBarcode.png", width-100, height-40,
        #                     width=100, height=40)
        # log.WriteText("here5"+dirName+"tempBarcode.png")
        myCanvas.setFont("Times", 18)
        myCanvas.drawCentredString(width/2,525, text="Inexa (NanTong) Interiors Co.Ltd Quotation Sheet")
        DrawLine(myCanvas,1,*coord(10, 28, height, mm),*coord(287, 28, height, mm))
        myCanvas.setFont("SimSun", 12)

        myCanvas.drawString(40,500, text="报价单号(Quotation Sheet No.):%s"%filename[-9:-4])
        myCanvas.drawRightString(width-50, 500, '出单日期(Date of Issue ):%s'%(datetime.date.today()))
        myCanvas.drawRightString(width-50, 480, '有效日期(Date of Expiry):%s'%(datetime.date.today()+datetime.timedelta(expiry)))
        myCanvas.drawString(40,470, text="Re:")
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,470, text="TNF accommodation system")
        myCanvas.drawString(40,450, text="%s) TNF Wall Panel"%wallIndexNum)
        DrawQuotationSheet(myCanvas,dataWall[pageNum*20:(pageNum+1)*20],currencyName)#A1代表非尾页，A3代表尾页
        if lastPageName == "WALL" and pageNum == (pageWall-1):
            myCanvas.setFont("SimSun", 8)
            if leftRows>len(annotationList):
                temp = len(annotationList)
            else:
                temp = leftRows
            for i in range(temp):
                myCanvas.drawString(40, 25+(leftRows-i-1)*18, text=annotationList[i])
        myCanvas.setFont("SimSun", 8)
        myCanvas.drawRightString(width - 50, 15, '页码(Page)：%s/%s' % (pageNum+1, pageTotal))
        myCanvas.showPage()  # 这句话相当于分页，显示页面即完成当前页面，开始新页面
    for pageNum in range(pageCeiling):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,550, text="伊纳克赛(南通)精致内饰材料有限公司产品报价单")
        # log.WriteText("here2"+bitmapDir+"logo.jpg")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 530,
                            width=40, height=40)
        # tempCode = 'O' + '%05d' % int(87) + '-' + '%s' % str(datetime.datetime.today())
        # tempCode = 'O' + '%05d' % int(87) + '-' + '%s' % "2022-07-28"
        # log.WriteText("here3"+dirName+"tempBarcode.png")
        # BarCodeGenerator(tempCode,dirName+"tempBarcode.png", log)
        # log.WriteText("overBarGenerator"+dirName+"tempBarcode.png")
        # myCanvas.drawImage(dirName+"tempBarcode.png", width-100, height-40,
        #                     width=100, height=40)
        # log.WriteText("here5"+dirName+"tempBarcode.png")
        myCanvas.setFont("Times", 18)
        myCanvas.drawCentredString(width/2,525, text="Inexa (NanTong) Interiors Co.Ltd Quotation Sheet")
        DrawLine(myCanvas,1,*coord(10, 28, height, mm),*coord(287, 28, height, mm))
        myCanvas.setFont("SimSun", 12)

        myCanvas.drawString(40,500, text="报价单号(Quotation Sheet No.):%s"%filename[-9:-4])
        myCanvas.drawRightString(width-50, 500, '出单日期(Date of Issue ):%s'%(datetime.date.today()))
        myCanvas.drawRightString(width-50, 480, '有效日期(Date of Expiry):%s'%(datetime.date.today()+datetime.timedelta(expiry)))
        myCanvas.drawString(40,470, text="Re:")
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,470, text="TNF accommodation system")
        myCanvas.drawString(40,450, text="%s) TNF Ceiling Panel"%ceilingIndexNum)
        DrawQuotationSheetCeiling(myCanvas,dataCeiling[pageNum*20:(pageNum+1)*20],currencyName)#A1代表非尾页，A3代表尾页
        if lastPageName == "CEILING" and pageNum == (pageCeiling-1):
            myCanvas.setFont("SimSun", 8)
            if leftRows>len(annotationList):
                temp = len(annotationList)
            else:
                temp = leftRows
            for i in range(temp):
                myCanvas.drawString(40, 25+(leftRows-i-1)*18, text=annotationList[i])
        myCanvas.setFont("SimSun", 8)
        myCanvas.drawRightString(width - 50, 15, '页码(Page)：%s/%s' % (pageNum +pageWall +1, pageTotal))
        myCanvas.showPage()  # 这句话相当于分页，显示页面即完成当前页面，开始新页面
    for pageNum in range(pageInteriorDoor):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,550, text="伊纳克赛(南通)精致内饰材料有限公司产品报价单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 530,
                            width=40, height=40)
        # tempCode = 'O' + '%05d' % int(87) + '-' + '%s' % str(datetime.datetime.today())
        # # BarCodeGenerator(tempCode,dirName+"tempBarcode.png",log)
        # myCanvas.drawImage(dirName+"tempBarcode.png", width-100, height-40,
        #                     width=100, height=40)
        myCanvas.setFont("Times", 18)
        myCanvas.drawCentredString(width/2,530, text="Inexa (NanTong) Interiors Co.Ltd Quotation Sheet")
        DrawLine(myCanvas,1,*coord(10, 28, height, mm),*coord(287, 28, height, mm))
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawString(40,500, text="报价单号(Quotation Sheet No.):%s"%filename[-9:-4])
        myCanvas.drawRightString(width-50, 500, '出单日期(Issue  Date):%s'%(datetime.date.today()))
        myCanvas.drawRightString(width-50, 480, '有效日期(Expiry Date):%s'%(datetime.date.today()+datetime.timedelta(expiry)))
        myCanvas.drawString(40,470, text="Re:")
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,470, text="TNF accommodation system")
        myCanvas.drawString(40,450, text="%s) TNF Interior Door"%interiorDoorIndexNum)
        DrawQuotationSheetInteriorDoor(myCanvas,dataInteriorDoor[pageNum*20:(pageNum+1)*19],currencyName)
        if lastPageName == "INTERIORDOOR" and pageNum == (pageInteriorDoor-1):
            myCanvas.setFont("SimSun", 8)
            if leftRows>len(annotationList):
                temp = len(annotationList)
            else:
                temp = leftRows
            for i in range(temp):
                myCanvas.drawString(40, 25+(leftRows-i-1)*18, text=annotationList[i])
        myCanvas.setFont("SimSun", 8)
        myCanvas.drawRightString(width - 50, 15, '页码(Page)：%s/%s' % (pageNum+1+pageWall+pageCeiling, pageTotal))
        myCanvas.showPage()  # 这句话相当于分页，显示页面即完成当前页面，开始新页面
    for pageNum in range(pageFireDoor):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,550, text="伊纳克赛(南通)精致内饰材料有限公司产品报价单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 530,
                            width=40, height=40)
        # tempCode = 'O' + '%05d' % int(87) + '-' + '%s' % str(datetime.datetime.today())
        # # BarCodeGenerator(tempCode,dirName+"tempBarcode.png",log)
        # myCanvas.drawImage(dirName+"tempBarcode.png", width-100, height-40,
        #                     width=100, height=40)
        myCanvas.setFont("Times", 18)
        myCanvas.drawCentredString(width/2,530, text="Inexa (NanTong) Interiors Co.Ltd Quotation Sheet")
        DrawLine(myCanvas,1,*coord(10, 28, height, mm),*coord(287, 28, height, mm))
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawString(40,500, text="报价单号(Quotation Sheet No.):%s"%filename[-9:-4])
        myCanvas.drawRightString(width-50, 500, '出单日期(Issue  Date):%s'%(datetime.date.today()))
        myCanvas.drawRightString(width-50, 480, '有效日期(Expiry Date):%s'%(datetime.date.today()+datetime.timedelta(expiry)))
        myCanvas.drawString(40,470, text="Re:")
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,470, text="TNF accommodation system")
        myCanvas.drawString(40,450, text="%s) TNF Fire Door"%fireDoorIndexNum)
        DrawQuotationSheetFireDoor(myCanvas,dataFireDoor[pageNum*20:(pageNum+1)*19],currencyName)
        if lastPageName == "FIREDOOR" and pageNum == (pageFireDoor-1):
            myCanvas.setFont("SimSun", 8)
            if leftRows>len(annotationList):
                temp = len(annotationList)
            else:
                temp = leftRows
            for i in range(temp):
                myCanvas.drawString(40, 25+(leftRows-i-1)*18, text=annotationList[i])
        myCanvas.setFont("SimSun", 8)
        myCanvas.drawRightString(width - 50, 15, '页码(Page)：%s/%s' % (pageNum+1+pageWall+pageCeiling+pageInteriorDoor, pageTotal))
        myCanvas.showPage()  # 这句话相当于分页，显示页面即完成当前页面，开始新页面
    for pageNum in range(pageWetUnit):
        myCanvas.setFont("SimSun", 18)
        myCanvas.drawCentredString(width/2,550, text="伊纳克赛(南通)精致内饰材料有限公司产品报价单")
        myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 530,
                            width=40, height=40)
        # tempCode = 'O' + '%05d' % int(87) + '-' + '%s' % str(datetime.datetime.today())
        # # BarCodeGenerator(tempCode,dirName+"tempBarcode.png",log)
        # myCanvas.drawImage(dirName+"tempBarcode.png", width-100, height-40,
        #                     width=100, height=40)
        myCanvas.setFont("Times", 18)
        myCanvas.drawCentredString(width/2,530, text="Inexa (NanTong) Interiors Co.Ltd Quotation Sheet")
        DrawLine(myCanvas,1,*coord(10, 28, height, mm),*coord(287, 28, height, mm))
        myCanvas.setFont("SimSun", 12)
        myCanvas.drawString(40,500, text="报价单号(Quotation Sheet No.):%s"%filename[-9:-4])
        myCanvas.drawRightString(width-50, 500, '出单日期(Issue  Date):%s'%(datetime.date.today()))
        myCanvas.drawRightString(width-50, 480, '有效日期(Expiry Date):%s'%(datetime.date.today()+datetime.timedelta(expiry)))
        myCanvas.drawString(40,470, text="Re:")
        myCanvas.setFont("Times", 12)
        myCanvas.drawCentredString(width/2,470, text="TNF accommodation system")
        myCanvas.drawString(40,450, text="%s) TNF Wet Unit"%wetUnitIndexNum)
        DrawQuotationSheetWetUnit(myCanvas,dataWetUnit[pageNum*20:(pageNum+1)*19],currencyName)
        if lastPageName == "WETUNIT" and pageNum == (pageWetUnit-1):
            myCanvas.setFont("SimSun", 8)
            if leftRows>len(annotationList):
                temp = len(annotationList)
            else:
                temp = leftRows
            for i in range(temp):
                myCanvas.drawString(40, 25+(leftRows-i-1)*18, text=annotationList[i])
        myCanvas.setFont("SimSun", 8)
        myCanvas.drawRightString(width - 50, 15, '页码(Page)：%s/%s' % (pageNum+1+pageWall+pageCeiling+pageInteriorDoor+pageFireDoor, pageTotal))
        myCanvas.showPage()  # 这句话相当于分页，显示页面即完成当前页面，开始新页面
    # if leftRows<12:
    #     myCanvas.setFont("SimSun", 18)
    #     myCanvas.drawCentredString(width/2,550, text="伊纳克赛(南通)精致内饰材料有限公司产品报价单")
    #     myCanvas.drawImage("D:/IPMS/dist/bitmaps/logo.jpg", 30, 530,
    #                         width=40, height=40)
    #     # tempCode = 'O' + '%05d' % int(87) + '-' + '%s' % str(datetime.datetime.today())
    #     # # BarCodeGenerator(tempCode,dirName+"tempBarcode.png",log)
    #     # myCanvas.drawImage(dirName+"tempBarcode.png", width-100, height-40,
    #     #                     width=100, height=40)
    #     myCanvas.setFont("Times", 18)
    #     myCanvas.drawCentredString(width/2,530, text="Inexa (NanTong) Interiors Co.Ltd Quotation Sheet")
    #     DrawLine(myCanvas,1,*coord(10, 28, height, mm),*coord(287, 28, height, mm))
    #     myCanvas.setFont("SimSun", 12)
    #     myCanvas.drawString(40,500, text="报价单号(Quotation Sheet No.):%s"%'64757-001')
    #     myCanvas.drawRightString(width-50, 500, '出单日期(Issue  Date):%s'%(datetime.date.today()))
    #     myCanvas.drawRightString(width-50, 480, '有效日期(Expiry Date):%s'%(datetime.date.today()+datetime.timedelta(expiry)))
    #     myCanvas.drawString(40,470, text="Re:")
    #     myCanvas.setFont("Times", 12)
    #     myCanvas.drawCentredString(width/2,470, text="TNF accommodation system")
    #     for i in range(12-leftRows):
    #         myCanvas.drawString(40, 440-i*18, text=annotationList[leftRows+i])
    #     myCanvas.showPage()
    myCanvas.save()
    log.WriteText("finish")

# def form_letter():
#     doc = SimpleDocTemplate("form_letter.pdf",
#                             pagesize=letter,
#                             rightMargin=72,
#                             leftMargin=72,
#                             topMargin=72,
#                             bottomMargin=18)
#     flowables = []
#     logo = bitmapDir+"/python_logo.png"
#     magName = "Pythonista"
#     issueNum = 12
#     subPrice = "99.00"
#     limitedDate = "03/05/2010"
#     freeGift = "tin foil hat"
#
#     formatted_time = time.ctime()
#     full_name = "Mike Driscoll"
#     address_parts = ["411 State St.", "Waterloo, IA 50158"]
#
#     im = Image(logo, 0.5 * inch, 0.5 * inch)
#     flowables.append(im)
#
#     styles = getSampleStyleSheet()
#     # Modify the Normal Style
#     styles["Normal"].fontSize = 12
#     styles["Normal"].leading = 14
#
#     # Create a Justify style
#     styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
#
#     flowables.append(Paragraph(formatted_time, styles["Normal"]))
#     flowables.append(Spacer(1, 12))
#
#     # Create return address
#     flowables.append(Paragraph(full_name, styles["Normal"]))
#     for part in address_parts:
#         flowables.append(Paragraph(part.strip(), styles["Normal"]))
#
#     flowables.append(Spacer(1, 12))
#     ptext = 'Dear {}:'.format(full_name.split()[0].strip())
#     flowables.append(Paragraph(ptext, styles["Normal"]))
#     flowables.append(Spacer(1, 12))
#
#     ptext = '''
#     We would like to welcome you to our subscriber
#     base for {magName} Magazine! You will receive {issueNum} issues at
#     the excellent introductory price of ${subPrice}. Please respond by
#     {limitedDate} to start receiving your subscription and get the
#     following free gift: {freeGift}.
#     '''.format(magName=magName,
#                issueNum=issueNum,
#                subPrice=subPrice,
#                limitedDate=limitedDate,
#                freeGift=freeGift)
#     flowables.append(Paragraph(ptext, styles["Justify"]))
#     flowables.append(Spacer(1, 12))
#
#     ptext = '''Thank you very much and we look
#     forward to serving you.'''
#
#     flowables.append(Paragraph(ptext, styles["Justify"]))
#     flowables.append(Spacer(1, 12))
#     ptext = 'Sincerely,'
#     flowables.append(Paragraph(ptext, styles["Normal"]))
#     flowables.append(Spacer(1, 48))
#     ptext = 'Ima Sucker'
#     flowables.append(Paragraph(ptext, styles["Normal"]))
#     flowables.append(Spacer(1, 12))
#     doc.build(flowables)


if __name__ == '__main__':
    # form_letter()
    # MakeGlueNoSheetTemplate(64730,1,"glue.pdf",[[121, 64730, '2', '1', '9', 'CREW  MESS', 'N.2SF.0867', '0', 'YC08E', 'G', '2160', '200', '25', 1, 'None', 'None', '64730-0121']])
    dataWall = [
            ['1', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['2', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['3', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['4', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['5', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['6', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['7', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['8', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['9', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['10', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['11', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['12', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['13', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['14', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['15', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['16', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['17', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['18', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['19', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['20', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            # ['21', '1122', 'N.2SA.0001', '1495', '548', '50', '79070', 'G', '', ''],
            # ['22', '1122', 'CC64001', '1495', '548', '25', '79070', 'G', '', ''],
            # ['23', '1122', 'N.2SA.0001', '1495', '548', '100', '79070', 'G', '', ''],
            # ['24', '1122', 'N.2SA.0001', '1495', '548', '50', '79070', 'G', '', ''],
            # ['25', '1122', 'N.2SA.0001', '1495', '548', '50', '79070', 'G', '', ''],
            # ['26', '1122', 'N.2SA.0001', '1495', '548', '50', '79070', 'G', '', ''],
            # ['27', '1122', 'CC64001', '1495', '548', '25', '79070', 'G', '', ''],
    ]
    dataCeiling = [
            ['1', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['2', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['3', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['4', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['5', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['6', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['7', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['8', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['9', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['10', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['11', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['12', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['13', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['14', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['15', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['16', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['17', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['18', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['19', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            ['20', 'TNF-2SF', 'B15 Partition', 'S.S(304)/S.S(304)','≤2500', '600','25','m2','1500','$235.15','$123456.15'],
            # ['21', '1122', 'N.2SA.0001', '1495', '548', '50', '79070', 'G', '', ''],
            # ['22', '1122', 'CC64001', '1495', '548', '25', '79070', 'G', '', ''],
            # ['23', '1122', 'N.2SA.0001', '1495', '548', '100', '79070', 'G', '', ''],
            # ['24', '1122', 'N.2SA.0001', '1495', '548', '50', '79070', 'G', '', ''],
            # ['25', '1122', 'N.2SA.0001', '1495', '548', '50', '79070', 'G', '', ''],
            # ['26', '1122', 'N.2SA.0001', '1495', '548', '50', '79070', 'G', '', ''],
            # ['27', '1122', 'CC64001', '1495', '548', '25', '79070', 'G', '', ''],
    ]
    MakeQuotationSheetTemplate(quotationSheetDir+'报价单00087.pdf',dataWall,dataCeiling)

