'''
MACD指標程式
快線(DIF)= MACD( Close, FastLength, SlowLength )  = var0  = MACD( Close, 12, 26 ) ;
慢線(MACD) = XAverage( var0, MACDLength )         = var1 = XAverage( var0, 9 ) ;
柱狀線(DIF-MACD)= 快線(DIF) - 慢線(MACD)           = var2 = var0 - var1 ;

柱狀由上升轉下降~多倉平倉 轉放空 有可能迴轉 (停損點)
      紅線與柱狀線交錯 加碼     有可能再交錯 
       
柱狀由下降轉上升~空倉平   轉多   有可能迴轉 (停損點)
      紅線與柱線交錯   加碼      迴轉 (再次交錯)
     
If 柱狀線> 0 and MA1 cross over MA2 then Buy this bar on close;

If var2> 0 and MA1 cross over MA2 then Buy this bar on close;
If var2< 0 and MA1 cross below MA2 then SellShort this bar on close;

  #在vnpy中 return macd[-1], signal[-1], hist[-1] 
    ArrayManager talib.MACD(self.close, fast_period, slow_period, signal_period)
    macd_DIF,macd_DEA ,macd_HIST  = self.am15.macd(12,26,9)

IF （快線穿入柱線在　上面　）(柱線>快線 & 快線>0 )　柱線OSC > 快線DIF　>0

self.pos： 倉位  怎麼判斷的check from on trade?

 

開倉檢查策略 時間週期長 >> 時間週期短 確保masttime 持倉策略長的能夠不被短的影響
短周期與長週期策略衝突  >> ATR*unit < Var 減持 or ATR unit > Var 開新反向短倉
 
 ver0.3
 　風控-
   1.
   4個Macd 長短週期使得決策複雜,倉位數量不足下使得多空單處理不良會有不對偁的狀況,長週期便於為取最長的上升下區段
   (只需要在長週期的下一次運算時計算更長周期即可確認此一長周期比例)
   風控靠長周期   ～置換成兩個主macd計算,由實際波段觀察這個使用15mins作為長區間,　用60mins 確認長周期範圍　
   買賣時間點短周期～短線週期用　5分鐘線 1分鐘假訊號太多要實際測試看濾網效果是否可以使用更敏感的分鐘線創造更佳的獲益率　
   2.開倉平倉策略
   分四次增持倉位　停頓兩次後　兩次減持    
   
       財務風險控制   最大/最小持倉    masktime
   60mins 2次/day         
   15mins 8次/day    2~1 / 1~0.5      10 mins   總共四個單位     
   5mins 16次/day       0.5  0.5       3 mins　　靠不同時間點分次採買達到目標持倉量
   1mins  6次/HR none offfical
   
   濾網 1
        突破訊號　濾網 (macd > 5)
        突破訊號　濾網 (快線向上　RSI < 40),( 快線向下 RSI > 60)
        
        mask 15mins 倉位建立後第一個訊號短倉反向訊號
    
    from_15_macd
       濾網　長時間震盪　- 濾網 (-5 ＜ 柱狀 < 5) 長倉無方向性　長倉歸零　
       　　　柱狀大小　定義持倉量　穿越方向決定　增倉方向
       
       長倉變動時間點
       1.macd 操作　穿越平倉　長倉
       2.　柱狀大小改變　增減持倉量 
       3.　無確保到特定點　平均長倉價位 ~ 短倉平倉點　持有長倉具有購買價值　增購幅度 50 1unit　
       4　短線止跌　增倉
       
       長倉震盪
       方向Guess 短倉震盪　操作
       短倉策略模組
       
        from 5_macd　利潤最大化　短倉
        濾網　長時間震盪　- 濾網 (-5 ＜ 柱狀 < 5) 長倉無方向性　長倉歸零　
       　　　柱狀大小　定義持倉量　穿越方向決定　增倉方向
       
    短倉持倉方式
    
    if (self.pos == 1unit or 2unit)  and          self.pos < max 
       buy   +1
       short +2
    
    短倉正向 平倉所有空倉  
    
    if (self.pos == 3 unit )           self.pos < max 
       short +2 
    平倉所有空倉  
    　　　buy +60 VAR 
    if (self.pos = 4 )           
        sell 1   最舊的
        short +2  
    平倉所有空倉
        buy +60VAR
        

VER 0.4
風控
   長周期::移動停利 --下降 移動停損點 前一根K棒 H + max (0.7*max((最高-收盤)),(最高-開盤)),25)
                        上升 移動停損點 前一根K棒 L - max (0.7*max((收盤-最低)),(開盤-最低)),25)
                        
   停利停損完 
          用找短周期買入訊號再買入 停損
   短倉 與長倉反向操作       
          淨持倉空 下單 ~
                        1.成交後遠的淨多單預設價位
                        2.TIME OR TARGET 停損價 獲利額
                        3 短訊號 平倉,買多
2020.2.1 KK Taiwan
修正模式 減少訊號 改用 5mins, 8mins, 15mins 實驗 macd 敏感度 >>

長周期定義 15mins 

 買進區間 到零點 最大持倉量為4  為T1 買進均價 > 最高最低點/2 >> 買進剩下的 >> 
                update 持倉週期的停損停利 時間週期2T if 獲利 跟新長期停損點以零點為基礎  時間週期3T 以2T為長期停損點
                停損停利點零點為基準的停損停利點
策略箱檢查順序
1.策略檢查平倉
2.短策略 做反向最多只有一單位 避免短周期操作失誤破壞長周期獲利
      a.Target update with long time signal ((mask long Target)
      b.overtime and Profit check 短線 與 停利訊號
      c.長策略的停損回補定價 than 現價
         
3.長策略 
      a.Target update
         
        
      b.1 than 現價  長策略訂單送出 >>大波段 最長周期停利位置 柱線>0 起點, 2.5HR後啟用  ,均線
            check訂單未實現短策略訂單 
            mask time > make long time signal
            last 突破時間點到 柱狀反向 為T (最高Ht 最低Lt) 兩點連線之趨勢線 超過為過熱 Touch 平倉訊號啟動~ 平倉一半額度
            
      c.短策略訊號跟新 >>
 
 
 
 1 平倉 目標 修改止價 >>停損零點
      
      多單 Max (前兩根LOW-70)
      TIME_OUT 停損買回預掛單(FIXED 賣出價 - (最高-最低)/2)
 2.短周期TOUCH 反向訊號
      已有平倉訂單 賣出訂單? 
      
 柱狀過最高後被停損 >> 反向策略
 
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
          

    #####
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
        
        macd_DIF,macd_DEA ,macd_HIST  = self.am15.macd(12,26,9)
        
        if  (macdhist > 0)
            if (macdhist < 3)
                震盪
            else if (macdhist > DIFF) and 前多少時間不是 (向下signal )
                if macd[-1]>macdsignal[-1]
        else if (macdhist < 0)
            if (-3 < macdhist)
                震盪 
            else
               
#當柱線 接近0時，持有持間短 柱線離0遠時持有持間長

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
        #调用sync_data函数后,策略持仓终于写入文件中
        
    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
