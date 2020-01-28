# 算法交易
算法交易可以用於把巨型單子拆分成一個個小單，能夠有效降低交易成本，沖擊成本等（冰山算法、狙擊手算法)；也可以在設定的閾值內進行高拋低吸操作(網格算法、套利算法）。

&nbsp;

## 模塊構成

算法交易模塊主要由4部分構成，如下圖：

- engine：定義了算法引擎，其中包括：引擎初始化、保存/移除/加載算法配置、啟動算法、停止算法、訂閱行情、掛撤單等。
- template：定義了交易算法模板，具體的算法示例，如冰山算法，都需要繼承於該模板。
- algos：具體的交易算法示例。用戶基於算法模板和官方提供是算法示例，可以自己搭建新的算法。
- ui：基於PyQt5的GUI圖形應用。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/algo_trader_document.png)

&nbsp;

## 基本操作

在VN Trader的菜單欄中點擊“功能”—>“算法交易”即可打開如圖算法交易模塊窗口，如下圖。

算法交易模塊有2部分構成：
- 委托交易，用於啟動算法交易；
- 數據監控，用於監控算法交易執行情況，並且能夠手動停止算法。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/algo_trader_all_section.png)

&nbsp;

### 委托交易

下面以時間加權平均算法為例，具體介紹如下圖委托交易功能選項。
- 算法：目前提供了5種交易算法：時間加權平均算法、冰山算法、狙擊手算法、條件委托、最優限價；
- 本地代碼：vt_symbol格式，如AAPL.SMART, 用於算法交易組建訂閱行情和委托交易；
- 方向：做多或者做空；
- 價格：委托下單的價格；
- 數量：委托的總數量，需要拆分成小單進行交易；
- 執行時間：運行改算法交易的總時間，以秒為單位；
- 每輪間隔：每隔一段時間（秒）進行委托下單操作；
- 啟動算法：設置好算法配置後，用於立刻執行算法交易。

所以，該算法執行的任務如下：通過時間加權平均算法，買入10000股AAPL（美股），執行價格為180美金，執行時間為600秒，間隔為6秒；即每隔6秒鐘，當買一價少於等於180時，以180的價格買入100股AAPL，買入操作分割成100次。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/trading_section.png)

交易配置可以保存在json文件，這樣每次打開算法交易模塊就不用重覆輸入配置。其操作是在“算法名稱”選項輸入該算法設置命名，然後點擊下方"保存設置”按鈕。保存的json文件在C:\Users\Administrator\\.vntrader文件夾的algo_trading_setting.json中，如圖。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/setting.png)

委托交易界面最下方的“全部停止”按鈕用於一鍵停止所有執行中的算法交易。

&nbsp;

### 數據監控

數據監控由4個部分構成。

- 活動組件：顯示正在運行的算法交易，包括：算法名稱、參數、狀態。最右邊的“停止”按鈕用於手動停止執行中的算法。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/action.png)

&nbsp;

- 歷史委托組件：顯示已完成的算法交易，同樣包括：算法名稱、參數、狀態。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/final.png)

&nbsp;

- 日志組件：顯示啟動、停止、完成算法的相關日志信息。在打開算法交易模塊後，會進行初始化，故日志上會首先顯示“算法交易引擎啟動”和“算法配置載入成功”。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/log_section.png)

&nbsp;

- 配置組件：用於載入algo_trading_setting.json的配置信息，並且以圖形化界面顯示出來。
用戶可以點擊“使用”按鈕立刻讀取配置信息，並顯示在委托交易界面上，點擊“啟動算法”即可開始進行交易；
用戶也可以點擊“移除”按鈕來移除該算法配置，同步更新到json文件內。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/algo_trader/setting_section.png)

&nbsp;

## 算法示例


### 直接委托算法

直接發出新的委托（限價單、停止單、市價單）

```
    def on_tick(self, tick: TickData):
        """"""
        if not self.vt_orderid:
            if self.direction == Direction.LONG:
                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    self.price,
                    self.volume,
                    self.order_type,
                    self.offset
                )
                
            else:
                self.vt_orderid = self.sell(
                    self.vt_symbol,
                    self.price,
                    self.volume,
                    self.order_type,
                    self.offset
                )
        self.put_variables_event()
```

&nbsp;

### 時間加權平均算法

- 將委托數量平均分布在某個時間區域內；
- 每隔一段時間用指定的價格掛出買單（或者賣單）。
- 買入情況：買一價低於目標價格時，發出委托，委托數量在剩余委托量與委托分割量中取最小值。
- 賣出情況：賣一價高於目標價格時，發出委托，委托數量在剩余委托量與委托分割量中取最小值。

```
    def on_timer(self):
        """"""
        self.timer_count += 1
        self.total_count += 1
        self.put_variables_event()

        if self.total_count >= self.time:
            self.write_log("執行時間已結束，停止算法")
            self.stop()
            return

        if self.timer_count < self.interval:
            return
        self.timer_count = 0

        tick = self.get_tick(self.vt_symbol)
        if not tick:
            return

        self.cancel_all()

        left_volume = self.volume - self.traded
        order_volume = min(self.order_volume, left_volume)

        if self.direction == Direction.LONG:
            if tick.ask_price_1 <= self.price:
                self.buy(self.vt_symbol, self.price,
                         order_volume, offset=self.offset)
        else:
            if tick.bid_price_1 >= self.price:
                self.sell(self.vt_symbol, self.price,
                          order_volume, offset=self.offset)
```

&nbsp;

### 冰山算法

- 在某個價位掛單，但是只掛一部分，直到全部成交。
- 買入情況：先檢查撤單：最新Tick賣一價低於目標價格，執行撤單；若無活動委托，發出委托：委托數量在剩余委托量與掛出委托量中取最小值。
- 賣出情況：先檢查撤單：最新Tick買一價高於目標價格，執行撤單；若無活動委托，發出委托：委托數量在剩余委托量與掛出委托量中取最小值。

```
    def on_timer(self):
        """"""
        self.timer_count += 1

        if self.timer_count < self.interval:
            self.put_variables_event()
            return

        self.timer_count = 0

        contract = self.get_contract(self.vt_symbol)
        if not contract:
            return

        # If order already finished, just send new order
        if not self.vt_orderid:
            order_volume = self.volume - self.traded
            order_volume = min(order_volume, self.display_volume)

            if self.direction == Direction.LONG:
                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    self.price,
                    order_volume,
                    offset=self.offset
                )
            else:
                self.vt_orderid = self.sell(
                    self.vt_symbol,
                    self.price,
                    order_volume,
                    offset=self.offset
                )
        # Otherwise check for cancel
        else:
            if self.direction == Direction.LONG:
                if self.last_tick.ask_price_1 <= self.price:
                    self.cancel_order(self.vt_orderid)
                    self.vt_orderid = ""
                    self.write_log(u"最新Tick賣一價，低於買入委托價格，之前委托可能丟失，強制撤單")
            else:
                if self.last_tick.bid_price_1 >= self.price:
                    self.cancel_order(self.vt_orderid)
                    self.vt_orderid = ""
                    self.write_log(u"最新Tick買一價，高於賣出委托價格，之前委托可能丟失，強制撤單")

        self.put_variables_event()
```

&nbsp;

### 狙擊手算法

- 監控最新tick推送的行情，發現好的價格立刻報價成交。
- 買入情況：最新Tick賣一價低於目標價格時，發出委托，委托數量在剩余委托量與賣一量中取最小值。
- 賣出情況：最新Tick買一價高於目標價格時，發出委托，委托數量在剩余委托量與買一量中取最小值。

```
    def on_tick(self, tick: TickData):
        """"""
        if self.vt_orderid:
            self.cancel_all()
            return

        if self.direction == Direction.LONG:
            if tick.ask_price_1 <= self.price:
                order_volume = self.volume - self.traded
                order_volume = min(order_volume, tick.ask_volume_1)

                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    self.price,
                    order_volume,
                    offset=self.offset
                )
        else:
            if tick.bid_price_1 >= self.price:
                order_volume = self.volume - self.traded
                order_volume = min(order_volume, tick.bid_volume_1)

                self.vt_orderid = self.sell(
                    self.vt_symbol,
                    self.price,
                    order_volume,
                    offset=self.offset
                )

        self.put_variables_event()
```

&nbsp;

### 條件委托算法

- 監控最新tick推送的行情，發現行情突破立刻報價成交。
- 買入情況：Tick最新價高於目標價格時，發出委托，委托價為目標價格加上超價。
- 賣出情況：Tick最新價低於目標價格時，發出委托，委托價為目標價格減去超價。

```
    def on_tick(self, tick: TickData):
        """"""
        if self.vt_orderid:
            return

        if self.direction == Direction.LONG:
            if tick.last_price >= self.stop_price:
                price = self.stop_price + self.price_add

                if tick.limit_up:
                    price = min(price, tick.limit_up)

                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    price,
                    self.volume,
                    offset=self.offset
                )
                self.write_log(f"停止單已觸發，代碼：{self.vt_symbol}，方向：{self.direction}, 價格：{self.stop_price}，數量：{self.volume}，開平：{self.offset}")                   

        else:
            if tick.last_price <= self.stop_price:
                price = self.stop_price - self.price_add
                
                if tick.limit_down:
                    price = max(price, tick.limit_down)

                self.vt_orderid = self.buy(
                    self.vt_symbol,
                    price,
                    self.volume,
                    offset=self.offset
                )
                self.write_log(f"停止單已觸發，代碼：{self.vt_symbol}，方向：{self.direction}, 價格：{self.stop_price}，數量：{self.volume}，開平：{self.offset}") 

        self.put_variables_event()
```

&nbsp;

### 最優限價算法

- 監控最新tick推送的行情，發現好的價格立刻報價成交。
- 買入情況：先檢查撤單：最新Tick買一價不等於目標價格時，執行撤單；若無活動委托，發出委托：委托價格為最新Tick買一價，委托數量為剩余委托量。
- 賣出情況：先檢查撤單：最新Tick買一價不等於目標價格時，執行撤單；若無活動委托，發出委托：委托價格為最新Tick賣一價，委托數量為剩余委托量。

```
    def on_tick(self, tick: TickData):
        """"""
        self.last_tick = tick

        if self.direction == Direction.LONG:
            if not self.vt_orderid:
                self.buy_best_limit()
            elif self.order_price != self.last_tick.bid_price_1:
                self.cancel_all()
        else:
            if not self.vt_orderid:
                self.sell_best_limit()
            elif self.order_price != self.last_tick.ask_price_1:
                self.cancel_all()

        self.put_variables_event()

    def buy_best_limit(self):
        """"""
        order_volume = self.volume - self.traded
        self.order_price = self.last_tick.bid_price_1
        self.vt_orderid = self.buy(
            self.vt_symbol,
            self.order_price,
            order_volume,
            offset=self.offset
        )        

    def sell_best_limit(self):
        """"""
        order_volume = self.volume - self.traded
        self.order_price = self.last_tick.ask_price_1
        self.vt_orderid = self.sell(
            self.vt_symbol,
            self.order_price,
            order_volume,
            offset=self.offset
        ) 
```

&nbsp;

### 網格算法

- 每隔一段時間檢查委托情況，若有委托則先清空。
- 基於用戶設置的價格步進（即網格）計算目標距離，目標距離=（目標價格- 當前價格）/價格步進，故當前價格低於目標價格，目標距離為正，方向為買入；當前價格高於目標價格，目標距離為負，方向為賣出。（高拋低吸概念）
- 計算目標倉位，目標倉位= 取整後的目標距離 * 委托數量步進。註意賣賣方向取整的方式是不同的：買入方向要向下取整math.floor()，如目標距離為1.6，取1；賣出方向要向上取整，如目標距離為-1.6，取-1。
- 計算具體委托倉位：若目標買入倉位大於當前倉位，執行買入操作；若目標賣出倉位低於當前倉位，執行賣出操作。
- 為了能夠快速成交，買入情況是基於ask price計算，賣出情況是基於bid price計算。


```
    def on_timer(self):
        """"""
        if not self.last_tick:
            return

        self.timer_count += 1
        if self.timer_count < self.interval:
            self.put_variables_event()
            return        
        self.timer_count = 0
        
        if self.vt_orderid:
            self.cancel_all()        

        # Calculate target volume to buy
        target_buy_distance = (self.price - self.last_tick.ask_price_1) / self.step_price
        target_buy_position = math.floor(target_buy_distance) * self.step_volume
        target_buy_volume = target_buy_position - self.last_pos

        # Buy when price dropping
        if target_buy_volume > 0:
            self.vt_orderid = self.buy(
                self.vt_symbol,
                self.last_tick.ask_price_1,
                min(target_buy_volume, self.last_tick.ask_volume_1)
            )
        
        # Calculate target volume to sell
        target_sell_distance = (self.price - self.last_tick.bid_price_1) / self.step_price
        target_sell_position = math.ceil(target_sell_distance) * self.step_volume
        target_sell_volume = self.last_pos - target_sell_position

        # Sell when price rising
        if target_sell_volume > 0:
            self.vt_orderid = self.sell(
                self.vt_symbol,
                self.last_tick.bid_price_1,
                min(target_sell_volume, self.last_tick.bid_volume_1)
            )
```

&nbsp;

### 套利算法

- 每隔一段時間檢查委托情況，若有委托則先清空；若主動腿還持有凈持倉，通過被動腿成交來對沖。
- 計算價差spread_bid_price 和 spread_ask_price, 以及對應的委托數量
- 賣出情況：主動腿價格相對被動腿上漲，其價差spread_bid_price大於spread_up時，觸發買入信號
- 買入情況：主動腿價格相對被動腿下跌，其價差spread_ask_price小於 - spread_down(spread_down默認設置為正數)時，觸發賣出信號
- 在買賣信號判斷加入最大持倉的限制，其作用是避免持倉過多導致保證金不足或者直接被交易所懲罰性強平；而且隨著價差持續波動，主動腿持倉可以從0 -> 10 -> 0 -> -10 -> 0,從而實現平倉獲利離場。


```
    def on_timer(self):
        """"""
        self.timer_count += 1
        if self.timer_count < self.interval:
            self.put_variables_event()
            return
        self.timer_count = 0

        if self.active_vt_orderid or self.passive_vt_orderid:
            self.cancel_all()
            return
        
        if self.net_pos:
            self.hedge()
            return
      
        active_tick = self.get_tick(self.active_vt_symbol)
        passive_tick = self.get_tick(self.passive_vt_symbol)
        if not active_tick or not passive_tick:
            return

        # Calculate spread
        spread_bid_price = active_tick.bid_price_1 - passive_tick.ask_price_1
        spread_ask_price = active_tick.ask_price_1 - passive_tick.bid_price_1

        spread_bid_volume = min(active_tick.bid_volume_1, passive_tick.ask_volume_1)
        spread_ask_volume = min(active_tick.ask_volume_1, passive_tick.bid_volume_1)

        # Sell condition      
        if spread_bid_price > self.spread_up:
            if self.acum_pos <= -self.max_pos:
                return
            else:
                self.active_vt_orderid = self.sell(
                    self.active_vt_symbol,
                    active_tick.bid_price_1,
                    spread_bid_volume               
                )

        # Buy condition
        elif spread_ask_price < -self.spread_down:
            if self.acum_pos >= self.max_pos:
                return
            else:
                self.active_vt_orderid = self.buy(
                    self.active_vt_symbol,
                    active_tick.ask_price_1,
                    spread_ask_volume
                )
        self.put_variables_event()
    
    def hedge(self):
        """"""
        tick = self.get_tick(self.passive_vt_symbol)
        volume = abs(self.net_pos)

        if self.net_pos > 0:
            self.passive_vt_orderid = self.sell(
                self.passive_vt_symbol,
                tick.bid_price_5,
                volume
            )
        elif self.net_pos < 0:
            self.passive_vt_orderid = self.buy(
                self.passive_vt_symbol,
                tick.ask_price_5,
                volume
            )

    def on_trade(self, trade: TradeData):
        """"""
        # Update net position volume
        if trade.direction == Direction.LONG:
            self.net_pos += trade.volume
        else:
            self.net_pos -= trade.volume

        # Update active symbol position           
        if trade.vt_symbol == self.active_vt_symbol:
            if trade.direction == Direction.LONG:
                self.acum_pos += trade.volume
            else:
                self.acum_pos -= trade.volume

        # Hedge if active symbol traded     
        if trade.vt_symbol == self.active_vt_symbol:
            self.hedge()
        
        self.put_variables_event()

```
