import os
from telethon import TelegramClient

# Telegram API credentials
api_id = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'
bot_token = os.getenv('TELEGRAM_TOKEN')

# Get chat IDs from environment variables
chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))  # Required
chat_id_2 = os.getenv('TELEGRAM_CHAT_ID_2')  # Optional

# Convert chat_id_2 to int only if it's not None
if chat_id_2 is not None:
    chat_id_2 = int(chat_id_2)

# Initialize the Telegram client
client = TelegramClient('github_bot', api_id, api_hash).start(bot_token=bot_token)

async def send_notification(message, file_path=None, thumbnail_path=None, is_success=False):
    try:
        if file_path:
            # Send file to Chat 1 with caption
            await client.send_file(chat_id, file_path, caption=message, thumb=thumbnail_path, parse_mode='markdown')
            # Send file to Chat 2 only if it's a success notification and chat_id_2 is set
            if is_success and chat_id_2 is not None:
                await client.send_file(chat_id_2, file_path, caption=message, thumb=thumbnail_path, parse_mode='markdown')
        else:
            # Send message to Chat 1 only (no file, no Chat 2 notification)
            await client.send_message(chat_id, message, parse_mode='markdown')
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
    workflow_file = os.getenv('WORKFLOW_FILE')  # Get workflow file name from environment
    build_tag = os.getenv('BUILD_TAG')  # Get build tag from environment

    # Determine build type
    build_type = "Release Build" if upload_to_release == 'true' else "CI Build"

    # Hidden markdown link for logo
    hidden_logo = "[‌](https://raw.githubusercontent.com/AlirezaParsi/pocof3/refs/heads/base/logo.jpg)"

    # Construct the notification message based on build status
    if build_status == 'start':
        message = (
            f"{hidden_logo}🚀 **Kernel Build Started**\n"
            f"📦 **Build Title**: {build_title}\n"
            f"📱 **Device Codename**: {codename}\n"
            f"🏷️ **Build Type**: {build_type}\n"
            f"🗃️ **Workflow File**: {workflow_file}\n"
            f"🔧 [View Workflow Run]({workflow_run_url})"
        )
    elif build_status == 'success':
        message = (
            f"{hidden_logo}✅ **Kernel Build Succeeded**\n"
            f"📦 **Build Title**: {build_title}\n"
            f"📱 **Device Codename**: {codename}\n"
            f"🏷️ **Build Type**: {build_type}\n"
            f"⏱️ **Elapsed Time**: {elapsed_time} seconds\n"
            f"📄 **File**: {zip_name}\n"
            f"🗃️ **Workflow File**: {workflow_file}\n"
            f"[Flashing Guide](https://t.me/ALPkernel/128)\n"
            f"#ALPKernel #alioth {build_tag}"
        )
        if download_link:
            message += f"\n📥 **Download Link**: [Release {build_title}]({download_link})"
    elif build_status == 'failure':
        message = (
            f"{hidden_logo}❌ **Kernel Build Failed**\n"
            f"📦 **Build Title**: {build_title}\n"
            f"📱 **Device Codename**: {codename}\n"
            f"🏷️ **Build Type**: {build_type}\n"
            f"⏱️ **Elapsed Time**: {elapsed_time} seconds\n"
            f"🗃️ **Workflow File**: {workflow_file}\n"
            f"🔧 [View Workflow Run]({workflow_run_url})"
        )
    elif build_status == 'canceled':
        message = (
            f"{hidden_logo}🚫 **Kernel Build Canceled**\n"
            f"📦 **Build Title**: {build_title}\n"
            f"📱 **Device Codename**: {codename}\n"
            f"🏷️ **Build Type**: {build_type}\n"
            f"🔧 [View Workflow Run]({workflow_run_url})\n"
            f"🗃️ **Workflow File**: {workflow_file}\n"
            f"👤 **Canceled by**: {github_actor}"
        )

    file_path = os.getenv('FILE_PATH')
    thumbnail_path = os.getenv('THUMBNAIL_PATH')

    # Determine if this is a success notification with a file
    is_success = build_status == 'success' and file_path is not None

    # Send the notification
    await send_notification(message, file_path, thumbnail_path, is_success)

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
