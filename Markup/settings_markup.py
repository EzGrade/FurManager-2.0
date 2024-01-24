from aiogram.utils.keyboard import InlineKeyboardBuilder

from Utils.classes import CallbackClasses
from Utils.classes import Keyboard
from Utils.functions import Channel


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
        channel_obj = await Channel.get_channel(channel_id)
        if channel_obj.active:
            active_text = "❌Disable"
        else:
            active_text = "✅Enable"

        if channel_obj.enhance_links:
            enhance_text = "❌Disable Enhance Links"
        else:
            enhance_text = "✅Enable Enhance Links"
        keyboard.button(text=active_text,
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelActiveCallback(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text=enhance_text,
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditEnhanceLinks(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text="✏️Change Posts Number",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditPostsNumberMenu(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text="⏳Edit Delay",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditDelayMenu(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text="✏️Edit Caption Template",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditTemplate(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text="🔙Back",
                        callback_data=CallbackClasses.ChannelCallbacks.EditChannelPageCallback(
                            user_id=user_id,
                            page=1
                        ))
        keyboard.adjust(2, 3, 1)
        return keyboard

    @staticmethod
    async def get_posts_number_menu(user_id: int, channel_id: int) -> InlineKeyboardBuilder:
        channel = await Channel.get_channel(channel_id)
        value = channel.posts_number
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="➖1",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditPostsNumberValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            posts_number=value - 1
                        ))
        keyboard.button(text=f"Current: {value}",
                        callback_data=CallbackClasses.EmptyCallback())
        keyboard.button(text="➕1",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditPostsNumberValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            posts_number=value + 1
                        ))
        keyboard.button(text="Set 1",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditPostsNumberValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            posts_number=1
                        ))
        keyboard.button(text="🔙Back",
                        callback_data=CallbackClasses.ChannelCallbacks.EditChannelCallback(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.adjust(3, 1, 1)
        return keyboard

    @staticmethod
    async def get_delay_main_menu(user_id: int, channel_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✏️Edit delay value",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayCallback(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text="🔄Set 00:00",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.SetDelay00(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text="🔄Set current time",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditDelayStartPoint(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text="🔙Back",
                        callback_data=CallbackClasses.ChannelCallbacks.EditChannelCallback(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.adjust(1, 2, 1)
        return keyboard

    @staticmethod
    async def get_delay_menu(user_id: int, channel_id: int) -> InlineKeyboardBuilder:
        curren_delay = await Channel.get_current_delay(channel_id)
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="➖10",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay - 10)
                        )
        keyboard.button(text="➕10",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay + 10)
                        )
        keyboard.button(text="➖5",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay - 5)
                        )
        keyboard.button(text="➕5",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay + 5)
                        )
        keyboard.button(text="➖1",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay - 1)
                        )
        keyboard.button(text="➕1",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue(
                            user_id=user_id,
                            channel_id=channel_id,
                            delay=curren_delay + 1)
                        )
        keyboard.button(text=f"Current: {curren_delay} minutes", callback_data=CallbackClasses.EmptyCallback())
        keyboard.button(text="🔙Back", callback_data=CallbackClasses.EditSingleChannelCallbacks.EditDelayMenu(
            user_id=user_id,
            channel_id=channel_id
        ))
        keyboard.adjust(2, 2, 2, 1)
        return keyboard

    @staticmethod
    async def get_template_menu(user_id: int, channel_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✏️Edit template",
                        callback_data=CallbackClasses.EditSingleChannelCallbacks.EditTemplateValue(
                            user_id=user_id,
                            channel_id=channel_id
                        ))
        keyboard.button(text="🔙Back", callback_data=CallbackClasses.ChannelCallbacks.EditChannelCallback(
            user_id=user_id,
            channel_id=channel_id
        ))
        keyboard.adjust(1, 2, 1)
        return keyboard


class AdminMenu:
    @staticmethod
    def get_admin_menu(user_id: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="✏️Enter Code",
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
            button_back=CallbackClasses.SettingsCallbacks.SettingsMenuCallback
        )
        return keyboard_adjuster.get_keyboard(user_id=user_id, page=page)
