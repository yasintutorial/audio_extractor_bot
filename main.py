# Import libraries
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import os, subprocess


# Send welcome message to new users
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to my audio extractor bot.')


# Download video , extract audio and send audio
def audio_extractor(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user['id']
    # Download video
    input_name = update.message.video.file_name
    input_ext = input_name.split('.')[-1]
    file_id = update.message.video.file_id
    file = context.bot.getFile(file_id)
    input_path = f'./temp/{file_id}.{input_ext}'
    output_path = f'./temp/{file_id}.mp3'
    file.download(input_path)
    # Extract audio
    command = ["ffmpeg", "-i", input_path, output_path]
    subprocess.call(command)
    # Send audio
    context.bot.send_audio(chat_id=user_id, audio=open(output_path, 'rb'))
    # Delete files
    os.remove(input_path)
    os.remove(output_path)


if __name__ == '__main__':
    updater = Updater(token='TOKEN',
                      request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.video, audio_extractor))

    updater.start_polling()
    updater.idle()
