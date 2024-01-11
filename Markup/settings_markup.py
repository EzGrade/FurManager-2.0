from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Utils.classes import CallbackClasses
from Utils.functions import Channel


class Keyboard:

    def __init__(
            self,
            elements_set: list,
            keyboard: InlineKeyboardBuilder,
            button_page: CallbackData,
            button_back: CallbackData
    ):
        self.elements_set = elements_set
        self.keyboard = keyboard
        self.button_page = button_page
        self.button_back = button_back

    # noinspection PyCallingNonCallable
    def get_keyboard(self, user_id: int, page: int) -> InlineKeyboardBuilder:
        if len(self.elements_set) > 1:
            if page != 1:
                self.keyboard.button(text="⬅️Previous",
                                     callback_data=self.button_page(
                                         user_id=user_id,
                                         page=page - 1))
            else:
                self.keyboard.button(text="Last Page",
                                     callback_data=self.button_page(
                                         user_id=user_id,
                                         page=len(
                                             self.elements_set)))
            if page != len(self.elements_set):
                self.keyboard.button(text="➡️Next",
                                     callback_data=self.button_page(
                                         user_id=user_id,
                                         page=page + 1))
            else:
                self.keyboard.button(text="First Page",
                                     callback_data=self.button_page(
                                         user_id=user_id,
                                         page=1))

        self.keyboard.button(text="🔙Back",
                             callback_data=self.button_back(user_id=user_id))
        if len(self.elements_set) == 1:
            if len(self.elements_set[0][0]) <= 3:
                self.keyboard.adjust(len(self.elements_set[0][0]), 1)
            elif len(self.elements_set[0][0]) <= 6:
                self.keyboard.adjust(3, len(self.elements_set[0][0]) - 3, 1)
            else:
                self.keyboard.adjust(3, 3, 1)
        else:
            if len(self.elements_set[page - 1][0]) <= 3:
                self.keyboard.adjust(len(self.elements_set[page - 1][0]), 2, 1)
            elif len(self.elements_set[page - 1][0]) <= 6:
                self.keyboard.adjust(3, len(self.elements_set[page - 1][0]) - 3, 2, 1)
            else:
                self.keyboard.adjust(3, 3, 2, 1)
        return self.keyboard


class SettingsMenu:
    @staticmethod
    def get_settings_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✏️Edit Channels",
                        callback_data=CallbackClasses.ChannelCallbacks.EditChannelsCallback(user_id=user_id))
        keyboard.button(text="➕Admin Connect",
                        callback_data=CallbackClasses.AdminCallbacks.AddAdminsCallback(user_id=user_id))
        keyboard.button(text="❌Cancel", callback_data=CallbackClasses.CommandCallbacks.CancelCallback(user_id=user_id))
        keyboard.adjust(2, 1)
        return keyboard


class AddChannelMenu:
    @staticmethod
    def add_channel_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✏️Edit channel",
                        callback_data=CallbackClasses.ChannelCallbacks.EditChannelPageCallback(user_id=user_id, page=1))
        keyboard.button(text="➕Add channel",
                        callback_data=CallbackClasses.ChannelCallbacks.AddChannelCallback(user_id=user_id))
        keyboard.button(text="➖Remove channel",
                        callback_data=CallbackClasses.ChannelCallbacks.RemoveChannelCallback(user_id=user_id))
        keyboard.button(text="🔙Back",
                        callback_data=CallbackClasses.SettingsCallbacks.SettingsMenuCallback(user_id=user_id))
        keyboard.adjust(1, 2, 1)
        return keyboard

    @staticmethod
    def add_process_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✅Done",
                        callback_data=CallbackClasses.ChannelCallbacks.AddChannelDoneCallback(user_id=user_id))
        keyboard.button(text="🔙Back",
                        callback_data=CallbackClasses.ChannelCallbacks.EditChannelsCallback(user_id=user_id))
        return keyboard


class RemoveChannelMenu:
    @staticmethod
    async def remove_channel_menu(user_id: int, page: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        channels = await Channel.get_channels_by_holder(user_id)
        channels_set = [[channels[i:i + 6]] for i in range(0, len(channels), 6)]
        if len(channels_set) == 0:
            keyboard.button(text="🔙Back",
                            callback_data=CallbackClasses.ChannelCallbacks.EditChannelsCallback(user_id=user_id))
            keyboard.adjust(1)
            return keyboard
        for set_page in channels_set[page - 1]:
            for channel in set_page:
                keyboard.button(text=channel["name"],
                                callback_data=CallbackClasses.ChannelCallbacks.RemoveChannelDoneCallback(
                                    user_id=user_id,
                                    channel_id=channel["id"]))

        keyboard_adjuster = Keyboard(
            elements_set=channels_set,
            keyboard=keyboard,
            button_page=CallbackClasses.ChannelCallbacks.RemovePageCallback,
            button_back=CallbackClasses.ChannelCallbacks.EditChannelsCallback
        )
        keyboard = keyboard_adjuster.get_keyboard(user_id=user_id, page=page)
        return keyboard


class EditChannelMenu:
    @staticmethod
    async def get_edit_channel_menu(user_id: int, page: int):
        keyboard = InlineKeyboardBuilder()
        channels = await Channel.get_channels_by_holder(user_id)
        channels_set = [[channels[i:i + 6]] for i in range(0, len(channels), 6)]
        if len(channels_set) == 0:
            keyboard.button(text="🔙Back",
                            callback_data=CallbackClasses.ChannelCallbacks.EditChannelsCallback(user_id=user_id))
            keyboard.adjust(1)
            return keyboard
        for set_page in channels_set[page - 1]:
            for channel in set_page:
                keyboard.button(text=channel["name"],
                                callback_data=CallbackClasses.ChannelCallbacks.EditChannelCallback(
                                    user_id=user_id,
                                    channel_id=channel["id"]))

        keyboard_adjuster = Keyboard(
            elements_set=channels_set,
            keyboard=keyboard,
            button_page=CallbackClasses.ChannelCallbacks.EditChannelPageCallback,
            button_back=CallbackClasses.ChannelCallbacks.EditChannelsCallback
        )
        return keyboard_adjuster.get_keyboard(user_id=user_id, page=page)


class EditSingleChannelMenu:
    @staticmethod
    async def get_main_menu(user_id: int, channel_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✏️Edit delay",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayCallback(
                            user_id=user_id, channel_id=channel_id))
        keyboard.button(text="🔙Back",
                        callback_data=CallbackClasses.ChannelCallbacks.EditChannelPageCallback(user_id=user_id, page=1))
        keyboard.adjust(1, 2, 1)
        return keyboard

    @staticmethod
    async def get_delay_menu(user_id: int, channel_id: int) -> InlineKeyboardBuilder:
        curren_delay = await Channel.get_current_delay(channel_id)
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="-10",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay - 10)
                        )
        keyboard.button(text="+10",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay + 10)
                        )
        keyboard.button(text="-5",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay - 5)
                        )
        keyboard.button(text="+5",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay + 5)
                        )
        keyboard.button(text=f"Current: {curren_delay}", callback_data=CallbackClasses.EmptyCallback())
        keyboard.button(text="🔙Back", callback_data=CallbackClasses.ChannelCallbacks.EditChannelCallback(
            user_id=user_id,
            channel_id=channel_id
        ))
        keyboard.adjust(2, 2, 1)
        return keyboard


class AdminMenu:
    @staticmethod
    def get_admin_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="➡️Enter Code",
                        callback_data=CallbackClasses.AdminCallbacks.AdminEnterLinkCallback(user_id=user_id))
        keyboard.button(text="➕Add admin",
                        callback_data=CallbackClasses.AdminCallbacks.AddAdminDoneCallback(user_id=user_id, page=1))
        keyboard.button(text="➖Remove admin",
                        callback_data=CallbackClasses.AdminCallbacks.AdminRemoveAdmin(user_id=user_id))
        keyboard.button(text="🔙Back",
                        callback_data=CallbackClasses.SettingsCallbacks.SettingsMenuCallback(user_id=user_id))
        keyboard.adjust(1, 2, 1)
        return keyboard

    @staticmethod
    async def get_add_admin_menu(user_id: int, page: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        channels = await Channel.get_channels_by_holder(user_id)
        if not channels:
            keyboard.button(text="🔙Back",
                            callback_data=CallbackClasses.AdminCallbacks.AddAdminsCallback(user_id=user_id))
            keyboard.adjust(1)
            return keyboard
        channels_set = [[channels[i:i + 6]] for i in range(0, len(channels), 6)]
        for set_page in channels_set[page - 1]:
            for channel in set_page:
                keyboard.button(text=channel["name"],
                                callback_data=CallbackClasses.ChannelCallbacks.GetChannelRequestLink(user_id=user_id,
                                                                                                     channel_id=channel[
                                                                                                         "id"]))

        keyboard_adjuster = Keyboard(
            elements_set=channels_set,
            keyboard=keyboard,
            button_page=CallbackClasses.AdminCallbacks.AddAdminPageCallback,
            button_back=CallbackClasses.AdminCallbacks.AddAdminsCallback
        )
        return keyboard_adjuster.get_keyboard(user_id=user_id, page=page)

    @staticmethod
    def accept_new_admin(user_id: int, channel_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✅Accept",
                        callback_data=CallbackClasses.AdminCallbacks.AdminAcceptRequest(user_id=user_id,
                                                                                        channel_id=channel_id))
        keyboard.button(text="❌Decline",
                        callback_data=CallbackClasses.AdminCallbacks.AdminDeclineRequest(user_id=user_id))
        return keyboard

    @staticmethod
    async def get_remove_admin_menu(user_id: int, page: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        channels = await Channel.get_channels_by_holder(user_id)
        if not channels:
            keyboard.button(text="🔙Back",
                            callback_data=CallbackClasses.AdminCallbacks.AddAdminsCallback(user_id=user_id))
            keyboard.adjust(1)
            return keyboard
        channels_set = [[channels[i:i + 6]] for i in range(0, len(channels), 6)]
        for set_page in channels_set[page - 1]:
            for channel in set_page:
                keyboard.button(text=channel["name"],
                                callback_data=CallbackClasses.AdminCallbacks.ChannelRemoveAdmin(
                                    user_id=user_id,
                                    channel_id=channel[
                                        "id"]))

        keyboard_adjuster = Keyboard(
            elements_set=channels_set,
            keyboard=keyboard,
            button_page=CallbackClasses.AdminCallbacks.AdminChannelRemoveAdminPage,
            button_back=CallbackClasses.AdminCallbacks.AddAdminsCallback
        )
        return keyboard_adjuster.get_keyboard(user_id=user_id, page=page)

    @staticmethod
    async def admins_to_remove_menu(user_id, channel_id, page):
        keyboard = InlineKeyboardBuilder()
        admins = await Channel.get_admins_by_channel(channel_id)
        if not admins:
            keyboard.button(text="🔙Back",
                            callback_data=CallbackClasses.AdminCallbacks.AdminRemoveAdmin(user_id=user_id))
            keyboard.adjust(1)
            return keyboard
        admins_set = [[admins[i:i + 6]] for i in range(0, len(admins), 6)]
        for set_page in admins_set[page - 1]:
            for admin in set_page:
                if admin["name"] != "Unknown":
                    keyboard.button(text=admin["name"],
                                    callback_data=CallbackClasses.AdminCallbacks.AdminRemoveAdminDone(user_id=user_id,
                                                                                                      channel_id=
                                                                                                      channel_id,
                                                                                                      admin_id=admin[
                                                                                                          "id"]))
                else:
                    keyboard.button(text=f'{admin["name"]}({admin["id"]})',
                                    callback_data=CallbackClasses.AdminCallbacks.AdminRemoveAdminDone(user_id=user_id,
                                                                                                      channel_id=channel_id,
                                                                                                      admin_id=admin[
                                                                                                          "id"]))
        keyboard_adjuster = Keyboard(
            elements_set=admins_set,
            keyboard=keyboard,
            button_page=CallbackClasses.AdminCallbacks.AdminRemoveAdminPage,
            button_back=CallbackClasses.AdminCallbacks.ChannelRemoveAdmin
        )
        return keyboard_adjuster.get_keyboard(user_id=user_id, page=page)
