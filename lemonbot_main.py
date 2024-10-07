from lemonbot_behavior import *
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,filters,MessageHandler
from config import TOKEN




def call_lemon_main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("hello", echo))
    app.add_handler(CommandHandler("start", start))
    app.add_handler((MessageHandler(filters.TEXT & ~filters.COMMAND, handle_weather_input)))
    app.add_handler(CommandHandler("startweather",start_weahter))
    app.add_handler(CommandHandler("stopweather",stop_weather))
    app.add_handler(CommandHandler("setcity",set_city))
    # app.add_handler(MessageHandler((~filters.COMMAND), other_command))
    app.run_polling()
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    call_lemon_main()
    
    