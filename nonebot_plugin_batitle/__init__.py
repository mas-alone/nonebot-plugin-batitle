from nonebot import on_startswith, require
from nonebot.plugin import PluginMetadata
from nonebot.params import EventPlainText, Startswith
from nonebot.matcher import Matcher
from .draw import draw_pic
from io import BytesIO
require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory, Image


__version__ = "0.1.5"
__plugin_meta__ = PluginMetadata(
    name="BlueArchive Title Generator",
    description="碧蓝档案式标题生成器",
    usage="batitle 前|后",
    type="application",
    homepage="https://github.com/MerCuJerry/nonebot-plugin-batitle",
    config=None,
    supported_adapters={
        "~onebot.v11",
        "~onebot.v12",
        "~kaiheila",
        "~telegram",
        "~feishu",
        "~red",
    },
    extra={
        "version": __version__,
        "author": "MerCuJerry <mercujerry@gmail.com>",
    },
)

batitle = ("ba ", "BA ", "Ba ")
batitle_matcher = on_startswith(msg=batitle, block=True, priority=5)


@batitle_matcher.handle()
async def _handler(
    matcher: Matcher, str_match: str = Startswith(), key: str = EventPlainText()
):
    try:
        keyword: str = key.replace(str_match, "")
        if "|" in keyword:
            params = keyword.split("|")
        else:
            params = keyword.split()
        if len(params) != 2 or not params[0].strip() or not params[1].strip():
            await matcher.finish("请检查命令格式是否正确，应为 [ba 参数|参数2] 或 [ba 参数 参数2]")
            return
        upper = params[0].strip()
        downer = params[1].strip()
        img_raw = draw_pic(front=upper, back=downer)
        img = BytesIO()
        img_raw.save(img, format="png")
        img_bytes: bytes = img.getvalue()
        img_raw.close()
        img.close()
        await MessageFactory(Image(img_bytes)).send()
        await matcher.finish()

    except OSError:
        await matcher.finish("生成失败，请重试")
    except IndexError:
        await matcher.finish("请检查命令格式是否正确，应为 [ba 参数|参数2] 或 [ba 参数 参数2]")
