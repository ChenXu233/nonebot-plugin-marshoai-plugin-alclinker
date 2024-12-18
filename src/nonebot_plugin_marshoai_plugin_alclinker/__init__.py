from nonebot import require

require("nonebot_plugin_alconna")
require("nonebot_plugin_marshoai")

from nonebot_plugin_alconna import on_alconna, Args, Option, Alconna

test = on_alconna(Alconna("test", Args["a", str]))


@test.handle()
async def _(a: str):
    await test.finish(a)


from .linker import *  # noqa: F403
