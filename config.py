#ポート
LISTEN_PORT = 8080

#ブランチ
BRANCH = "main"

#データパックの検証
#ローカルで検証を行う(mecha)
LOCAL_VALIDATE_DATAPACK = False
#GitHub Actionsで検証を行う
#この項目が有効な場合pullはActionsの後に実行されます
GITHUB_ACTIONS = True

#検証時のエラーを無視してサーバーへの適用を行うかどうか
IGNORE_VALIDATE_ERROR = False

#Minecraftサーバーのルートディレクトリへの絶対パス
MCSERVER_PATH = "path_to_server"

#データパック名 (datapacksフォルダ全体の場合は記入しない)
DATAPACK_NAME = ""

#自動リロード (RCON設定が必須)
AUTO_RELOAD = False

#サーバー内への通知 (RCON設定が必須)
TELL_INFO = True

#特定のタグを持つプレイヤーにのみ通知を送る
TELL_TAG = "op"

#RCON設定
RCON_ADDRESS = "127.0.0.1"
RCON_PORT = 25575
RCON_PASSWORD = "password"


#以下は触らない
MCSERVER_PATH = MCSERVER_PATH.rstrip("/")