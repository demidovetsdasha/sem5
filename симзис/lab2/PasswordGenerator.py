import random


class PasswordGenerator:
    def generate_password(self, pass_len: int):
        password: list[chr] = []

        for _ in range(0, pass_len):
            password.append(self.__generate_random_char())

        return ''.join(password)

    def __generate_random_char(self):
            return chr(random.randint(65, 90))
