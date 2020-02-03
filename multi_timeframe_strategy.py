'''
vnpy\trader\object.py   @dataclass  class BarData(BaseData):
vnpy\trader\utility.py              class BarGenerator:
 self.bg5 = BarGenerator(self.on_bar, 5, self.on_5min_bar)
    1. generating 1 minute bar data from tick data
    2. generateing x minute bar/x hour bar data from 1 minute data
    Notice:
    1. for x minute bar, x must be able to divide 60: 2, 3, 5, 6, 10, 15, 20, 30
    2. for x hour bar, x can be any number

週期策略    on_bar(self, bar: BarData): 短長周期跟新檢查

2020.2.1 KK Taiwan
修正模式 減少訊號 改用 5mins, 8mins, 15mins 實驗 macd 敏感度 >>

長周期定義 15mins 

  買進區間 短突破長向上~到零點之間價位 最高最低 時間區間 
  賣出區間 短突破長向下~到零點之間價位 最高最低 時間區間

 買進區間 到零點 最大持倉量為4  為T1 買進均價 > 最高最低點/2 >> 買進剩下的 >> 
                update 持倉週期的停損停利 時間週期2T if 獲利 跟新長期停損點以零點為基礎  時間週期3T 以2T為長期停損點
                停損停利點零點為基準的停損停利點
 非買進區間 最大買賣量為2
  
  停利訊號
 
 平倉 目標 修改止價 >>停損零點
 
   
短周期定義  5mins


風控  新增持倉
      確認長期訊號 >> 確認短期操作時間點
      長期訊號經過時間 /前一個長期訊號時間長短
       if 額度 < 3 淨持倉 
       if Buy_singal_Long_MACD  
          if Buy_sigal-Short
             buy
       else Sell_singal_Long_MACD  
          if Sell_sigal-Short 
             short
風控  減少持倉
     短期倉過期,部分停損停利 
      1 符合長期訊號 > 跟新短倉持有時限
      1 尋找平倉機會
        sell
        cover
      2 震盪區 保險對稱單

'''
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


class MultiTimeframeStrategy(CtaTemplate):
    """"""
    author = "KK Taiwan 交易員"

    rsi_signal = 20
    rsi_window = 14
    fast_window = 12 # init define for 5mins * 12 = 1HR  
    slow_window = 30# inti define for 5mins * 36 = 3HR
    fixed_size = 1

    rsi_value = 0
    rsi_long = 0
    rsi_short = 0
    fast_ma = 0
    slow_ma = 0
    ma_trend = 0

    parameters = ["rsi_signal", "rsi_window",
                  "fast_window", "slow_window",
                  "fixed_size"]

    variables = ["rsi_value", "rsi_long", "rsi_short",
                 "fast_ma", "slow_ma", "ma_trend","fast_ma1","slow_ma1"]
    

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.rsi_long = 50 + self.rsi_signal
        self.rsi_short = 50 - self.rsi_signal

        self.bg5 = BarGenerator(self.on_bar, 5, self.on_5min_bar)
        self.am5 = ArrayManager()

        self.bg15 = BarGenerator(self.on_bar, 15, self.on_15min_bar)
        self.am15 = ArrayManager()
        
            



    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg5.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        確認長短週期策略
        """
        self.bg5.update_bar(bar)
        self.bg15.update_bar(bar)

    def on_5min_bar(self, bar: BarData):
        """"""
        self.cancel_all()

        self.am5.update_bar(bar)
        if not self.am5.inited:
            return

        if not self.ma_trend:
            return

        self.rsi_value = self.am5.rsi(self.rsi_window)

        if self.pos == 0:
            if self.ma_trend > 0 and self.rsi_value >= self.rsi_long:
                self.buy(bar.close_price + 5, self.fixed_size)
            elif self.ma_trend < 0 and self.rsi_value <= self.rsi_short:
                self.short(bar.close_price - 5, self.fixed_size)

        elif self.pos > 0:
            if self.ma_trend < 0 or self.rsi_value < 50:
                self.sell(bar.close_price - 5, abs(self.pos))

        elif self.pos < 0:
            if self.ma_trend > 0 or self.rsi_value > 50:
                self.cover(bar.close_price + 5, abs(self.pos))

        ###KK 跟新長倉策略
        self.pettyfast_ma = self.am5.sma(self.fast_window)
        self.pettyslow_ma = self.am5.sma(self.slow_window)
        if self.pettyfast_ma > self.pettyslow_ma:
            self.ma_pettytrend = 1
        else:
            self.ma_pettytrend = -1
          
 
        
        if(buy list) 
          if (self.ma_pettytrend < 0) and (time > 0)
             if 虧 
              平倉時間點限制 - 2 time
              if < 1 平倉
             else
              平倉時間點限制 - time 
             if < 1
               跟新下限 from 15 mins均線
               #改為短平倉 and update limit
          else if time < 10
             平倉時間點限制 +time

        if(short list) 
           if (self.ma_pettytrend > 0) and (time > 0)
             if 虧 
               平倉時間點限制 - 2 time
               if timw<1
                  平倉
             else
              平倉時間點限制 - time
               if < 1
                   跟新下限 from 15 mins均線
          else if time < 10 
             平倉時間點限制 + time

        if self.pos == 0:
            if self.ma_trend > 0 and self.rsi_value >= self.rsi_long:
                self.buy_signal(bar.close_price + 5, self.fixed_size)
            elif self.ma_trend < 0 and self.rsi_value <= self.rsi_short:
                self.short(bar.close_price - 5, self.fixed_size)

        elif self.pos > 0:
            if self.ma_trend < 0 or self.rsi_value < 50:
                self.sell_signal(bar.close_price - 5, abs(self.pos))

        elif self.pos < 0:
            if self.ma_trend > 0 or self.rsi_value > 50:
                self.cover_signal(bar.close_price + 5, abs(self.pos))
        ###
            
        self.put_event()

    def on_15min_bar(self, bar: BarData):
        """"""
        self.am15.update_bar(bar)
        if not self.am15.inited:
            return

        self.fast_ma = self.am15.sma(self.fast_window)
        self.slow_ma = self.am15.sma(self.slow_window)
        if self.fast_ma > self.slow_ma:
            self.ma_trend = 1     增持
        else:
            self.ma_trend = -1    減持
          
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]
        cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1
        
#當柱線 接近0時，持有持間短 柱線離0遠時持有持間長
#MACD = DIF12的9日移動平均 = EMA(DIF,9)
#柱線OSC = 時間差DIF–MACD = (Ema12 - Ema26) - 9日均線(Ema12 - Ema26) =[(fast_ma[0]+fast_ma[-1]+fast_ma[-2]+...fast_ma[-8]) -(slow_ma[0]+slow_ma[-1]+slow_ma[-2]...+slow_ma[-8])]/9
#EMA(26)可視為MACD的零
       check long 倉位
        柱狀下面 奇數次向上突破 淨多單 
                 偶數次突破     平倉
       
   
   
        if cross_over: 紅向上穿出 
        if 下半部柱狀
           開倉多單
        else if 上半部柱狀
           開倉空單
        if cross_over: 紅穿入
           if 下半部柱狀
              平倉多單
           else if 上半部柱狀
              平倉空單
            
            if self.pos == 0:                    #1.柱線由負轉正，為買進訊號。
                self.buy(bar.close_price, 1)     #15mins   越0 增持到長多滿足 第二次買進
            elif self.pos < 0:
                if net stock 多 or 0
                   self.buy(bar.close_price, 1)     #15mins 抄低點增持多單  第一次買進
                else net stock 空
                   self.cover(bar.close_price, 1) #減持空單
           
        elif cross_below:
            if self.pos == 0:                   #柱線由正轉負，為賣出訊號。 
                self.short(bar.close_price, 1)  #15 mins 越0 增持到空單滿足 第二次空單
            elif self.pos > 0:
                if net stock 空 or 0                  #增持空單
                   self.short(bar.close_price, 1)     #15mins 抄低點增持多單  第一次買進
                else net stock 多
                   self.sell(bar.close_price, 1) # 減持多單         

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
