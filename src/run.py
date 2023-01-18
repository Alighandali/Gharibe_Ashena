from loguru import logger
from src.utils.io import write_json, read_json
from src.data import DATA_DIR
from src.constance import keyboards, keys, states
from src.utils.filters import IsAdmin
from src.bot import bot
import emoji
import random


class Bot:
    def __init__(self, telebot):
        # create bot object
        self.bot = telebot

        # add custom filter
        self.bot.add_custom_filter(IsAdmin())

        # register handler
        self.handler()

        # create json database
        self.temp_db = read_json(DATA_DIR / 'Message.json')
        logger.info('Reading from db')

        # run bot
        self.bot.infinity_polling()

    def handler(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            """
            Replay to command messages
            """
            self.temp_db[str(message.chat.id)] = message.json
            self.temp_db[str(message.chat.id)]['state'] = states.main
            write_json(DATA_DIR / 'Message.json', self.temp_db)
            logger.info('Writing first info on db')
            self.send_message(
                message.chat.id,
                f"Hey {message.chat.first_name}!",
                reply_markup=keyboards.main
            )

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(
                message.chat.id,
                '<strong>You are admin of this group</strong>!',
                reply_markup=keyboards.main
            )

        # @self.bot.message_handler(func=lambda m: True)
        # def echo_all(message):
        #     """
        #     Replay to a text message
        #     """
        #     write_json(DATA_DIR / 'Message.json', message.json)
        #     self.bot.reply_to(message, message.text)

        @self.bot.message_handler(regexp=emoji.emojize(keys.random_connect))
        def random_connect(message):
            """
            Send message to a text message and show markup keyboard
            """
            self.temp_db[str(message.chat.id)]['state'] = states.random_connect
            write_json(DATA_DIR / 'Message.json', self.temp_db)
            logger.info('Writing random connect state on db')
            self.send_message(
                message.chat.id,
                ':magnifying_glass_tilted_right: Searching For a Stranger',
                reply_markup=keyboards.exit)
            members = list(self.temp_db.keys())
            while len(members) > 1:
                other_one = random.choice(members)
                if (other_one != str(message.chat.id) and
                        self.temp_db[other_one]['state'] ==
                        states.random_connect):
                    self.temp_db[other_one]['state'] = states.connected
                    self.temp_db[str(message.chat.id)]['state'] = states.connected
                    self.send_message(
                        other_one,
                        f''':winking_face: You Have Been Selected
                        by {message.chat.first_name}! You Can Talk Now!'''
                    )
                    self.send_message(
                        message.chat.id,
                        f''':winking_face: You Have Been 2 Selected by
                         {self.temp_db[other_one]['chat']['first_name']}
                         ! You Can Talk Now!'''
                    )
                    break
            self.send_message(
                other_one, message.text)

        @self.bot.message_handler(regexp=emoji.emojize(keys.exit))
        def exit(message):
            """
            Send message to a text message and show markup keyboard
            """
            self.temp_db[str(message.chat.id)]['state'] = states.main
            write_json(DATA_DIR / 'Message.json', self.temp_db)
            logger.info('Writing main state on db')
            self.send_message(
                message.chat.id, ':cross_mark: Searching has been Canceled',
                reply_markup=keyboards.main)

        # @self.bot.message_handler(func=lambda m: True)
        # def echo_all(message):
        #     """
        #     Send message to a text message and show markup keyboard
        #     """
        #     print(emoji.demojize(message.text))
        #     self.send_message(
        #         message.chat.id, message.text,
        #         reply_markup=keyboards.main)

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
    logger.info('Done!')
