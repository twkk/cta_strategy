        
vnpy\trader\object.py   @dataclass  class BarData(BaseData):
vnpy\trader\utility.py              class BarGenerator:
 self.bg5 = BarGenerator(self.on_bar, 5, self.on_5min_bar)
    1. generating 1 minute bar data from tick data
    2. generateing x minute bar/x hour bar data from 1 minute data
    Notice:
    1. for x minute bar, x must be able to divide 60: 2, 3, 5, 6, 10, 15, 20, 30
    2. for x hour bar, x can be any number

週期策略    on_bar(self, bar: BarData): 短長周期跟新檢查

#################################################################


ver0.2
    財務風險控制   最大/最小持倉  開倉   VarMax  add  unit       masktime
   60mins 2次/day     2/1    2    1       1     0.2  0.5        30           net 採購倉位 > 0.7 分次採買
   30mins 4次/day   1.5/0.7  1.3 2/3    0.7     0.2  0.5         15
   15mins 8次/day     1/0.5  1    1/2    0.5     0.2  0.5         5    
   5mins 16次/day       0.5  0.5  1/4    0.5     0.2  0.5         1
   不被time mask extra 增減倉 min RSI >70 縮減 反轉訊號  賣出訊號  RSI <30 +-10mins 買進訊號
   
   震盪幅度= max (前日最高最低價,當日) >> assume 8HR  1/3 as range 開盤+- 1/2 range
   max (前日 前前日)
        
 正向倉位處理
   org   max target= 最大正向訊號 (L4,L3 0.5 +L2 0.3 +L1 0.1) + 間隔開倉量 +- 最大震幅保險 range
   式1   待開新倉量 = min(1.5, 反向訊號 (L3 0.8 +L2 0.7 +L1 0.5))            
   式2   立即開倉量 = max target - 待開新倉量 +- 最大震幅保險 range
 反向倉位處理
   立即平倉 = min(立即開倉量,反向倉位)
   待平倉   = 反向倉位-立即平倉
 
開倉檢查策略 時間週期長 >> 時間週期短 確保masttime 持倉策略長的能夠不被短的影響
短周期與長週期策略衝突  >> ATR*unit < Var 減持 or ATR unit > Var 開新反向短倉
