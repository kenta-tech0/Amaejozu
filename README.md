# SpeakEasy - 英語スピーキング練習アプリ

AIとのシナリオベースの英会話練習で、スピーキング力を鍛えるWebアプリケーションです。

## 機能

- **シナリオベースの英会話練習**: レストラン注文、ホテルチェックイン、就職面接など、実践的なシーンでのロールプレイ
- **音声入力**: ブラウザの Web Speech API を使って英語で話しかける
- **AI会話パートナー**: Claude API による自然な英語応答
- **リアルタイムフィードバック**: 文法修正・表現アドバイスを日本語で表示
- **音声読み上げ**: AIの応答を英語で読み上げ
- **総合評価**: セッション終了時にスコアと改善ポイントを提示
- **練習履歴**: 過去のセッション記録を閲覧

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| フロントエンド | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| バックエンド | FastAPI, Python 3.11, SQLAlchemy (Async) |
| データベース | MySQL 8.0 |
| AI | Anthropic Claude API |
| 音声 | Web Speech API (Recognition + Synthesis) |
| インフラ | Docker Compose |

## セットアップ

### 1. 環境変数の設定

```bash
cp .env.example .env
```

`.env` ファイルを編集し、`ANTHROPIC_API_KEY` を設定してください。

### 2. 起動

```bash
docker-compose up -d --build
```

### 3. アクセス

- フロントエンド: http://localhost:3000
- バックエンド API: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs

## 使い方

1. トップページでシナリオを選択
2. マイクボタンを押して英語で話す
3. AIが応答し、文法修正やアドバイスを表示
4. 練習を終了すると総合評価を確認できる

## プロジェクト構成

```
├── frontend/          # Next.js フロントエンド
│   └── src/
│       ├── app/       # ページ（ホーム、練習、結果、履歴）
│       ├── components/  # 共通コンポーネント
│       └── lib/       # API クライアント、音声処理
├── backend/           # FastAPI バックエンド
│   └── app/
│       ├── api/       # API エンドポイント
│       ├── core/      # 設定、DB 接続
│       ├── models/    # SQLAlchemy モデル
│       └── services/  # Claude API サービス
├── database/          # MySQL 初期化スクリプト
└── docker-compose.yml
```
