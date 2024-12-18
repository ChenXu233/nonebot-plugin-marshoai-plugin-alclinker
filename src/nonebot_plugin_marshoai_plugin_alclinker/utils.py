import asyncio
from typing import Any, Union, Dict

from nonebot import get_driver
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot_plugin_marshoai.plugin import String, Integer, Array

tasks: set["asyncio.Task"] = set()


@get_driver().on_shutdown
async def cancel_tasks():
    for task in tasks:
        if not task.done():
            task.cancel()

    await asyncio.gather(
        *(asyncio.wait_for(task, timeout=10) for task in tasks),
        return_exceptions=True,
    )


def converts(args: Dict[str, Any]) -> Dict[str, Union[String, Integer, Array]]:
    for i in args:
        try:
            args[i] = int(args[i])
        except TypeError:
            args[i] = str(args[i])
        if isinstance(args[i], str):
            args[i] = String(description=filter_string(args[i] + str(type(args[i]))))
        elif isinstance(args[i], int):
            args[i] = Integer(description=filter_string(args[i] + str(type(args[i]))))
        elif isinstance(args[i], list):
            args[i] = Array(
                items=str(type(args[i])), description=filter_string(args[i][0])
            )
        else:
            args[i] = String(
                description=filter_string(str(args[i]) + str(type(args[i])))
            )
    return args


def push_event(bot: Bot, event: MessageEvent) -> None:
    task = asyncio.create_task(bot.handle_event(event))  # type: ignore
    task.add_done_callback(tasks.discard)
    tasks.add(task)


import re


def filter_string(s):
    return re.sub(r"[^a-zA-Z0-9_-]+", "", s)
