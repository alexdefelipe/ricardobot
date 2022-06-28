import os

from flask import request

from ricardobot.configuration.app_config import app, bot
from ricardobot.persistance.utils.recreate_db import RecreateDb

@app.route('/main', methods=['POST'])
def main():
    bot.process_update(request.json)
    return '', 204


@app.route('/reset', methods=['PUT'])
def reset():
    RecreateDb.run()
    return '', 204


if __name__ == '__main__':
    root_path = f"{os.environ['RICARDOBOT_ROOT_PATH']}"
    app.run(host='0.0.0.0', port=8443, ssl_context=(f"{root_path}/cert.pem", f"{root_path}/key.pem"))
    print("holi")
