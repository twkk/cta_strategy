合理的報酬率大約落在5~60%之間，最大風險值應該在30%以內。
基於 MDQL5 BASE 的策略方式

    整體風控
      
      
      淨多單
      淨空單
      
      停損 > 當日絕對值
      停利 > signal 
       
      停倉
      策略失敗率高 >> 停止
    
    短倉
      營利目標
      停損
      停利
      開倉條件
      停倉條件
      
    長倉
      營利目標
      停損
      停利
      開倉條件
      停倉條件
      
      
      開倉策略
            0. < 淨最大開倉數量
            1. < 策略開數量
            2. 時間訊號遮罩 避免高頻交易
            3. 訊號,目前持倉 (淨持倉方向) > 開倉類型
            4.   停損策略    <<  開倉類型
            5.   數量<<淨持倉,策略訊號
               
            停損點 趨勢訊號 固定停損點
                  反轉訊號 無停損停利點
            目標淨持倉 >> 數量
                       
      平倉策略
            1.check 反向訊號 get
            2.check 停損策略 
            
            停損策略
               固定停損點 (open policy 長倉,短倉) Trailing Stop based on fixed Stop level
               平衡倉     open without 停損停利   > Trailing stop not use
                  反轉點
                  震盪    Trailing stop based on Parabolic SAR
               獲利區間       
                           Trailing stop based on MA(MA policy with)
         
      
        
