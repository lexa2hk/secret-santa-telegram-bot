"""
Multi-language support for Secret Santa Bot
"""

TRANSLATIONS = {
    "en": {
        # Start command
        "start_private": "Hi {name}!\n\nI'm your Secret Santa bot. Add me to a group to get started!\n\nCommands:\n/setup - Initialize Secret Santa in a group (admin only)\n/setdate <YYYY-MM-DD> - Set event date\n/setprice <amount> - Set maximum gift price\n/join - Join the Secret Santa\n/participants - See all participants\n/info - View group settings\n/assign - Assign Secret Santas (admin only)\n/myassignment - View your Secret Santa assignment\n/chat <message> - Send anonymous message to your Secret Santa\n/lang <code> - Change language (ru/en)",
        "start_group": "Hello! Use /setup to initialize Secret Santa in this group.",

        # Setup command
        "setup_private_only": "This command only works in groups!",
        "setup_admin_only": "Only group admins can set up Secret Santa!",
        "setup_success_with_link": "Secret Santa group created!\n\nAdmin: {admin}\n\nShare this link with your friends:\n{link}\n\n",
        "setup_success_no_link": "Secret Santa group created!\n\nAdmin: {admin}\n\nTo invite friends:\n1. Make sure I'm an admin with 'Invite Users' permission\n2. Share the group invite link manually, or\n3. Add friends directly to this group\n\n",
        "setup_next_steps": "Next steps:\n1. Use /setdate to set the event date\n2. Use /setprice to set max gift price\n3. Have everyone use /join to participate\n4. Use /assign when everyone has joined",
        "setup_error": "Error setting up Secret Santa. Try again!",

        # Set date command
        "setdate_group_only": "This command only works in groups!",
        "setdate_admin_only": "Only group admins can set the date!",
        "setdate_setup_first": "Please use /setup first!",
        "setdate_usage": "Usage: /setdate YYYY-MM-DD\nExample: /setdate 2025-12-25",
        "setdate_success": "Event date set to: {date}",
        "setdate_error": "Error setting date. Try again!",
        "setdate_invalid_format": "Invalid date format! Use YYYY-MM-DD",

        # Set price command
        "setprice_group_only": "This command only works in groups!",
        "setprice_admin_only": "Only group admins can set the price!",
        "setprice_setup_first": "Please use /setup first!",
        "setprice_usage": "Usage: /setprice <amount>\nExample: /setprice 50",
        "setprice_positive": "Price must be greater than 0!",
        "setprice_success": "Maximum gift price set to: {price:.2f}",
        "setprice_error": "Error setting price. Try again!",
        "setprice_invalid": "Invalid price! Please enter a number.",

        # Join command
        "join_group_only": "This command only works in groups!",
        "join_setup_first": "Please ask an admin to use /setup first!",
        "join_already_assigned": "Secret Santas have already been assigned for this group!",
        "join_success": "{name} has joined Secret Santa!",
        "join_already_in": "{name}, you're already in!",

        # Participants command
        "participants_group_only": "This command only works in groups!",
        "participants_setup_first": "Please use /setup first!",
        "participants_none": "No participants yet! Use /join to participate.",
        "participants_list": "Participants ({count}):\n\n{list}",

        # Info command
        "info_group_only": "This command only works in groups!",
        "info_setup_first": "Please use /setup first!",
        "info_header": "Secret Santa Info:\n\n",
        "info_event_date": "Event Date: {date}\n",
        "info_event_date_not_set": "Event Date: Not set\n",
        "info_max_price": "Max Price: {price:.2f}\n",
        "info_max_price_not_set": "Max Price: Not set\n",
        "info_participants": "Participants: {count}\n",
        "info_status_assigned": "Status: Assigned",
        "info_status_not_assigned": "Status: Not assigned yet",

        # Assign command
        "assign_group_only": "This command only works in groups!",
        "assign_admin_only": "Only group admins can assign Secret Santas!",
        "assign_setup_first": "Please use /setup first!",
        "assign_already_assigned": "Secret Santas have already been assigned!",
        "assign_min_participants": "Need at least 2 participants!",
        "assign_button_text": "Assign Secret Santas",
        "assign_confirmation": "Ready to assign Secret Santas?\n\nParticipants: {count}\nClick the button below to proceed:",
        "assign_success": "Secret Santas have been assigned! Check your DMs for your assignment.",
        "assign_error": "Error assigning Secret Santas. Try again!",

        # Assignment DM
        "assignment_header": "Your Secret Santa assignment:\n\n",
        "assignment_for": "You are Secret Santa for: {name}",
        "assignment_event_date": "Event Date: {date}\n",
        "assignment_max_price": "Max Price: {price:.2f}\n",
        "assignment_keep_secret": "\nKeep it secret!",

        # My assignment command
        "myassignment_group_only": "This command only works in private chat! DM me to see your assignment.",
        "myassignment_not_ready": "You'll receive your assignment via DM once the admin assigns Secret Santas in your group!",

        # Language command
        "lang_success": "Language changed to English!",
        "lang_usage": "Usage: /lang <code>\nAvailable languages:\n/lang en - English\n/lang ru - Russian",

        # Chat with Secret Santa command
        "chat_group_only": "This command only works in private chat! DM me to send messages.",
        "chat_no_groups": "You don't have any Secret Santa assignments yet!",
        "chat_usage": "Usage: /chat <message>\nExample: /chat Do you have any gift preferences?",
        "chat_message_sent": "✅ Your message has been sent anonymously to your Secret Santa!",
        "chat_error": "Error sending message. Try again!",
        "chat_received_header": "📨 Anonymous message from your Secret Santa recipient:\n\n",
        "chat_select_group": "You're in multiple Secret Santa groups. Reply with the group number to select:\n\n{groups}\n\nThen use /chat again to send your message.",
        "chat_group_selected": "Group selected: {group}\nNow use /chat <message> to send a message.",
    },
    "ru": {
        # Start command
        "start_private": "Привет, {name}!\n\nЯ бот для Тайного Санты. Добавь меня в группу, чтобы начать!\n\nКоманды:\n/setup - Инициализировать Тайного Санту в группе (только админ)\n/setdate <ГГГГ-ММ-ДД> - Установить дату события\n/setprice <сумма> - Установить максимальную цену подарка\n/join - Присоединиться к Тайному Санте\n/participants - Посмотреть всех участников\n/info - Посмотреть настройки группы\n/assign - Назначить Тайных Сант (только админ)\n/myassignment - Посмотреть твоё назначение\n/chat <сообщение> - Отправить анонимное сообщение своему Тайному Санте\n/lang <код> - Изменить язык (ru/en)",
        "start_group": "Привет! Используй /setup чтобы инициализировать Тайного Санту в этой группе.",

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
