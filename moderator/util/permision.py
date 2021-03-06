# -*- coding: utf-8 -*-

from telegram.chatmember import ChatMember
from telegram.error import BadRequest

from moderator.db.model import TelegramChat, AllChats
from moderator.util.logger import logger
from moderator.util.message import send_message


def admin(f):
    def wrapper(bot, update):
        message = update.message
        chat_id = message.chat.id
        user_id = message.from_user.id
        chat_member = bot.get_chat_member(chat_id, user_id)

        # 私聊的情况
        if message.chat.type == "private":
            send_message(bot, chat_id, "请在群组中操作")
            return

        # 增加当前用户组至数据库
        if chat_id not in AllChats.get_chat_ids():
            TelegramChat.add(message.chat.id, message.chat.title)

        # 用户必须是管理员才可以操作
        if chat_member.status not in (ChatMember.CREATOR, ChatMember.ADMINISTRATOR):
            send_message(bot, chat_id, "对不起, 您无管理员权限")
            return

        f(bot, update)

    return wrapper


def telegram_atom(f):
    def wrapper(self, bot, chat_id):
        try:
            f(self, bot, chat_id)

        except BadRequest as e:
            logger.error(e, str(e))
            if "Not enough rights" in str(e) or "admin" in str(e):
                send_message(bot, chat_id, "⚠️ 当前机器人权限不足～")

        except Exception as e:
            send_message(bot, chat_id, str(e), parse_mode=None)
            logger.error(e, str(e))

    return wrapper
