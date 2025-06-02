# IbUkeharai システム改修計画

## 概要

本計画書は、熊本生産Ｇにおける発送運賃請求内容入力漏れの会計処理ミスの再発防止対応として、請求マスタ機能の改善を行うための詳細なコード修正計画を記載しています。

## 改修要件

1. 単価、数量入力後、金額が自動計算される機能を追加
2. 単価、数量いずれか未入力の場合、入力を促す背景反転色付けする機能を追加
3. 金額は手入力ができないようグレーアウトにする
4. 請求書記載の数量の単位については、「単位」単独の項目を追加
5. 追加項目の単位は入力必須項目とし、未入力の場合背景色付けエラーにする

## 修正対象ファイル一覧

1. **データベース修正スクリプト**
   - 新規作成: `/home/ubuntu/repos/devin_tokunou_Iseki/DB/add_tani_column.sql`

2. **請求マスター登録画面**
   - `/home/ubuntu/repos/devin_tokunou_Iseki/IbUkeharai/IbUkeharai/RegisterSeikyuMasterForm.vb`

3. **請求書出力クラス**
   - `/home/ubuntu/repos/devin_tokunou_Iseki/IbUkeharai/IbUkeharai/clsDirectPrintSeikyu.vb`

4. **データグリッドビュー関連**
   - `/home/ubuntu/repos/devin_tokunou_Iseki/IbUkeharai/IbUkeharai/UcDataGridView.vb`

## 詳細修正計画

### 1. データベース修正スクリプト

**ファイル**: `/home/ubuntu/repos/devin_tokunou_Iseki/DB/add_tani_column.sql`（新規作成）

**修正前**: ファイルが存在しない

**修正後**:
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

### 2. 請求マスター登録画面の修正

**ファイル**: `/home/ubuntu/repos/devin_tokunou_Iseki/IbUkeharai/IbUkeharai/RegisterSeikyuMasterForm.vb`

#### 2.1 セル編集完了時の自動計算処理追加

**行番号**: 約1581-1632付近

**修正前**:
```vb
Private Sub UcDgv_CellEndEdit(sender As Object, e As DataGridViewCellEventArgs) Handles UcDgv.DgvCellEndEdit
    Dim customDataGridView As CustomDataGridView = CType(sender, CustomDataGridView)
    Dim dataGridViewColumn As DataGridViewColumn = customDataGridView.Columns(e.ColumnIndex)
    
    ' 値が変更されていない場合は何もしない
    If Operators.ConditionalCompareObjectEqual(customDataGridView.CellValuePre, customDataGridView.Rows(e.RowIndex).Cells(e.ColumnIndex).Value, False) Then
        Return
    End If
    
    ' 既存の処理（SAKI_CD、KAZEI_KBN、MEISAI_UMUなどの処理）
    If "SAKI_CD".Equals(dataGridViewColumn.Name) Then
        ' 既存のコード
    End If
    
    If "KAZEI_KBN".Equals(dataGridViewColumn.Name) Then
        ' 既存のコード
    End If
    
    If "MEISAI_UMU".Equals(dataGridViewColumn.Name) Then
        ' 既存のコード
    End If
End Sub
```

**修正後**:
```vb
Private Sub UcDgv_CellEndEdit(sender As Object, e As DataGridViewCellEventArgs) Handles UcDgv.DgvCellEndEdit
    Dim customDataGridView As CustomDataGridView = CType(sender, CustomDataGridView)
    Dim dataGridViewColumn As DataGridViewColumn = customDataGridView.Columns(e.ColumnIndex)
    Dim dataGridViewRow As DataGridViewRow = customDataGridView.Rows(e.RowIndex)
    
    ' 値が変更されていない場合は何もしない
    If Operators.ConditionalCompareObjectEqual(customDataGridView.CellValuePre, dataGridViewRow.Cells(e.ColumnIndex).Value, False) Then
        Return
    End If
    
    ' 数量または単価が変更された場合、金額を自動計算
    If "SURYO".Equals(dataGridViewColumn.Name) OrElse "TANKA".Equals(dataGridViewColumn.Name) Then
        ' 数量と単価の値を取得
        Dim suryo As Decimal = 0
        Dim tanka As Decimal = 0
        
        ' 数量の取得と検証
        If Not IsDBNull(dataGridViewRow.Cells("SURYO").Value) AndAlso Not String.IsNullOrEmpty(Conversions.ToString(dataGridViewRow.Cells("SURYO").Value)) Then
            If Not Decimal.TryParse(Conversions.ToString(dataGridViewRow.Cells("SURYO").Value), suryo) Then
                dataGridViewRow.Cells("SURYO").ErrorText = "数値を入力してください"
                Return
            Else
                dataGridViewRow.Cells("SURYO").ErrorText = Nothing
            End If
        Else
            ' 数量が未入力の場合は背景色を変更
            dataGridViewRow.Cells("SURYO").Style.BackColor = Color.FromArgb(255, 221, 221) ' 薄い赤色
        End If
        
        ' 単価の取得と検証
        If Not IsDBNull(dataGridViewRow.Cells("TANKA").Value) AndAlso Not String.IsNullOrEmpty(Conversions.ToString(dataGridViewRow.Cells("TANKA").Value)) Then
            If Not Decimal.TryParse(Conversions.ToString(dataGridViewRow.Cells("TANKA").Value), tanka) Then
                dataGridViewRow.Cells("TANKA").ErrorText = "数値を入力してください"
                Return
            Else
                dataGridViewRow.Cells("TANKA").ErrorText = Nothing
            End If
        Else
            ' 単価が未入力の場合は背景色を変更
            dataGridViewRow.Cells("TANKA").Style.BackColor = Color.FromArgb(255, 221, 221) ' 薄い赤色
        End If
        
        ' 両方の値が有効な場合は金額を計算
        If suryo > 0 AndAlso tanka > 0 Then
            Dim kingaku As Decimal = suryo * tanka
            dataGridViewRow.Cells("KINGAKU").Value = kingaku
            
            ' 背景色を元に戻す
            dataGridViewRow.Cells("SURYO").Style.BackColor = Me._bkcolor_normal
            dataGridViewRow.Cells("TANKA").Style.BackColor = Me._bkcolor_normal
        End If
    End If
    
    ' 単位の入力チェック
    If "TANI".Equals(dataGridViewColumn.Name) Then
        dataGridViewRow.Cells("TANI").ErrorText = Nothing
        If IsDBNull(dataGridViewRow.Cells("TANI").Value) OrElse String.IsNullOrEmpty(Conversions.ToString(dataGridViewRow.Cells("TANI").Value)) Then
            ' 単位が未入力の場合は背景色を変更
            dataGridViewRow.Cells("TANI").Style.BackColor = Color.FromArgb(255, 221, 221) ' 薄い赤色
        Else
            dataGridViewRow.Cells("TANI").Style.BackColor = Me._bkcolor_normal
        End If
    End If
    
    ' 既存の処理（変更なし）
    If "SAKI_CD".Equals(dataGridViewColumn.Name) Then
        ' 既存のコード
    End If
    
    If "KAZEI_KBN".Equals(dataGridViewColumn.Name) Then
        ' 既存のコード
    End If
    
    If "MEISAI_UMU".Equals(dataGridViewColumn.Name) Then
        ' 既存のコード
    End If
End Sub
```

#### 2.2 グリッドビュー初期化時の設定追加

**行番号**: 約1572-1578付近

**修正前**:
```vb
Dim gridViewInfo As New ControlDataGridView(custDgv, Me._conf)
ucDgv.CustDgv = custDgv
Me._gridViewInfo = gridViewInfo
Me._gridViewInfo.listOfHidden.Add("SAKU_KBN")

Me._gridViewInfo.DisplayGridView(sql, 0)
```

**修正後**:
```vb
Dim gridViewInfo As New ControlDataGridView(custDgv, Me._conf)
ucDgv.CustDgv = custDgv
Me._gridViewInfo = gridViewInfo
Me._gridViewInfo.listOfHidden.Add("SAKU_KBN")

' 金額列を読み取り専用に設定
Me._gridViewInfo.dataInfo.ItemDetail("KINGAKU").ReadOnly = True

Me._gridViewInfo.DisplayGridView(sql, 0)
```

#### 2.3 入力チェック機能の強化

**行番号**: 約507-514付近（chkInput メソッド内）

**修正前**:
```vb
Private Function chkInput(ByVal a_execFlag As Boolean) As Boolean
    ' 既存のコード
    
    ' 取引先コードのチェック
    If String.IsNullOrEmpty(Me.ComboTori1.Text.Trim()) Then
        Me.lblMessage.Text = "取引先コードを入力してください。"
        Me.ComboTori1.Focus()
        Return False
    End If
    
    ' 既存のコード
    
    Return True
End Function
```

**修正後**:
```vb
Private Function chkInput(ByVal a_execFlag As Boolean) As Boolean
    ' 既存のコード
    
    ' 取引先コードのチェック
    If String.IsNullOrEmpty(Me.ComboTori1.Text.Trim()) Then
        Me.lblMessage.Text = "取引先コードを入力してください。"
        Me.ComboTori1.Focus()
        Return False
    End If
    
    ' グリッドの必須項目チェック
    For Each row As DataGridViewRow In Me.UcDgv.CustDgv.Rows
        ' 削除されていない行のみチェック
        If row.Index < Me.UcDgv.CustDgv.NewRowIndex AndAlso Not row.IsNewRow Then
            ' 数量チェック
            If IsDBNull(row.Cells("SURYO").Value) OrElse String.IsNullOrEmpty(Conversions.ToString(row.Cells("SURYO").Value)) Then
                Me.lblMessage.Text = "数量を入力してください。"
                Me.UcDgv.CustDgv.CurrentCell = row.Cells("SURYO")
                Return False
            End If
            
            ' 単位チェック
            If IsDBNull(row.Cells("TANI").Value) OrElse String.IsNullOrEmpty(Conversions.ToString(row.Cells("TANI").Value)) Then
                Me.lblMessage.Text = "単位を入力してください。"
                Me.UcDgv.CustDgv.CurrentCell = row.Cells("TANI")
                Return False
            End If
            
            ' 単価チェック
            If IsDBNull(row.Cells("TANKA").Value) OrElse String.IsNullOrEmpty(Conversions.ToString(row.Cells("TANKA").Value)) Then
                Me.lblMessage.Text = "単価を入力してください。"
                Me.UcDgv.CustDgv.CurrentCell = row.Cells("TANKA")
                Return False
            End If
        End If
    Next
    
    ' 既存のコード
    
    Return True
End Function
```

#### 2.4 グリッドビュー初期化時の列プロパティ設定

**行番号**: 約1570-1580付近（RegisterSeikyuMasterForm_Load メソッド内）

**修正前**:
```vb
' 既存のコード（列プロパティの設定なし）
```

**修正後**:
```vb
' 金額列を読み取り専用に設定
For Each col As DataGridViewColumn In Me.UcDgv.CustDgv.Columns
    If col.Name = "KINGAKU" Then
        col.ReadOnly = True
        col.DefaultCellStyle.BackColor = Me._bkcolor_readonly
    End If
Next
```

### 3. 請求書出力クラスの修正

**ファイル**: `/home/ubuntu/repos/devin_tokunou_Iseki/IbUkeharai/IbUkeharai/clsDirectPrintSeikyu.vb`

#### 3.1 SQL クエリに単位カラムを追加

**行番号**: 約126-127付近

**修正前**:
```vb
Dim text2 As String = "SELECT H.TORI_CD, H.SEIKYU_YYYYMM, H.SEIKYU_TYPE, H.SEIKYU_NO, H.KAZEI, H.HIKAZEI, H.SYOHIZEI, H.GOUKEI, M.SEIKYU_SQNO, M.SAKU_KBN, M.UCHIWAKE, M.SURYO, M.TANI, "
text2 += " M.TANKA, M.KINGAKU, M.MEISAI_UMU, M.SAKI_CD, M.TEKIYO, T.TORI_NAME"
```

**修正後**: 既に `M.TANI` が含まれているため、修正は不要です。

### 4. データグリッドビュー関連の修正

**ファイル**: `/home/ubuntu/repos/devin_tokunou_Iseki/IbUkeharai/IbUkeharai/UcDataGridView.vb`

#### 4.1 グリッドビューの初期化時に単位列の設定を追加

**行番号**: 約100-150付近（InitializeComponent メソッド内）

**修正前**:
```vb
' 既存のコード（単位列の設定なし）
```

**修正後**:
```vb
' 単位列の最大入力文字数を設定
For Each col As DataGridViewColumn In Me.CustDgv.Columns
    If col.Name = "TANI" Then
        Dim textBoxCell As DataGridViewTextBoxColumn = TryCast(col, DataGridViewTextBoxColumn)
        If textBoxCell IsNot Nothing Then
            textBoxCell.MaxInputLength = 10
        End If
    End If
Next
```

## 実装手順

1. データベース修正スクリプトを作成し、実行する
2. RegisterSeikyuMasterForm.vb の修正
   - セル編集完了時の自動計算処理を追加
   - グリッドビュー初期化時の設定を追加
   - 入力チェック機能を強化
3. UcDataGridView.vb の修正
   - グリッドビューの初期化時に単位列の設定を追加
4. 修正後のテスト
   - 請求マスター登録画面での動作確認
   - 請求書出力での単位表示確認

## テスト計画

1. **単位項目の追加確認**
   - 請求マスター登録画面で単位項目が表示されることを確認
   - 単位項目に10文字まで入力できることを確認

2. **自動計算機能の確認**
   - 数量を入力後、単価を入力すると金額が自動計算されることを確認
   - 単価を入力後、数量を入力すると金額が自動計算されることを確認
   - 数量または単価を変更すると金額が再計算されることを確認

3. **入力制御の確認**
   - 金額項目が読み取り専用になっていることを確認
   - 単価、数量、単位が未入力の場合に背景色が変わることを確認

4. **入力チェック機能の確認**
   - 必須項目（単価、数量、単位）が未入力の状態で登録ボタンを押すとエラーメッセージが表示されることを確認
   - 単価、数量に数値以外を入力するとエラーメッセージが表示されることを確認

5. **請求書出力の確認**
   - 請求書に単位情報が表示されることを確認
