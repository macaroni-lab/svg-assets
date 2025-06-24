# SVGアセット集作成ツール（高品質版）

画像ファイル（PNG、JPEG等）から背景を透過し、高品質なSVG形式に変換するツールです。

## 🚀 新機能（v2.0）

### 品質プリセット
- **ドラフト品質**: 高速処理優先、基本品質
- **標準品質**: バランスの取れた品質と速度
- **高品質**: 品質重視、処理時間やや長
- **ウルトラ品質**: 最高品質、処理時間長（解像度制限なし）

### 画像前処理パイプライン
- **ノイズ除去**: OpenCVの双方向フィルタ
- **シャープ化**: アンシャープマスキング
- **コントラスト強化**: CLAHE（適応ヒストグラム平均化）
- **エッジ強化**: 詳細保持とエッジ定義の向上

### 最適化されたパラメータ
- **VTracerパラメータ**: 高品質出力に最適化
- **背景除去**: 改良されたアルファマッティング
- **解像度管理**: 品質に応じた制限調整

## セットアップ

1. 必要なライブラリをインストール:
```bash
pip install -r requirements.txt
```

2. （オプション）セットアップスクリプトの実行:
```bash
chmod +x setup.sh
./setup.sh
```

## 使用方法

### 基本使用（従来互換）
```bash
python convert_to_svg.py
```

### 高品質版（推奨）
```bash
# 標準品質
python convert_to_svg_enhanced.py

# 高品質モード
python convert_to_svg_enhanced.py --quality high

# ウルトラ品質モード（最高品質）
python convert_to_svg_enhanced.py --quality ultra

# 品質プリセット一覧表示
python convert_to_svg_enhanced.py --list-presets

# 現在の設定表示
python convert_to_svg_enhanced.py --show-config --quality high
```

### オプション
- `--quality, -q`: 品質プリセット（draft/standard/high/ultra）
- `--verbose, -v`: 詳細な出力を表示
- `--list-presets`: 利用可能な品質プリセットを表示
- `--show-config`: 現在の設定を表示
- `--system-info`: システム情報を表示

## 画像配置

1. 変換したい画像を `knowledge/` フォルダに配置
   - 対応形式: `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`
2. 変換されたSVGファイルは `output/` フォルダに保存

## フォルダ構成

```
svg-assets/
├── knowledge/              # 入力画像フォルダ
│   └── images/            # 画像ファイルを配置
├── output/                # 出力SVGフォルダ
├── config.py              # 設定ファイル（拡張済み）
├── quality_presets.py     # 品質プリセット定義
├── image_processor.py     # 画像前処理パイプライン
├── utils.py               # ユーティリティ関数
├── convert_to_svg.py      # 基本スクリプト（従来互換）
├── convert_to_svg_enhanced.py # 高品質版スクリプト（推奨）
├── requirements.txt       # 依存関係（OpenCV追加）
├── setup.sh              # セットアップスクリプト
└── README.md             # このファイル
```

## 品質比較

| プリセット | 解像度制限 | 前処理 | 処理時間 | 品質 | 推奨用途 |
|----------|----------|-------|---------|-----|---------|
| draft    | 512x512  | なし   | 高速     | 基本 | プロトタイプ、プレビュー |
| standard | 1024x1024| 軽微   | 標準     | 良好 | 一般的な用途 |
| high     | 2048x2048| 充実   | やや長   | 高品質| 印刷、商用利用 |
| ultra    | 無制限    | 最大   | 長時間   | 最高 | プロ用途、アーカイブ |

## 設定のカスタマイズ

### 品質プリセットの選択
```bash
# ドラフト品質（最速）
python convert_to_svg_enhanced.py --quality draft

# 高品質（推奨）
python convert_to_svg_enhanced.py --quality high

# ウルトラ品質（最高品質）
python convert_to_svg_enhanced.py --quality ultra
```

### カスタム設定
`quality_presets.py`でプリセットを編集できます：

#### VTracerパラメータ最適化例
```python
"vtracer": {
    "filter_speckle": 2,      # 小→詳細保持、大→ノイズ除去
    "color_precision": 8,     # 高→色精度向上
    "layer_difference": 8,    # 低→グラデーション滑らか
    "corner_threshold": 80,   # 高→曲線滑らか
    "length_threshold": 3.5,  # 低→詳細度向上
}
```

#### 前処理設定
```python
"preprocessing": {
    "noise_reduction": True,      # ノイズ除去
    "sharpening": True,          # シャープ化
    "contrast_enhancement": True, # コントラスト強化
    "edge_enhancement": True,    # エッジ強化
}
```

## パフォーマンス最適化

### 処理時間短縮
1. `draft`プリセット使用
2. 画像サイズの事前縮小
3. 不要な前処理の無効化

### 品質向上
1. `high`または`ultra`プリセット使用
2. 高解像度画像の使用
3. 前処理の有効化

## トラブルシューティング

### メモリ不足エラー
- 低い品質プリセットを使用
- 画像サイズを事前に縮小
- `ultra`品質は高性能マシンで使用

### 品質が期待に届かない
- より高い品質プリセットを試行
- 元画像の品質を確認
- 前処理パラメータの調整

### 処理が遅い
- `draft`または`standard`プリセットを使用
- バッチ処理は時間のある時に実行
- 不要なファイルを事前に削除

### 依存関係のインストールエラー
```bash
# 仮想環境の使用を推奨
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```