import pandas as pd
import matplotlib.pyplot as plt
# 引用 pymsql 套件
import pymysql

# 建立和資料庫連線，參數為資料庫系統位址(localhost 為本機電腦別名), 帳號(預設為 root，實務上不建議直接使用), 密碼(預設為空), 資料庫名稱
# charset 為使用編碼，cursorclass 則使用 dict 取代 tuple 當作回傳資料格式
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             # 資料庫預設為 3306 若自己有更改不同 port 請依照需求更改
                             port=3306,
                             db='demo_shop_logs',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# 使用 try...finally 錯誤處理，可以讓程式即便錯誤最後會關閉資料庫連線避免浪費資源
try:
    # 使用　with...as 可以讓我們程式正確執行下自動關閉資料庫連線
    with connection.cursor() as cursor:
        # 執行 SQL 敘述查詢資料，使用 """ raw string 符號將字串包起可以維持跨行
        sql = """
        SELECT
            keyword,
            result_num,
            COUNT(*) AS search_count
        FROM user_search_logs
        WHERE action = 'SEARCH' AND result_num = 0
        GROUP BY keyword, result_num
        ORDER BY search_count DESC;
        """
        cursor.execute(sql)
        # 取出所有結果
        items = cursor.fetchall()
finally:
    # 即便程式錯誤也會執行到這行關閉資料庫連線
    connection.close()

keyword_stats = {}

# 將 SQL 查詢資料一一取出
for item in items:
    # 取出欄位資料
    keyword = item['keyword']
    search_count = item['search_count']
    keyword_stats[keyword] = search_count

series_search_keyword = pd.Series(keyword_stats)
# 使用 matplotlib 建立圖表
plt.title('Search No Match keyword')
# 建立單一圖表
series_search_keyword.plot(kind='bar')
plt.show()