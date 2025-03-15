import os
from telethon import TelegramClient

# Telegram API credentials
api_id = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'
bot_token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
chat_id_2 = os.getenv('TELEGRAM_CHAT_ID_2')

# Initialize the Telegram client
client = TelegramClient('github_bot', api_id, api_hash).start(bot_token=bot_token)

async def send_notification(message, file_path=None, thumbnail_path=None):
    try:
        if file_path:
            await client.send_file(chat_id, file_path, caption=message, thumb=thumbnail_path)
            await client.send_file(chat_id_2, file_path, caption=message, thumb=thumbnail_path)
        else:
            await client.send_message(chat_id, message)
            await client.send_message(chat_id_2, message)
    except Exception as e:
        print(f"Failed to send notification: {e}")

async def main():
    # Read inputs from environment variables
    build_status = os.getenv('BUILD_STATUS')
    build_title = os.getenv('BUILD_TITLE')
    codename = os.getenv('CODENAME')
    elapsed_time = os.getenv('ELAPSED_TIME')
    zip_name = os.getenv('ZIP_NAME')
    workflow_run_url = os.getenv('WORKFLOW_RUN_URL')
    upload_to_release = os.getenv('UPLOAD_TO_RELEASE')
    download_link = os.getenv('DOWNLOAD_LINK')
    github_actor = os.getenv('GITHUB_ACTOR')
    build_tag = os.getenv('BUILD_TAG')

    # Determine build type
    build_type = "Release Build" if upload_to_release == 'true' else "CI Build"

    # Construct the notification message based on build status
    if build_status == 'start':
        message = (
            f"🚀 Kernel Build Started\n"
            f"📦 Build Title: {build_title}\n"
            f"📱 Device Codename: {codename}\n"
            f"🏷️ Build Type: {build_type}\n"
            f"🔧 View Workflow Run: {workflow_run_url}"
        )
    elif build_status == 'success':
        message = (
            f"✅ Kernel Build Succeeded\n"
            f"📦 Build Title: {build_title}\n"
            f"📱 Device Codename: {codename}\n"
            f"🏷️ Build Type: {build_type}\n"
            f"⏱️ Elapsed Time: {elapsed_time} seconds\n"
            f"📄 File: {zip_name}\n"
            f"{build_tag}"
        )
        if download_link:
            message += f"\n📥 Download Link: {download_link}"
    elif build_status == 'failure':
        message = (
            f"❌ Kernel Build Failed\n"
            f"📦 Build Title: {build_title}\n"
            f"📱 Device Codename: {codename}\n"
            f"🏷️ Build Type: {build_type}\n"
            f"⏱️ Elapsed Time: {elapsed_time} seconds\n"
            f"🔧 View Workflow Run: {workflow_run_url}"
        )
    elif build_status == 'canceled':
        message = (
            f"🚫 Kernel Build Canceled\n"
            f"📦 Build Title: {build_title}\n"
            f"📱 Device Codename: {codename}\n"
            f"🏷️ Build Type: {build_type}\n"
            f"🔧 View Workflow Run: {workflow_run_url}\n"
            f"👤 Canceled by: {github_actor}"
        )

    file_path = os.getenv('FILE_PATH')
    thumbnail_path = os.getenv('THUMBNAIL_PATH')

    await send_notification(message, file_path, thumbnail_path)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
