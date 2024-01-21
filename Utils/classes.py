from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
                self.keyboard.button(text="⬅️",
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
                self.keyboard.button(text="➡️",
                                     callback_data=self.button_page(
                                         user_id=user_id,
                                         page=page + 1))
            else:
                self.keyboard.button(text="First Page",
                                     callback_data=self.button_page(
                                         user_id=user_id,
                                         page=1))
        if self.button_back is not None:
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


class CallbackClasses:
    class EmptyCallback(CallbackData, prefix="empty"):
        pass

    class QuitCallback(CallbackData, prefix="quit"):
        pass

    class AdminCallbacks:
        class AddAdminsCallback(CallbackData, prefix="add_admins"):
            user_id: int

        class AddAdminDoneCallback(CallbackData, prefix="add_admin_done"):
            user_id: int
            page: int

        class AddAdminPageCallback(CallbackData, prefix="add_admin_page"):
            user_id: int
            page: int

        class AdminEnterLinkCallback(CallbackData, prefix="admin_enter_link"):
            user_id: int

        class AdminAcceptRequest(CallbackData, prefix="admin_accept_request"):
            user_id: int
            channel_id: int

        class AdminDeclineRequest(CallbackData, prefix="admin_decline_request"):
            user_id: int

        class AdminRemoveAdmin(CallbackData, prefix="admin_remove_admin"):
            user_id: int

        class ChannelRemoveAdmin(CallbackData, prefix="channel_remove_admin"):
            user_id: int
            channel_id: int

        class AdminRemoveAdminDone(CallbackData, prefix="admin_remove_admin_done"):
            user_id: int
            channel_id: int
            admin_id: int

        class AdminRemoveAdminPage(CallbackData, prefix="admin_remove_admin_page"):
            user_id: int
            channel_id: int
            page: int

        class AdminChannelRemoveAdminPage(CallbackData, prefix="admin_channel_remove_admin_page"):
            user_id: int
            page: int

    class ChannelCallbacks:
        class EditChannelsCallback(CallbackData, prefix="edit_channels"):
            user_id: int

        class AddChannelCallback(CallbackData, prefix="add_channel"):
            user_id: int

        class RemoveChannelCallback(CallbackData, prefix="remove_channel"):
            user_id: int

        class AddChannelDoneCallback(CallbackData, prefix="add_channel_done"):
            user_id: int

        class RemoveChannelDoneCallback(CallbackData, prefix="remove_channel_done"):
            user_id: int
            channel_id: int

        class RemovePageCallback(CallbackData, prefix="page"):
            user_id: int
            page: int

        class GetChannelRequestLink(CallbackData, prefix="get_channel_request_link"):
            user_id: int
            channel_id: int

        class EditChannelPageCallback(CallbackData, prefix="edit_channel_page"):
            user_id: int
            page: int

        class EditChannelCallback(CallbackData, prefix="edit_channel"):
            user_id: int
            channel_id: int

    class EditSingleChannelCallbacks:
        class EditChannelDelayCallback(CallbackData, prefix="edit_channel_delay"):
            user_id: int
            channel_id: int

        class EditChannelDelayValue(CallbackData, prefix="edit_channel_delay_value"):
            user_id: int
            channel_id: int
            delay: int

        class EditChannelActiveCallback(CallbackData, prefix="edit_channel_active"):
            user_id: int
            channel_id: int

        class EditDelayStartPoint(CallbackData, prefix="edit_delay_start_point"):
            user_id: int
            channel_id: int

        class EditDelayMenu(CallbackData, prefix="edit_delay_menu"):
            user_id: int
            channel_id: int

        class SetDelay00(CallbackData, prefix="set_delay_00"):
            user_id: int
            channel_id: int

        class EditTemplate(CallbackData, prefix="edit_template"):
            user_id: int
            channel_id: int

        class EditTemplateValue(CallbackData, prefix="edit_template_value"):
            user_id: int
            channel_id: int

        class EditPostsNumberMenu(CallbackData, prefix="edit_posts_number"):
            user_id: int
            channel_id: int

        class EditPostsNumberValue(CallbackData, prefix="edit_posts_number_value"):
            user_id: int
            channel_id: int
            posts_number: int

        class EditEnhanceLinks(CallbackData, prefix="edit_enhance_links"):
            user_id: int
            channel_id: int

    class SettingsCallbacks:
        class SettingsMenuCallback(CallbackData, prefix="settings_menu"):
            user_id: int

    class CommandCallbacks:
        class CancelCallback(CallbackData, prefix="cancel"):
            user_id: int

    class PostCallbacks:
        class ChooseChannelCallback(CallbackData, prefix="choose_channel"):
            user_id: int
            channel_id: int
            page: int

        class ChannelsMenuCallback(CallbackData, prefix="channels_menu"):
            user_id: int
            page: int

        class PostToQueue(CallbackData, prefix="to_queue"):
            user_id: int

        class PostNow(CallbackData, prefix="post_now"):
            user_id: int

        class SelectAll(CallbackData, prefix="select_all"):
            user_id: int
            page: int

    class MyPosts:
        class MyPostsMenu(CallbackData, prefix="my_posts_menu"):
            user_id: int
            page: int

        class DeletePost(CallbackData, prefix="delete_post"):
            user_id: int
            page: int
            post_id: int

        class PostNow(CallbackData, prefix="post_now"):
            user_id: int
            page: int
            post_id: int

        class EditChannels(CallbackData, prefix="edit_channels"):
            user_id: int
            page: int
            post_id: int

        class AddChannelToPost(CallbackData, prefix="update_post_channels"):
            user_id: int
            page: int
            post_id: int
            channel_id: int

        class RemoveChannelFromPost(CallbackData, prefix="remove_channel_from_post"):
            user_id: int
            page: int
            post_id: int
            channel_id: int

        class BackToMain(CallbackData, prefix="back_to_main"):
            user_id: int

    class AdminPanel(CallbackData, prefix="admin_panel"):
        class GlobalMessage(CallbackData, prefix="global_message"):
            user_id: int

        class GlobalForward(CallbackData, prefix="global_forward"):
            user_id: int
