# A.策略失效   策略失敗率高 >> 停止
 
## **實際基於 MDQL5 BASE 的物件化策略方式**
* **輸入EA bot 參數**
    1. 訊號參數 
    1. 停損, 停利 營利目標 >>開倉類型
    1. 最大淨持倉 max bot net position 
    1. 訊號有效期間 time sort  
onBar >>  
  1.建立訊號 local signal  
  2.檢查訊號   
    a.停損策略 update  
    b.風控 manager  
      1.總體盈利風控  
      2.singal by local + Gloab net position >> policy  
         >> new open reverose policy  
         >> close 停損 bot1,bot2  
    c.update    移動停損 <<singal ,time   
    d.open    check open policy  
 
# C.開倉策略
   1. < Gloab 淨最大開倉數量
   1. < local 策略開數量
   1. Gloab 時間訊號遮罩 避免高頻交易
   1. local 訊號,目前持倉 (Gloab 淨持倉方向) 
### >> 開倉類型   
>   a.mv new  
>   b.blance  
>   c.fix for holding  
       3-1. 停損策略    << 開倉類型  
       3-2. 開倉數量    << Gloab 淨持倉,策略訊號 
               
            停損點 趨勢訊號 固定停損點  
                  反轉訊號 無停損停利點  
            目標淨持倉 >> 數量  
                       
# D.平倉策略
   1. check 反向訊號  local 
   1. check 停損策略
            
>   停損策略  
>     固定停損點 (open policy 長倉,短倉) Trailing Stop based on fixed Stop level  
>     平衡倉     open without 停損停利   > Trailing stop not use  
>        a.反轉點  
>        b.震盪  Trailing stop based on Parabolic SAR  
>     獲利區間       
>                Trailing stop based on MA(MA policy with)  
               
# E.資金獲利管控
   1. local 策略訊號 > ????? 更新移動停損策略
   1. 跟新時間限制 << 盈虧 ,local 訊號
   1. local 移動跟新停損停利 << ATR 震動幅度 跟新 波動範圍
   1. 超時-->> close or hold
                << money manager --net + bot check profolio ,long time policy
                短倉 獲利確認,未達成下單
                反轉 獲利確認
                    
                 
            


       

    
    合理的報酬率大約落在5~60%之間，最大風險值應該在30%以內。
