# SVGアセット集作成ツール

画像ファイル（PNG、JPEG等）から背景を透過し、SVG形式に変換するツールです。

## 機能

- 自動背景除去（rembgライブラリ使用）
- 高品質なSVG変換（vtracerライブラリ使用）
- 画像の自動リサイズ
- バッチ処理対応

## セットアップ

1. 必要なライブラリをインストール:
```bash
pip install -r requirements.txt
```

## 使用方法

1. 変換したい画像を `knowledge/` フォルダに配置します
   - 対応形式: `.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`

2. スクリプトを実行:
```bash
python convert_to_svg.py
```

3. 変換されたSVGファイルは `output/` フォルダに保存されます

## フォルダ構成

```
svg-assets/
├── knowledge/        # 入力画像フォルダ
│   └── images/      # 画像ファイルを配置
├── output/          # 出力SVGフォルダ
├── config.py        # 設定ファイル
├── convert_to_svg.py # メインスクリプト
├── requirements.txt  # 依存関係
└── README.md        # このファイル
```

## 設定のカスタマイズ

`config.py` ファイルで以下の設定を変更できます：

### 画像リサイズ設定
- `max_width`: 最大幅（デフォルト: 1024px）
- `max_height`: 最大高さ（デフォルト: 1024px）
- `maintain_aspect_ratio`: アスペクト比を維持（デフォルト: True）

### SVG変換設定
- `colormode`: カラーモード（"color" または "binary"）
- `filter_speckle`: ノイズ除去レベル（デフォルト: 4）
- その他vtracerの詳細設定

### 背景除去設定
- `model`: 使用するAIモデル（デフォルト: "u2net"）
- `alpha_matting`: アルファマッティングの有効化

## トラブルシューティング

### メモリ不足エラー
大きな画像を処理する際にメモリ不足になる場合は、`config.py`の`max_width`と`max_height`を小さくしてください。

### 背景除去がうまくいかない
`config.py`の`REMBG_CONFIG`セクションでパラメータを調整してください。