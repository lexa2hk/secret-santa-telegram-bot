"""
Multi-language support for Secret Santa Bot
"""

TRANSLATIONS = {
    "en": {
        # Start command
        "start_private": "🎅 Hi {name}!\n\nI'm your Secret Santa bot! I help you organize gift exchanges with your friends.\n\n📚 Use /help to see all commands and instructions.",
        "start_group": "🎄 Hello! I'm the Secret Santa bot.\n\n👉 Admin: Use /setup to get started\n📖 Everyone: Use /help for instructions",

        # Help command
        "help_private": "🎁 *Secret Santa Bot - Help*\n\n*For Group Admins:*\n• `/setup` - Create a Secret Santa group\n• `/setdate YYYY-MM-DD` - Set event date\n• `/setprice <amount>` - Set max gift price\n• `/assign` - Randomly assign Secret Santas\n• `/lang en` or `/lang ru` - Change language\n\n*For Participants:*\n• `/join` - Join the Secret Santa\n• `/info` - View event details\n• `/participants` - See who's participating\n• `/wish <text>` - Set your gift wish\n• `/myassignment` - View your assignment\n• `/chat <message>` - Send anonymous message\n\n*Getting Started:*\n1️⃣ Add me to a group\n2️⃣ Admin uses /setup\n3️⃣ Set date and price\n4️⃣ Everyone joins with /join\n5️⃣ Admin assigns with /assign\n6️⃣ Check your assignment with /myassignment",
        "help_group": "🎁 *Secret Santa Bot - Help*\n\n*Admins:* /setup • /setdate • /setprice • /assign\n*Everyone:* /join • /info • /participants\n\nUse /help in private chat with me for detailed instructions!",

        # Setup command
        "setup_private_only": "❌ This command only works in groups!\n\n💡 Add me to a group and try again.",
        "setup_admin_only": "❌ Only group admins can set up Secret Santa!\n\n💡 Ask a group admin to run /setup",
        "setup_success_with_link": "✅ *Secret Santa group created!*\n\n👤 Admin: {admin}\n\n🔗 *Share this link with friends:*\n{link}\n\n",
        "setup_success_no_link": "✅ *Secret Santa group created!*\n\n👤 Admin: {admin}\n\n📝 *To invite friends:*\n1️⃣ Make me a group admin with 'Invite Users' permission\n2️⃣ Or share the group link manually\n3️⃣ Or add friends directly\n\n",
        "setup_next_steps": "📋 *Next steps:*\n\n1️⃣ Set event date: `/setdate 2025-12-25`\n2️⃣ Set max price: `/setprice 50`\n3️⃣ Have everyone join: `/join`\n4️⃣ Assign Santas: `/assign`",
        "setup_error": "❌ Error setting up Secret Santa.\n\n💡 Please try again or contact support.",

        # Set date command
        "setdate_group_only": "❌ This command only works in groups!",
        "setdate_admin_only": "❌ Only admins can set the date!\n\n💡 Ask a group admin to run this command.",
        "setdate_setup_first": "❌ Please use /setup first to create the group!",
        "setdate_usage": "📅 *Set Event Date*\n\nUsage: `/setdate YYYY-MM-DD`\n\n✅ Example: `/setdate 2025-12-25`",
        "setdate_success": "✅ Event date set to: *{date}*",
        "setdate_error": "❌ Error setting date. Please try again!",
        "setdate_invalid_format": "❌ Invalid date format!\n\n💡 Use: `/setdate YYYY-MM-DD`\n✅ Example: `/setdate 2025-12-25`",

        # Set price command
        "setprice_group_only": "❌ This command only works in groups!",
        "setprice_admin_only": "❌ Only admins can set the price!\n\n💡 Ask a group admin to run this command.",
        "setprice_setup_first": "❌ Please use /setup first to create the group!",
        "setprice_usage": "💰 *Set Maximum Gift Price*\n\nUsage: `/setprice <amount>`\n\n✅ Example: `/setprice 50`",
        "setprice_positive": "❌ Price must be greater than 0!\n\n💡 Try: `/setprice 50`",
        "setprice_success": "✅ Maximum gift price set to: *${price:.2f}*",
        "setprice_error": "❌ Error setting price. Please try again!",
        "setprice_invalid": "❌ Invalid price!\n\n💡 Enter a number: `/setprice 50`",

        # Join command
        "join_group_only": "❌ This command only works in groups!",
        "join_setup_first": "❌ Group not set up yet!\n\n💡 Ask an admin to use /setup first.",
        "join_already_assigned": "❌ Secret Santas have already been assigned!\n\n💡 Use /myassignment to see your assignment.",
        "join_success": "✅ *{name}* has joined Secret Santa! 🎉",
        "join_already_in": "✅ *{name}*, you're already participating!",

        # Participants command
        "participants_group_only": "❌ This command only works in groups!",
        "participants_setup_first": "❌ Please use /setup first to create the group!",
        "participants_none": "❌ No participants yet!\n\n💡 Use /join to participate.",
        "participants_list": "👥 *Participants ({count}):*\n\n{list}",

        # Info command
        "info_group_only": "❌ This command only works in groups!",
        "info_setup_first": "❌ Please use /setup first to create the group!",
        "info_header": "ℹ️ *Secret Santa Info*\n\n",
        "info_event_date": "📅 Event Date: *{date}*\n",
        "info_event_date_not_set": "📅 Event Date: _Not set_\n",
        "info_max_price": "💰 Max Price: *${price:.2f}*\n",
        "info_max_price_not_set": "💰 Max Price: _Not set_\n",
        "info_participants": "👥 Participants: *{count}*\n",
        "info_status_assigned": "✅ Status: *Assigned*",
        "info_status_not_assigned": "⏳ Status: *Not assigned yet*",

        # Assign command
        "assign_group_only": "❌ This command only works in groups!",
        "assign_admin_only": "❌ Only admins can assign Secret Santas!\n\n💡 Ask a group admin to run this command.",
        "assign_setup_first": "❌ Please use /setup first to create the group!",
        "assign_already_assigned": "✅ Secret Santas have already been assigned!\n\n💡 Use /myassignment to see your assignment.",
        "assign_min_participants": "❌ Need at least 2 participants!\n\n💡 Have people join with /join first.",
        "assign_button_text": "🎲 Assign Secret Santas",
        "assign_confirmation": "🎁 *Ready to assign Secret Santas?*\n\n👥 Participants: *{count}*\n\n⚠️ Once assigned, you cannot change them!\n\n👇 Click the button below:",
        "assign_success": "✅ *Secret Santas have been assigned!* 🎉\n\n📬 Everyone will receive a DM with their assignment.\n\n💡 Use /myassignment to check anytime!",
        "assign_error": "❌ Error assigning Secret Santas.\n\n💡 Please try again!",

        # Assignment DM
        "assignment_header": "🎅 *Your Secret Santa Assignment*\n\n",
        "assignment_for": "🎁 You are Secret Santa for: *{name}*",
        "assignment_event_date": "📅 Event Date: *{date}*\n",
        "assignment_max_price": "💰 Max Price: *${price:.2f}*\n",
        "assignment_keep_secret": "\n🤫 *Keep it secret!*\n\n💬 Use /chat to send anonymous messages!",

        # My assignment command
        "myassignment_group_only": "❌ This command only works in private chat!\n\n💡 DM me to see your assignment.",
        "myassignment_not_ready": "⏳ You don't have any assignments yet!\n\n💡 Join a Secret Santa group and wait for the admin to assign Santas.\n\n📖 Use /help for instructions.",

        # Language command
        "lang_success": "✅ Language changed to English!",
        "lang_usage": "🌍 *Change Language*\n\nUsage: `/lang <code>`\n\n🇬🇧 `/lang en` - English\n🇷🇺 `/lang ru` - Russian",

        # Chat with Secret Santa command
        "chat_group_only": "❌ This command only works in private chat!\n\n💡 DM me to send messages.",
        "chat_no_groups": "❌ You don't have any Secret Santa assignments yet!\n\n💡 Join a group and wait for assignments.",
        "chat_usage": "💬 *Send Anonymous Message*\n\nUsage: `/chat <message>`\n\n✅ Example: `/chat Do you have any gift preferences?`\n\n🤫 Your message will be sent anonymously to your Secret Santa!",
        "chat_message_sent": "✅ Your message has been sent anonymously! 📬",
        "chat_error": "❌ Error sending message.\n\n💡 Please try again!",
        "chat_received_header": "📨 *Anonymous message from your Secret Santa recipient:*\n\n",
        "chat_select_group": "❌ You're in multiple Secret Santa groups.\n\n💡 Reply with the group number to select:\n\n{groups}\n\nThen use /chat again to send your message.",
        "chat_group_selected": "✅ Group selected: *{group}*\n\n💡 Now use /chat <message> to send a message.",

        # Wish command
        "wish_private_only": "❌ This command only works in private chat!\n\n💡 DM me to set your wish.",
        "wish_no_groups": "❌ You're not participating in any Secret Santa groups yet!\n\n💡 Join a group first with /join",
        "wish_usage": "🎁 *Set Your Gift Wish*\n\nUsage: `/wish <your wish>`\n\n✅ Example: `/wish I'd love a book or coffee mug!`\n\n💡 Your Secret Santa will see this when checking their assignment.",
        "wish_set_success": "✅ Your wish has been saved!\n\n🎁 Wish: _{wish}_\n\n💡 Your Secret Santa will be notified!",
        "wish_notification": "🎁 *Good news!*\n\n{name} has set a gift wish:\n\n_{wish}_\n\n💡 This should help you choose the perfect gift!",
        "wish_error": "❌ Error saving your wish.\n\n💡 Please try again!",
        "wish_display": "🎁 Wish: _{wish}_\n",
        "wish_not_set": "🎁 Wish: _Not set yet_\n",
    },
    "ru": {
        # Start command
        "start_private": "🎅 Привет, {name}!\n\nЯ бот для Тайного Санты! Я помогаю организовать обмен подарками с друзьями.\n\n📚 Используй /help чтобы увидеть все команды и инструкции.",
        "start_group": "🎄 Привет! Я бот для Тайного Санты.\n\n👉 Админ: Используй /setup для начала\n📖 Все: Используй /help для инструкций",

        # Help command
        "help_private": "🎁 *Бот Тайный Санта - Помощь*\n\n*Для админов группы:*\n• `/setup` - Создать группу Тайного Санты\n• `/setdate ГГГГ-ММ-ДД` - Установить дату события\n• `/setprice <сумма>` - Установить макс. цену\n• `/assign` - Случайно назначить Тайных Сант\n• `/lang en` или `/lang ru` - Сменить язык\n\n*Для участников:*\n• `/join` - Присоединиться к Тайному Санте\n• `/info` - Посмотреть детали события\n• `/participants` - Кто участвует\n• `/wish <текст>` - Указать пожелание\n• `/myassignment` - Твоё назначение\n• `/chat <сообщение>` - Анонимное сообщение\n\n*Как начать:*\n1️⃣ Добавь меня в группу\n2️⃣ Админ использует /setup\n3️⃣ Установить дату и цену\n4️⃣ Все присоединяются через /join\n5️⃣ Админ назначает через /assign\n6️⃣ Проверь назначение через /myassignment",
        "help_group": "🎁 *Бот Тайный Санта - Помощь*\n\n*Админы:* /setup • /setdate • /setprice • /assign\n*Все:* /join • /info • /participants\n\nИспользуй /help в личке со мной для подробных инструкций!",

        # Setup command
        "setup_private_only": "Эта команда работает только в группах!",
        "setup_admin_only": "Только админы группы могут настроить Тайного Санту!",
        "setup_success_with_link": "Группа Тайного Санты создана!\n\nАдмин: {admin}\n\nПоделись этой ссылкой с друзьями:\n{link}\n\n",
        "setup_success_no_link": "Группа Тайного Санты создана!\n\nАдмин: {admin}\n\nЧтобы пригласить друзей:\n1. Сделай меня админом с правом 'Приглашать пользователей'\n2. Поделись ссылкой на группу вручную, или\n3. Добавь друзей напрямую в группу\n\n",
        "setup_next_steps": "Следующие шаги:\n1. Используй /setdate чтобы установить дату события\n2. Используй /setprice чтобы установить максимальную цену подарка\n3. Попроси всех использовать /join для участия\n4. Используй /assign когда все присоединятся",
        "setup_error": "Ошибка при настройке Тайного Санты. Попробуй снова!",

        # Set date command
        "setdate_group_only": "Эта команда работает только в группах!",
        "setdate_admin_only": "Только админы группы могут установить дату!",
        "setdate_setup_first": "Пожалуйста, сначала используй /setup!",
        "setdate_usage": "Использование: /setdate ГГГГ-ММ-ДД\nПример: /setdate 2025-12-25",
        "setdate_success": "Дата события установлена: {date}",
        "setdate_error": "Ошибка при установке даты. Попробуй снова!",
        "setdate_invalid_format": "Неверный формат даты! Используй ГГГГ-ММ-ДД",

        # Set price command
        "setprice_group_only": "Эта команда работает только в группах!",
        "setprice_admin_only": "Только админы группы могут установить цену!",
        "setprice_setup_first": "Пожалуйста, сначала используй /setup!",
        "setprice_usage": "Использование: /setprice <сумма>\nПример: /setprice 50",
        "setprice_positive": "Цена должна быть больше 0!",
        "setprice_success": "Максимальная цена подарка установлена: {price:.2f}",
        "setprice_error": "Ошибка при установке цены. Попробуй снова!",
        "setprice_invalid": "Неверная цена! Пожалуйста, введи число.",

        # Join command
        "join_group_only": "Эта команда работает только в группах!",
        "join_setup_first": "Пожалуйста, попроси админа использовать /setup сначала!",
        "join_already_assigned": "Тайные Санты уже назначены для этой группы!",
        "join_success": "{name} присоединился к Тайному Санте!",
        "join_already_in": "{name}, ты уже участвуешь!",

        # Participants command
        "participants_group_only": "Эта команда работает только в группах!",
        "participants_setup_first": "Пожалуйста, используй /setup сначала!",
        "participants_none": "Пока нет участников! Используй /join для участия.",
        "participants_list": "Участники ({count}):\n\n{list}",

        # Info command
        "info_group_only": "Эта команда работает только в группах!",
        "info_setup_first": "Пожалуйста, используй /setup сначала!",
        "info_header": "Информация о Тайном Санте:\n\n",
        "info_event_date": "Дата события: {date}\n",
        "info_event_date_not_set": "Дата события: Не установлена\n",
        "info_max_price": "Макс. цена: {price:.2f}\n",
        "info_max_price_not_set": "Макс. цена: Не установлена\n",
        "info_participants": "Участников: {count}\n",
        "info_status_assigned": "Статус: Назначены",
        "info_status_not_assigned": "Статус: Еще не назначены",

        # Assign command
        "assign_group_only": "Эта команда работает только в группах!",
        "assign_admin_only": "Только админы группы могут назначить Тайных Сант!",
        "assign_setup_first": "Пожалуйста, используй /setup сначала!",
        "assign_already_assigned": "Тайные Санты уже назначены!",
        "assign_min_participants": "Нужно минимум 2 участника!",
        "assign_button_text": "Назначить Тайных Сант",
        "assign_confirmation": "Готов назначить Тайных Сант?\n\nУчастников: {count}\nНажми кнопку ниже для продолжения:",
        "assign_success": "Тайные Санты назначены! Проверь личные сообщения для своего назначения.",
        "assign_error": "Ошибка при назначении Тайных Сант. Попробуй снова!",

        # Assignment DM
        "assignment_header": "Твоё назначение Тайного Санты:\n\n",
        "assignment_for": "Ты Тайный Санта для: {name}",
        "assignment_event_date": "Дата события: {date}\n",
        "assignment_max_price": "Макс. цена: {price:.2f}\n",
        "assignment_keep_secret": "\nСохрани это в секрете!",

        # My assignment command
        "myassignment_group_only": "Эта команда работает только в личных сообщениях! Напиши мне в личку, чтобы увидеть назначение.",
        "myassignment_not_ready": "Ты получишь своё назначение в личные сообщения, когда админ назначит Тайных Сант в твоей группе!",

        # Language command
        "lang_success": "Язык изменен на русский!",
        "lang_usage": "Использование: /lang <код>\nДоступные языки:\n/lang en - English\n/lang ru - Русский",

        # Chat with Secret Santa command
        "chat_group_only": "Эта команда работает только в личных сообщениях! Напиши мне в личку, чтобы отправить сообщение.",
        "chat_no_groups": "У тебя пока нет назначений Тайного Санты!",
        "chat_usage": "Использование: /chat <сообщение>\nПример: /chat Есть ли у тебя предпочтения по подарку?",
        "chat_message_sent": "✅ Твоё сообщение отправлено анонимно твоему Тайному Санте!",
        "chat_error": "Ошибка при отправке сообщения. Попробуй снова!",
        "chat_received_header": "📨 Анонимное сообщение от получателя твоего подарка:\n\n",
        "chat_select_group": "Ты участвуешь в нескольких группах Тайного Санты. Ответь номером группы для выбора:\n\n{groups}\n\nЗатем используй /chat снова, чтобы отправить сообщение.",
        "chat_group_selected": "Группа выбрана: {group}\nТеперь используй /chat <сообщение> для отправки.",

        # Wish command
        "wish_private_only": "Эта команда работает только в личных сообщениях! Напиши мне в личку, чтобы установить пожелание.",
        "wish_no_groups": "Ты еще не участвуешь ни в одной группе Тайного Санты!\n\nПрисоединись к группе с помощью /join",
        "wish_usage": "Использование: /wish <твоё пожелание>\nПример: /wish Хотел бы книгу или кружку для кофе!",
        "wish_set_success": "✅ Твоё пожелание сохранено!\n\n🎁 Пожелание: _{wish}_\n\nТвой Тайный Санта будет уведомлен!",
        "wish_notification": "🎁 *Хорошие новости!*\n\n{name} указал пожелание:\n\n_{wish}_\n\nЭто поможет выбрать идеальный подарок!",
        "wish_error": "Ошибка при сохранении пожелания. Попробуй снова!",
        "wish_display": "🎁 Пожелание: _{wish}_\n",
        "wish_not_set": "🎁 Пожелание: _Не указано_\n",
    }
}


def get_text(lang: str, key: str, **kwargs) -> str:
    """
    Get translated text for a given language and key.

    Args:
        lang: Language code ('en' or 'ru')
        key: Translation key
        **kwargs: Format arguments for the text

    Returns:
        Translated and formatted text
    """
    # Default to English if language not found
    if lang not in TRANSLATIONS:
        lang = "en"

    # Get translation, fallback to English if key not found
    text = TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS["en"].get(key, f"Missing translation: {key}"))

    # Format with provided arguments
    try:
        return text.format(**kwargs)
    except KeyError:
        return text
