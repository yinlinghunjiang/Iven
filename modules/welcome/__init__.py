from graia.ariadne.event.mirai import MemberJoinEvent
from graia.saya import Channel
from graia.ariadne.model import Group,Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.app import Ariadne
from graia.ariadne.util.saya import listen
from graia.ariadne.message.element import At
channel = Channel.current()

@listen(MemberJoinEvent)
async def onMemberJoin(app: Ariadne, group:  Group, event: MemberJoinEvent,member: Member):
    await app.send_message(
        group,
        MessageChain([At(member.id)," 欢迎新成员"]),
    )
