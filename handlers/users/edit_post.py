import urlextract
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.default import actions
from keyboards.default.edit_post_keys import edit_actions, back
from states.edit_post_state import EditPost
from utils.post_pickle.post_pickle import load_post, save_post

router = Router()


@router.message(F.text == "Редактирование")
async def start_editing(message: types.Message, state: FSMContext):
    await message.answer("Внимание! Вы выбрали изменение поста", reply_markup=edit_actions)
    await state.set_state(EditPost.EditPostState)
    temp_post = load_post()
    temp_post.calc_buttons()
    await state.update_data(temp_post=temp_post)


@router.message(F.text == "Просмотреть пост", EditPost.EditPostState)
async def view_temp_post(message: types.Message, state: FSMContext):
    data = await state.get_data()
    temp_post = data.get("temp_post")
    await message.answer_photo(photo=temp_post.photo_id, caption=temp_post.text,
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=temp_post.keyboard))
    await state.set_state(EditPost.EditPostState)


@router.message(F.text == "Отмена", EditPost.EditPostState)
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы отменили изменение поста", reply_markup=actions)


@router.message(F.text == "Сохранить", EditPost.EditPostState)
async def save_changes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    temp_post = data.get("temp_post")
    save_post(temp_post)
    await message.answer("Пост сохранен", reply_markup=actions)
    await state.clear()


@router.message(F.text == "Назад")
async def get_back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        return
    await state.set_state(EditPost.EditPostState)
    await message.answer("Вы вернулись назад", reply_markup=edit_actions)


@router.message(F.text == "Изменить количество кнопок в строке", EditPost.EditPostState)
async def start_change_buttons_quantity(message: types.Message, state: FSMContext):
    await message.answer("Введите новое число кнопок в строке")
    await state.set_state(EditPost.EditButtonsQuantity)


@router.message(EditPost.EditButtonsQuantity)
async def change_buttons_quantity(message: types.Message, state: FSMContext):
    quantity = message.text
    try:
        quantity = int(quantity)
    except ValueError:
        await message.answer("Введите целое положительное число")
        return
    if quantity <= 0:
        await message.answer("Введите целое положительное число")
        return
    data = await state.get_data()
    temp_post = data.get("temp_post")
    temp_post.buttons_in_row = quantity
    temp_post.calc_buttons()
    await state.set_state(EditPost.EditPostState)
    await message.answer("Количество кнопок в строке изменено", reply_markup=edit_actions)


@router.message(F.text == "Изменить текст поста", EditPost.EditPostState)
async def start_edit_text(message: types.Message, state: FSMContext):
    await message.answer("Введите новый текст", reply_markup=back)
    await state.set_state(EditPost.EditText)


@router.message(EditPost.EditText)
async def edit_text(message: types.Message, state: FSMContext):
    if message.text == "Убрать текст":
        text = None
    else:
        text = message.text
    data = await state.get_data()
    temp_post = data.get("temp_post")
    temp_post.text = text
    await state.update_data(temp_post=temp_post)
    await state.set_state(EditPost.EditPostState)
    await message.answer("Текст изменен", reply_markup=edit_actions)


@router.message(F.text == "Изменить фото", EditPost.EditPostState)
async def start_edit_photo(message: types.Message, state: FSMContext):
    await message.answer("Отправьте новое фото", reply_markup=back)
    await state.set_state(EditPost.EditPhoto)


@router.message(EditPost.EditPhoto)
async def edit_photo(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Отправьте фото")
        return
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    temp_post = data.get("temp_post")
    temp_post.photo_id = photo_id
    await state.update_data(temp_post=temp_post)
    await state.set_state(EditPost.EditPostState)
    await message.answer("Фото изменено", reply_markup=edit_actions)


@router.message(F.text == "Добавить кнопку", EditPost.EditPostState)
async def start_add_button(message: types.Message, state: FSMContext):
    await message.answer("Отправьте текст кнопки", reply_markup=back)
    await state.set_state(EditPost.AddButtonText)


@router.message(EditPost.AddButtonText)
async def add_button_text(message: types.Message, state: FSMContext):
    text = message.text
    await message.answer("Отправьте ссылку", reply_markup=back)
    await state.set_state(EditPost.AddButtonLink)
    await state.update_data(text=text)


@router.message(EditPost.AddButtonLink)
async def add_button_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    temp_post = data.get("temp_post")
    extractor = urlextract.URLExtract()
    urls = extractor.find_urls(message.text)
    if not urls:
        await message.answer("Ссылка некорректна, попробуйте еще раз", reply_markup=back)
        return
    url = urls[0]
    button = InlineKeyboardButton(text=text, url=url)
    temp_post.add_button(button)
    await state.update_data(temp_post=temp_post)
    await message.answer("Кнопка добавлена", reply_markup=edit_actions)
    await state.set_state(EditPost.EditPostState)


@router.message(F.text == "Удалить кнопку", EditPost.EditPostState)
async def start_delete_button(message: types.Message, state: FSMContext):
    await message.answer("Введите текст кнопки")
    await state.set_state(EditPost.DeleteButton)


@router.message(EditPost.DeleteButton)
async def delete_button(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    temp_post = data.get("temp_post")
    result = temp_post.delete_button(text)
    if result:
        await message.answer("Кнопка удалена", reply_markup=edit_actions)
    else:
        await message.answer("Кнопка не найдена", reply_markup=edit_actions)
    await state.set_state(EditPost.EditPostState)


@router.message(F.text == "Изменить кнопку", EditPost.EditPostState)
async def start_edit_button(message: types.Message, state: FSMContext):
    await state.set_state(EditPost.FindButtonText)
    print(await state.get_state())
    await message.answer("Отправьте текст кнопки", reply_markup=back)


@router.message(EditPost.FindButtonText)
async def find_button_text(message: types.Message, state: FSMContext):
    print("Зашли")
    text = message.text
    data = await state.get_data()
    temp_post = data.get("temp_post")
    index = temp_post.find_button(text)
    if index is None:
        await message.answer("Кнопка не найдена", reply_markup=edit_actions)
        await state.set_state(EditPost.EditPostState)
        return
    await state.update_data(old_text=text)
    await state.set_state(EditPost.EditButtonText)
    await message.answer("Отправьте новый текст", reply_markup=back)


@router.message(EditPost.EditButtonText)
async def edit_button_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await state.set_state(EditPost.EditButtonLink)
    await message.answer("Введите новую ссылку", reply_markup=back)


@router.message(EditPost.EditButtonLink)
async def edit_button_link(message: types.Message, state: FSMContext):
    extractor = urlextract.URLExtract()
    urls = extractor.find_urls(message.text)
    if not urls:
        await message.answer("Ссылка некорректна, попробуйте еще раз", reply_markup=back)
        return
    url = urls[0]
    data = await state.get_data()
    temp_post = data.get("temp_post")
    old_text = data.get("old_text")
    text = data.get("text")
    index = data.get("index")
    temp_post.edit_button(old_text, text, url)
    await state.update_data(temp_post=temp_post)
    await state.set_state(EditPost.EditPostState)
    await message.answer("Кнопка изменена", reply_markup=edit_actions)
