"""
在python策略中使用Ta-lib計算技術指標

# macd = 12 天 EMA - 26 天 EMA   快線
# macdsignal = 9 天 MACD的EMA    慢線
# macdhist = MACD - MACD signal  柱狀圖

ArrayManager>>
vnpy_eng/vnpy/trader/utility.py 
import json
from pathlib import Path
from typing import Callable
from decimal import Decimal

import numpy as np
import talib

class ArrayManager(object):
@property
    def close(self):
    def volume(self):
    def close(self):
    def low(self):
    def high(self):
    def open(self):
    def sma(self, n, array=False):
    def macd(self, fast_period, slow_period, signal_period, array=False):
    def boll(self, n, dev, array=False):
    def keltner(self, n, dev, array=False):
    
    def macd(self, fast_period, slow_period, signal_period, array=False):
        """
        MACD.
        """
        macd, signal, hist = talib.MACD(
            self.close, fast_period, slow_period, signal_period
        )
        if array:
            return macd, signal, hist
        return macd[-1], signal[-1], hist[-1]
"""

import talib
import numpy 
import pandas

from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)



def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
    """"""
    super(MultiTimeframeStrategy, self).__init__(
          cta_engine, strategy_name, vt_symbol, setting
         )
    context.s1 = "000024.XSHE"
    self.bg15 = BarGenerator(self.on_bar, 15, self.on_15min_bar)
    self.am15 = ArrayManager()

def handle_bar(context, bar_dict):

    close       = history_bars(context.s1,50,'1d','close')
    closeArray  = numpy.array(self.closeHistory)
    
    macd,macdsignal,macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
   
    #在vnpy中 return macd[-1], signal[-1], hist[-1] 
    ArrayManager talib.MACD(self.close, fast_period, slow_period, signal_period)
    macd,DIFF,macdhist = self.am15.macd(12,26,9)
     
    SMA = talib.MA(close,30,matype=0)[-1]
    EMA = talib.MA(close,30,matype=1)[-1]
    WMA = talib.MA(close,30,matype=2)[-1]
    DEMA = talib.MA(close,30,matype=3)[-1]
    TEMA = talib.MA(close,30,matype=4)[-1]
