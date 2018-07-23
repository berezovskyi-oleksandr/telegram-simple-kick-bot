import logging
import os
import sys

from telegram.ext import Updater, MessageHandler, Filters

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(name)-30s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M')

LOG = logging.getLogger(__name__)


def check_new_user(user):
    return len(user.full_name.split()) > 5


def new_user_handler(bot, update):
    kicked = False
    for member in update.message.new_chat_members:
        if check_new_user(member):
            update.message.chat.kick_member(member.id)
            LOG.info(f'Kicked "{member.full_name}"')
            kicked = True
    if kicked:
        LOG.debug('Deleting new message')
        update.message.delete()


if __name__ == '__main__':
    token = os.environ.get('TOKEN')
    if not token:
        logging.error('Please set TOKEN env variable')
        sys.exit(1)

    updater = Updater(token)
    updater.dispatcher.add_handler(
        MessageHandler(callback=new_user_handler, filters=Filters.status_update.new_chat_members)
    )
    updater.start_polling()
    logging.info('Bot started')
    updater.idle()
