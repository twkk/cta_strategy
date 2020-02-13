# A.策略失效   策略失敗率高 >> 停止
 
## **實際基於 MDQL5 BASE 多EA物件策略方式**
讓EA 交易選擇其未結訂單用magic number--對應EA bot 進行識別 << 平倉時確認 
一個完整的策略模型建構是一個3維數組。V1交易系統的數目，V2 是交易系統上操作的時間軸 time range 的數目，V3 是用於交易系統的交易工具數目

照各個模式多貨幣交易下會使交易系統規模高速擴展，如果交易系統規模更大、EA 交易的投資組合範圍更廣，則解決方案的數量就會輕鬆超過500 個，逐個人工配置不可能 。因此，有必要通過這種方式建立一個系統，使其能夠自動調整每個組合，將其載入EA 交易的內存，然後EA 交易就可以基於該組合特定實例的規則進行交易了。
ex當其同時使用8 個主要貨幣對時，也會出現152 種獨立的解決方案：  1 EA 交易* 8 貨幣對* 19 時間表（未包含周和月時間表）。

* **輸入EA bot 參數**
    1. indicator 所需參數 >> 訊號  
    1. local 停損, 停利 營利目標 >> 開倉類型
    1. local 最大淨持倉 max net position 
    1. local 訊號有效期間 time sort  

* **onbar**
  1. 建立訊號 local signal  
  1. 檢查訊號 >>  singal by local + Gloab net position >> policy    
    a. 停損策略 update  
    b. local 平倉策略close  >> close 停損 bot1,bot2  
    c. Global 平倉 time  
    d. local 開倉策略 new open reverose policy   
    e. local 資金控管跟新 - 移動停損 update << singal,time   
---   
# C.開倉策略 
* 輸入參數
   1. Global 淨最大開倉數量  
   1. local 策略開數量  
   1. Global 時間訊號遮罩 避免高頻交易  
   1. local 訊號(< indicator),目前持倉 (Global 淨持倉方向)   
* 開倉類型   
  a .mv new  
  b .blance  
  c .fix for holding  
* 輸出停損策略 << 開倉類型  
**  輸出開倉數量 << Gloab 淨持倉,策略訊號  

      停損點 趨勢訊號 固定停損點  
             反轉訊號 無停損停利點  
           目標淨持倉 >> 數量  
                       
# D.平倉策略
* 輸入參數  
   1. signal  
   2. time  
   3. 停損停利  
* functions  
   1. check 反向訊號  local 
   1. check 停損策略
           
* 停損策略   
    1. 固定停損點 (open policy 長倉,短倉) Trailing Stop based on fixed Stop level  
    2. 平衡倉     open without 停損停利   > Trailing stop not use  
        a.反轉點  
        b.震盪  Trailing stop based on Parabolic SAR  
    3. 獲利區間       
               Trailing stop based on MA(MA policy with)  
               
# E.資金獲利管控
   1. local 策略訊號 > ????? 更新移動停損策略
   1. 跟新時間限制 << 盈虧 ,local 訊號
   1. local 移動跟新停損停利 << ATR 震動幅度 跟新 波動範圍
   1. 超時-->> close or hold
                << money manager --net + bot check profolio ,long time policy
                短倉 獲利確認,未達成下單
                反轉 獲利確認
                    
                 
            

目前還沒考慮的
# onTrade >>
  1. 未成交訂單修改或是取消
  1. 需要使用紀錄訂單號 總金額與或是風險 部分平倉時找到目標訂單的方式       
  1. 紀錄訂單原因 >> 哪個策略發出的訂單>>對移動止損 以外交易策略編碼 ~ 易於進行交易檢討 
  1. 交易訂單 用限價 還是 時價 發出
  1. 2013 用VOM虛擬訂單管理模式  
  1. 在MetaTrader 5中，掛單一直存在，直到交易實際完成的那一刻。  
     假設EA交易發布了一個已執行訂單。總持倉量已發生變化。一段時間過後，EA交易需要平倉。
  1.除自身數據外，CTableOrders類還包含一個十分重要的Add()函數。該函數用於接收訂單號，這需要記錄到表格中
  
我們無法像在MetaTrader 4中那樣對具體訂單進行平倉，因為缺少訂單平倉的概念，但我們可以實現全部平倉或部分平倉。
    合理的報酬率大約落在5~60%之間，最大風險值應該在30%以內。
    
    
# 設計抽象交易模型
https://www.mql5.com/zh/articles/217
