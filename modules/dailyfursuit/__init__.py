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
Tailapi=utils.transfur.Tailapi("./config/bot.json")#call only once
async def img_resp(url:str) -> bytes:
    session = Ariadne.service.client_session
    async with session.get(url) as resp:  # type: ignore
        img_bytes = await resp.read()
    return img_bytes
@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def on_get_fursuit_rand(app: Ariadne, group: Group, message: MessageChain):
    if message.display == "每日鉴毛" or message.display == "随机每日鉴毛":
        jsonfy=Tailapi.getDaliyFursuitRand()
        await app.send_message(
            group,
            MessageChain([Image(data_bytes=await img_resp(jsonfy["data"]["url"]))]),
        )
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight.from_command("每日鉴毛 {furname}")],
    )
)
async def on_get_fursuit_by_name(app: Ariadne, group: Group, message: MessageChain, sparkle: Sparkle):
    lyrics1 = sparkle["furname"]
    jsonfy=Tailapi.getDaliyFursuitByName(str(lyrics1.result))
    if jsonfy['code'] == 200:
        await app.send_message(
            group,
            MessageChain([Image(data_bytes=await img_resp(jsonfy["data"]["url"]))]),
        )
    else:
        await app.send_message(
            group,
            MessageChain(["该每日鉴毛不存在"]),
        )
