###  何設計一個魯棒的RestAPI 務實的API有以下設計原則：    
1.一個API的好用與否取決於它的文檔- 所以文檔要好好寫  
2.API是開發者的用戶界面- 所以多花點功夫使其更友好  
3.定義一個容易理解的錯誤格式  
4.高效的使用HTTP狀態碼  
5.對於POST、PATCH和PUT的請求返回一些有用的東西  
6.使用RESTful的URL和action  
####  7.通過URL來控製版本，不要通過header  
8.盡量使用JSON，迫不得已的時候使用XML  
9.考慮對POST、PUT和PATCH等請求的body使用JSON格式  
理論上你應該在JSON中使用駝峰格式，但是下劃線格式的可讀性比駝峰格式要高20%  
10.默認情況API要輸出完整的內容，並且要確認支持gzip  
11.使用查詢參數來實現高級功能：過濾、排序和搜索  

12.提供一種方法來覆蓋HTTP方法  
13.提供一種方法來自動加載相關資源的內容  
14.提供響應header用來對請求頻次進行限制  
15.使用Link header分頁  
16.默認情況下不要在響應內容的外邊再套一層大括號  

21.所有地方都要使用SSL，沒有例外  
22.使用token來進行普通驗證，當需要用戶授權的時候使用OAuth2  
23.要在響應header中包含緩存所使用的header  
24.提供方法用來限制從API返回的字段  
HATEOAS當前還不太實用

其實，也有很多架構師和學者提出了API-First的設計思想【2】。
究其本質，在整個系統設計的藍圖中，面向數據流是最主流的方法，而數據節點之間的溝通方式就是我們的API設計的起點。  
或者說抓住了API這個關鍵節點，也有助於我們理解整個數據的流動，從而給出更好的系統設計。  

![image](https://cdn.bigquant.com/community/uploads/default/original/3X/8/b/8b7bc5de0e966d62691f2d28b47f06377738d78a.png)  
一個小知識，REST的來歷是Resource Representational State Transfer，說白了就是資源、表現形式和狀態變化。
進一步來說，在深入淺出REST的文章中，給出了五個核心原則【5】：

為所有“事物”定義ID  
將所有事物鏈接在一起  
**使用標準方法  
**  
**資源多重表述  
**  
無狀態通信  
總結來說，REST提供了一套機器之間溝通並且人也能一眼看懂的語言。  


我會在矽谷之路的免費直播中和大家深入剖析這道題目，現在想要深入學習的朋友，可以參考以下資料：

設計一個務實的RESTful API 1   
RESTful API 設計指南  
aisuhua/restful-api-design-references  
怎樣用通俗的語言解釋什麼叫REST，以及什麼是RESTful？  
深入淺出REST  
