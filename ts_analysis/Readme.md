# 檔案說明

## 1. 程式檔說明
目錄位置： src資料夾內
+ preliminary_analysis.ipynb: 前期分析視覺化工具，幫助我們更快了解數據集各層面的樣貌
+ rfm.ipynb: 利用RFM模型將顧客依據常歸客、新顧客、沉睡課、流失客，協助我們推薦對的商品給對的客群
+ product_grossprofit.ipnb: 以gross profit的角度進行分析，了解每月與每日淨賺的變化，哪些年齡層讓商片賺了最多錢、哪些商品幫助商店賺最多錢等
+ apriori_analysis.ipynb: 進行關聯性分析，得出哪些商品組合最容易被一起購入，像是如果顧客買了A商品，我們推薦最有可能他會想一起購入的商品B給他

## 2. csv檔案說明
目錄位置: file資料夾內
+ purchase_list.csv: 將我們的顧客進行RFM分析，並建立出所有顧客的分群結果
+ clientId_weighted_average.csv: 為所有顧客的活躍程度分析表
+ gross_profit.csv: 為所有商品的為商店帶來的利潤分析結果
+ 推薦商品組合.csv: 透過關聯性分析得出的商品組合