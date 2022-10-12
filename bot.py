import pkgutil
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.saya import Saya
import json
saya = create(Saya)
with open('./config/bot.json') as f:
	cfg = json.load(f)
app = Ariadne(
    connection=config(
        int(cfg["bot"]["qq"]),  
        cfg["bot"]["verifykey"],
        HttpClientConfig(host="http://localhost:8080"),
        WebsocketClientConfig(host="http://localhost:8080"),
    ),
)
with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        saya.require(f"modules.{module_info.name}")

app.launch_blocking()
