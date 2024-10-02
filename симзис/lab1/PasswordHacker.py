import time

from PasswordGenerator import PasswordGenerator


class PasswordHacker:
    def __init__(self, password_generator: PasswordGenerator):
        self.__password_generator = password_generator

    def get_hack_time_of_password(self, password: str):
        start_time = time.time()
        new_password = self.__password_generator.generate_password(len(password))

        while(new_password != password):
            new_password = self.__password_generator.generate_password(len(password))

        end_time = time.time()

        return end_time - start_time
