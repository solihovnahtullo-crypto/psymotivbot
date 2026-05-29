import os,logging
from dotenv import load_dotenv
from groq import Groq
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
load_dotenv()
logging.basicConfig(format="%(asctime)s-%(message)s",level=logging.INFO)
logger=logging.getLogger(__name__)
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
client=Groq(api_key=GROQ_API_KEY)
PROMPT="Tu psixologi Markazi Motiv hasti. Nomatat Motiv. Hamesa tojiki gap zan. Avval ehsos purs. Yakto savol bipurs. Kutoh javob deh."
sessions={}
def hist(u):return sessions.setdefault(u,[])
def add(u,r,t):
 hist(u).append({"role":r,"content":t})
 if len(sessions[u])>20:sessions[u]=sessions[u][-20:]
def ask(u,t):
 add(u,"user",t)
 r=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[{"role":"system","content":PROMPT}]+hist(u),max_tokens=500)
 rep=r.choices[0].message.content
 add(u,"assistant",rep)
 return rep
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
 u=update.effective_user.id
 sessions[u]=[]
 msg="Salom! Man Motiv hastam.\n\nImruz chi ba dilat dori?"
 add(u,"assistant",msg)
 await update.message.reply_text(msg)
async def handle(update:Update,context:ContextTypes.DEFAULT_TYPE):
 u=update.effective_user.id
 await context.bot.send_chat_action(chat_id=update.effective_chat.id,action="typing")
 try:await update.message.reply_text(ask(u,update.message.text))
 except Exception as e:
  logger.error(e)
  await update.message.reply_text("Xato ruy dod. /start navis.")
def main():
 app=Application.builder().token(TELEGRAM_TOKEN).build()
 app.add_handler(CommandHandler("start",start))
 app.add_handler(MessageHandler(filters.TEXT&~filters.COMMAND,handle))
 logger.info("Bot started!")
 app.run_polling()
if __name__=="__main__":main()
