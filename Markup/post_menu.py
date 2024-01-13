from aiogram.utils.keyboard import InlineKeyboardBuilder

from Utils.classes import CallbackClasses
from Utils.functions import User, Channel


class PostMenu:
    @staticmethod
    async def get_channels_menu(user_id: int, checked_channels_list: list, page: int = 1):
        user_obj = await User.get_user(user_id)
        channels_list = await Channel.filter_activated(user_obj.channel_id)
        keyboard = InlineKeyboardBuilder()
        if len(channels_list) != 0:
            if user_obj.channel_id != list(map(int, checked_channels_list)):
                select_text = "✅Select all"
            else:
                select_text = "❌Select all"

            keyboard.button(text=select_text, callback_data=CallbackClasses.PostCallbacks.SelectAll(
                user_id=user_id,
                page=page
            ))
        channels_set = [[channels_list[i:i + 6]] for i in range(0, len(channels_list), 6)]
        if len(channels_set) == 0:
            keyboard.button(text="🔙Back",
                            callback_data=CallbackClasses.QuitCallback())
            keyboard.adjust(1)
            return keyboard
        for channel in channels_set[page - 1]:
            for channel_id in channel:
                channel_obj = await Channel.get_channel(channel_id)
                if channel_obj.channel_id in checked_channels_list:
                    keyboard.button(text=f"✅{channel_obj.channel_name}",
                                    callback_data=CallbackClasses.PostCallbacks.ChooseChannelCallback(
                                        channel_id=channel_id,
                                        user_id=user_id,
                                        page=page
                                    ))
                else:
                    keyboard.button(text=f"❌{channel_obj.channel_name}",
                                    callback_data=CallbackClasses.PostCallbacks.ChooseChannelCallback(
                                        channel_id=channel_id,
                                        user_id=user_id,
                                        page=page))

        if len(channels_set) > 1:
            if page != 1:
                keyboard.button(text="⬅️Previous",
                                callback_data=CallbackClasses.PostCallbacks.ChannelsMenuCallback(
                                    user_id=user_id,
                                    page=page - 1))
            else:
                keyboard.button(text="Last Page",
                                callback_data=CallbackClasses.PostCallbacks.ChannelsMenuCallback(
                                    user_id=user_id,
                                    page=len(
                                        channels_set)))
            if page != len(channels_set):
                keyboard.button(text="➡️Next",
                                callback_data=CallbackClasses.PostCallbacks.ChannelsMenuCallback(
                                    user_id=user_id,
                                    page=page + 1))
            else:
                keyboard.button(text="First Page",
                                callback_data=CallbackClasses.PostCallbacks.ChannelsMenuCallback(
                                    user_id=user_id,
                                    page=1))

        keyboard.button(text="🔙Cancel",
                        callback_data=CallbackClasses.QuitCallback(user_id=user_id))
        if len(channels_set) == 1:
            if len(channels_set[0][0]) <= 3:
                keyboard.adjust(1, len(channels_set[0][0]), 2, 1)
            elif len(channels_set[0][0]) <= 6:
                keyboard.adjust(1, 3, len(channels_set[0][0]) - 3, 2, 1)
            else:
                keyboard.adjust(1, 3, 3, 1)
        else:
            if len(channels_set[page - 1][0]) <= 3:
                keyboard.adjust(1, len(channels_set[page - 1][0]), 2, 2, 1)
            elif len(channels_set[page - 1][0]) <= 6:
                keyboard.adjust(1, 3, len(channels_set[page - 1][0]) - 3, 2, 2, 1)
            else:
                keyboard.adjust(1, 3, 3, 2, 2, 1)

        keyboard.button(text=f"⏳To queue",
                        callback_data=CallbackClasses.PostCallbacks.PostToQueue(
                            user_id=user_id,
                        ))
        keyboard.button(text="✅Post now", callback_data=CallbackClasses.PostCallbacks.PostNow(
            user_id=user_id,
        ))
        return keyboard
