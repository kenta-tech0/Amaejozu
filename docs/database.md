# データベーススキーマドキュメント

**最終更新日**: 2026-01-10
**データベース**: MySQL 8.0
**マイグレーションバージョン**: 11e02588c898

## 概要

Amaejozuアプリケーションのデータベーススキーマドキュメントです。開発者向けにテーブル構造とリレーションシップを記載しています。

## テーブル一覧

| テーブル名 | 説明 | 主要な用途 |
|-----------|------|-----------|
| users | ユーザーアカウント情報 | 認証、プロフィール管理 |
| brands | ブランド情報 | 商品のブランド分類 |
| categories | 商品カテゴリー（階層構造） | 商品の分類・検索 |
| products | 商品情報 | 価格追跡対象の商品データ |
| price_histories | 価格変動履歴 | 価格グラフ表示、分析 |
| watchlists | ウォッチリスト | ユーザーの追跡商品管理 |
| notifications | 通知履歴 | 価格下落通知、お知らせ |
| reviews | 商品レビュー | 楽天APIから取得したレビュー |
| weekly_rankings | 週次ランキング | AI生成のTOP10商品 |

---

## ER図（簡易版）

```
users ──┬─< watchlists >── products ──┬─< price_histories
        │                              │
        └─< notifications              ├─< reviews
                 │                     │
                 └─< watchlists        ├─< weekly_rankings
                                       │
                                       ├──> brands
                                       │
                                       └──> categories ──> categories (self)
```

---

## テーブル詳細

### 1. users（ユーザー）

ユーザーアカウント情報を管理するテーブル。

**モデルファイル**: `backend/app/models/user.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | ユーザーID（主キー） |
| email | VARCHAR(255) | NO | - | メールアドレス（ユニーク、ログインID） |
| hashed_password | VARCHAR(255) | NO | - | bcryptハッシュ化パスワード |
| nickname | VARCHAR(100) | YES | NULL | ニックネーム |
| is_active | BOOLEAN | NO | TRUE | アカウント有効フラグ |
| is_verified | BOOLEAN | NO | FALSE | メール認証済みフラグ |
| notification_token | VARCHAR(500) | YES | NULL | プッシュ通知トークン |
| email_notification_enabled | BOOLEAN | NO | TRUE | メール通知有効フラグ |
| last_login_at | DATETIME | YES | NULL | 最終ログイン日時 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP | 更新日時 |

**インデックス**:
- PRIMARY KEY: `id`
- UNIQUE: `email`
- INDEX: `is_active`, `created_at`

**リレーションシップ**:
- `watchlists` (1対多): ユーザーのウォッチリスト
- `notifications` (1対多): ユーザーへの通知

---

### 2. brands（ブランド）

化粧品ブランド情報を管理するテーブル。

**モデルファイル**: `backend/app/models/brand.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | ブランドID（主キー） |
| name | VARCHAR(200) | NO | - | ブランド名（ユニーク） |
| name_kana | VARCHAR(200) | YES | NULL | ブランド名（カナ） |
| logo_url | VARCHAR(500) | YES | NULL | ブランドロゴURL |
| description | TEXT | YES | NULL | ブランド説明 |
| official_site_url | VARCHAR(500) | YES | NULL | 公式サイトURL |
| rakuten_brand_id | VARCHAR(100) | YES | NULL | 楽天ブランドID |
| is_active | BOOLEAN | NO | TRUE | 有効フラグ |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP | 更新日時 |

**インデックス**:
- PRIMARY KEY: `id`
- UNIQUE: `name`
- INDEX: `is_active`, `rakuten_brand_id`

**リレーションシップ**:
- `products` (1対多): ブランドの商品一覧

---

### 3. categories（カテゴリー）

商品カテゴリーを管理する階層構造テーブル。

**モデルファイル**: `backend/app/models/category.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | カテゴリーID（主キー） |
| name | VARCHAR(200) | NO | - | カテゴリー名 |
| name_kana | VARCHAR(200) | YES | NULL | カテゴリー名（カナ） |
| parent_id | BIGINT | YES | NULL | 親カテゴリーID（外部キー） |
| display_order | INT | NO | 0 | 表示順序 |
| is_active | BOOLEAN | NO | TRUE | 有効フラグ |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP | 更新日時 |

**インデックス**:
- PRIMARY KEY: `id`
- INDEX: `parent_id`, `display_order`, `is_active`

**リレーションシップ**:
- `parent` (多対1): 親カテゴリー（自己参照）
- `children` (1対多): 子カテゴリー（自己参照）
- `products` (1対多): カテゴリーの商品一覧

**階層構造例**:
```
スキンケア (parent_id: NULL)
  ├─ 洗顔料 (parent_id: 1)
  ├─ 化粧水 (parent_id: 1)
  └─ 乳液 (parent_id: 1)
```

---

### 4. products（商品）

化粧品の商品情報を管理するメインテーブル。

**モデルファイル**: `backend/app/models/product.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | 商品ID（主キー） |
| rakuten_item_code | VARCHAR(200) | NO | - | 楽天商品コード（ユニーク） |
| name | VARCHAR(500) | NO | - | 商品名 |
| brand_id | BIGINT | YES | NULL | ブランドID（外部キー） |
| category_id | BIGINT | YES | NULL | カテゴリーID（外部キー） |
| image_url | VARCHAR(500) | YES | NULL | 商品画像URL |
| rakuten_url | VARCHAR(500) | NO | - | 楽天商品ページURL |
| affiliate_url | VARCHAR(500) | YES | NULL | アフィリエイトURL |
| msrp_price | DECIMAL(10,2) | YES | NULL | メーカー希望小売価格 |
| current_price | DECIMAL(10,2) | NO | - | 現在価格 |
| is_on_sale | BOOLEAN | NO | FALSE | セール中フラグ |
| discount_rate | DECIMAL(5,2) | YES | NULL | 割引率（%） |
| review_average | DECIMAL(3,2) | YES | NULL | レビュー平均（0.00-5.00） |
| review_count | INT | NO | 0 | レビュー件数 |
| description | TEXT | YES | NULL | 商品説明 |
| stock_status | VARCHAR(50) | YES | NULL | 在庫状態 |
| last_checked_at | DATETIME | NO | CURRENT_TIMESTAMP | 最終チェック日時 |
| is_active | BOOLEAN | NO | TRUE | 有効フラグ |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP | 更新日時 |

**インデックス**:
- PRIMARY KEY: `id`
- UNIQUE: `rakuten_item_code`
- INDEX: `brand_id`, `category_id`, `is_on_sale`, `last_checked_at`, `is_active`, `current_price`, `review_average`
- COMPOSITE: `idx_products_search(category_id, is_on_sale, current_price)` - 検索最適化用

**リレーションシップ**:
- `brand` (多対1): 商品のブランド
- `category` (多対1): 商品のカテゴリー
- `watchlists` (1対多): ウォッチリスト登録
- `price_histories` (1対多): 価格履歴
- `reviews` (1対多): レビュー
- `weekly_rankings` (1対多): 週次ランキング履歴

---

### 5. price_histories（価格履歴）

商品の価格変動履歴を記録するテーブル。

**モデルファイル**: `backend/app/models/price_history.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | 価格履歴ID（主キー） |
| product_id | BIGINT | NO | - | 商品ID（外部キー） |
| price | DECIMAL(10,2) | NO | - | 記録時の価格 |
| is_on_sale | BOOLEAN | NO | FALSE | セール中フラグ |
| discount_rate | DECIMAL(5,2) | YES | NULL | 割引率（%） |
| checked_at | DATETIME | NO | - | チェック日時 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |

**インデックス**:
- PRIMARY KEY: `id`
- INDEX: `product_id`, `checked_at`
- COMPOSITE: `idx_price_histories_product_time(product_id, checked_at)` - 時系列クエリ最適化

**リレーションシップ**:
- `product` (多対1): 価格が記録された商品

**運用メモ**:
- バックグラウンドワーカーが1日2回価格をチェック
- 価格変動があった場合のみレコード作成
- 古いデータ（1年以上前）は定期削除

---

### 6. watchlists（ウォッチリスト）

ユーザーが追跡している商品を管理するテーブル。

**モデルファイル**: `backend/app/models/watchlist.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | ウォッチリストID（主キー） |
| user_id | BIGINT | NO | - | ユーザーID（外部キー） |
| product_id | BIGINT | NO | - | 商品ID（外部キー） |
| target_price | DECIMAL(10,2) | YES | NULL | 目標価格（この価格以下で通知） |
| initial_price | DECIMAL(10,2) | NO | - | 登録時の価格 |
| lowest_price | DECIMAL(10,2) | YES | NULL | 追跡中の最安値 |
| is_notified | BOOLEAN | NO | FALSE | 通知済みフラグ |
| last_notified_at | DATETIME | YES | NULL | 最終通知日時 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP | 更新日時 |

**インデックス**:
- PRIMARY KEY: `id`
- UNIQUE COMPOSITE: `idx_watchlists_user_product(user_id, product_id)` - 重複登録防止
- INDEX: `user_id`, `product_id`, `is_notified`
- COMPOSITE: `idx_watchlists_user_recent(user_id, created_at)` - ユーザーの最近のウォッチリスト取得用

**リレーションシップ**:
- `user` (多対1): ウォッチリストの所有者
- `product` (多対1): 追跡対象の商品
- `notifications` (1対多): このウォッチリストに関連する通知

---

### 7. notifications（通知）

ユーザーへの通知履歴を管理するテーブル。

**モデルファイル**: `backend/app/models/notification.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | 通知ID（主キー） |
| user_id | BIGINT | NO | - | ユーザーID（外部キー） |
| watchlist_id | BIGINT | YES | NULL | ウォッチリストID（外部キー） |
| notification_type | VARCHAR(50) | NO | - | 通知タイプ（後述） |
| title | VARCHAR(200) | NO | - | 通知タイトル |
| message | TEXT | NO | - | 通知メッセージ |
| metadata | JSON | YES | NULL | 追加情報（JSON形式） |
| is_read | BOOLEAN | NO | FALSE | 既読フラグ |
| sent_at | DATETIME | YES | NULL | 送信日時 |
| read_at | DATETIME | YES | NULL | 既読日時 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |

**通知タイプ**:
- `price_drop`: 価格下落通知
- `target_reached`: 目標価格到達通知
- `weekly_ranking`: 週次TOP10ランキング通知
- `stock_alert`: 在庫復活通知

**インデックス**:
- PRIMARY KEY: `id`
- INDEX: `user_id`, `watchlist_id`, `is_read`, `sent_at`
- COMPOSITE: `idx_notifications_unread(user_id, is_read, sent_at)` - 未読通知取得用

**リレーションシップ**:
- `user` (多対1): 通知の受取人
- `watchlist` (多対1): 関連するウォッチリスト（ある場合）

**Pythonでのアクセス方法**:
```python
# JSONカラムは 'notification_metadata' としてアクセス
notification.notification_metadata = {"old_price": 1000, "new_price": 800}
```

---

### 8. reviews（レビュー）

商品レビュー情報を管理するテーブル。

**モデルファイル**: `backend/app/models/review.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | レビューID（主キー） |
| product_id | BIGINT | NO | - | 商品ID（外部キー） |
| rakuten_review_id | VARCHAR(100) | NO | - | 楽天レビューID（ユニーク） |
| reviewer_name | VARCHAR(100) | YES | NULL | レビュアー名 |
| rating | INT | NO | - | 評価（1-5） |
| review_text | TEXT | YES | NULL | レビュー本文 |
| helpful_count | INT | NO | 0 | 参考になった数 |
| review_date | DATE | NO | - | レビュー日付 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP | 更新日時 |

**インデックス**:
- PRIMARY KEY: `id`
- UNIQUE: `rakuten_review_id`
- INDEX: `product_id`, `rating`, `review_date`

**リレーションシップ**:
- `product` (多対1): レビュー対象の商品

---

### 9. weekly_rankings（週次ランキング）

AI生成の週次TOP10商品ランキングを管理するテーブル。

**モデルファイル**: `backend/app/models/weekly_ranking.py`

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | BIGINT | NO | AUTO_INCREMENT | ランキングID（主キー） |
| product_id | BIGINT | NO | - | 商品ID（外部キー） |
| week_start_date | DATE | NO | - | 週の開始日（月曜日） |
| rank_position | INT | NO | - | ランキング順位（1-10） |
| score | DECIMAL(10,4) | NO | - | スコア（算出根拠） |
| watchlist_count | INT | NO | 0 | ウォッチリスト登録数 |
| price_drop_rate | DECIMAL(5,2) | YES | NULL | 価格下落率（%） |
| ai_description | TEXT | YES | NULL | AI生成の商品説明 |
| created_at | DATETIME | NO | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | CURRENT_TIMESTAMP | 更新日時 |

**インデックス**:
- PRIMARY KEY: `id`
- UNIQUE COMPOSITE: `idx_weekly_rankings_week_rank(week_start_date, rank_position)` - 週ごとの順位重複防止
- INDEX: `product_id`, `week_start_date`
- COMPOSITE: `idx_weekly_rankings_week(week_start_date, rank_position)` - ランキング取得用

**リレーションシップ**:
- `product` (多対1): ランキング対象の商品

**スコア計算式**:
```python
score = (watchlist_count × 0.4) + (price_drop_rate × 0.3) + (review_average × 0.2) + (1 / rank_position × 0.1)
```

---

## 外部キー制約

| 子テーブル | 子カラム | 親テーブル | 親カラム | ON DELETE | ON UPDATE |
|-----------|---------|----------|---------|-----------|-----------|
| categories | parent_id | categories | id | CASCADE | CASCADE |
| products | brand_id | brands | id | SET NULL | CASCADE |
| products | category_id | categories | id | SET NULL | CASCADE |
| price_histories | product_id | products | id | CASCADE | CASCADE |
| watchlists | user_id | users | id | CASCADE | CASCADE |
| watchlists | product_id | products | id | CASCADE | CASCADE |
| notifications | user_id | users | id | CASCADE | CASCADE |
| notifications | watchlist_id | watchlists | id | SET NULL | CASCADE |
| reviews | product_id | products | id | CASCADE | CASCADE |
| weekly_rankings | product_id | products | id | CASCADE | CASCADE |

**設計方針**:
- ユーザー削除時: 関連するウォッチリスト・通知も削除（CASCADE）
- 商品削除時: 関連する履歴データも削除（CASCADE）
- ブランド/カテゴリー削除時: 商品は残してNULL設定（SET NULL）

---

## データアクセス例

### ユーザーのウォッチリスト取得

```python
from sqlalchemy import select
from app.models import User, Watchlist, Product

async def get_user_watchlist(db: AsyncSession, user_id: int):
    """ユーザーのウォッチリスト一覧を取得（商品情報含む）"""
    result = await db.execute(
        select(Watchlist)
        .where(Watchlist.user_id == user_id)
        .order_by(Watchlist.created_at.desc())
        .options(selectinload(Watchlist.product))
    )
    return result.scalars().all()
```

### 商品の価格履歴取得

```python
async def get_price_history(db: AsyncSession, product_id: int, days: int = 30):
    """指定日数分の価格履歴を取得"""
    cutoff_date = datetime.now() - timedelta(days=days)
    result = await db.execute(
        select(PriceHistory)
        .where(
            PriceHistory.product_id == product_id,
            PriceHistory.checked_at >= cutoff_date
        )
        .order_by(PriceHistory.checked_at.asc())
    )
    return result.scalars().all()
```

### 未読通知の取得

```python
async def get_unread_notifications(db: AsyncSession, user_id: int):
    """ユーザーの未読通知を取得"""
    result = await db.execute(
        select(Notification)
        .where(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        .order_by(Notification.sent_at.desc())
    )
    return result.scalars().all()
```

---

## マイグレーション管理

### 現在のバージョン確認

```bash
docker-compose exec backend alembic current
```

### テーブル構造の確認

```bash
# 特定テーブルの構造確認
docker-compose exec db mysql -u app_user -papp_password -D cosmetics_price_db -e "DESCRIBE users;"

# 全テーブル一覧
docker-compose exec db mysql -u app_user -papp_password -D cosmetics_price_db -e "SHOW TABLES;"

# インデックス確認
docker-compose exec db mysql -u app_user -papp_password -D cosmetics_price_db -e "SHOW INDEX FROM products;"
```

### モデル変更時の手順

1. `backend/app/models/*.py`でモデル定義を変更
2. マイグレーションファイル生成:
   ```bash
   docker-compose exec backend alembic revision --autogenerate -m "変更内容の説明"
   ```
3. 生成されたファイル確認: `backend/alembic/versions/xxx_*.py`
4. マイグレーション適用:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

---

## パフォーマンスチューニング

### スロークエリの確認

```sql
-- MySQLスロークエリログの有効化（my.cnf）
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow-query.log
long_query_time = 2
```

### 統計情報の更新

```bash
# 週次実行推奨
docker-compose exec db mysql -u app_user -papp_password -D cosmetics_price_db -e "ANALYZE TABLE products, price_histories, watchlists;"
```

---

## トラブルシューティング

### マイグレーションエラー

**問題**: `target_metadata is None` エラー
**解決**: `alembic/env.py`で全モデルが正しくインポートされているか確認

**問題**: 外部キー制約エラー
**解決**: 親レコードが存在するか確認。削除順序に注意（子→親の順）

### パフォーマンス問題

**問題**: 価格履歴取得が遅い
**解決**: `idx_price_histories_product_time`インデックスが存在するか確認

**問題**: ウォッチリスト一覧が遅い
**解決**: `selectinload()`でN+1問題を回避

---

## 関連ドキュメント

- [詳細設計書](../database_design.md) - テーブル設計の詳細
- [APIドキュメント](http://localhost:8000/docs) - FastAPI Swagger UI
- [README](../README.md) - プロジェクト概要とセットアップ

---

**最終更新者**: けんた
**マイグレーションバージョン**: 11e02588c898 (Initial migration)