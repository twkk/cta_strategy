""" 
 init from vnpy double_ma_strategy.py
 org cutomer args 
     fast_window = 10,slow_window = 20,self.load_bar(10) 
2020.2.1 KK Taiwan
修正模式 減少訊號 改用 5mins, 8mins, 15mins 實驗 macd 敏感度 >>


風控  新增持倉
      確認長期訊號 >> 確認短期操作時間點
       if 額度 < 3 淨持倉 
       if Buy_singal_Long_MACD  
          if Buy_sigal-Short
       else Sell_singal_Long_MACD  
          if Sell_sigal-Short 

風控  減少持倉
     短期倉過期,部分停損停利 
      1 符合長期訊號 > 跟新短倉持有時限
      1 尋找平倉機會
      2 震盪區 保險對稱單

From 海龜 
if bar.datetime.time() < self.exit_time:
  if self.pos == 0:     
    if bar.close_price > self.day_open:
       if not self.long_entered:
           self.buy(self.long_entry, self.fixed_size, stop=True)
        else:
            if not self.short_entered:
               self.short(self.short_entry, self.fixed_size, stop=True)
   else:            
     if self.pos > 0:
        self.sell(bar.close_price * 0.99, abs(self.pos))
     elif self.pos < 0:
        self.cover(bar.close_price * 1.01, abs(self.pos))
      
on_order(self, order: OrderData):
order.vt_orderid 訂單
移動平均線收斂/發散  技術指標是26週期和12週期指數移動平均線（EMA）之間的差
買/賣機會，MACD圖表上繪製了一條所謂的信號線（該指標的9個週期移動均線）
這邊非標準的 macd 訊號~ double_ma 使用了Sma 訊號代替 Ema訊號 (計算上簡單多了)
先利用收盤價的指數移動平均值 EMA（12日／26日）計算出差離值
EMA(26)可視為MACD的零軸

DEMA Double Exponential Moving Average
EMA Exponential Moving Average
SMA Simple Moving Average
T3 Triple Exponential Moving Average (T3)
TEMA Triple Exponential Moving Average
TRIMA Triangular Moving Average
WMA Weighted Moving Average

不支持ema ?看看Talib，要改改arraymanager就可以，不过记得有文章讨论过，这个ema和国内行情软件ema不是一样
"""

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


class DoubleMaStrategy(CtaTemplate):
    author = "KK Taiwan 交易員"

    fast_window = 12   # init define for 5mins * 12 = 1HR   
    slow_window = 36   # inti define for 5mins * 36 = 3HR

    fast_ma0 = 0.0
    fast_ma1 = 0.0

    slow_ma0 = 0.0
    slow_ma1 = 0.0

    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(36)       #回測時載入10個交易日用於數據初始化

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

        self.put_event()

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """

        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        fast_ma = am.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]

        slow_ma = am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]

        cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1

        if cross_over:
            if self.pos == 0:
                self.buy(bar.close_price, 1)
            elif self.pos < 0:
                self.cover(bar.close_price, 1)
                self.buy(bar.close_price, 1)

        elif cross_below:
            if self.pos == 0:
                self.short(bar.close_price, 1)
            elif self.pos > 0:
                self.sell(bar.close_price, 1)
                self.short(bar.close_price, 1)

        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
