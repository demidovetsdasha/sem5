from model import *
from view import *

class AccountLoginController:
    def __init__(self, loginView: LoginView, account_storage: AccountStorage, current_session: CurrentSession,
                 factory: AccountFactory):
        self.__loginView = loginView
        self.__account_storage = account_storage
        self.__current_session = current_session
        self.__factory = factory

    def __login(self):
        pass

    def __sign_in(self):
        pass


class ParcelTrackInputController:
    def __init__(self, parcel_input_view: ParcelInputView, parcel_storage: ParcelStorage, current_session: CurrentSession):
        self.__current_session = current_session
        self.__parcel_input_view = parcel_input_view
        self.__parcel_storage = parcel_storage

    def __find(self):
        pass

class UserParselViewController:
    def __init__(self, parcel: Parcel, parcel_view: UserParcelView):
        self.__parcel_view = parcel_view
        self.__parcel = parcel

    def __show(self):
        pass

class OperatorParcelViewController(UserParselViewController):
    def __init__(self, parcel_storage: ParcelStorage, parcel: Parcel, parcel_view: OperatorParcelView):
        super().__init__(parcel, parcel_view)
        self.__parcel_storage = parcel_storage

    def __edit_info(self):
        pass

    def __delete(self):
        pass


class ParcelCreatorController:
    def __init__(self, parcel_creator_view: ParcelCreatorView, parcel_storage: ParcelStorage, parcel_factory: ParcelFactory):
        self.__parcel_factory = parcel_factory
        self.__parcel_storage = parcel_storage
        self.__parcel_creator_view = parcel_creator_view

    def __create_parcel(self):
        pass


