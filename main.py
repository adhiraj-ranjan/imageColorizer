from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import colorize
import os
from subprocess import Popen

Popen(['python', '-m', 'http.server'])

TOKEN= os.environ['token']

IMAGE_PATH = "temps/image.jpg"
async def start_command(update, context):
    await update.message.reply_text("Hello! Send Black and White Image, you want to colorize.")

async def handle_image(update, context):
    try:
        photo_file_id = update.message.photo[-1].file_id
        # Download the photo and save it
        photo = await context.bot.get_file(photo_file_id)
        await photo.download_to_drive(IMAGE_PATH)
        colorize.update(IMAGE_PATH)
    
        with open(colorize.TEMP_IMAGE_PATH, 'rb') as image_file:
            await update.message.reply_photo(photo=image_file)
    except Exception as e:
        print(e)
        await update.message.reply_text(str(e))
    
# Log errors
async def error(update, context):
    print(f'Update {update} caused error {context.error}')

# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    # Log all errors
    app.add_error_handler(error)

    app.run_polling(poll_interval=5)
