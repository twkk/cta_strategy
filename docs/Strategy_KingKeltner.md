## 凱特王交易系統

以移動平均線計算為主要指標用在凱特王交易系統中。移動平均線通過計算X週期日期求和並且區分累計求和通過X值。一些時間這些計算用在固定數字的日期指向上。
你有了很多資料指示後，新資料指示很少影響在最終的平均價值。長期移動均線指標試圖解決長期趨勢運動。
相反，短期移動平均線試圖察覺短期市場波動。賈斯特、凱特介紹這個移動均線系統是在1960年。

凱特系統展示了依據最高、最低、和收盤價建設的移動平均線系統和在移動均線最高和最低價雙邊市場形成的波段和通道中。
買入信號發生在當市場價格穿越上軌，賣出信號發生在當市場價格穿越下軌。我們可以應用基本的凱特方法，但需要增加一些鈴聲和汽笛。
我們希望，賈斯特，當市場發生突發的移動均線從一個方向移動，他是趨勢發生變化的信號。

在凱特王系統中，上下波段的穿透被視為為趨勢改變的信號。我們將跟隨趨勢在強勢中買入在弱市中賣出。我們將隨著贏利或虧損當市場折回移動均線的時候平倉離場。

主要問題是通道突破系統是一個假突破。主要時間裏，通道展示出市場力量耗盡時候趨勢轉換。
經常地市場耗盡他本身力量移動到上軌或下軌並且立即回來朝相反的方向運動。這個是我們最擔心出現的。

然而，自從我們認識到這個類型系統的弱點，我們設計程式止損在移動均線。
當交易開始的時候許多交易方法將失敗並且一些形式的保護止損應該被執行。如果許多交易方法失敗，之後為什麼確定交易在第一個位置。

成功的交易是消減短小的損失並且讓利潤持續。這個基本的交易原則

在資金管理領域。你的交易系統讓你參與到交易中並且資金管理系統管理你的頭寸最終合理離場。
在凱特王系統中， 移動均線的指示和軌道的穿透是我們入場交易的手法，和我們頭寸離場在移動均線系統是我們資金管理系統。
我們的資金管理止損將及可能是保護性止損也可能是盈利性止損。

如果我們抓長期趨勢，移動均線應該朝一個方向移動隨著我們入場信號並且幸運地獲得好的移動收入。

永遠記住出場技巧入場技巧的成功與否。

### 凱特王系統是一個長期趨勢系統，短期盈利不是我們的目的。

我們將獲利如果他們按照我們的計畫，但是這個類型的系統他們最終可能達不到預想的目的。
### 這個系統很少超過50%的成功率，我們抓到少數大的趨勢將彌補多數小的虧損。

### 大多數均線系統都是非常簡單的程式並且這個也不例外，我們僅僅需要兩個工具
（1）最高、最低、收盤價的移動平均線。
（2）移動平均線真實排列。

你可能不熟悉真實排列這個術語。每日的日線排列就是通過計算每日最高價最低價的加減。這些排列的平均將是對期貨價格排列的一個評估。
所以真實排列計算延伸出來的日線排列就是前日的收盤價（真實排列=MAX（昨日收盤，當日最高價）-MIN（昨日收盤，當日最低）
因此，擴展了日線的範圍從而包括一些昨日收盤造成的缺口。我們認為真實排列給出了一些更精確的測定市場波動的方法。
因此我們努力獲取長期移動趨勢，我們將用40日參數為我們平均參考計算。

### King Keltner Pseudocode

King Keltner Program  
{King Keltner by George Pruitt—based on trading system presented by Chester Keltner}  

Inputs: avgLength(40), atrLength(40);  
Vars: upBand(0),dnBand(0),liquidPoint(0),movAvgVal(0);  
movAvgVal = Average(((High + Low + Close)/3),40);  
upBand = movAvgVal + AvgTrueRange(TrueRange,40);  
dnBand = movAvgVal – AvgTrueRange(TrueRange,40);  
liquidPoint = movAvgVal  

A long position will be initiated when today's movAvg is greater than yesterday's and market action >= upBand  
A short position will be initiated when today's movAvg is less than yesterday's and market action <= dnBand  
A long position will be liquidated when today's market action <= liquidPoint  
A short position will be liquidated when today's market action >= liquidPoint  

if(movAvgVal > movAvgVal[1]) then Buy ("KKBuy") tomorrow at upBand stop;  
if(movAvgVal < movAvgVal[1]) then Sell Short("KKSell") tomorrow at dnBand  
stop;  

liquidPoint = movAvgVal;  
112 Building Winning Trading Systems with TradeStation  
If(MarketPosition = 1) then Sell tomorrow at liquidPoint stop;  
If(MarketPosition = –1) then Buy To Cover tomorrow at liquidPoint stop;  
