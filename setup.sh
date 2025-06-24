#!/bin/bash

echo "SVGアセット変換ツールのセットアップ"
echo "=================================="

# pipのインストール確認
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "pipがインストールされていません。"
    echo "以下のコマンドでpipをインストールしてください："
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt update && sudo apt install python3-pip"
    echo ""
    echo "Windows (管理者権限で実行):"
    echo "  python -m ensurepip --upgrade"
    echo ""
    exit 1
fi

# 仮想環境の作成（推奨）
echo "仮想環境を作成しますか？ (推奨) [y/N]"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python3 -m venv venv
    echo "仮想環境を有効化してください："
    echo "  Linux/Mac: source venv/bin/activate"
    echo "  Windows: venv\\Scripts\\activate"
    echo ""
    echo "その後、以下のコマンドを実行してください："
    echo "  pip install -r requirements.txt"
else
    echo "依存関係をインストールします..."
    pip install -r requirements.txt || pip3 install -r requirements.txt
fi

echo ""
echo "セットアップが完了したら、以下のコマンドで実行できます："
echo "  python convert_to_svg.py"