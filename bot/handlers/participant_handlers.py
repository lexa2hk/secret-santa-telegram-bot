"""
Participant command handlers for Secret Santa Bot
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.utils import get_lang, db
from bot.translations import get_text

logger = logging.getLogger(__name__)


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


async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send anonymous message to Secret Santa."""
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != "private":
        # In group, use group's language
        lang = get_lang(chat.id)
        await update.message.reply_text(get_text(lang, "chat_group_only"))
        return

    # Get all groups where user has assignments
    user_groups = db.get_user_groups(user.id)

    if not user_groups:
        # Default to English for private chat if no groups found
        await update.message.reply_text(get_text("en", "chat_no_groups"))
        return

    # Check if message provided
    if not context.args:
        # Use language from first group
        lang = user_groups[0][1] if user_groups else "en"
        await update.message.reply_text(get_text(lang, "chat_usage"))
        return

    message_text = " ".join(context.args)

    # If user is in multiple groups, let them select (for now, send to first group)
    # TODO: Add proper group selection with inline keyboard
    if len(user_groups) > 1:
        # For now, send to all groups
        sent_count = 0
        for group_id, group_lang in user_groups:
            # Find who is giving to this user (their Secret Santa)
            secret_santa = db.get_secret_santa_for_user(group_id, user.id)
            if secret_santa:
                santa_user_id, santa_username, santa_first_name = secret_santa
                try:
                    # Send message to Secret Santa
                    full_message = get_text(group_lang, "chat_received_header") + message_text
                    await context.bot.send_message(chat_id=santa_user_id, text=full_message)
                    sent_count += 1
                except Exception as e:
                    logger.error(f"Could not send chat message to user {santa_user_id}: {e}")

        if sent_count > 0:
            lang = user_groups[0][1]
            await update.message.reply_text(get_text(lang, "chat_message_sent"))
        else:
            await update.message.reply_text(get_text("en", "chat_error"))
    else:
        # Single group - send to that group's Secret Santa
        group_id, group_lang = user_groups[0]

        # Find who is giving to this user (their Secret Santa)
        secret_santa = db.get_secret_santa_for_user(group_id, user.id)
        if secret_santa:
            santa_user_id, santa_username, santa_first_name = secret_santa
            try:
                # Send message to Secret Santa
                full_message = get_text(group_lang, "chat_received_header") + message_text
                await context.bot.send_message(chat_id=santa_user_id, text=full_message)
                await update.message.reply_text(get_text(group_lang, "chat_message_sent"))
            except Exception as e:
                logger.error(f"Could not send chat message to user {santa_user_id}: {e}")
                await update.message.reply_text(get_text(group_lang, "chat_error"))
        else:
            await update.message.reply_text(get_text(group_lang, "chat_error"))
