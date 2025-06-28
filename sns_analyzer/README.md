# SNSソーシャルリスニングアプリ

Redditの投稿からSNSの声を収集・分析し、感情やキーワード傾向を可視化するStreamlit製のWebアプリです。

## 🚀 機能概要

- Reddit投稿をキーワード検索＋セマンティック検索
- 投稿の感情分析（positive / negative / neutral）
- 結果の可視化（棒グラフ・円グラフ・WordCloudなど）
- 検索期間の指定機能

## 🧪 動作環境（Google Colab推奨）

- Python 3.10以上
- streamlit
- pyngrok
- praw（Reddit APIクライアント）
- transformers, sentence-transformers
- wordcloud, matplotlib

## 🔧 セットアップ手順

### 1. このリポジトリをクローン

```bash
git clone https://github.com/c-panda-san/lecture-ai-engineering/sns-analyze.git
cd sns-analyze
```

### 2. ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 3. Reddit APIキーの設定
- .env.example をコピーして .env にリネームし、以下の内容を記入してください：

```ini
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
```
※ REDDIT_USER_AGENT はデフォルトで設定されています。

### 4. アプリの起動
```bash
streamlit run scr/app.py
```
Colabの場合は ngrok を使ってポートを公開してください。

## 📝 注意事項
- 感情分析は英語投稿に最適化されています（日本語投稿は "neutral" とされる可能性あり）
- セマンティック検索は最大100件の投稿候補から、日付範囲でさらに絞り込みを行います

### 補足：Reddit APIキーの取得方法

1. [Redditのアプリ登録ページ](https://www.reddit.com/prefs/apps) にアクセス
2. 下部の「Developed Applications」から「Create App」または「Create Another App」をクリック
3. 以下のように入力してアプリを作成：
   - **name**：任意（例：SNS Analyzer）
   - **type**：「script」を選択
   - **redirect uri**：`http://localhost:8080`（固定）
   - **description**：空でOK

4. 作成後、アプリ詳細に表示される以下の2つをコピー：
   - `client_id`（画面上部に表示される英数字）
   - `client_secret`（発行される秘密鍵）

5. `.env` ファイルに以下のように記載：
   ```ini
   REDDIT_CLIENT_ID=xxxxx
   REDDIT_CLIENT_SECRET=xxxxx
   ```
   
6. env ファイルはセキュリティのため 絶対にGitHubにアップロードしない よう注意してください。

## 📄 ライセンスについて
本プロジェクトには、Googleの Noto フォント（Apache License 2.0）が含まれています。  
詳細は [fonts/](fonts/) フォルダおよび [LICENSE](LICENSE) をご覧ください。

