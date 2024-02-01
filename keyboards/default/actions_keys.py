from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

actions = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Просмотр поста")
        ],
        [
            KeyboardButton(text="Редактирование")
        ]
    ],
)
