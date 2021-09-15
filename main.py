from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, JobQueue, CallbackContext
from datetime import time


from model.User import User
from model.UserRule import UserRule
from persistance.ControllerPersistance import get_state_data, get_all_users, save_state_data

TOKEN = open('token.txt').read().strip()


def help(update, context):
    s = "/definerule <idrule> <hour> <minute> <msg> Define a rule that sends a <msg> at <hour>:<minute> every day.\n" \
        "/listrules List the defined rules."

    context.bot.send_message(chat_id=update.message.chat_id, text=s)


def chat_user_run(chatid: str, rule: UserRule):
    def callback_minute(context: CallbackContext):
        print("activated job")
        context.bot.send_message(chat_id=chatid, text=rule.msg)
    return callback_minute


def definerule(update, context):
    job_queue = context.job_queue
    id_chat = update.message.chat_id
    user = get_state_data(id_chat)
    rules = update.message.text.split()
    if len(rules) < 5:
        context.bot.send_message(chat_id=id_chat, text="Error, you must specify <idrule> <hour> <minute> <msg>")
    elif not rules[2].isnumeric() or not rules[3].isnumeric():
        context.bot.send_message(chat_id=id_chat, text="Error, you must specify numeric hour and minute")
    else:
        hour = int(rules[2])
        minute = int(rules[3])
        idrule = rules[1]
        msg = rules[4]
        if user.exists_rule(idrule):
            context.bot.send_message(chat_id=id_chat)
        rule = user.add_rule(hour, minute, msg, idrule)
        job_queue.run_daily(chat_user_run(user.chat_id, rule), time = time(hour = rule.hour-2, minute = rule.minute, second = 00), days=(0,1,2,3,4,5,6))
        save_state_data(user)
        context.bot.send_message(chat_id=id_chat, text="Rule created correctly ;)")

def listrules(update, context):
    id_chat = update.message.chat_id
    user = get_state_data(id_chat)
    rules = user.get_str_rules()
    context.bot.send_message(chat_id=id_chat, text='Your defined rules:\n'+rules)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

job = updater.job_queue
users = get_all_users()
for user in users:
    for rule in user.rules:
        job.run_daily(chat_user_run(user.chat_id, rule), time=time(hour=rule.hour-2, minute=rule.minute, second=00), days=(0,1,2,3,4,5,6))


dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('definerule', definerule, pass_job_queue=True))
dispatcher.add_handler(CommandHandler('listrules', listrules))

updater.start_polling()
