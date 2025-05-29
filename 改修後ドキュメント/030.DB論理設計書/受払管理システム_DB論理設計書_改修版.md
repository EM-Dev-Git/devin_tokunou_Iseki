# 受払管理システム_DB論理設計書 改修版

## 概要
本ドキュメントは、「受払管理システム_DB論理設計書.xlsx」の改修版です。請求マスターテーブルに単位カラムを追加する変更を反映しています。

## 1. テーブル定義変更

### 1.1 請求マスターテーブル（M_SEIKYU）

#### 変更前
| No. | 論理名 | 物理名 | データ型 | 桁数 | NULL | 主キー | 外部キー | デフォルト値 | 備考 |
|-----|--------|--------|----------|------|------|--------|----------|--------------|------|
| 1 | 取引先コード | TORI_CD | VARCHAR | 10 | NOT NULL | ○ | M_TORI.TORI_CD | - | - |
| 2 | 部品コード | BUHIN_CD | VARCHAR | 15 | NOT NULL | ○ | M_BUHIN.BUHIN_CD | - | - |
| 3 | 数量 | KOSU | DECIMAL | 10,3 | NOT NULL | - | - | - | 小数点以下3桁 |
| 4 | 単価 | TANKA | DECIMAL | 10,2 | NOT NULL | - | - | - | 小数点以下2桁 |
| 5 | 金額 | KINGAKU | DECIMAL | 12,0 | NOT NULL | - | - | - | - |
| 6 | 登録日時 | INS_DATE | DATETIME | - | NOT NULL | - | - | CURRENT_TIMESTAMP | - |
| 7 | 更新日時 | UPD_DATE | DATETIME | - | NOT NULL | - | - | CURRENT_TIMESTAMP | - |
| 8 | 登録ユーザー | INS_USER | VARCHAR | 20 | NOT NULL | - | - | - | - |
| 9 | 更新ユーザー | UPD_USER | VARCHAR | 20 | NOT NULL | - | - | - | - |

#### 変更後
| No. | 論理名 | 物理名 | データ型 | 桁数 | NULL | 主キー | 外部キー | デフォルト値 | 備考 |
|-----|--------|--------|----------|------|------|--------|----------|--------------|------|
| 1 | 取引先コード | TORI_CD | VARCHAR | 10 | NOT NULL | ○ | M_TORI.TORI_CD | - | - |
| 2 | 部品コード | BUHIN_CD | VARCHAR | 15 | NOT NULL | ○ | M_BUHIN.BUHIN_CD | - | - |
| 3 | 数量 | KOSU | DECIMAL | 10,3 | NOT NULL | - | - | - | 小数点以下3桁 |
| 4 | **単位** | **TANI** | **VARCHAR** | **10** | **NOT NULL** | - | - | - | **例: 個、箱、kg など** |
| 5 | 単価 | TANKA | DECIMAL | 10,2 | NOT NULL | - | - | - | 小数点以下2桁 |
| 6 | 金額 | KINGAKU | DECIMAL | 12,0 | NOT NULL | - | - | - | - |
| 7 | 登録日時 | INS_DATE | DATETIME | - | NOT NULL | - | - | CURRENT_TIMESTAMP | - |
| 8 | 更新日時 | UPD_DATE | DATETIME | - | NOT NULL | - | - | CURRENT_TIMESTAMP | - |
| 9 | 登録ユーザー | INS_USER | VARCHAR | 20 | NOT NULL | - | - | - | - |
| 10 | 更新ユーザー | UPD_USER | VARCHAR | 20 | NOT NULL | - | - | - | - |

※ 太字は今回の改修で追加・変更された項目

### 1.2 変更内容の詳細
1. **単位カラムの追加**
   - 論理名: 単位
   - 物理名: TANI
   - データ型: VARCHAR(10)
   - NULL許容: NOT NULL
   - 主キー: なし
   - 外部キー: なし
   - デフォルト値: なし
   - 備考: 数量の単位を表す（例: 個、箱、kg など）

## 2. 関連テーブルへの影響

### 2.1 請求書出力関連テーブル
請求書出力機能で使用されるテーブルがある場合、単位情報を連携するための対応が必要です。具体的なテーブル名と変更内容は以下の通りです：

#### 2.1.1 請求書出力履歴テーブル（T_SEIKYU_HISTORY）
請求書出力履歴を保存するテーブルがある場合、単位情報を保存するカラムの追加が必要です。

#### 2.1.2 請求書明細テーブル（T_SEIKYU_MEISAI）
請求書の明細情報を保存するテーブルがある場合、単位情報を保存するカラムの追加が必要です。

## 3. データ移行計画

### 3.1 既存データの対応
既存の請求マスターデータに対して、単位カラムの初期値設定が必要です。

#### 3.1.1 移行手順
1. 既存データのバックアップを取得
2. 単位カラムを追加するALTER TABLE文を実行
3. 既存データの単位カラムに初期値を設定するUPDATE文を実行

#### 3.1.2 移行SQLサンプル
```sql
-- バックアップテーブル作成
SELECT * INTO M_SEIKYU_BACKUP FROM M_SEIKYU;

-- 単位カラム追加
ALTER TABLE M_SEIKYU ADD TANI VARCHAR(10) NOT NULL DEFAULT '個';

-- 初期値設定（デフォルトで「個」を設定）
UPDATE M_SEIKYU SET TANI = '個';

-- デフォルト制約の削除（必要に応じて）
ALTER TABLE M_SEIKYU ALTER COLUMN TANI DROP DEFAULT;
```

## 4. インデックス設定

### 4.1 既存インデックス
請求マスターテーブル（M_SEIKYU）の既存インデックスは以下の通りです：

| インデックス名 | 対象カラム | 種類 | 備考 |
|----------------|------------|------|------|
| PK_M_SEIKYU | TORI_CD, BUHIN_CD | 主キー | クラスター化 |
| IX_M_SEIKYU_TORI | TORI_CD | 非クラスター化 | - |
| IX_M_SEIKYU_BUHIN | BUHIN_CD | 非クラスター化 | - |

### 4.2 新規インデックス
新規追加カラム（TANI）に対するインデックス設定は不要です。

## 5. 外部キー制約

### 5.1 既存外部キー制約
請求マスターテーブル（M_SEIKYU）の既存外部キー制約は以下の通りです：

| 制約名 | 参照元 | 参照先 | 備考 |
|--------|--------|--------|------|
| FK_M_SEIKYU_TORI | M_SEIKYU.TORI_CD | M_TORI.TORI_CD | - |
| FK_M_SEIKYU_BUHIN | M_SEIKYU.BUHIN_CD | M_BUHIN.BUHIN_CD | - |

### 5.2 新規外部キー制約
単位マスターテーブルが存在する場合は、外部キー制約の検討が必要です。現状では単位マスターテーブルは存在しないため、外部キー制約は追加しません。

## 6. 改修影響範囲

本改修によるDB設計への影響範囲は以下の通りです：

1. テーブル定義変更
   - 請求マスターテーブル（M_SEIKYU）に単位カラム（TANI）を追加

2. データ移行
   - 既存データに対する単位カラムの初期値設定

3. アプリケーション連携
   - 請求マスター登録機能での単位情報の登録
   - 請求書出力機能での単位情報の取得・表示
