from aiogram.types import InlineKeyboardButton


class Post:
    def __init__(self, text, photo_id, all_buttons, buttons_in_row=1):
        self.buttons_in_row = buttons_in_row
        self.text = text
        self.photo_id = photo_id
        self.all_buttons = all_buttons
        self.keyboard = []

    def calc_buttons(self):
        keyboard = []
        rows_count = len(self.all_buttons) // self.buttons_in_row + 1
        for i in range(rows_count):
            keyboard.append([])
        current_button = 0
        for i in range(rows_count):
            for j in range(current_button,
                           current_button + min(self.buttons_in_row, len(self.all_buttons) - current_button)):
                keyboard[i].append(self.all_buttons[j])
                current_button += 1
        self.keyboard = keyboard

    def find_button(self, text):
        for i in range(len(self.all_buttons)):
            if self.all_buttons[i].text == text:
                return i
        return

    def delete_button(self, text):
        index = self.find_button(text)
        if not index:
            return False
        self.all_buttons.pop(index)
        self.calc_buttons()
        return True

    def add_button(self, button):
        self.all_buttons.append(button)
        if len(self.keyboard[-1]) < self.buttons_in_row:
            self.keyboard[-1].append(button)
        else:
            self.keyboard.append([button])

    def edit_button(self, text, new_text, url):
        index = self.find_button(text)
        if index is None:
            return False
        self.all_buttons[index] = InlineKeyboardButton(text=new_text, url=url)
        self.calc_buttons()