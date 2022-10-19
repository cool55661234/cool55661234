import pandas as pd
import matplotlib.pyplot as plt


# 讀取 CSV 資料
df = pd.read_csv('performance.csv')

# 選取所有列的 date, year_revenue 欄資料
data = df.loc[:, ['date', 'year_revenue']]
# 將 date 設為 index，要當作 X 軸使用
data = data.set_index('date')
print('data',data)

# 產生 line chart
data.plot(kind='bar')
# 設定圖表標頭
plt.title('stock performance')
# 顯示圖表
plt.show()