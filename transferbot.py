#!/usr/bin/env python
# coding: utf-8
# transfer.sh telegram bot
# Version:  0.1
# Author:   Jhonata Poma - jhonata.poma@gmail.com

""" Send any telegram-supported media to this bot and it will be uploaded over transfer.sh
"""

import logging, re, requests, os
from telegram.ext   import Updater, CommandHandler, MessageHandler
from telegram.ext   import Filters, CallbackQueryHandler

#   GLOBALZ
VERSION     = '0.1'
FILES_POOL  = '/tmp/'
SIZE_LIMIT  = 20971520

#   LOGGER
logging.basicConfig (format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger (__name__)

try:
    TOKEN   = open ('conf/token.conf', 'r').read ().replace ("\n", "")
except Exception, e:
    logger.error ("Could not find 'conf/token.conf'.")
    exit (1) 

def remove (filename):
    """ Removes the file after transfer.
    """
    try:
        os.remove(FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Removed %s", filename)

def transfer (filename):
    """ Sends filename then calls remove to delete it. Returns transfer.sh file's url.
    """
    upload_url = "https://transfer.sh/" + filename
    try:
        req = requests.put (url=upload_url, data=open (FILES_POOL + filename, "r"))
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Transfered %s", filename)
    remove (filename)
    try:
        return (req.text.strip ())
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return

#   HANDLERS
def cmd_start (bot, update):
    """ Send a message when the command /start is issued.
    """
    update.message.reply_text ('Transferbot ' + VERSION)
    update.message.reply_text ('Just send a picture, video, song or any other of telegram-supported ' \
                               'media to upload it over transfer.sh')

def cmd_help (bot, update):
    """ Send a message when the command /help is issued.
    """
    update.message.reply_text ('Just send a picture, video, song or any other of telegram-supported ' \
                               'media to upload it over transfer.sh')

def cmd_unknown (bot, update):
    """ Send a message if the command is not defined.
    """
    update.message.reply_text ('Command not found. Type /help.')

def cmd_error (bot, update, error):
    """ Log Errors caused by updates.
    """
    logger.warning ('Update "%s" caused error "%s"', update, error)

#   ATTACHMENT's FALLBACKS
def fbk_document (bot, update):
    """ Get document, then transfer it.
    """
    #   Check if exceeds the 20mbs limit 
    if (update.message.document.file_size > SIZE_LIMIT):
        update.message.reply_text ("Your file is too big! Size limited to 20mb by Telegram Bot API")
        logger.warn ("Rejected file, size was %s" %(update.message.document.file_size))
        return
    user        = update.message.from_user
    document    = bot.get_file (update.message.document.file_id)
    try:
        document.download (FILES_POOL + update.message.document.file_name)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got document from %s: %s", user.first_name, update.message.document.file_name)
    update.message.reply_text ('Your transfer.sh link: ' + transfer (update.message.document.file_name))

def fbk_audio (bot, update):
    """ Get audio, then transfer it.
    """
    #   Check if exceeds the 20mbs limit 
    if (update.message.audio.file_size > SIZE_LIMIT):
        update.message.reply_text ("Your file is too big! Size limited to 20mb by Telegram Bot API")
        logger.warn ("Rejected file, size was %s" %(update.message.audio.file_size))
        return
    FIRST_EMT   = 0
    ext         = re.findall (r'/(\w+)', update.message.audio.mime_type)[FIRST_EMT]
    filename    = update.message.audio.file_id + '.' + ext
    user        = update.message.from_user
    document    = bot.get_file (update.message.audio.file_id)
    try:
        document.download (FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got audio from %s: %s", user.first_name, filename)
    update.message.reply_text ('Your transfer.sh link: ' + transfer (filename))

def fbk_voice (bot, update):
    """ Get audio, then transfer it.
    """
    #   Check if exceeds the 20mbs limit 
    if (update.message.voice.file_size > SIZE_LIMIT):
        update.message.reply_text ("Your file is too big! Size limited to 20mb by Telegram Bot API")
        logger.warn ("Rejected file, size was %s" %(update.message.voice.file_size))
        return
    FIRST_EMT   = 0
    ext         = re.findall (r'/(\w+)', update.message.voice.mime_type)[FIRST_EMT]
    filename    = update.message.voice.file_id + '.' + ext
    user        = update.message.from_user
    document    = bot.get_file (update.message.voice.file_id)
    try:
        document.download (FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got voice from %s: %s", user.first_name, filename)
    update.message.reply_text ('Your transfer.sh link: ' + transfer (filename))

def fbk_video (bot, update):
    """ Get video, then transfer it.
    """
    #   Check if exceeds the 20mbs limit 
    if (update.message.video.file_size > SIZE_LIMIT):
        update.message.reply_text ("Your file is too big! Size limited to 20mb by Telegram Bot API")
        logger.warn ("Rejected file, size was %s" %(update.message.video.file_size))
        return
    FIRST_EMT   = 0
    ext         = re.findall (r'/(\w+)', update.message.video.mime_type)[FIRST_EMT]
    filename    = update.message.video.file_id + '.' + ext
    user        = update.message.from_user
    document    = bot.get_file (update.message.video.file_id)
    try:
        document.download (FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got video from %s: %s", user.first_name, filename)
    update.message.reply_text ('Your transfer.sh link: ' + transfer (filename))

def fbk_photo (bot, update):
    """ Get chat photo, the biggest from the list
    """
    #   Check if exceeds the 20mbs limit 
    if (update.message.photo.file_size > SIZE_LIMIT):
        update.message.reply_text ("Your file is too big! Size limited to 20mb by Telegram Bot API")
        logger.warn ("Rejected file, size was %s" %(update.message.photo.file_size))
        return
    pic_index   = len (update.message.photo) - 1 
    filename    = update.message.photo[pic_index].file_id + '.jpg'
    user        = update.message.from_user
    document    = bot.get_file (update.message.photo[pic_index].file_id)
    try:
        document.download (FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got photo from %s: %s", user.first_name, filename)
    update.message.reply_text ('Your transfer.sh link: ' + transfer (filename))

#   MAIN
def main ():
    """ Start the bot.
    """
    #   Create the EventHandler and pass it your bot's token.
    updater = Updater (TOKEN)

    #   Get the dispatcher to register handlers
    dp = updater.dispatcher

    #   On different commands - answer in Telegram
    dp.add_handler (CommandHandler ("start",        cmd_start))
    dp.add_handler (CommandHandler ("help",         cmd_help))

    #   On unknown command, put some help text
    dp.add_handler (MessageHandler (Filters.command,    cmd_unknown))
    
    #   We don't need text interactions, give /help instead 
    dp.add_handler (MessageHandler (Filters.text,       cmd_help))

    #   Add stuff to handle
    dp.add_handler (MessageHandler (Filters.photo,      fbk_photo))
    dp.add_handler (MessageHandler (Filters.audio,      fbk_audio))
    dp.add_handler (MessageHandler (Filters.voice,      fbk_voice))
    dp.add_handler (MessageHandler (Filters.video,      fbk_video))
    dp.add_handler (MessageHandler (Filters.document,   fbk_document))

    #   log all errors
    dp.add_error_handler (cmd_error)

    #   Start the Bot
    updater.start_polling ()
    logger.info ('Kicking')

    #   Loop until SIGNALS
    updater.idle ()

if __name__ == '__main__':
    main ()
