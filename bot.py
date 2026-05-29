import os,logging
from google import genai
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,ConversationHandler
logging.basicConfig(format="%(asctime)s-%(message)s",level=logging.INFO)
logger=logging.getLogger(name)
TELEGRAM_TOKEN=os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")
client=genai.Client(api_key=GEMINI_API_KEY)
PROMPTS={
"tj":"Ту психологи Маркази Мотив ҳастӣ. Номат Мотив. ҲАМЕША ба забони тоҷикӣ гап зан. Аввал эҳсос пурс. Якто савол бипурс. Кӯтоҳ ҷавоб деҳ.",
"ru":"Ты психолог Центра Мотив. Тебя зовут Мотив. ВСЕГДА говори только на русском языке. Сначала спроси про чувства. Задавай один вопрос. Отвечай коротко.",
"uz":"Sen Motiv psixologiya markazining psixologisan. Isming Motiv. DOIMO o'zbek tilida gapir. Avval his-tuyg'ularni so'ra. Bitta savol ber. Qisqa javob ber."
}
LANG,CHAT=0,1
sessions={}
def hist(u):return sessions.setdefault(u,{"lang":"tj","msgs":[]})
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
 kb=[["\U0001f1f9\U0001f1ef Тоҷикӣ","\U0001f1f7\U0001f1fa Русский","\U0001f1fa\U0001f1ff O'zbekcha"]]
 await update.message.reply_text("Забонро интихоб кунед / Выберите язык / Tilni tanlang:",reply_markup=ReplyKeyboardMarkup(kb,one_time_keyboard=True,resize_keyboard=True))
 return LANG
async def set_lang(update:Update,context:ContextTypes.DEFAULT_TYPE):
 txt=update.message.text
 u=update.effective_user.id
 if "Тоҷикӣ" in txt:lang="tj";msg="Салом! Ман Мотив ҳастам.\n\nИмрӯз чӣ ба дилат дорӣ?"
 elif "Русский" in txt:lang="ru";msg="Привет! Я Мотив.\n\nКак ты себя чувствуешь сегодня?"
 else:lang="uz";msg="Salom! Men Motivman.\n\nBugun qanday his qilyapsiz?"
 sessions[u]={"lang":lang,"msgs":[{"role":"model","parts":[{"text":msg}]}]}
 await update.message.reply_text(msg,reply_markup=ReplyKeyboardRemove())
 return CHAT
async def handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
 u=update.effective_user.id
 data=hist(u)
 data["msgs"].append({"role":"user","parts":[{"text":update.message.text}]})
 if len(data["msgs"])>20:data["msgs"]=data["msgs"][-20:]
 await context.bot.send_chat_action(chat_id=update.effective_chat.id,action="typing")
 try:
  r=client.models.generate_content(model="gemini-2.0-flash",contents=data["msgs"],config=genai.types.GenerateContentConfig(system_instruction=PROMPTS[data["lang"]]))
  rep=r.text
  data["msgs"].append({"role":"model","parts":[{"text":rep}]})
  await update.message.reply_text(rep)
 except Exception as e:
  logger.error(e)
  await update.message.reply_text("Xato. /start yozing.")
 return CHAT
conv=ConversationHandler(entry_points=[CommandHandler("start",start)],states={LANG:[MessageHandler(filters.TEXT&~filters.COMMAND,set_lang)],CHAT:[MessageHandler(filters.TEXT&~filters.COMMAND,handle)]},fallbacks=[CommandHandler("start",start)])
app=Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(conv)
logger.info("Bot started!")
app.run_polling(drop_pending_updates=True)
