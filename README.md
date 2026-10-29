# BBC News LINE Bot

BBCニュースの最新記事を自動取得し、Gemini APIで日本語に翻訳してLINEに通知するPythonプログラムです。

## 主な機能

- BBCのRSSフィードから最新5件のニュースを取得
- Gemini APIを使ってニュース見出しを日本語に翻訳
- LINE Messaging APIでニュースと記事URLを送信
- JSONファイルで送信履歴を管理し、重複送信を防止
- Windowsタスク スケジューラによる毎朝8時の自動実行

## 使用技術

- Python
- feedparser
- Google Gemini API
- LINE Messaging API
- JSON
- Windows タスク スケジューラ

## セキュリティ

APIキーやアクセストークンは環境変数で管理し、ソースコードには記載していません。

## 開発目的

Pythonと生成AIを組み合わせた業務自動化の学習として制作しました。外部APIとの連携、データの保存、重複チェック、定期実行までを実装しています。
