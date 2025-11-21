import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from database import Database
from translations import get_text

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()


def get_lang(chat_id: int) -> str:
    """Get language preference for a chat"""
    return db.get_language(chat_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat = update.effective_chat
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(
            get_text(lang, "start_private", name=user.first_name)
        )
    else:
        await update.message.reply_text(
            get_text(lang, "start_group")
        )


async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set up Secret Santa in a group (admin only)."""
    chat = update.effective_chat
    user = update.effective_user
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(get_text(lang, "setup_private_only"))
        return

    # Check if user is admin
    member = await chat.get_member(user.id)
    if member.status not in ["creator", "administrator"]:
        await update.message.reply_text(get_text(lang, "setup_admin_only"))
        return

    # Create group in database
    if db.create_group(chat.id, user.id):
        # Try to get invite link (requires bot to be admin with invite link permission)
        try:
            invite_link = await chat.export_invite_link()
            message = get_text(lang, "setup_success_with_link", admin=user.first_name, link=invite_link)
        except Exception as e:
            logger.warning(f"Could not export invite link: {e}")
            message = get_text(lang, "setup_success_no_link", admin=user.first_name)

        message += get_text(lang, "setup_next_steps")
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(get_text(lang, "setup_error"))


async def set_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set the event date for Secret Santa."""
    chat = update.effective_chat
    user = update.effective_user
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(get_text(lang, "setdate_group_only"))
        return

    # Check if user is admin
    member = await chat.get_member(user.id)
    if member.status not in ["creator", "administrator"]:
        await update.message.reply_text(get_text(lang, "setdate_admin_only"))
        return

    # Check if group exists
    group = db.get_group(chat.id)
    if not group:
        await update.message.reply_text(get_text(lang, "setdate_setup_first"))
        return

    # Parse date
    if not context.args:
        await update.message.reply_text(get_text(lang, "setdate_usage"))
        return

    date_str = context.args[0]
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        if db.update_group_settings(chat.id, event_date=date_str):
            await update.message.reply_text(get_text(lang, "setdate_success", date=date_str))
        else:
            await update.message.reply_text(get_text(lang, "setdate_error"))
    except ValueError:
        await update.message.reply_text(get_text(lang, "setdate_invalid_format"))


async def set_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set the maximum gift price."""
    chat = update.effective_chat
    user = update.effective_user
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(get_text(lang, "setprice_group_only"))
        return

    # Check if user is admin
    member = await chat.get_member(user.id)
    if member.status not in ["creator", "administrator"]:
        await update.message.reply_text(get_text(lang, "setprice_admin_only"))
        return

    # Check if group exists
    group = db.get_group(chat.id)
    if not group:
        await update.message.reply_text(get_text(lang, "setprice_setup_first"))
        return

    # Parse price
    if not context.args:
        await update.message.reply_text(get_text(lang, "setprice_usage"))
        return

    try:
        price = float(context.args[0])
        if price <= 0:
            await update.message.reply_text(get_text(lang, "setprice_positive"))
            return

        if db.update_group_settings(chat.id, max_price=price):
            await update.message.reply_text(get_text(lang, "setprice_success", price=price))
        else:
            await update.message.reply_text(get_text(lang, "setprice_error"))
    except ValueError:
        await update.message.reply_text(get_text(lang, "setprice_invalid"))


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Join the Secret Santa in this group."""
    chat = update.effective_chat
    user = update.effective_user
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(get_text(lang, "join_group_only"))
        return

    # Check if group exists
    group = db.get_group(chat.id)
    if not group:
        await update.message.reply_text(get_text(lang, "join_setup_first"))
        return

    # Check if already assigned
    if db.is_group_assigned(chat.id):
        await update.message.reply_text(get_text(lang, "join_already_assigned"))
        return

    # Add participant
    if db.add_participant(chat.id, user.id, user.username, user.first_name):
        await update.message.reply_text(get_text(lang, "join_success", name=user.first_name))
    else:
        await update.message.reply_text(get_text(lang, "join_already_in", name=user.first_name))


async def participants(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show all participants in the Secret Santa."""
    chat = update.effective_chat
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(get_text(lang, "participants_group_only"))
        return

    # Check if group exists
    group = db.get_group(chat.id)
    if not group:
        await update.message.reply_text(get_text(lang, "participants_setup_first"))
        return

    # Get participants
    parts = db.get_participants(chat.id)
    if not parts:
        await update.message.reply_text(get_text(lang, "participants_none"))
        return

    participant_list = "\n".join(
        [f"{i+1}. {p[2] or 'Unknown'} (@{p[1] or 'no username'})" for i, p in enumerate(parts)]
    )
    await update.message.reply_text(
        get_text(lang, "participants_list", count=len(parts), list=participant_list)
    )


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show group information."""
    chat = update.effective_chat
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(get_text(lang, "info_group_only"))
        return

    # Check if group exists
    group = db.get_group(chat.id)
    if not group:
        await update.message.reply_text(get_text(lang, "info_setup_first"))
        return

    group_id, admin_id, event_date, max_price, language, is_assigned = group
    parts = db.get_participants(chat.id)

    info_text = get_text(lang, "info_header")
    if event_date:
        info_text += get_text(lang, "info_event_date", date=event_date)
    else:
        info_text += get_text(lang, "info_event_date_not_set")

    if max_price:
        info_text += get_text(lang, "info_max_price", price=max_price)
    else:
        info_text += get_text(lang, "info_max_price_not_set")

    info_text += get_text(lang, "info_participants", count=len(parts))
    info_text += get_text(lang, "info_status_assigned" if is_assigned else "info_status_not_assigned")

    await update.message.reply_text(info_text)


async def assign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show button to assign Secret Santas (admin only)."""
    chat = update.effective_chat
    user = update.effective_user
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(get_text(lang, "assign_group_only"))
        return

    # Check if user is admin
    member = await chat.get_member(user.id)
    if member.status not in ["creator", "administrator"]:
        await update.message.reply_text(get_text(lang, "assign_admin_only"))
        return

    # Check if group exists
    group = db.get_group(chat.id)
    if not group:
        await update.message.reply_text(get_text(lang, "assign_setup_first"))
        return

    # Check if already assigned
    if db.is_group_assigned(chat.id):
        await update.message.reply_text(get_text(lang, "assign_already_assigned"))
        return

    # Check minimum participants
    parts = db.get_participants(chat.id)
    if len(parts) < 2:
        await update.message.reply_text(get_text(lang, "assign_min_participants"))
        return

    # Create confirmation button
    keyboard = [
        [
            InlineKeyboardButton(get_text(lang, "assign_button_text"), callback_data=f"assign_{chat.id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text(lang, "assign_confirmation", count=len(parts)),
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("assign_"):
        group_id = int(data.split("_")[1])
        chat = await context.bot.get_chat(group_id)
        user = query.from_user
        lang = get_lang(group_id)

        # Check if user is admin
        member = await chat.get_member(user.id)
        if member.status not in ["creator", "administrator"]:
            await query.edit_message_text(get_text(lang, "assign_admin_only"))
            return

        # Assign Secret Santas
        if db.assign_secret_santas(group_id):
            await query.edit_message_text(get_text(lang, "assign_success"))

            # Send DMs to all participants
            participants = db.get_participants(group_id)
            group_info = db.get_group(group_id)
            _, _, event_date, max_price, language, _ = group_info

            for user_id, username, first_name, _ in participants:
                assignment = db.get_assignment(group_id, user_id)
                if assignment:
                    assigned_user_id, assigned_username, assigned_first_name = assignment
                    try:
                        message = get_text(lang, "assignment_header")
                        message += get_text(lang, "assignment_for", name=assigned_first_name)
                        if assigned_username:
                            message += f" (@{assigned_username})"
                        message += "\n\n"

                        if event_date:
                            message += get_text(lang, "assignment_event_date", date=event_date)
                        if max_price:
                            message += get_text(lang, "assignment_max_price", price=max_price)

                        message += get_text(lang, "assignment_keep_secret")

                        await context.bot.send_message(chat_id=user_id, text=message)
                    except Exception as e:
                        logger.error(f"Could not send DM to user {user_id}: {e}")
        else:
            await query.edit_message_text(get_text(lang, "assign_error"))


async def my_assignment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user's Secret Santa assignment in private chat."""
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != "private":
        # In group, use group's language
        lang = get_lang(chat.id)
        await update.message.reply_text(get_text(lang, "myassignment_group_only"))
        return

    # Get all groups where user has assignments
    user_groups = db.get_user_groups(user.id)

    if not user_groups:
        # Default to English for private chat if no groups found
        await update.message.reply_text(get_text("en", "myassignment_not_ready"))
        return

    # Show all assignments
    for group_id, group_lang in user_groups:
        group_info = db.get_group(group_id)
        if not group_info:
            continue

        _, _, event_date, max_price, language, is_assigned = group_info

        assignment = db.get_assignment(group_id, user.id)
        if assignment:
            assigned_user_id, assigned_username, assigned_first_name = assignment

            # Get group name
            try:
                group_chat = await context.bot.get_chat(group_id)
                group_name = group_chat.title
            except Exception:
                group_name = f"Group {group_id}"

            # Build message in the group's language
            message = f"🎁 {group_name}\n\n"
            message += get_text(group_lang, "assignment_header")
            message += get_text(group_lang, "assignment_for", name=assigned_first_name)
            if assigned_username:
                message += f" (@{assigned_username})"
            message += "\n\n"

            if event_date:
                message += get_text(group_lang, "assignment_event_date", date=event_date)
            if max_price:
                message += get_text(group_lang, "assignment_max_price", price=max_price)

            message += get_text(group_lang, "assignment_keep_secret")

            await update.message.reply_text(message)


async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Change language for the group."""
    chat = update.effective_chat
    user = update.effective_user
    current_lang = get_lang(chat.id)

    if chat.type == "private":
        await update.message.reply_text(get_text(current_lang, "setup_private_only"))
        return

    # Check if user is admin
    member = await chat.get_member(user.id)
    if member.status not in ["creator", "administrator"]:
        await update.message.reply_text(get_text(current_lang, "setup_admin_only"))
        return

    # Check if group exists
    group = db.get_group(chat.id)
    if not group:
        await update.message.reply_text(get_text(current_lang, "setdate_setup_first"))
        return

    # Parse language
    if not context.args:
        await update.message.reply_text(get_text(current_lang, "lang_usage"))
        return

    new_lang = context.args[0].lower()
    if new_lang not in ["en", "ru"]:
        await update.message.reply_text(get_text(current_lang, "lang_usage"))
        return

    # Update language
    if db.set_language(chat.id, new_lang):
        await update.message.reply_text(get_text(new_lang, "lang_success"))
    else:
        await update.message.reply_text(get_text(current_lang, "setup_error"))


def main():
    """Start the bot."""
    token = os.getenv("BOT_TOKEN")
    if not token:
        logger.error("No BOT_TOKEN found in environment variables!")
        return

    # Create the Application
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setup", setup))
    application.add_handler(CommandHandler("setdate", set_date))
    application.add_handler(CommandHandler("setprice", set_price))
    application.add_handler(CommandHandler("join", join))
    application.add_handler(CommandHandler("participants", participants))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("assign", assign))
    application.add_handler(CommandHandler("myassignment", my_assignment))
    application.add_handler(CommandHandler("lang", lang_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot
    logger.info("Starting Secret Santa bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
