from aiogram.utils.keyboard import InlineKeyboardBuilder

from Utils.Functions import Channel
from Utils.classes import CallbackClasses


class SettingsMenu:
    @staticmethod
    def get_settings_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✏️Change post delay", callback_data=CallbackClasses.DelayCallback(user_id=user_id))
        keyboard.button(text="✏️Edit Channels", callback_data=CallbackClasses.EditChannelsCallback(user_id=user_id))
        keyboard.button(text="➕Admin Connect", callback_data=CallbackClasses.AddAdminsCallback(user_id=user_id))
        keyboard.button(text="❌Cancel", callback_data=CallbackClasses.CancelCallback(user_id=user_id))
        keyboard.adjust(3, 2)
        return keyboard


class AddChannelMenu:
    @staticmethod
    def add_channel_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="➕Add channel", callback_data=CallbackClasses.AddChannelCallback(user_id=user_id))
        keyboard.button(text="➖Remove channel", callback_data=CallbackClasses.RemoveChannelCallback(user_id=user_id))
        keyboard.button(text="🔙Back", callback_data=CallbackClasses.SettingsMenuCallback(user_id=user_id))
        return keyboard

    @staticmethod
    def add_process_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✅Done", callback_data=CallbackClasses.AddChannelDoneCallback(user_id=user_id))
        keyboard.button(text="🔙Back", callback_data=CallbackClasses.EditChannelsCallback(user_id=user_id))
        return keyboard


class RemoveChannelMenu:
    @staticmethod
    async def remove_channel_menu(user_id: int, page: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        channels = await Channel.get_channels_by_holder(user_id)
        channels_set = [[channels[i:i + 6]] for i in range(0, len(channels), 6)]
        for set_page in channels_set[page - 1]:
            for channel in set_page:
                keyboard.button(text=channel["name"],
                                callback_data=CallbackClasses.RemoveChannelDoneCallback(user_id=user_id,
                                                                                        channel_id=channel["id"]))
        if len(channels_set) > 1:
            if page != 1:
                keyboard.button(text="⬅️Previous",
                                callback_data=CallbackClasses.RemovePageCallback(user_id=user_id, page=page - 1))
            else:
                keyboard.button(text="Last Page",
                                callback_data=CallbackClasses.RemovePageCallback(user_id=user_id,
                                                                                 page=len(channels_set)))
            if page != len(channels_set):
                keyboard.button(text="➡️Next",
                                callback_data=CallbackClasses.RemovePageCallback(user_id=user_id, page=page + 1))
            else:
                keyboard.button(text="First Page",
                                callback_data=CallbackClasses.RemovePageCallback(user_id=user_id, page=1))

        keyboard.button(text="🔙Back", callback_data=CallbackClasses.EditChannelsCallback(user_id=user_id))
        if len(channels_set) == 1:
            if len(channels_set[0][0]) <= 3:
                keyboard.adjust(len(channels_set[0][0]), 1)
            elif len(channels_set[0][0]) <= 6:
                keyboard.adjust(3, len(channels_set[0][0]) - 3, 1)
            else:
                keyboard.adjust(3, 3, 1)
        else:
            if len(channels_set[page - 1][0]) <= 3:
                keyboard.adjust(len(channels_set[page - 1][0]), 2, 1)
            elif len(channels_set[page - 1][0]) <= 6:
                keyboard.adjust(3, len(channels_set[page - 1][0]) - 3, 2, 1)
            else:
                keyboard.adjust(3, 3, 2, 1)
        return keyboard


class AdminMenu:
    @staticmethod
    def get_admin_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="➕Add admin", callback_data=CallbackClasses.AddAdminDoneCallback(user_id=user_id, page=1))
        keyboard.button(text="➖Remove admin", callback_data=CallbackClasses.AddChannelDoneCallback(user_id=user_id))
        keyboard.button(text="🔙Back", callback_data=CallbackClasses.SettingsMenuCallback(user_id=user_id))
        return keyboard

    @staticmethod
    async def get_add_admin_menu(user_id: int, page: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        channels = await Channel.get_channels_by_holder(user_id) * 20
        channels_set = [[channels[i:i + 6]] for i in range(0, len(channels), 6)]
        for set_page in channels_set[page - 1]:
            for channel in set_page:
                keyboard.button(text=channel["name"],
                                callback_data=CallbackClasses.GetChannelRequestLink(user_id=user_id,
                                                                                    channel_id=channel["id"]))
        if len(channels_set) > 1:
            if page != 1:
                keyboard.button(text="⬅️Previous",
                                callback_data=CallbackClasses.AddAdminPageCallback(user_id=user_id, page=page - 1))
            else:
                keyboard.button(text="Last Page",
                                callback_data=CallbackClasses.AddAdminPageCallback(user_id=user_id,
                                                                                   page=len(channels_set)))
            if page != len(channels_set):
                keyboard.button(text="➡️Next",
                                callback_data=CallbackClasses.AddAdminPageCallback(user_id=user_id, page=page + 1))
            else:
                keyboard.button(text="First Page",
                                callback_data=CallbackClasses.AddAdminPageCallback(user_id=user_id, page=1))

        keyboard.button(text="🔙Back", callback_data=CallbackClasses.AddAdminsCallback(user_id=user_id))
        if len(channels_set) == 1:
            if len(channels_set[0][0]) <= 3:
                keyboard.adjust(len(channels_set[0][0]), 1)
            elif len(channels_set[0][0]) <= 6:
                keyboard.adjust(3, len(channels_set[0][0]) - 3, 1)
            else:
                keyboard.adjust(3, 3, 1)
        else:
            if len(channels_set[page - 1][0]) <= 3:
                keyboard.adjust(len(channels_set[page - 1][0]), 2, 1)
            elif len(channels_set[page - 1][0]) <= 6:
                keyboard.adjust(3, len(channels_set[page - 1][0]) - 3, 2, 1)
            else:
                keyboard.adjust(3, 3, 2, 1)
        return keyboard
