import asyncio
from datetime import datetime
from platform import python_version
from darmilibs import __version__ as gver
from darmilibs import join
from darmilibs import BOT_VER
from darmilibs.darmi.helper.PyroHelpers import ReplyCheck
from pyrogram import __version__, filters, Client
from pyrogram.types import Message
from config import ALIVE_PIC, ALIVE_TEXT
from Darmi import START_TIME, SUDO_USER, app
from Darmi.modules.basic import add_command_help
from Darmi.modules.bot.inline import get_readable_time
from Darmi import cmds

alive_logo = ALIVE_PIC or "https://telegra.ph/file/80ddddfcd915d468bdb1a.png"

if ALIVE_TEXT:
   txt = ALIVE_TEXT
else:
    txt = (
        f"**darmi Pyro Userbot**\n\n"
        f"〄 **Versi**: `{BOT_VER}`\n"
        f"  ├• **Uptime**: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f"  ├• **Phython**: `{python_version()}`\n"
        f"  ├• **Pyrogram**: `{__version__}`\n"
        f"  └• **darmi Library**: `{gver}`\n\n"
        f"©️2023 [darmi](t.me/medsupportt)\n"
    )

@Client.on_message(filters.command(["darmi"], cmds) & filters.me)
async def module_help(client: Client, message: Message):
    await join(client)
    cmd = message.command
    help_arg = ""
    bot_username = (await app.get_me()).username
    if len(cmd) > 1:
        help_arg = "".join(cmd[1:])
    elif not message.reply_to_message and len(cmd) == 1:
        try:
            nice = await client.get_inline_bot_results(bot=bot_username, query="Alive")
            await asyncio.gather(
                message.delete(),
                client.send_inline_bot_result(
                    message.chat.id, nice.query_id, nice.results[0].id
                ),
            )
        except BaseException as e:
            print(f"{e}")

@Client.on_message(
    filters.command(["alive", "awake"], cmds) & (filters.me | filters.user(SUDO_USER))
)
async def alive(client: Client, message: Message):
    xx = await message.reply_text("⚡️")
    await join(client)
    await asyncio.sleep(3)
    try:
       await message.delete()
    except:
       pass
    send = client.send_video if alive_logo.endswith(f"{cmds}mp4") else client.send_photo
    xd = (f"{txt}")
    try:
        await asyncio.gather(
            xx.delete(),
            send(
                message.chat.id,
                alive_logo,
                caption=xd,
                reply_to_message_id=ReplyCheck(message),
            ),
        )
    except BaseException:
        await xx.edit(xd, disable_web_page_preview=True)

@Client.on_message(filters.command("repo", cmds) & filters.me)
async def repo(bot: Client, message: Message):
    await asyncio.sleep(1)
    await message.edit("Fetching Source Code.....")
    await asyncio.sleep(1)
    await message.edit("Here is repo: \n\n\nhttps://github.com/iskandar777-dar/DarmiPyro")


@Client.on_message(filters.command("creator", cmds) & filters.me)
async def creator(bot: Client, message: Message):
    await message.edit("https://gitHub.com/iskandar777-dar")


@Client.on_message(filters.command("id", cmds) & filters.me)
async def get_id(bot: Client, message: Message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"**File ID**: `{rep.audio.file_id}`"
            file_id += "**File Type**: `audio`"

        elif rep.document:
            file_id = f"**File ID**: `{rep.document.file_id}`"
            file_id += f"**File Type**: `{rep.document.mime_type}`"

        elif rep.photo:
            file_id = f"**File ID**: `{rep.photo.file_id}`"
            file_id += "**File Type**: `photo`"

        elif rep.sticker:
            file_id = f"**Sicker ID**: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"**Sticker Set**: `{rep.sticker.set_name}`\n"
                file_id += f"**Sticker Emoji**: `{rep.sticker.emoji}`\n"
                if rep.sticker.is_animated:
                    file_id += f"**Animated Sticker**: `{rep.sticker.is_animated}`\n"
                else:
                    file_id += "**Animated Sticker**: `False`\n"
            else:
                file_id += "**Sticker Set**: __None__\n"
                file_id += "**Sticker Emoji**: __None__"

        elif rep.video:
            file_id = f"**File ID**: `{rep.video.file_id}`\n"
            file_id += "**File Type**: `video`"

        elif rep.animation:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `GIF`"

        elif rep.voice:
            file_id = f"**File ID**: `{rep.voice.file_id}`\n"
            file_id += "**File Type**: `Voice Note`"

        elif rep.video_note:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += "**File Type**: `Video Note`"

        elif rep.location:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.location.latitude}`"

        elif rep.venue:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.venue.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.venue.location.latitude}`\n\n"
            file_id += "**Address**:\n"
            file_id += f"**title**: `{rep.venue.title}`\n"
            file_id += f"**detailed**: `{rep.venue.address}`\n\n"

        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`"
        await message.edit(user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = (
                f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
            )
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.id}`\n\n"
        user_detail += file_id
        await message.edit(user_detail)

    else:
        await message.edit(f"**Chat ID**: `{message.chat.id}`")




add_command_help(
    "start",
    [
        [f"{cmds}alive", "Check if the bot is alive or not."],
        [f"{cmds}repo", "Display the repo of this userbot."],
        [f"{cmds}creator", "Show the creator of this userbot."],
        [f"{cmds}id", "Send id of what you replied to."],
    ],
)

add_command_help(
    "restart",
    [
        [f"{cmds}restart", "You are retarded if you do not know what this does."],
    ],
)
