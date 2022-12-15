# MCDatapack-CI/CD
 GitHubからリアルタイムにデータパックを検証/同期するツール

## Installation
Windows環境での動作は未確認です
 1. Python3.10以上をインストール
 2. `pip install -r requirements.txt`で必要なパッケージのインストール
 3. `config.py`の編集
 4. `config.py`で設定したポートを開放
 5. GitHubで対象のリポジトリを開き  
    Settings > Webhooks > Add webhookでwebhookを追加し  
    Payload URLに`http://サーバーアドレス/`  
    Content typeを`application/json`  
    イベントを`Just the push event.`  
    に設定する
 6. `python main.py`でサーバーを起動

## GitHub Actionsでデータパックの検証を行う場合
1. [ここ](https://github.com/ChenCMD/datapack-linter)のREADMEを参考にActionsの設定を追加
2. `config.py`の`GITHUB_ACTIONS`を`True`に設定
3. GitHubのwebhookの設定を開き  
   `Let me select individual events.`から`Pushes`と`workflow runs`を有効化