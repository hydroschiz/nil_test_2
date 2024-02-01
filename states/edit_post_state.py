from aiogram.fsm.state import StatesGroup, State


class EditPost(StatesGroup):
    EditPostState = State()
    EditText = State()
    EditPhoto = State()
    AddButtonText = State()
    AddButtonLink = State()
    DeleteButton = State()
    FindButtonText = State()
    EditButtonText = State()
    EditButtonLink = State()
    StartEditButtonText = State()
    EditButtonsQuantity = State()
