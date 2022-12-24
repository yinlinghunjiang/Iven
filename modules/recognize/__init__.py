from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, Member
from graia.ariadne.message.element import Image, At
from graia.saya import Channel, Saya
import asyncio
from graia.ariadne.util.cooldown import CoolDown
import utils.detr_resnet
from creart import create
from graia.ariadne.message.parser.base import MatchContent
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from graia.saya.builtins.broadcast.schema import ListenerSchema

saya = Saya.current()
channel = Channel.current()
inc = create(InterruptControl)


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchContent(".rec")],
        inline_dispatchers=[CoolDown(30)],
    )
)
async def ero(app: Ariadne, group: Group, member: Member, message: MessageChain):
    await app.send_message(group, MessageChain("请在30秒内发送一张需要识别的图"))

    @Waiter.create_using_function([GroupMessage])
    async def img_waiter(g: Group, m: Member, msg: MessageChain):
        if group.id == g.id and member.id == m.id:
            imgs = msg[Image]
            if imgs == []:
                return ""
            else:
                img = imgs[0].url
                return img

    try:
        ret_msg = await inc.wait(img_waiter, timeout=30)  # 强烈建议设置超时时间否则将可能会永远等待
    except asyncio.TimeoutError:
        await app.send_message(group, MessageChain("已超时，本次操作取消。"))
    else:
        imgs = ret_msg
        if imgs != "":
            await app.send_message(group, MessageChain([At(member.id), " 正在识别中，请稍等"]))
            res = await utils.detr_resnet.query(imgs)
            await app.send_message(
                group, MessageChain([At(member.id), " 识别结果如下：\n", Image(base64=res)])
            )
        else:
            await app.send_message(group, MessageChain("未检测到图片或图片失效，请30s后重试"))
