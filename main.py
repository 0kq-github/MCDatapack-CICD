from flask import Flask, request
import mecha
from mcrcon import MCRcon
import glob
import config
import logging
import sys
from git import Repo
import time

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
  report = mecha.DiagnosticCollection()
  for i in glob.glob(datapack_path+"/**/*.mcfunction",recursive=True):
    try:
      mc.compile(open(i,mode="r",encoding="utf-8").read())
    except mecha.diagnostic.DiagnosticError as e:
      error = True
      logger.error(f"File: {i} {e}")
      if config.TELL_INFO:
        with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
          cmd = 'tellraw @a [{"text":"["},{"text":"DATAPACK VALIDATION ERROR","color":"red"},{"text":"] File: %s","color":"white"}]' % (i.replace("\\","/"))
          cmd = cmd
          mcr.command(cmd)
  return error

@app.route("/",methods=["POST"])
def listner():
  global datapack_path
  #logger.info(f"Received webhook: {request.json}")
  if request.method == "POST":
    data = request.json
    if config.GITHUB_ACTIONS:
      if "action" in data.keys():
        if data["action"] == "completed":
          if data["workflow_run"]["conclusion"] == "success":
            Repo(datapack_path).remote().pull()
            if config.TELL_INFO:
              with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
                mcr.command(
                  'tellraw @a [{"text":"["},{"text":"GITHUB ACTINOS","color":"gray"},{"text":"]","color":"white"},{"text":" %s "},{"text":"%s ","color":"green"},{"text":"(","color":"white"},{"text":"Summary","color":"aqua","clickEvent":{"action":"open_url","value":"%s"}},{"text":")","color":"white"}]' 
                  % (data["workflow_run"]["name"],data["workflow_run"]["conclusion"],data["workflow_run"]["html_url"])
                  )
            if config.AUTO_RELOAD:
              with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
                mcr.command("reload")
          elif config.TELL_INFO:
            if config.IGNORE_VALIDATE_ERROR:
              Repo(datapack_path).remote().pull()
              if config.AUTO_RELOAD:
                with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
                  mcr.command("reload")
            with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
              mcr.command(
                'tellraw @a [{"text":"["},{"text":"GITHUB ACTINOS","color":"gray"},{"text":"]","color":"white"},{"text":" %s "},{"text":"%s ","color":"red"},{"text":"(","color":"white"},{"text":"Summary","color":"aqua","clickEvent":{"action":"open_url","value":"%s"}},{"text":")","color":"white"}]' 
                % (data["workflow_run"]["name"],data["workflow_run"]["conclusion"],data["workflow_run"]["html_url"])
                )
          else:
            if config.IGNORE_VALIDATE_ERROR:
              Repo(datapack_path).remote().pull()
            return "",200
      else:
        return "",200
    elif "ref" in data.keys():
      if data["ref"] == "refs/heads/"+config.BRANCH:
        if config.LOCAL_VALIDATE_DATAPACK:
          error = validate_datapack()
          if not config.IGNORE_VALIDATE_ERROR and error:
            return "",200
        Repo(datapack_path).remote().pull()
        for c in data['commits']:
          logger.info(f"New Commit! {c['message']}")
        if config.TELL_INFO:
          with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
            for c in data["commits"]:
              mcr.command('tellraw @a [{"text":"["},{"text":"NEW COMMIT","color":"green"},{"text":"] %s","color":"white"}]' % c["message"].replace("\"","\\\""))
        if config.AUTO_RELOAD:
          with MCRcon(config.RCON_ADDRESS,config.RCON_PASSWORD,config.RCON_PORT) as mcr:
            mcr.command("reload")
    return "",200

if __name__ == "__main__":
  setup_logging()
  app.run(debug=True,use_reloader=False,threaded=False,host="0.0.0.0",port=config.LISTEN_PORT)
  
