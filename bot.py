def main():
 app=Application.builder().token(TELEGRAM_TOKEN).build()
 app.add_handler(CommandHandler("start",start))
 app.add_handler(MessageHandler(filters.TEXT&~filters.COMMAND,handle))
 logger.info("Bot started!")
 app.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__=="__main__":main()
