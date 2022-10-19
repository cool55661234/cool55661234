import pandas as pd
import matplotlib.pyplot as plt
# 引入 Python 內建網址解析套件
from urllib.parse import urlsplit, parse_qs
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
        # 執行 SQL 敘述查詢資料
        sql = 'SELECT * FROM user_purchase_logs'
        cursor.execute(sql)
        # 取出所有結果
        items = cursor.fetchall()
finally:
    # 即便程式錯誤也會執行到這行關閉資料庫連線
    connection.close()

# 建立 dict 儲存 UTM 統計資料
utm_stats = {
    'utm_source': {},
    'utm_medium': {},
    'utm_campaign': {}
}

# 將 SQL 查詢資料一一取出

# 將 SQL 查詢資料一一取出
for item in items:
    # 取出 referrer 欄位資料
    referrer = item['referrer']
    # 使用 urlsplit 將 referrer 網址分解成網址物件，取出屬性 query
    query_str = urlsplit(referrer).query
    # 將網址後面所接的參數轉為 dict：{}
    query_dict = parse_qs(query_str)

    # 將 query string 一一取出 {'utm_source': ['newsletter-weekly'], 'utm_medium': ['email'], 'utm_campaign': ['spring-summer']}
    for query_key, query_value in query_dict.items():
        # 取第 0 個 index 取出內容值
        utm_value = query_value[0]
        # 若參數值曾經出現過在 dict 的 key 中則累加 1
        if utm_value in utm_stats[query_key]:
            utm_stats[query_key][utm_value] += 1
        # 否則初始化成 1
        else:
            utm_stats[query_key][utm_value] = 1