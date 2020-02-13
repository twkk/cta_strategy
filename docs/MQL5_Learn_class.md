 停損停利策略　跟踪敞口倉位
      Trailing Stop based on fixed Stop level
         StopLevel 
         ProfitLevel
      Trailing stop based on MA
      
      Trailing stop based on Parabolic SAR   
       
         
      
資金與風險管理
         Trading with fixed trade volume
            Lots – 以手數計算交易量
            Percent – 允許的最大風險百分比。
         Trading with fixed trade margin
         Trading with fixed trade risk
         Trading with minmal allowed trade volume
            Percent 
         Trading with optimize trade volume
            Decrease Factor
            Percent
            

      
      CMoneyFixedLot – 以固定交易量交易。
         如果Inp_Money_FixLot_Percent 參數中指定了一個損失（作為當前資產淨值一個給定的百分比），則CMoneyFixedLot 類會建議“EA 交易”強行為不盈利倉位平倉，而且也會這樣執行。
         Money_FixLot_Percent 與Money_FixLot_Lots 輸入參數
      CMoneyFixedMargin – 以固定预付款交易。
      CMoneyFixedRisk – 以固定风险交易。
      CMoneyNone – 以允许的最低交易量交易。
      CMoneySizeOptimized – 以经过优化的交易量交易。
  
  
  VOM (Virtual Order Management)
