
import os
import json
import feedparser
import requests
from google import genai

# 送信済みの記事リンクを読み込む関数
def load_sent_links():
    try:
        with open("sent_news.json", "r", encoding="utf-8") as f:
            return set(json.load(f))

    except FileNotFoundError:
        return set()

# 送信済みの記事リンクを保存する関数
def save_sent_links(sent_links):
    with open("sent_news.json", "w", encoding="utf-8") as f:
        json.dump(list(sent_links), f, ensure_ascii=False, indent=2)


# ① ニュースを取得する関数
def fetch_news():
    news = feedparser.parse(
        "https://feeds.bbci.co.uk/news/rss.xml"
    )

    if not news.entries:
        raise RuntimeError("ニュースを取得できませんでした")

    return news.entries[:5]


# ② ニュースを翻訳する関数
def translate_news(articles):
    english_text = ""

    for i, article in enumerate(articles, start=1):
        english_text += f"{i}. {article.title}\n"

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=(
            "以下のBBCニュース見出しを自然な日本語に翻訳してください。"
            "番号と順番を維持し、翻訳結果だけを出力してください。\n"
            + english_text
        )
    )

    if not response.text:
        raise RuntimeError("翻訳結果が空でした")

    return response.text


# ③ LINEに送信する関数
def send_line(articles, japanese_text):
    message = f"【BBCニュース{len(articles)}件】\n\n"
    message += japanese_text
    message += "\n\n【記事リンク】\n"

    for i, article in enumerate(articles, start=1):
        message += f"{i}. {article.link}\n"

    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    result = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "to": user_id,
            "messages": [
                {"type": "text", "text": message}
            ]
        },
        timeout=20
    )

    result.raise_for_status()

    print("LINEへの送信が成功しました！")


def main():
    articles = fetch_news()
    sent_links = load_sent_links()

    new_articles = []

    for article in articles:
        if article.link not in sent_links:
            new_articles.append(article)

    if new_articles:
        japanese_text = translate_news(new_articles)
        send_line(new_articles, japanese_text)

        for article in new_articles:
            sent_links.add(article.link)

        save_sent_links(sent_links)

    else:
        print("新しいニュースはありません")

# プログラムの開始地点
if __name__ == "__main__":
    main()
