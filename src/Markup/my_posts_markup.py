from aiogram.utils.keyboard import InlineKeyboardBuilder

from Utils.classes import CallbackClasses, Keyboard
from Utils.functions import Post, Channel


class MyPosts:
    @staticmethod
    async def get_my_posts(user_id: int, page: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        posts = await Post.get_posts_by_user(user_id)
        if len(posts) == 0:
            keyboard.button(text="🔙Cancel", callback_data=CallbackClasses.QuitCallback())
            return keyboard

        if len(posts) < page:
            page_delete = 1
        else:
            page_delete = page

        keyboard.button(text="✏️Edit channels",
                        callback_data=CallbackClasses.MyPosts.EditChannels(
                            user_id=user_id,
                            post_id=posts[page - 1]["pk"],
                            page=1
                        )
                        )
        keyboard.button(text="➖Delete post",
                        callback_data=CallbackClasses.MyPosts.DeletePost(
                            user_id=user_id,
                            post_id=posts[page - 1][
                                "pk"],
                            page=page_delete
                        ))
        keyboard.button(text="✅Post now",
                        callback_data=CallbackClasses.MyPosts.PostNow(
                            user_id=user_id,
                            page=page_delete,
                            post_id=posts[page - 1]["pk"]
                        ))

        if page == 1:
            keyboard.button(text="Last page",
                            callback_data=CallbackClasses.MyPosts.MyPostsMenu(
                                user_id=user_id,
                                page=len(posts)
                            ))
        else:
            keyboard.button(text="⬅️",
                            callback_data=CallbackClasses.MyPosts.MyPostsMenu(
                                user_id=user_id,
                                page=page - 1
                            ))

        keyboard.button(text=f"{page}/{len(posts)}", callback_data=CallbackClasses.QuitCallback())

        if page == len(posts):
            keyboard.button(text="First page",
                            callback_data=CallbackClasses.MyPosts.MyPostsMenu(
                                user_id=user_id,
                                page=1
                            ))
        else:
            keyboard.button(text="➡️",
                            callback_data=CallbackClasses.MyPosts.MyPostsMenu(
                                user_id=user_id,
                                page=page + 1
                            ))
        keyboard.button(text="🔙Cancel",
                        callback_data=CallbackClasses.QuitCallback()
                        )
        keyboard.adjust(3, 3)
        return keyboard

    @staticmethod
    async def get_edit_channels_menu(user_id: int, post_id: int, page: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        post = await Post.get_post(post_id)
        user_channels = await Channel.get_channels_by_user_id(user_id)
        checked_channels = [await Channel.get_channel(channel["id"]) for channel in post["channels"]]
        channels = []
        for channel in user_channels:
            if channel in checked_channels:
                channels += [{"name": channel.channel_name, "id": channel.channel_id, "checked": True}]
            else:
                channels += [{"name": channel.channel_name, "id": channel.channel_id, "checked": False}]
        channels_set = [[channels[i:i + 6]] for i in range(0, len(channels), 6)]
        for channel_page in channels_set[page - 1]:
            for channel_obj in channel_page:
                if channel_obj["checked"]:
                    keyboard.button(text=f"✅{channel_obj['name']}",
                                    callback_data=CallbackClasses.MyPosts.RemoveChannelFromPost(
                                        user_id=user_id,
                                        post_id=post_id,
                                        channel_id=channel_obj["id"],
                                        page=page
                                    ))
                else:
                    channel_ids = [channel["id"] for channel in post["channels"]] + [channel_obj["id"]]
                    channel_ids = str(channel_ids)
                    keyboard.button(text=f"{channel_obj['name']}",
                                    callback_data=CallbackClasses.MyPosts.AddChannelToPost(
                                        user_id=user_id,
                                        post_id=post_id,
                                        channel_id=channel_obj["id"],
                                        page=page
                                    ))
        keyboard_adjuster = Keyboard(
            elements_set=channels_set,
            keyboard=keyboard,
            button_page=CallbackClasses.MyPosts.EditChannels,
            button_back=CallbackClasses.MyPosts.BackToMain
        )
        keyboard = keyboard_adjuster.get_keyboard(user_id=user_id, page=page)
        return keyboard
