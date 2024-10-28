# Icon Browser

## ダウンロード

このアプリケーションはバージョン管理にGit Large File Storageを利用している。
git lfsを利用していない方は以下のリンクに従ってgit lfsをインストール。
<https://github.com/git-lfs/git-lfs?utm_source=gitlfs_site&utm_medium=installation_link&utm_campaign=gitlfs#installing>

以下のコマンドでソースコードおよび実行に必要なデータをダウンロード

```bash
    git lfs clone https://github.com/hodhodhod/icon-browser.git
```

## 依存関係のインストール

このアプリケーションはパッケージ管理にuvを利用している。
uvを利用していない方は以下のリンクに従ってuvをインストール。
<https://docs.astral.sh/uv/getting-started/installation/>

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
