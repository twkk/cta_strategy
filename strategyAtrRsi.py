# 編碼：UTF-8

“”
一個ATR-RSI指標結合的交易策略，適合用在股指的1分鐘和5分鐘線上。
注意事項：
1.作者不對交易盈利做任何保證，策略代碼有所參考
2.本策略需要用到talib，沒有安裝的用戶請先參考www.vnpy.org上的教程安裝
3.將IF0000_1min.csv用ctaHistoryData.py引入MongoDB後，直接運行本文件即可回測策略
“”


from ctaBase import *
from ctaTemplate import CtaTemplate

import talib
import numpy as np


########################################################################
class AtrRsiStrategy(CtaTemplate):
    “”“”結合ATR和RSI指標的一個分鐘線交易策略“”“
    className = 'AtrRsiStrategy'
    author = u'用Python的交易员'

    # 策略参数
    atrLength = 22          # 計算ATR指标的窗口數 
    atrMaLength = 10        # 計算ATR均线的窗口數
    rsiLength = 5           # 計算RSI的窗口數
    rsiEntry = 16           # RSI的開倉信號
    trailingPercent = 0.8   # 百分比移動止損
    initDays = 10           # 初始化數據所用的天數

    # 策略变量
    bar = None                  # K線對象
    barMinute = EMPTY_STRING    # K線當前的分鐘

    bufferSize = 100                    # 需要暫存的數據大小
    bufferCount = 0                     # 已經暫存的數據計數
    highArray = np.zeros(bufferSize)    # K線最高價的數據
    lowArray = np.zeros(bufferSize)     # K線最低價的數據
    closeArray = np.zeros(bufferSize)   # K線收盤價价的數據

    atrCount = 0                        # 目前已经暫存了的ATR的計數
    atrArray = np.zeros(bufferSize)     # ATR指标的数组
    atrValue = 0                        # 最新的ATR指标數值
    atrMa = 0                           # ATR移动平均的數值

    rsiValue = 0                        # RSI指标的數值
    rsiBuy = 0                          # RSI买开閥值
    rsiSell = 0                         # RSI卖开閥值
    intraTradeHigh = 0                  # 移动止損用的持倉期内最高價
    intraTradeLow = 0                   # 移动止損用的持倉期内最低價

    orderList = []                      # 保存委托代码的列表

    # 参数列表，保存了参数的名稱
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol',
                 'atrLength',
                 'atrMaLength',
                 'rsiLength',
                 'rsiEntry',
                 'trailingPercent']    

    # 變量列表，保存了變量的名稱
    varList = ['inited',
               'trading',
               'pos',
               'atrValue',
               'atrMa',
               'rsiValue',
               'rsiBuy',
               'rsiSell']  

    #----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        """Constructor"""
        super(AtrRsiStrategy, self).__init__(ctaEngine, setting)

    #----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户繼承實現）"""
        self.writeCtaLog(u'%s策略初始化' %self.name)

        # 初始化RSI入場閥值
        self.rsiBuy = 50 + self.rsiEntry
        self.rsiSell = 50 - self.rsiEntry

        # 载入歷史數據，并采用回放计算的方式初始化策略数值
        initData = self.loadBar(self.initDays)
        for bar in initData:
            self.onBar(bar)

        self.putEvent()

    #----------------------------------------------------------------------
    def onStart(self):
        """啟動策略（必须由用户繼承實現）"""
        self.writeCtaLog(u'%s策略啟動' %self.name)
        self.putEvent()

    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户繼承實現）"""
        self.writeCtaLog(u'%s策略停止' %self.name)
        self.putEvent()

    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        # 計算K線
        tickMinute = tick.datetime.minute

        if tickMinute != self.barMinute:    
            if self.bar:
                self.onBar(self.bar)

            bar = CtaBarData()              
            bar.vtSymbol = tick.vtSymbol
            bar.symbol = tick.symbol
            bar.exchange = tick.exchange

            bar.open = tick.lastPrice
            bar.high = tick.lastPrice
            bar.low = tick.lastPrice
            bar.close = tick.lastPrice

            bar.date = tick.date
            bar.time = tick.time
            bar.datetime = tick.datetime    # K线的时间设为第一个Tick的时间

            self.bar = bar                  # 这种写法为了减少一层访问，加快速度
            self.barMinute = tickMinute     # 更新当前的分钟
        else:                               # 否则继续累加新的K线
            bar = self.bar                  # 写法同样为了加快速度

            bar.high = max(bar.high, tick.lastPrice)
            bar.low = min(bar.low, tick.lastPrice)
            bar.close = tick.lastPrice

    #----------------------------------------------------------------------
    def onBar(self, bar):
        “”“收到Bar按下（必須由用戶繼承實現）”“”
        # 取消之前發出的尚未成交的委託（包括限價單和停止單）
        for orderID in self.orderList:
            self.cancelOrder(orderID)
        self.orderList = []

        # 保存K線數據
        self.closeArray[0:self.bufferSize-1] = self.closeArray[1:self.bufferSize]
        self.highArray[0:self.bufferSize-1] = self.highArray[1:self.bufferSize]
        self.lowArray[0:self.bufferSize-1] = self.lowArray[1:self.bufferSize]

        self.closeArray[-1] = bar.close
        self.highArray[-1] = bar.high
        self.lowArray[-1] = bar.low

        self.bufferCount += 1
        if self.bufferCount < self.bufferSize:
            return

        # 计算指标数值
        self.atrValue = talib.ATR(self.highArray, 
                                  self.lowArray, 
                                  self.closeArray,
                                  self.atrLength)[-1]
        self.atrArray[0:self.bufferSize-1] = self.atrArray[1:self.bufferSize]
        self.atrArray[-1] = self.atrValue

        self.atrCount += 1
        if self.atrCount < self.bufferSize:
            return

        self.atrMa = talib.MA(self.atrArray, 
                              self.atrMaLength)[-1]
        self.rsiValue = talib.RSI(self.closeArray, 
                                  self.rsiLength)[-1]

        # 判断是否要进行交易

        # 当前无仓位
        if self.pos == 0:
            self.intraTradeHigh = bar.high
            self.intraTradeLow = bar.low

            #ATR數值上穿其移動平均線，說明行情短期內波動增大
            #即處於趨勢的概率緊張，適合CTA開倉
            if self.atrValue > self.atrMa:
                ＃使用RSI指標的趨勢行情時，會在超買超賣區鈍化特徵，作為開倉信號
                if self.rsiValue > self.rsiBuy:
                    ＃這里為了保證成交，選擇超價5個整指數點下單
                    self.buy(bar.close+5, 1)
                    return

                if self.rsiValue < self.rsiSell:
                    self.short(bar.close-5, 1)
                    return

        # 持有多頭倉位
        if self.pos == 1:
            # 計算多頭持有期内的最高價，以及重置最低價
            self.intraTradeHigh = max(self.intraTradeHigh, bar.high)
            self.intraTradeLow = bar.low
            ＃計算多頭移動止損
            longStop = self.intraTradeHigh * (1-self.trailingPercent/100)
            ＃發布本地止損委託，並把委託號記錄下來，用於後續撤單
            orderID = self.sell(longStop, 1, stop=True)
            self.orderList.append(orderID)
            return

        # 持有空頭倉位
        if self.pos == -1:
            self.intraTradeLow = min(self.intraTradeLow, bar.low)
            self.intraTradeHigh = bar.high

            shortStop = self.intraTradeLow * (1+self.trailingPercent/100)
            orderID = self.cover(shortStop, 1, stop=True)
            self.orderList.append(orderID)
            return

        # 發出狀態跟事件
        self.putEvent()

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托變化推送（必须由用户繼承實現）"""
        pass

    #----------------------------------------------------------------------
    def onTrade(self, trade):
        pass


if __name__ == '__main__':
    # 提供直接雙擊回測的功能
    # 導入PyQt4的包是为了保證 matplotlib使用PyQt4 而不是PySide，防止初始化出错
    from ctaBacktesting import *
    from PyQt4 import QtCore, QtGui

    # 創建回测引擎
    engine = BacktestingEngine()

    # 設置引擎的回測模式为K線
    engine.setBacktestingMode(engine.BAR_MODE)

    # 設置回测用的數據起始日期
    engine.setStartDate('20150101')

    # 载入歷史數據到引擎中
    engine.loadHistoryData(MINUTE_DB_NAME, 'IF0000')

    # 設置產品相關參數
    engine.setSlippage(0.2)     # 股指1跳
    engine.setRate(0.3/10000)   # 0.3/萬
    engine.setSize(300)         # 股指合约大小    

    # 在引擎中創建策略對象
    engine.initStrategy(AtrRsiStrategy, {})

    # 開始跑回測
    engine.runBacktesting()

    # 顯示回測结果
    engine.showBacktestingResult()
