from nonebot import get_driver
from nonebot.adapters import Bot
from nonebot.matcher import Matcher
from nonebot.log import logger
from nonebot.exception import FinishedException
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot_plugin_alconna import command_manager
from nonebot_plugin_marshoai.plugin import on_function_call
from nonebot_plugin_marshoai.plugin.func_call.caller import Caller

from .utils import converts, push_event


@get_driver().on_startup
def parse_alc_command():

    for cmd in command_manager.get_commands():
        descreption = (
            cmd.meta.description
            if cmd.meta.description != "Unkown"
            else "用法：" + cmd.get_help()
        )
        cmd_name = cmd.name.replace("-", "_")
        arg_names = [(i.name).replace("-", "_") for i in cmd.args.argument]
        arg_type = [i.value.origin for i in cmd.args.argument]
        args = dict(zip(arg_names, arg_type))
        logger.info(f"小棉加载命令：{cmd_name}，描述：{descreption}，参数：{args}")

        @on_function_call(name=cmd_name, description=descreption).params(
            **converts(args)
        )
        async def func_call(
            event: MessageEvent, caller: Caller, bot: Bot, matcher: Matcher, **args
        ) -> str:
            logger.debug(f"小棉调用命令：{cmd_name}，参数：{args}" "")
            msg = f"/{cmd_name}"
            for arg_name, value in args.items():
                msg += f"--{arg_name} {value}"
            fake_msg_event = event
            fake_msg_event.message = Message(MessageSegment.text(msg))
            push_event(bot, fake_msg_event)
            raise FinishedException

        logger.info(f"小棉加载命令：{cmd_name}完成")
