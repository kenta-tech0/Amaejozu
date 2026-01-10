# 化粧品価格比較アプリケーション（Amaejozu）

化粧品の価格を自動で監視し、価格変動を通知するWebアプリケーションです。楽天市場APIとAzure OpenAIを活用して、ユーザーが希望する化粧品の価格を追跡し、お得な情報をメールで通知します。

## プロジェクト概要

このプロジェクトは、以下の機能を提供します：

- 化粧品の価格監視と追跡
- 楽天市場APIを利用した価格情報の取得
- Azure OpenAI (ChatGPT)を活用した商品情報の分析
- 価格変動時のメール通知（Resend経由）
- ユーザー認証とセキュアなデータ管理
- 定期的な価格更新とバックグラウンド処理

## 技術スタック

### フロントエンド
- **Next.js** - Reactベースのフロントエンドフレームワーク
- **Node.js** - JavaScript実行環境

### バックエンド
- **FastAPI** (v0.128.0) - Python製の高速Webフレームワーク
- **Python 3.11** - プログラミング言語
- **SQLAlchemy** (v2.0.45) - ORMとデータベース管理
- **Pydantic** (v2.12.5) - データバリデーション

### データベース
- **MySQL 8.0** - リレーショナルデータベース
- **Alembic** (v1.17.2) - データベースマイグレーションツール

### 外部API・サービス
- **楽天市場API** - 商品情報と価格データの取得
- **Azure OpenAI** (GPT-4o-mini) - 商品情報の分析とAI機能
- **Resend** (v2.5.0) - メール通知サービス

### 認証・セキュリティ
- **python-jose** (v3.3.0) - JWT認証
- **passlib + bcrypt** - パスワードハッシュ化
- **cryptography** (v44.0.0) - セキュア接続

### タスク管理
- **APScheduler** (v3.10.4) - 定期実行とバックグラウンドタスク

### 開発・テストツール
- **pytest** (v8.3.4) - テストフレームワーク
- **black** (v24.10.0) - コードフォーマッター
- **ruff** (v0.8.4) - 高速リンター
- **mypy** (v1.13.0) - 型チェック

### インフラ
- **Docker & Docker Compose** - コンテナ化と開発環境
- **uvicorn** - ASGIサーバー

## プロジェクト構造

```
Amaejozu/
├── backend/                          # FastAPIバックエンド
│   ├── alembic/                      # Alembicマイグレーション管理
│   │   ├── versions/                 # マイグレーションファイル格納
│   │   ├── env.py                    # Alembic環境設定
│   │   └── script.py.mako            # マイグレーションテンプレート
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/                      # APIエンドポイント
│   │   │   └── __init__.py
│   │   ├── core/                     # 設定、セキュリティ、ユーティリティ
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # 環境変数・設定管理
│   │   │   └── database.py           # DB接続・セッション管理
│   │   ├── models/                   # SQLAlchemyモデル（ORMクラス定義）
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # ユーザーモデル
│   │   │   ├── product.py            # 商品モデル
│   │   │   ├── watchlist.py          # ウォッチリストモデル
│   │   │   └── notification.py       # 通知モデル
│   │   ├── services/                 # ビジネスロジック
│   │   │   ├── __init__.py
│   │   │   ├── rakuten_api.py        # 楽天API連携
│   │   │   ├── azure_openai.py       # Azure OpenAI連携
│   │   │   └── email_service.py      # メール送信サービス
│   │   └── tasks/                    # バックグラウンドタスク
│   │       ├── __init__.py
│   │       └── price_tracker.py      # 価格追跡タスク
│   ├── alembic.ini                   # Alembic設定ファイル
│   ├── main.py                       # FastAPIエントリーポイント
│   ├── worker.py                     # バックグラウンドワーカー
│   ├── Dockerfile                    # バックエンドDockerイメージ
│   └── requirements.txt              # Python依存関係
│
├── frontend/                         # Next.jsフロントエンド
│   ├── src/
│   │   ├── app/                      # App Router (ページ)
│   │   ├── components/               # Reactコンポーネント
│   │   └── lib/                      # ユーティリティとヘルパー
│   ├── Dockerfile                    # フロントエンドDockerイメージ
│   ├── next.config.ts                # Next.js設定
│   ├── package.json                  # Node.js依存関係
│   └── tsconfig.json                 # TypeScript設定
│
├── database/                         # データベース初期化設定
│   └── init/                         # Docker初期化スクリプト
│       └── init.sql                  # MySQL初期化SQL
│
├── docker-compose.yml                # Docker Compose設定
├── .env.example                      # 環境変数のサンプル
├── .gitignore                        # Git除外設定
└── README.md                         # プロジェクトドキュメント
```

## 開発環境のセットアップ

### 前提条件

以下のツールがインストールされている必要があります：

- Docker Desktop
- Git
- テキストエディタ（VS Code推奨）

### セットアップ手順

#### 1. リポジトリのクローン

```bash
git clone <git@github.com:kenta-tech0/Amaejozu.git>
cd Amaejozu
```

#### 2. 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、必要な値を設定します。

```bash
cp .env.example .env
```

`.env` ファイルを編集して以下の値を設定：

```env
# 楽天API
RAKUTEN_API_KEY=your_rakuten_api_key_here

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-07-18-preview

# Resend（メール通知）これは仮なのでスルーしてください！！
RESEND_API_KEY=your_resend_api_key_here

# Database（開発環境ではデフォルト値で問題ありません）
DATABASE_URL=mysql+pymysql://app_user:app_password@db:3306/cosmetics_price_db

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# Frontend
NEXT_PUBLIC_API_ENDPOINT=http://localhost:8000
```

#### 3. Dockerコンテナの起動

```bash
# コンテナのビルドと起動
docker-compose up -d --build

# ログの確認
docker-compose logs -f
```

#### 4. データベースマイグレーションの実行（初回のみ）

```bash
# バックエンドコンテナに入る
docker-compose exec backend bash

# 初回マイグレーションを作成して適用
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# コンテナから抜ける
exit
```

#### 5. アプリケーションへのアクセス

起動が完了したら、以下のURLでアクセスできます：

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **APIドキュメント**: http://localhost:8000/docs
- **MySQL**: localhost:3306

**ヘルスチェック:**
```bash
# APIの動作確認
curl http://localhost:8000/
# 期待される結果: {"message":"Amaejozu API is running","version":"0.1.0","status":"healthy"}

curl http://localhost:8000/health
# 期待される結果: {"status":"healthy","database":"connected"}
```

### コンテナの管理

```bash
# コンテナの停止
docker-compose down

# コンテナの再起動
docker-compose restart

# ログの確認
docker-compose logs -f [service-name]

# 特定のコンテナに入る
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec db bash

# データベースのリセット（ボリュームも削除）
docker-compose down -v
```

## 開発ワークフロー

### バックエンド開発

```bash
# コンテナに入る
docker-compose exec backend bash

# テストの実行
pytest

# コードフォーマット
black .

# リンター実行
ruff check .

# 型チェック
mypy .
```

### データベースマイグレーション（Alembic）

```bash
# コンテナに入る
docker-compose exec backend bash

# 初回マイグレーションの作成
alembic revision --autogenerate -m "Initial migration"

# マイグレーションの適用
alembic upgrade head

# マイグレーション履歴の確認
alembic history

# 現在のバージョン確認
alembic current

# マイグレーションのロールバック（1つ前に戻す）
alembic downgrade -1

# 特定バージョンにロールバック
alembic downgrade <revision_id>

# モデル変更後の新規マイグレーション作成
# 1. app/models/*.py を編集
# 2. 以下のコマンドで自動検出・マイグレーション生成
alembic revision --autogenerate -m "Add new column to user table"
# 3. 生成されたファイルを確認後、適用
alembic upgrade head
```

### フロントエンド開発

```bash
# コンテナに入る
docker-compose exec frontend sh

# 開発サーバー起動（docker-composeで自動起動済み）
npm run dev

# ビルド
npm run build
```
### 開発運用ルール
- IssueとPRを紐づける（説明のところにCloses #<紐付けたいIssueの番号>と書くことで、プルリクエストとIssueを紐付けることができます）
- PR相互レビューをする（基本的には他の人がレビューする）
- ローカル動作が確認にできたら承認・マージ

### ブランチルール
- 作業を始める前に最新のmainブランチをフェッチ/プルする
- 命名規則
  - feature  → 新機能追加
  - fix      → バグ修正
  - refactor → リファクタリング
  - docs     → ドキュメントのみ変更
  - chore    → 環境設定・ビルド関連
 
- フォーマット
  - `<type>/#<issue番号>-<brief-description>`
- 例
  - `feature/#17-add-watchlist-api`
  - `fix/#25-notification-email-bug`
