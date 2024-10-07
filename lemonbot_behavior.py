from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,CallbackContext
from config import TOKEN,BOT_NAME
import re
from get_data import get_current_data,get_forcast_data,temps_list_procees,rain_process,wind_process
import schedule
from threading import Thread

weather_enabled = False
user_city = None 

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello!!! {update.effective_user.first_name}')

# 回复固定内容  
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    
    await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Welcome to 暖男{BOT_NAME},Please input "weather_CITYNAME" for check the current weahter. For an example: weather_Taipei. And input "forcast_CITYNAME" to check forecast of city.')  

async def handle_weather_input(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    # await context.bot.send_message(chat_id=update.effective_chat.id,  
    #                                text=f"需要幫忙請按/help")  
    match = re.match(r'weather_(\w+)', user_input)
    if match:
        await update.message.reply_text(f"{BOT_NAME} is loading from the heart...")
        city = match.group(1)  # 抓取城市名稱
        # print(city)

        result,weather_data = get_current_data(city)
        if result:
            await update.message.reply_text(f'The weather info in {city} as following:The weahter is  {weather_data["weather_des"].lower()}. \
            The temperature is {weather_data["temp"]} degree.It feels like {weather_data["app_temp"]} degree.')
            # wind
            if weather_data["wind_spd"] > 0 :
                await update.message.reply_text(f'The speed of wind is {weather_data["wind_spd"]}')
            # rain
            if weather_data["precip"] > 0 and weather_data["precip"]<2.6:
                await update.message.reply_text(f'Slow and light rainfall, usually does not interfere with outdoor activities much.')
            elif weather_data["precip"] >= 2.6 and weather_data["precip"]<7.7:
                await update.message.reply_text(f'Noticeably heavier rain.{BOT_NAME} suggest you should bring an umbrella')
            elif weather_data["precip"] >= 7.7 and weather_data["precip"]<51:
                await update.message.reply_text(f'Strong rain and reduced visibility.{BOT_NAME} suggest you should bring an umbrella and be carefully for driving.')    
            elif weather_data["precip"] >= 51:
                await update.message.reply_text(f'Extremely intense rainfall.{BOT_NAME} suggest you should stay indoors until the rain lightens up.')    
            
            # UV
            if weather_data["uv"]>=3 and weather_data["uv"]<6:
                await update.message.reply_text(f'The UV index is moderate today. {BOT_NAME} recommend to wear sunscreen, a hat, or sunglasses, and try to avoid staying in direct sunlight for extended periods.')
            elif weather_data["uv"]>=6 and weather_data["uv"]<8:
                await update.message.reply_text(f'The UV index is high today. {BOT_NAME} recommend you to apply sunscreen (SPF 30+), stay in the shade when possible, and avoid the intense midday sun.')
            elif weather_data["uv"]>=8 and weather_data["uv"]<11:
                await update.message.reply_text(f"The UV index is very high! {BOT_NAME} recommend you to use sunscreen with SPF 50+ and wear protective clothing. It's best to avoid going out during midday.")
            elif weather_data["uv"]>=11:
                await update.message.reply_text(f"Try to limit outdoor activities as much as possible.")
            else:
                pass
        else:
            await update.message.reply_text("Sorry something went wrong.CitronTempsBot would try to fix it.")


    match_1 = re.match(r'forecast_(\w+)', user_input)
    if match_1:
        await update.message.reply_text(f"{BOT_NAME} is loading from the heart...")
        city = match_1.group(1)  # 抓取城市名稱
        print(city)

        result,forcast_data = get_forcast_data(city)
        if result:

            # temps
            temp_list= temps_list_procees(forcast_data)
            await update.message.reply_text(f'In {len(forcast_data)} hours the highest temperature is {max(temp_list)} degrees, and the lowest temperature is {min(temp_list)} degrees.')

            # rain
            rain_list = rain_process(forcast_data)
            if len(rain_list) > 0:
                start = rain_list[0]["timestamp_local"][-8:-6]
                await update.message.reply_text(f'It will rain in at {start}. {BOT_NAME} suggest you bring an umbrella : )')

            #wind
            wind_list = wind_process(forcast_data)
            if len(wind_list) > 0:
                await update.message.reply_text(f"The wind is strong, so remember to wear an extra jacket and stay warm!")
        else:
            await update.message.reply_text("Sorry something went wrong.CitronTempsBot would try to fix it.")
    else:
        await update.message.reply_text("請使用 'forcast_城市名' 的格式查詢今日天氣預報，例如: 'forcast_Taipei'")


async def start_weahter(update: Update, context: CallbackContext) -> None:
    global weather_enabled

    if user_city is None:
        await update.message.reply_text(f'Please set your city with "/setcity [CITYNAME]"')
        return
    
    if not weather_enabled:
        weather_enabled = True

        await update.message.reply_text(f"{BOT_NAME} set weather checker at 7:30.")
        
        schedule.every().day.at("15:54").do(send_rain_alert)

        scheduler_thread = Thread(target=run_schedule)
        scheduler_thread.start()
    else:
        await update.message.reply_text(f'The weather checker is enabled.')
async def stop_weather(update: Update, context: CallbackContext) -> None:
    global weather_notifications_enabled
    if weather_enabled:
        weather_enabled = False
        await update.message.reply_text('The weather checker is disabled.')
    else:
        await update.message.reply_text('The weather checker is still disabled.')
def run_schedule():
    global weather_enabled
    while weather_notifications_enabled:
        schedule.run_pending()
        time.sleep(1)



async def send_rain_alert():
    await update.message.reply_text(f'{BOT_NAME} 查詢天氣中')
    if user_city:
        result,forcast_data = get_forcast_data(city)
        if result:
            rain_list = rain_process(forcast_data)
            if len(rain_list) > 0:
                start = rain_list[0]["timestamp_local"][-8:-6]
                await update.message.reply_text(f'It will rain in at {start}. {BOT_NAME} suggest you bring an umbrella : )')            

async def set_city(update: Update, context: CallbackContext) -> None:
    global user_city
    if len(context.args) > 0:
        user_city = ' '.join(context.args)
        await update.message.reply_text(f'The user_city is set as {user_city}')
    else:
        await update.message.reply_text('Please input /setcity [CityName]。')

# async def other_command(update: Update, context: ContextTypes.DEFAULT_TYPE):  
#     # 定义一些行为
#     # 省略
#     pass
#     await context.bot.send_message(chat_id=update.effective_chat.id,  
#                                    text=f"需要幫忙請按/help")  

