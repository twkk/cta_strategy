以布林帶策略（BollStrategy）的引數優化為例：所以在算力少一半的情況下，遺傳演算法的優勢差不多是窮舉演算法的12倍多!!!

###  怎麼用  
 ![image](https://cdn.bigquant.com/community/uploads/default/original/3X/d/7/d70da11bd1db292f30a0a5829f3efdc5e06d7f6a.jpeg)  
在CTA回測元件的引數優化對話方塊中，設定好要優化的引數後點擊第二個按鈕“遺傳演算法優化”就行，沒有任何其他步驟（這才叫做整合~）。  
當然考慮到vn.py社群總有這麼一群不甘寂寞熱愛折騰的使用者，
遺傳演算法優化功能也同樣可以通過cta_strategy模組的BacktestingEngine呼叫，函式名為：run_ga_optimization，支援更多的可選引數配置。  

最後，上述遺傳演算法優化功能基於Python資料分析生態中強大的DEAP庫，除了最常用的遺傳演算法外，還有更多相對小眾但特別的優化演算法：粒子演算法、蟻群演算法等等，絕對能滿足你的折騰愛好。

###  行情記錄模塊  
![image](https://cdn.bigquant.com/community/uploads/default/original/3X/3/7/377f23cf60a03276e7a561fc4411d0959be614ab.jpeg)

###  全域性配置  

VN Trader中的一些內部功能需要通過全域性配置來管理，之前需要使用者手動修改使用者目錄下的.vntrader/vt_setting.json，
在v2.0.3中也新增了全域性配置對話方塊，注意： 所有修改儲存後必須重啟VN Trader才能生效 。

 ![image](https://cdn.bigquant.com/community/uploads/default/original/3X/3/5/35b7c5796558c1bbac389d511d2a202a5acb0a79.jpeg)  
