# 📈 Stock Data Collector

**株価データ取得＆SQLite保存ツール**  
Python と yfinance を使って指定期間の株価（始値・高値・安値・終値）を取得し、SQLite データベースに保存します。

---

## 🚀 目次

- [機能概要](#機能概要)  
- [スクリーンショット](#スクリーンショット)  
- [セットアップ](#セットアップ)  
- [使い方](#使い方)  
- [ディレクトリ構成](#ディレクトリ構成)  
- [依存関係](#依存関係)  
- [ライセンス](#ライセンス)  

---

## 機能概要

1. 任意の銘柄コードリストを指定  
2. 指定期間の株価データを取得  
3. 小数点以下を切り捨てた整数値として整形  
4. `Stock_ID` / `Acquired_Date` / `Open` / `High` / `Low` / `Close` の 6 カラムで SQLite に一括保存  

---

## スクリーンショット

<!-- 実行結果やテーブル構造の画像を貼ると効果的 -->
![実行例](./docs/screenshot.png)

---

## セットアップ

```bash
git clone https://github.com/itou200107/stock-data-collector.git
cd stock-data-collector

# 仮想環境を作る（推奨）
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# targets, start/end は main.py 内で変更可能
python main.py