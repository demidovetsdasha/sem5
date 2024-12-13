class Saveable:
    @property
    def key(self):
        pass

    def load(self, data_saver):
        pass

    def save(self, data_saver):
        pass
            
        
class DataSaver:
    def __init__(self):
        pass

    def save(self, key, data):
        pass

    def load(self, key) -> object:
        pass


class ParcelIdentifier:
    def __init__(self):
        self.__tracks: list[str] = []
    
    def create_track(self) -> str:
        pass

    def clean_track(self, track: str):
        self.__tracks.remove(track)


class Parcel:
    def __init__(self, track: str, status: str, sender: str, getter: str, date: str):
        self.__track = track
        self.__status = status
        self.__sender = sender
        self.__getter = getter
        self.__date = date

    @property
    def track(self) -> str:
        return self.__track
    
    @property
    def status(self) -> str:
        return self.__status
    
    @property
    def sender(self):
        return self.__sender
    
    @property
    def getter(self):
        return self.__getter
    
    @property
    def date(self):
        return self.__date

    def change_status(self, new_status):
        self.__status = new_status

    def change_date(self, new_date):
        self.__date = new_date


class ParcelFactory:
    def __init__(self, parcel_indentifier: ParcelIdentifier):
        self.__parcel_Identifier = parcel_indentifier

    def create_parcel(self, sender, getter) -> Parcel:
        track = self.__parcel_Identifier.create_track()
        status = "Created"
        date = "NotDefined"

        return Parcel(track, status, sender, getter, date)
    

class ParcelStorage(Saveable):
    def __init__(self):
        self.__parcels: dict[str, Parcel] = {}

    @property
    def key(self) -> str:
        return "PARCEL_STORAGE"

    def add(self, parcel: Parcel):
        self.__parcels[parcel.track] = parcel

    def remove(self, parcel: Parcel):
        self.__parcels.remove(parcel)

    def find_parcel(self, track: str) -> Parcel:
        return self.__parcels[track]
            
    def load(self, data_saver: DataSaver):
        self.__parcels = data_saver.load(self.key)

    def save(self, data_saver: DataSaver):
        data_saver.save(self.key, self.__parcels)


class Account:
    def __init__(self, login: str, password: str):
        self.__login = login
        self.__password = password

    @property
    def login(self):
        return self.__login

    def try_autificate(self, password: str) -> bool:
        return password == self.__password


class AccountFactory:
    def __init__(self):
        pass

    def create_account(self, login, password) -> Account:
        return Account(login, password)
    

class AccountStorage(Saveable):
    def __init__(self):
        self.__accounts: dict[str, Account] = {}

    @property
    def key(self) -> str:
        return "ACCOUNT_STORAGE"

    def add(self, account: Account):
        self.__parcels[account.login] = account

    def find_account(self, login: str) -> Account:
        return self.__accounts[login]
            
    def load(self, data_saver: DataSaver):
        self.__accounts = data_saver.load(self.key)

    def save(self, data_saver: DataSaver):
        data_saver.save(self.key, self.__accounts)
        

class CurrentSession:
    def __init__(self):
        self.__account = None

    def is_authorised(self):
        return self.__account is not None
    
    def log_in(self, account):
        self.__account = account
    
    def log_out(self):
        self.__account = None