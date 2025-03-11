import os
   from telegram import Bot
   from telegram.constants import ParseMode

   # Get secrets from environment variables
   TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
   TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

   # Initialize the bot
   bot = Bot(token=TELEGRAM_TOKEN)

   # Define the file and caption
   file_path = "test_upload.zip"
   caption = """
   #ALPKernel #Alioth
   For MIUI/HyperOS, add -miui to the ZIP name; for the 4500 variant, add -bat. Example: ALPKernel-miui-bat-dtb.zip.
   Test Upload: ALP Kernel AOSP Build for {codename} - {build_date}
   """.format(
       codename=os.getenv("INPUT_CODENAME"),
       build_date=os.getenv("BUILD_DATE")
   )

   # Upload the file with caption
   with open(file_path, "rb") as file:
       bot.send_document(
           chat_id=TELEGRAM_CHAT_ID,
           document=file,
           caption=caption,
           parse_mode=ParseMode.MARKDOWN
       )

   print("File uploaded successfully with full caption!")
