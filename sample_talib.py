"""
在python策略中使用Ta-lib計算技術指標

# macd = 12 天 EMA - 26 天 EMA   快線
# macdsignal = 9 天 MACD的EMA    慢線
# macdhist = MACD - MACD signal  柱狀圖

MACD指標程式
快線(DIF)= MACD( Close, FastLength, SlowLength )  = var0  = MACD( Close, 12, 26 ) ;
慢線(MACD) = XAverage( var0, MACDLength )         = var1 = XAverage( var0, 9 ) ;
柱狀線(DIF-MACD)= 快線(DIF) - 慢線(MACD)           = var2 = var0 - var1 ;
#柱線OSC = 時間差DIF–MACD = (Ema12 - Ema26) - 9日均線(Ema12 - Ema26) =[(fast_ma[0]+fast_ma[-1]+fast_ma[-2]+...fast_ma[-8]) -(slow_ma[0]+slow_ma[-1]+slow_ma[-2]...+slow_ma[-8])]/9
#MACD = DIF12的9日移動平均 = EMA(DIF,9)
#EMA(26)可視為MACD的零

MA1=Average(close,Len1);
MA2=Average(close,Len2);



"""

import talib
import numpy 
import pandas

def init(context):  
    context.s1 = "000024.XSHE"
    
def handle_bar(context, bar_dict):

    


    close       = history_bars(context.s1,50,'1d','close')
    closeArray  = numpy.array(self.closeHistory)
    #DIFF，使用talib的EMA 函數直接計算 
    self.MACD_DIFF_array[-1] = talib.EMA(self.close_array,timeperiod = self.MACD_SHORT)[-1] - talib.EMA(self.close_array,timeperiod = self.MACD_LONG)[-1]
    #DEA
    self.MACD_DEA_array[-1] = talib.EMA(self.MACD_DIFF_array,timeperiod = self.MACD_M)[-1]
    #柱狀線  2*(DIFF-DEA),COLORSTICK;//DIFF减DEA的2倍 畫柱狀線
    self.MACD_array[-1] = (self.MACD_DIFF_array[-1] - self.MACD_DEA_array[-1]) * 2
    
    macd,macdsignal,macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    在vnpy中
    macd,macdsignal,macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    
    SMA = talib.MA(close,30,matype=0)[-1]
    EMA = talib.MA(close,30,matype=1)[-1]
    WMA = talib.MA(close,30,matype=2)[-1]
    DEMA = talib.MA(close,30,matype=3)[-1]
    TEMA = talib.MA(close,30,matype=4)[-1]
