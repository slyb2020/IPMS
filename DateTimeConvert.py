import datetime
import wx
def pydate2wxdate(date):
     assert isinstance(date, (datetime.datetime, datetime.date))
     tt = date.timetuple()
     dmy = (tt[2], tt[1]-1, tt[0])
     return wx.DateTime.FromDMY(*dmy)

def wxdate2pydate(date):
     assert isinstance(date, wx.DateTime)
     if date.IsValid():
          ymd = map(int, date.FormatISODate().split('-'))
          return datetime.date(*ymd)
     else:
          return None

def str2wxdate(dateStr):
     date = dateStr.split('-')
     date = wx.DateTime.FromDMY(int(date[2]), int(date[1])-1, int(date[0]))
     return date
