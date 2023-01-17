from loguru import logger
from src.utils.io import write_json
from src.data import DATA_DIR
from src.constance import keyboards
from src.utils.filters import IsAdmin
from src.bot import bot
import emoji


class Bot:
    def __init__(self, telebot):
        # create bot object
        self.bot = telebot

        # add custom filter
        self.bot.add_custom_filter(IsAdmin())

        # register handler
        self.handler()

        # run bot
        self.bot.infinity_polling()

    def handler(self):
        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(
                message.chat.id,
                '<strong>You are admin of this group</strong>!'
            )

        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            """
            Replay to command messages
            """
            self.bot.reply_to(message, "Howdy, how are you doing?")

        # @self.bot.message_handler(func=lambda m: True)
        # def echo_all(message):
        #     """
        #     Replay to a text message
        #     """
        #     write_json(DATA_DIR / 'Message.json', message.json)
        #     self.bot.reply_to(message, message.text)

        @self.bot.message_handler(func=lambda m: True)
        def echo_all(message):
            """
            Send message to a text message and show markup keyboard
            """
            write_json(DATA_DIR / 'Message.json', message.json)
            self.send_message(
                message.chat.id, message.text,
                reply_markup=keyboards.main)

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        send message to telegram bot
        """
        if emojize:
            text = emoji.emojize(text)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)


if __name__ == '__main__':
    logger.info('Bot Started')
    bot = Bot(telebot=bot)
    # bot.run()
    logger.info('Done!')
