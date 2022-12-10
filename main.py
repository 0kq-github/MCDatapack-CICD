from flask import Flask, request
import mecha
from mcrcon import MCRcon
import glob
import config
import logging
import sys
from git import Repo
import json

app = Flask(__name__)
mc = mecha.Mecha()

if config.DATAPACK_NAME:
  datapack_path = f"{config.MCSERVER_PATH}/world/datapacks/{config.DATAPACK_NAME}"
else:
  datapack_path = f"{config.MCSERVER_PATH}/world/datapacks"


def setup_logging():
  global logger
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)
  fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
  handler = logging.StreamHandler(stream=sys.stdout)
  handler.setFormatter(fmt)
  logger.addHandler(handler)


def validate_datapack():
  global datapack_path
  error = False
  for i in glob.glob(datapack_path+"/**/*.mcfunction"):
    try:
      mc.compile(open(i).read())
    except mecha.diagnostic.DiagnosticError as e:
      error = True
      logger.error(f"File: {i} {e}")
      if config.TELL_INFO:
        with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
          mcr.command( \
'tellraw @a {"text":"[DATAPACK_VALIDATION_ERROR] \n\
================\n\
File: %s\n\
%s\n\
================"}'\
% (i,e))

  return error

@app.route("/",methods=["POST"])
def listner():
  global datapack_path
  #logger.info(f"Received webhook: {request.json}")
  if request.method == "POST":
    data = request.json
    if data["ref"] == "refs/heads/"+config.BRANCH:
      if config.VALIDATE_DATAPACK:
        error = validate_datapack()
        if not config.IGNORE_VALERROR and error:
          return
      Repo(datapack_path).remote().pull()
      for c in data['commits']:
        logger.info(f"New Commit! {c['message']}")
      if config.TELL_INFO:
        with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
          for c in data["commits"]:
            mcr.command('tellraw @a {"text":"[NEW COMMIT] %s"}' % c["message"].replace("\"","\\\""))
      if config.AUTO_RELOAD:
        with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
          mcr.command("reload")
  return "",200

if __name__ == "__main__":
  setup_logging()
  app.run(debug=True,use_reloader=False,threaded=False,host="0.0.0.0",port=config.LISTEN_PORT)
  
