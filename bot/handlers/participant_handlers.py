"""
Participant command handlers for Secret Santa Bot
"""
import logging
from telegram import Update
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
        logger.info(
            f"➕ New participant joined | "
            f"Group: {chat.id} ({chat.title}) | "
            f"User: {user.id} (@{user.username or 'N/A'}, {user.first_name})"
        )
        await update.message.reply_text(get_text(lang, "join_success", name=escape_markdown(user.first_name)))
    else:
        logger.info(
            f"Duplicate join attempt | "
            f"Group: {chat.id} | "
            f"User: {user.id} (@{user.username or 'N/A'})"
        )
        await update.message.reply_text(get_text(lang, "join_already_in", name=escape_markdown(user.first_name)))


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
        [f"{i+1}. {escape_markdown(p[2] or 'Unknown')} (@{escape_markdown(p[1] or 'no username')})" for i, p in enumerate(parts)]
    )
    await update.message.reply_text(
        get_text(lang, "participants_list", count=len(parts), list=participant_list),
        parse_mode=ParseMode.MARKDOWN
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

    await update.message.reply_text(info_text, parse_mode=ParseMode.MARKDOWN)


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
        # Default to Russian for private chat if no groups found
        await update.message.reply_text(get_text("ru", "myassignment_not_ready"))
        return

    # Show all assignments
    for group_id, group_lang in user_groups:
        group_info = db.get_group(group_id)
        if not group_info:
            continue

        _, _, event_date, max_price, language, is_assigned = group_info

        assignment = db.get_assignment(group_id, user.id)
        if assignment:
            assigned_user_id, assigned_username, assigned_first_name, assigned_wish = assignment

            # Get group name
            try:
                group_chat = await context.bot.get_chat(group_id)
                group_name = group_chat.title
            except Exception:
                group_name = f"Group {group_id}"

            # Build message in the group's language
            message = f"🎁 {escape_markdown(group_name)}\n\n"
            message += get_text(group_lang, "assignment_header")
            message += get_text(group_lang, "assignment_for", name=escape_markdown(assigned_first_name))
            if assigned_username:
                message += f" (@{escape_markdown(assigned_username)})"
            message += "\n\n"

            if event_date:
                message += get_text(group_lang, "assignment_event_date", date=event_date)
            if max_price:
                message += get_text(group_lang, "assignment_max_price", price=max_price)

            # Show wish if available
            if assigned_wish:
                message += get_text(group_lang, "wish_display", wish=escape_markdown(assigned_wish))
            else:
                message += get_text(group_lang, "wish_not_set")

            message += get_text(group_lang, "assignment_keep_secret")

            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


async def wish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set a gift wish for Secret Santa."""
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != "private":
        # In group, use group's language
        lang = get_lang(chat.id)
        await update.message.reply_text(get_text(lang, "wish_private_only"))
        return

    # Get all groups where user is a participant
    user_groups = db.get_user_groups(user.id)

    # Also check for groups where user joined but assignments not done yet
    all_user_groups = []
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT DISTINCT g.group_id, g.language
                    FROM participants p
                    JOIN groups g ON p.group_id = g.group_id
                    WHERE p.user_id = %s
                """, (user.id,))
                all_user_groups = cursor.fetchall()
    except Exception as e:
        logger.error(f"Error getting user groups for wish: {e}")

    if not all_user_groups:
        # Default to Russian for private chat if no groups found
        await update.message.reply_text(get_text("ru", "wish_no_groups"))
        return

    # Check if wish provided
    if not context.args:
        # Use language from first group
        lang = all_user_groups[0][1] if all_user_groups else "ru"
        await update.message.reply_text(get_text(lang, "wish_usage"))
        return

    wish_text = " ".join(context.args)

    # Set wish for all groups the user is in
    success_count = 0
    lang = all_user_groups[0][1] if all_user_groups else "ru"

    for group_id, group_lang in all_user_groups:
        if db.set_wish(group_id, user.id, wish_text):
            success_count += 1
            logger.info(
                f"🎁 Wish set | "
                f"Group: {group_id} | "
                f"User: {user.id} (@{user.username or 'N/A'}) | "
                f"Wish length: {len(wish_text)} chars"
            )

            # Notify Secret Santa if assignments have been made
            if db.is_group_assigned(group_id):
                secret_santa = db.get_secret_santa_for_user(group_id, user.id)
                if secret_santa:
                    santa_user_id, santa_username, santa_first_name = secret_santa
                    try:
                        notification = get_text(
                            group_lang,
                            "wish_notification",
                            name=escape_markdown(user.first_name or user.username or "Someone"),
                            wish=escape_markdown(wish_text)
                        )
                        await context.bot.send_message(
                            chat_id=santa_user_id,
                            text=notification,
                            parse_mode=ParseMode.MARKDOWN
                        )
                        logger.info(
                            f"🔔 Wish notification sent | "
                            f"Group: {group_id} | "
                            f"From: {user.id} (@{user.username or 'N/A'}) | "
                            f"To Santa: {santa_user_id} (@{santa_username or 'N/A'})"
                        )
                    except Exception as e:
                        logger.error(
                            f"❌ Failed to send wish notification | "
                            f"Group: {group_id} | "
                            f"Santa: {santa_user_id} (@{santa_username or 'N/A'}) | "
                            f"Error: {e}"
                        )

    if success_count > 0:
        await update.message.reply_text(
            get_text(lang, "wish_set_success", wish=escape_markdown(wish_text)),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(get_text(lang, "wish_error"))


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
        # Default to Russian for private chat if no groups found
        await update.message.reply_text(get_text("ru", "chat_no_groups"))
        logger.info(f"User {user.id} (@{user.username}) attempted to send anonymous message but has no assigned groups")
        return

    # Check if message provided
    if not context.args:
        # Use language from first group
        lang = user_groups[0][1] if user_groups else "ru"
        await update.message.reply_text(get_text(lang, "chat_usage"))
        return

    message_text = " ".join(context.args)
    message_preview = message_text[:50] + "..." if len(message_text) > 50 else message_text

    # If user is in multiple groups, let them select (for now, send to first group)
    # TODO: Add proper group selection with inline keyboard
    if len(user_groups) > 1:
        # For now, send to all groups
        sent_count = 0
        logger.info(
            f"Anonymous message from user {user.id} (@{user.username}) "
            f"to {len(user_groups)} groups, message length: {len(message_text)}"
        )

        for group_id, group_lang in user_groups:
            # Find who is giving to this user (their Secret Santa)
            secret_santa = db.get_secret_santa_for_user(group_id, user.id)
            if secret_santa:
                santa_user_id, santa_username, santa_first_name = secret_santa
                try:
                    # Send message to Secret Santa
                    full_message = get_text(group_lang, "chat_received_header") + escape_markdown(message_text)
                    await context.bot.send_message(chat_id=santa_user_id, text=full_message, parse_mode=ParseMode.MARKDOWN)
                    sent_count += 1

                    logger.info(
                        f"✅ Anonymous message delivered | "
                        f"Group: {group_id} | "
                        f"From: {user.id} (@{user.username or 'N/A'}) | "
                        f"To Santa: {santa_user_id} (@{santa_username or 'N/A'}) | "
                        f"Preview: '{message_preview}'"
                    )
                except Exception as e:
                    logger.error(
                        f"❌ Failed to send anonymous message | "
                        f"Group: {group_id} | "
                        f"From: {user.id} (@{user.username or 'N/A'}) | "
                        f"To Santa: {santa_user_id} (@{santa_username or 'N/A'}) | "
                        f"Error: {e}"
                    )

        if sent_count > 0:
            lang = user_groups[0][1]
            await update.message.reply_text(get_text(lang, "chat_message_sent"))
            logger.info(f"User {user.id} successfully sent anonymous messages to {sent_count}/{len(user_groups)} groups")
        else:
            await update.message.reply_text(get_text("ru", "chat_error"))
            logger.warning(f"User {user.id} failed to send anonymous messages to any groups")
    else:
        # Single group - send to that group's Secret Santa
        group_id, group_lang = user_groups[0]

        # Find who is giving to this user (their Secret Santa)
        secret_santa = db.get_secret_santa_for_user(group_id, user.id)
        if secret_santa:
            santa_user_id, santa_username, santa_first_name = secret_santa
            try:
                # Send message to Secret Santa
                full_message = get_text(group_lang, "chat_received_header") + escape_markdown(message_text)
                await context.bot.send_message(chat_id=santa_user_id, text=full_message, parse_mode=ParseMode.MARKDOWN)
                await update.message.reply_text(get_text(group_lang, "chat_message_sent"))

                logger.info(
                    f"✅ Anonymous message delivered | "
                    f"Group: {group_id} | "
                    f"From: {user.id} (@{user.username or 'N/A'}, {user.first_name}) | "
                    f"To Santa: {santa_user_id} (@{santa_username or 'N/A'}, {santa_first_name}) | "
                    f"Length: {len(message_text)} chars | "
                    f"Preview: '{message_preview}'"
                )
            except Exception as e:
                logger.error(
                    f"❌ Failed to send anonymous message | "
                    f"Group: {group_id} | "
                    f"From: {user.id} (@{user.username or 'N/A'}) | "
                    f"To Santa: {santa_user_id} (@{santa_username or 'N/A'}) | "
                    f"Error: {e}"
                )
                await update.message.reply_text(get_text(group_lang, "chat_error"))
        else:
            logger.warning(
                f"No Secret Santa found for user {user.id} (@{user.username}) in group {group_id}"
            )
            await update.message.reply_text(get_text(group_lang, "chat_error"))
