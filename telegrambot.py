import telegram
from telegram import ChatAction,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler,MessageHandler,Filters,PicklePersistence,CallbackQueryHandler,ConversationHandler
from telegram.ext.dispatcher import run_async
import logging
import os
import requests
apikeys=range(1)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@run_async
def start(update,context):
	name=update.message.chat.first_name
	update.message.reply_text("Hello "+name+" 😃\nWelcome to GPlinks.in shortener bot ,\nYou can use your GPlink.in account using this bot.\nTo use this bot first login by using command /login")

@run_async
def login(update,context):
	try:
		apikey=context.user_data['apikey']
		if len(apikey)==0:
			update.message.reply_text("Send your api token to login")
			return apikeys
		else:
			update.message.reply_text("You are already Logged in \nTo logout use command /logout")
		
		
	except KeyError:
		update.message.reply_text("Send your api token to login")
		return apikeys
	
	
@run_async
def logout(update,context):
	try:
		apikey=context.user_data['apikey']
		apikey.clear()
		update.message.reply_text("Logged out successfully")
	except KeyError:
		update.message.reply_text("You are not logged in to logout")
		return ConversationHandler.END
	
@run_async
def apikey (update,context):
	api=update.message.text
	if len(api)==40:
		try:
			apikey=context.user_data['apikey']
		except KeyError:
			apikey= context.user_data['apikey'] = []
		apikey.append(api)
		update.message.reply_text("You have Logged in successfully 😃 \nNow send your long link that you want to short ")
		return ConversationHandler.END
	else:
		update.message.reply_text("‼️You entered incorrect api token‼️\nEnter correct api token to continue to login")


@run_async
def link(update,context):
	try:
		apikey=context.user_data['apikey']
		if len(apikey)==0:
			update.message.reply_text("Login first by command /login and then send your long link")
		else:
			link=update.message.text
			apikey=context.user_data['apikey']
			api=apikey[0]
			shortlink=shortlinks(api,link)
			update.message.reply_text("Your Short link is 👇\n"+shortlink)
				
			
	except KeyError:
		update.message.reply_text("Login first by command /login and then send your long link")
	
	

def shortlinks(api,link):
	response = requests.get('https://gplinks.in/api/?api='+api+'&url='+link)
	print(response)
	data=response.json()
	shortlink=data['shortenedUrl']
	return shortlink
	
def cancel(update, context):
	update.message.reply_text('Current Operation cancelled')
	return ConversationHandler.END
	
	
persistence=PicklePersistence('data')
def main():
    token=os.environ.get("BOT_TOKEN", "")
    updater = Updater(token,use_context=True, persistence=persistence)
    dp=updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login)],

        states={
            apikeys: [MessageHandler(Filters.text, apikey)],

        },

        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('logout',logout))
    dp.add_handler(CallbackQueryHandler (button))
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text,link))
    updater.start_polling()
    updater.idle()
 
	
if __name__=="__main__":
	main()



