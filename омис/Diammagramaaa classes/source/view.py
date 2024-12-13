class ParcelInputView:
    def __init__(self):
        pass


class UserParcelView:
    def __init__(self):
        pass


class OperatorParcelView(UserParcelView):
    def __init__(self):
        super().__init__()


class LoginView:
    def __init__(self):
        pass

class ParcelCreatorView:
    def __init__(self):
        pass


class ViewsFactory:
    def __init__(self):
        pass

    def create_parcel_input_view(self) -> ParcelInputView:
        pass

    def create_parcel_view(self, is_operator) -> UserParcelView:
        pass

    def create_login_view(self) -> LoginView:
        pass

    def create_parcel_creator_view(self):
        pass