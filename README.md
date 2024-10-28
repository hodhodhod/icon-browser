# Icon Browser

## 依存関係のインストール

このアプリケーションはパッケージ管理にuvを利用している。
uvを利用していない方は以下のリンクからuvをインストール。

以下のコマンドで依存関係のインストールができる。

```bash
    uv sync
```

## インデックスの作成(自分で実行する場合)

下記のコマンドを実行するとアイコン画像をダウンロードしインデックスを生成できる。

```bash
    uv run python download_images.py
    uv run python create_index.py
```

## アプリケーションの実行

下記のコマンドを実行するとlocalhostの8000番のポートでアプリが開く。

```bash
    uv run python app.py
```
