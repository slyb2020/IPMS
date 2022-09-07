# code128
from pystrich.code128 import Code128Encoder
def BarCodeGenerator(code,filename="tempBarcode.png",log=None):
    log.WriteText("making barcode:"+filename)
    encoder = Code128Encoder(code)
    encoder.save(filename, bar_width=2)

import os
import barcode
from barcode.writer import ImageWriter

# import matplotlib.pyplot as plt  # plt 用于显示图片
# import matplotlib.image as image
# name = barcode.generate(u'code128', u'363287468748243', writer=ImageWriter(), output='barcode_png')
# im = image.imread(name)  # 读取图片文件
# plt.imshow(im)  # 显示图片
# plt.axis('off')  # 不显示坐标轴
# plt.show()
# os.remove(name)
# def BarCodeGenerator(code,filename="tempBarcode",log=None):
#     print("here code",filename)
#     filename=filename[:-4]
#     EAN = barcode.get_barcode_class('code39')  # 创建ean13格式的条形码格式对象 参数为支持的格式
#     ean = EAN(code,writer=ImageWriter())  # 创建条形码对象，内容为5901234123457
#     ean.save("D:\\IPMS\\dist\\temp")  # #此处不需要输入文件后缀 保存条形码图片，并返回保存路径。图片格式为png
