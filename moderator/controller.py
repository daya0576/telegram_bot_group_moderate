# -*- coding: utf-8 -*-
from telegram import Update, Bot

from moderator.model.model import TelegramUser
from moderator.util import get_chat_id_and_users, logger, reply

TIP_TEMPLATE = "直接回复消息或 at 用户名，"


def start(bot: Bot, update: Update):
    reply(update, '👋👋👋')


def ban(bot: Bot, update: Update):
    logger.info("ban user...")
    chat_id, users = get_chat_id_and_users(update)

    if not users:
        reply(update, TIP_TEMPLATE + '进行踢出～')

    for user in users:
        try:
            if user.user_id:
                bot.kick_chat_member(chat_id, user_id=user.user_id)
                reply(update, f'已将该用户全球封杀！')
            else:
                reply(update, '用户尚未发言，暂时无法踢出。')
        except Exception as e:
            reply(update, str(e))
    logger.info("ban user done!!!")


def unban(bot: Bot, update: Update):
    logger.info("unban user...")
    chat_id, users = get_chat_id_and_users(update)
    if not users:
        reply(update, TIP_TEMPLATE + '进行解冻')
    for user in users:
        try:
            if user.user_id:
                bot.unban_chat_member(chat_id, user_id=user.user_id)

                reply(update, '知错能改，已将该用户解封！')
            else:
                reply(update, '未找到该用户，请联系管理员排查')
        except Exception as e:
            reply(update, str(e))
    logger.info("unban user done!!!")


def get_status(bot: Bot, update: Update):
    logger.info("get_status user...")
    chat_id, users = get_chat_id_and_users(update)

    if not users:
        reply(update, TIP_TEMPLATE + '进行用户状态查看')

    for user in users:
        status = "正常👏👏" if user.is_active else "封印中🔞🔞"
        reply(update, f'该用户的状态：{status}')

    logger.info("get_status done!!")


def reply_handler(bot: Bot, update: Update):
    logger.info("handle user message...")
    t_user = update.message.from_user
    user, created = TelegramUser.get_or_create(t_user.id, t_user.username)
    logger.info(f"handle user done!! user: {user}, created: {created}")
