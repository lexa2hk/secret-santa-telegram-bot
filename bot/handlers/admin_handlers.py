"""
Admin command handlers for Secret Santa Bot
"""
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from bot.utils import get_lang, db
from bot.translations import get_text

logger = logging.getLogger(__name__)


def escape_markdown(text: str) -> str:
    """Escape special Markdown characters to prevent parsing errors."""
    if not text:
        return text
    # Escape Markdown special characters
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return text


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
        logger.info(
            f"🎄 New Secret Santa group created | "
            f"Group: {chat.id} ({chat.title}) | "
            f"Admin: {user.id} (@{user.username or 'N/A'}, {user.first_name})"
        )

        # Try to get invite link (requires bot to be admin with invite link permission)
        try:
            invite_link = await chat.export_invite_link()
            message = get_text(lang, "setup_success_with_link", admin=escape_markdown(user.first_name), link=invite_link)
            logger.info(f"Invite link generated for group {chat.id}: {invite_link}")
        except Exception as e:
            logger.warning(f"Could not export invite link for group {chat.id}: {e}")
            message = get_text(lang, "setup_success_no_link", admin=escape_markdown(user.first_name))

        message += get_text(lang, "setup_next_steps")
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    else:
        logger.error(f"Failed to create Secret Santa group {chat.id}")
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
            logger.info(
                f"📅 Event date set | "
                f"Group: {chat.id} | "
                f"Date: {date_str} | "
                f"Admin: {user.id} (@{user.username or 'N/A'})"
            )
            await update.message.reply_text(get_text(lang, "setdate_success", date=date_str))
        else:
            logger.error(f"Failed to set event date for group {chat.id}")
            await update.message.reply_text(get_text(lang, "setdate_error"))
    except ValueError:
        await update.message.reply_text(get_text(lang, "setdate_invalid_format"))


async def set_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set the maximum gift price."""
    if not update.effective_message:
        return

    chat = update.effective_chat
    user = update.effective_user
    lang = get_lang(chat.id)

    if chat.type == "private":
        await update.effective_message.reply_text(get_text(lang, "setprice_group_only"))
        return

    # Check if user is admin
    member = await chat.get_member(user.id)
    if member.status not in ["creator", "administrator"]:
        await update.effective_message.reply_text(get_text(lang, "setprice_admin_only"))
        return

    # Check if group exists
    group = db.get_group(chat.id)
    if not group:
        await update.effective_message.reply_text(get_text(lang, "setprice_setup_first"))
        return

    # Parse price
    if not context.args:
        await update.effective_message.reply_text(get_text(lang, "setprice_usage"))
        return

    try:
        price = float(context.args[0])
        if price <= 0:
            await update.effective_message.reply_text(get_text(lang, "setprice_positive"))
            return

        if db.update_group_settings(chat.id, max_price=price):
            logger.info(
                f"💰 Max price set | "
                f"Group: {chat.id} | "
                f"Price: {price} | "
                f"Admin: {user.id} (@{user.username or 'N/A'})"
            )
            await update.effective_message.reply_text(get_text(lang, "setprice_success", price=price))
        else:
            logger.error(f"Failed to set max price for group {chat.id}")
            await update.effective_message.reply_text(get_text(lang, "setprice_error"))
    except ValueError:
        await update.effective_message.reply_text(get_text(lang, "setprice_invalid"))


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
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
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
            participants = db.get_participants(group_id)
            logger.info(
                f"🎁 Secret Santas assigned | "
                f"Group: {group_id} | "
                f"Participants: {len(participants)} | "
                f"Admin: {user.id} (@{user.username or 'N/A'})"
            )

            await query.edit_message_text(get_text(lang, "assign_success"), parse_mode=ParseMode.MARKDOWN)

            # Send DMs to all participants
            group_info = db.get_group(group_id)
            _, _, event_date, max_price, language, _ = group_info

            dm_sent_count = 0
            dm_failed_count = 0

            for user_id, username, first_name, _ in participants:
                assignment = db.get_assignment(group_id, user_id)
                if assignment:
                    assigned_user_id, assigned_username, assigned_first_name = assignment
                    try:
                        message = get_text(lang, "assignment_header")
                        message += get_text(lang, "assignment_for", name=escape_markdown(assigned_first_name))
                        if assigned_username:
                            message += f" (@{escape_markdown(assigned_username)})"
                        message += "\n\n"

                        if event_date:
                            message += get_text(lang, "assignment_event_date", date=event_date)
                        if max_price:
                            message += get_text(lang, "assignment_max_price", price=max_price)

                        message += get_text(lang, "assignment_keep_secret")

                        await context.bot.send_message(chat_id=user_id, text=message, parse_mode=ParseMode.MARKDOWN)
                        dm_sent_count += 1

                        logger.info(
                            f"📬 Assignment DM sent | "
                            f"Group: {group_id} | "
                            f"To: {user_id} (@{username or 'N/A'}) | "
                            f"Assigned: {assigned_first_name} (@{assigned_username or 'N/A'})"
                        )
                    except Exception as e:
                        dm_failed_count += 1
                        logger.error(
                            f"❌ Failed to send assignment DM | "
                            f"Group: {group_id} | "
                            f"To: {user_id} (@{username or 'N/A'}) | "
                            f"Error: {e}"
                        )

            logger.info(
                f"Assignment DM summary for group {group_id}: "
                f"{dm_sent_count} sent, {dm_failed_count} failed out of {len(participants)} participants"
            )
        else:
            logger.error(f"Failed to assign Secret Santas for group {group_id}")
            await query.edit_message_text(get_text(lang, "assign_error"))


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
        logger.info(
            f"🌐 Language changed | "
            f"Group: {chat.id} | "
            f"From: {current_lang} → To: {new_lang} | "
            f"Admin: {user.id} (@{user.username or 'N/A'})"
        )
        await update.message.reply_text(get_text(new_lang, "lang_success"))
    else:
        logger.error(f"Failed to set language for group {chat.id}")
        await update.message.reply_text(get_text(current_lang, "setup_error"))
