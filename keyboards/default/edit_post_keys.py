from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

edit_actions = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Изменить текст поста")
        ],
        [
            KeyboardButton(text="Изменить фото")
        ],
        [
            KeyboardButton(text="Изменить количество кнопок в строке")
        ],
        [
            KeyboardButton(text="Добавить кнопку")
        ],
        [
            KeyboardButton(text="Изменить кнопку"),
            KeyboardButton(text="Удалить кнопку")
        ],
        [
            KeyboardButton(text="Просмотреть пост")
        ],
        [
            KeyboardButton(text="Сохранить")
        ],
        [
            KeyboardButton(text="Отмена")
        ]
    ]
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад")
        ]
    ]
)