from aiogram.filters.callback_data import CallbackData


class CallbackClasses:
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

    class DelayCallbacks:
        class DelayCallback(CallbackData, prefix="delay"):
            user_id: int

    class SettingsCallbacks:
        class SettingsMenuCallback(CallbackData, prefix="settings_menu"):
            user_id: int

    class CommandCallbacks:
        class CancelCallback(CallbackData, prefix="cancel"):
            user_id: int
