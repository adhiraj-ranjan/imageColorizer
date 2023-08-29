from telegram.ext import Application, CommandHandler, MessageHandler, filters
import colorize
import os

TOKEN = os.environ['TOKEN']
CHANNEL_USERNAME = "@truebotsc"
IMAGE_PATH = "temps/image.jpg"


async def start_command(update, context):
    await update.message.reply_text(
        "Hello! Send Black and White Image, you want to colorize.")


async def handle_image(update, context):
    user_member = await context.bot.get_chat_member(
        chat_id=CHANNEL_USERNAME, user_id=update.message.from_user.id)

    if user_member.status == "member" or user_member.status == "administrator" or user_member.status == "creator":
        pass
    else:
        await update.message.reply_text(
            f"Join TrueBots [💀] {CHANNEL_USERNAME} to use the bot and to Explore more useful bots"
        )
        return

    try:
        await update.message.reply_text("Processing your image")
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

    app.run_polling()
