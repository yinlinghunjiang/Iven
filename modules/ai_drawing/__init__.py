from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group,Member
from graia.ariadne.message.element import Image,At,Plain
from graia.saya import Channel,Saya
import asyncio
from graia.ariadne.util.cooldown import CoolDown
import utils.detr_resnet
from creart import create
from graia.ariadne.message.parser.base import MatchContent
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from graia.saya.builtins.broadcast.schema import ListenerSchema
import utils.ai_drawing
from typing import Union
saya = Saya.current()
channel = Channel.current()
queue={}
class TagWaiter(Waiter.create([GroupMessage])):

    def __init__(self, group: Union[Group, int], member: Union[Member, int]):
        self.group = group if isinstance(group, int) else group.id
        self.member = member if isinstance(member, int) else member.id

    async def detected_event(self, group: Group, member: Member, message: MessageChain):
        if self.group == group.id and self.member == member.id:
            return message

inc = create(InterruptControl)
@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchContent(".aiDrawing")],
        inline_dispatchers=[CoolDown(30)]
    )
)
async def ai_drawing(
    app: Ariadne, group: Group, message: MessageChain, member: Member
):
    await app.send_message(group, MessageChain("请输入prompt"))
    queues=list(queue.keys())
    if member.id in queues:
        await app.send_message(group,MessageChain(At(member.id),[" 您有一个任务正在队列中，请稍等"]))
    else:
        try:
            ret_msg = await inc.wait(TagWaiter(group, member), timeout=30)  # 强烈建议设置超时时间否则将可能会永远等待
        except asyncio.TimeoutError:
            await app.send_message(group, MessageChain("你说话了吗？"))
        else:
            await app.send_message(group,MessageChain(At(member.id),[" 绘制中，请稍等.."]))
            queue[member.id]=ret_msg
            res= await utils.ai_drawing.getData(ret_msg)
            if res != "":
                await app.send_message(group,MessageChain([At(member.id)," 绘制完成",Image(data_bytes=res)]))
                queue.pop(member.id)
            else:
                await app.send_message(group,MessageChain([At(member.id)," 绘制失败，您可以在30s后重试"]))
                queue.pop(member.id)
