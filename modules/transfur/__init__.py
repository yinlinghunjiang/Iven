from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.ariadne.message.element import Image
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import (
    Sparkle,
    Twilight,
)
import utils.transfur

channel = Channel.current()
Tailapi = utils.transfur.Tailapi("./config/bot.json")  # call only once


async def img_resp(url: str) -> bytes:
    session = Ariadne.service.client_session
    async with session.get(url) as resp:  # type: ignore
        img_bytes = await resp.read()
    return img_bytes


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def on_get_fursuit_rand(app: Ariadne, group: Group, message: MessageChain):
    if message.display == "来只毛":
        jsonfy = Tailapi.getFursuitRand()
        await app.send_message(
            group,
            MessageChain(
                [
                    "--- 每日吸毛 Bot ---\nID：{}\n毛毛名字：{}\n搜索方法：全局随机".format(
                        jsonfy["data"]["id"], jsonfy["data"]["name"]
                    ),
                    Image(data_bytes=await img_resp(jsonfy["data"]["url"])),
                ]
            ),
        )


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight.from_command("来只 {furname}")],
    )
)
async def on_get_fursuit_by_name(
    app: Ariadne, group: Group, message: MessageChain, sparkle: Sparkle
):
    lyrics1 = sparkle["furname"]
    jsonfy = Tailapi.getFursuitByName(str(lyrics1.result))
    if jsonfy["code"] == 200:
        await app.send_message(
            group,
            MessageChain(
                [
                    "--- 每日吸毛 Bot ---\nID：{}\n毛毛名字：{}\n搜索方法：全局模糊".format(
                        jsonfy["data"]["id"], jsonfy["data"]["name"]
                    ),
                    Image(data_bytes=await img_resp(jsonfy["data"]["url"])),
                ]
            ),
        )
    else:
        await app.send_message(
            group,
            MessageChain(["这只毛毛不存在"]),
        )


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight.from_command("搜毛图 {furid}")],
    )
)
async def on_get_fursuit_by_id(
    app: Ariadne, group: Group, message: MessageChain, sparkle: Sparkle
):
    lyrics1 = sparkle["furid"]
    jsonfy = Tailapi.getFursuitByID(str(lyrics1.result))
    if jsonfy["code"] == 200:
        await app.send_message(
            group,
            MessageChain(
                [
                    "--- 每日吸毛 Bot ---\nID：{}\n毛毛名字：{}\n搜索方法：全局精确".format(
                        jsonfy["data"]["id"], jsonfy["data"]["name"]
                    ),
                    Image(data_bytes=await img_resp(jsonfy["data"]["url"])),
                ]
            ),
        )
    else:
        await app.send_message(
            group,
            MessageChain(["这只毛毛不存在"]),
        )
