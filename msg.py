"""
A file that contains all the messaging functionalities of Kiltisbot.
"""

import settings

sent_messages = {}

with open("ohje.txt", "r") as f:
    manual = f.read()

with open("ohje_en.txt", "r") as f:
    manual_en = f.read()

def ohje(bot, update):
    """Send help"""

    bot.send_message(update.effective_chat.id, manual, parse_mode = "HTML")

def ohje_in_english(bot, update):
    """Send help"""

    bot.send_message(update.effective_chat.id, manual_en, parse_mode = "HTML")

def robust_send_message(bot, msg, to, reply_id):
    """A robust method for forwarding different types of messages anonymously"""

    sent = None

    if msg.text:
        sent = bot.send_message(to, msg.text, reply_to_message_id = reply_id)
    elif msg.sticker:
        sent = bot.send_sticker(to, msg.sticker.file_id, reply_to_message_id = reply_id)
    elif msg.photo:
        sent = bot.send_photo(to, msg.photo[0].file_id, msg.caption, reply_to_message_id = reply_id)
    elif msg.video:
        sent = bot.send_video(to, msg.video.file_id, msg.caption, reply_to_message_id = reply_id)
    elif msg.video_note:
        sent = bot.send_video_note(to, msg.video_note.file_id, reply_to_message_id = reply_id)
    elif msg.document:
        sent = bot.send_document(to, msg.document.file_id, reply_to_message_id = reply_id)
    elif msg.voice:
        sent = bot.send_voice(to, msg.voice.file_id, reply_to_message_id = reply_id)
    elif msg.audio:
        sent = bot.send_audio(to, msg.audio.file_id, reply_to_message_id = reply_id)
    elif msg.location:
        sent = bot.send_location(to, location = msg.location, reply_to_message_id = reply_id)
    else:
        bot.send_message(msg.chat.id, "Tiedostomuoto ei ole tuettu :(")

    return sent

def send_from_private(bot, update):
    """Forward a private message sent for the bot to the receiving chat anonumously"""

    msg = update.effective_message

    for i in settings.secrets["chats"]:
        if settings.secrets["chats"][i]["messages"]:
            sent_message = robust_send_message(bot, msg, int(i), None)
            sent_messages[sent_message.message_id] = (msg.chat.id, msg.message_id)

def reply(bot, update):
    """Forward reply from receiving chat back to the original sender"""

    id = update.effective_message.reply_to_message.message_id
    if id in sent_messages:
        org = sent_messages[id]
        robust_send_message(bot, update.effective_message, org[0], org[1])
