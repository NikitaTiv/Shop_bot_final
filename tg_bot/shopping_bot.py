import logging
from telegram.ext import (
    Updater, CommandHandler,
    ConversationHandler, Filters,
    MessageHandler, CallbackQueryHandler,
)
from settings_box import settings, constants
from tg_bot.handlers import (
    greet_user, main_menu, operations_with_receipt,
    add_receipt, my_receipts, check_user_photo, cancel,
    operation_phone_number, authorization_with_code, web_app,
    next_receipt,previous_receipt, tell_check_id,
    show_debtors_for_user
)

logging.basicConfig(filename='bot.log',
                    format='[%(asctime)s][%(levelname)s] => %(message)s',
                    level=logging.INFO)


def tg_main() -> None:
    """Run the bot."""
    mybot = Updater(settings.API_KEY, use_context=True)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', greet_user)],
        states={
            constants.MAIN_MENU: [
                MessageHandler(Filters.regex('^(Привет 👋)$'), main_menu),
            ],
            constants.ACTIONS_WITH_THE_RECEIPT: [
                MessageHandler(Filters.regex(
                    '^(Операции с чеками 💰)$',
                    ), operations_with_receipt),
                MessageHandler(Filters.regex(
                    '^(У меня есть код авторизации 📢)$'
                ), web_app),
                MessageHandler(Filters.regex(
                    '^(Хочу узнать кто сколько должен 🤑)$'
                ), tell_check_id),
            ],
            constants.RECEIPT_DEBTORS: [
                MessageHandler(Filters.regex(
                    '^(Возврат в предыдущее меню ↩️)$',
                ), main_menu),
                MessageHandler(Filters.text, show_debtors_for_user),
            ],
            constants.MENU_RECEIPT: [
                MessageHandler(Filters.regex(
                    '^(Добавить чек 🆕)$',
                    ), add_receipt),
                MessageHandler(Filters.regex('^(Мои чеки 📑)$'), my_receipts),
                MessageHandler(Filters.regex(
                    '^(Возврат в предыдущее меню ↩️)$',
                    ), main_menu),
                CallbackQueryHandler(previous_receipt, pattern='^'+str(0)+'$'),
                CallbackQueryHandler(next_receipt, pattern='^'+str(1)+'$')
            ],
            constants.ADD_CHECK: [
                MessageHandler(Filters.photo, check_user_photo),
                MessageHandler(Filters.regex(
                    '^(Возврат в предыдущее меню ↩️)$',
                    ), operations_with_receipt),
            ],
            constants.PHONE_NUMBER: [
                MessageHandler(Filters.regex(
                    '^(Возврат в предыдущее меню ↩️)$',
                    ), operations_with_receipt),
                MessageHandler(Filters.text,
                    operation_phone_number),
            ],
            constants.CODE: [
                MessageHandler(Filters.regex(
                    '^(Возврат в предыдущее меню ↩️)$',
                    ), operations_with_receipt),
                MessageHandler(Filters.text,
                    authorization_with_code),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp = mybot.dispatcher
    dp.add_handler(conv_handler)

    mybot.start_polling()
    mybot.idle()
