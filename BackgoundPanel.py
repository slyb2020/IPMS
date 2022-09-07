import cv2
import wx
import images
from ID_DEFINE import *
from MyLog import MyLogCtrl

class BackgroundPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_THEME)
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, evt):
        self.Refresh()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("WHITE"))
        dc.Clear()
        x,y = self.GetClientSize()
        bmp = wx.Image(bitmapDir+'/BackgroundPIC.jpg').Scale(width=x, height=y,
                                                  quality=wx.IMAGE_QUALITY_BOX_AVERAGE).ConvertToBitmap()
        dc.DrawBitmap(bmp, 0, 0, True)
