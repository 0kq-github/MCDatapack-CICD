#ポート
LISTEN_PORT = 8080

#データパックの検証
VALIDATE_DATAPACK = True

#検証時のエラーを無視してサーバーへの適用を行うかどうか
IGNORE_VALERROR = False

#Minecraftサーバーのルートディレクトリへのパス
MCSERVER_PATH = "~/server"

#データパック名 (datapacksフォルダ全体の場合は記入しない)
DATAPACK_NAME = ""

#自動リロード (RCON設定が必須)
AUTO_RELOAD = False

#サーバー内への通知 (RCON設定が必須)
TELL_INFO = False

#RCON設定
RCON_ADDRESS = "127.0.0.1"
RCON_PORT = 25575
RCON_PASSWORD = "password"


#以下は触らない
MCSERVER_PATH = MCSERVER_PATH.rstrip("/")