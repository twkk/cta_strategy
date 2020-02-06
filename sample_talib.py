"""
在python策略中使用Ta-lib計算技術指標

# macd = 12 天 EMA - 26 天 EMA   快線
# macdsignal = 9 天 MACD的EMA    慢線
# macdhist = MACD - MACD signal  柱狀圖

"""

import talib
import numpy 
import pandas

def init(context):  
    context.s1 = "000024.XSHE"
    
def handle_bar(context, bar_dict):

    


    close       = history_bars(context.s1,50,'1d','close')
    closeArray  = numpy.array(self.closeHistory)
    
    macd,macdsignal,macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    在vnpy中
    macd,macdsignal,macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    
    SMA = talib.MA(close,30,matype=0)[-1]
    EMA = talib.MA(close,30,matype=1)[-1]
    WMA = talib.MA(close,30,matype=2)[-1]
    DEMA = talib.MA(close,30,matype=3)[-1]
    TEMA = talib.MA(close,30,matype=4)[-1]
