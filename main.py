# module install
import sqlite3
import yfinance as yf
import pandas as pd
import numpy as np

# 変数
targets = ['3350.T', '5535.T', '3823.T'] # メタプラ、ミガロ、ワイハウ
start = '2018-01-01' # 開始日
end = '2025-06-14' # 終了日

# DB作成&接続
dbname = 'StockData.db'
conn = sqlite3.connect(dbname)

# 先にテーブルがあればドロップ（毎回クリアしたい場合）
conn.execute("DROP TABLE IF EXISTS StockData")
conn.commit()

# 各銘柄のDataFrameをためるリスト
dfs = []

# forループ
for target in targets:
    print(f"{target}のデータを取得中..ちょっとまってね")

    # データ取得
    df = yf.download(target, start=start, end=end, auto_adjust=False)[['Open', 'High', 'Low', 'Close', 'Volume']]

    # MultiIndex 列を flatten
    df.columns = df.columns.get_level_values(0)

    if df.empty:
        print(f"→ {target}のデータなし")
        continue

    # 小数点以下い切り捨て&型変換
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = np.floor(df[col]).astype(int)

    # 日付を列に戻し
    df.index.name = 'Acquired_Date'
    df = df.reset_index()
    df['Acquired_Date'] = df['Acquired_Date'].dt.strftime('%Y-%m-%d') #日付を文字列に変換
    
    # 銘柄コードを追加(ID列)
    df['Stock_ID'] = target
    
    # 列の順番を指定
    df = df[['Stock_ID', 'Acquired_Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    dfs.append(df)

    # 結合&MultiIndex平坦化
if dfs:
    all_df = pd.concat(dfs, ignore_index=True)

    # 重複した列名を削除
    all_df = all_df.loc[:, ~all_df.columns.duplicated()]
    
    # カラムの順番を指定
    all_df = all_df[['Stock_ID', 'Acquired_Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

    print(">> 最終的なカラム:", all_df.columns.tolist())

# 一度にまとめて書き込む

    all_df.to_sql(
        'StockData',
        conn,
        if_exists='replace',
        index=False
    )
    conn.commit()
conn.close()

print("全銘柄保存完了！")