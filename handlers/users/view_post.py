from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup

from utils.post_pickle.post_pickle import load_post

router = Router()


@router.message(F.text == "Просмотр поста")
async def view_post(message: types.Message):
    current_post = load_post()
    current_post.calc_buttons()
    await message.answer_photo(photo=current_post.photo_id, caption=current_post.text,
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=current_post.keyboard))
