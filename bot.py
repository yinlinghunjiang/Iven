import pkgutil
from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.saya import Saya
from config import init_config

# 初始化Saya
saya = create(Saya)

# 读配置
configs = init_config("./config/bot.json")

app = Ariadne(
    connection=config(
        configs.mirai["qq"],
        configs.mirai["verifykey"],
        HttpClientConfig(host=configs.mirai["host"]),
        WebsocketClientConfig(host=configs.mirai["host"]),
    ),
)
with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        saya.require(f"modules.{module_info.name}")

app.launch_blocking()
