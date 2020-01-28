# 算法交易
算法交易可以用於把巨型單子拆分成一個個小單，能夠有效降低交易成本，沖擊成本等（冰山算法、狙擊手算法)；也可以在設定的閾值內進行高拋低吸操作(網格算法、套利算法）。


- [冰山算法](#冰山算法)
- [狙擊手算法](#狙擊手算法)
- [直接委托算法](#直接委托算法)
- [網格算法](#網格算法)
- [套利算法](#套利算法)
- [條件委托算法](#條件委托算法)
- [時間加權平均算法](#時間加權平均算法)
- [最優限價算法](#最優限價算法)

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
