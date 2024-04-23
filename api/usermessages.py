from data.users import User


class UserMessages:

    def MissingFields(self):
        return "Отсутствуют обязательные поля"

    def UserRegistered(self, user: User):
        return f"Пользователь {user.full_name()} успешно зарегистрирован"

    def UserUpdated(self, user: User):
        return f"Учетная запись пользователя {user.full_name()} обновлена"

    def UserDeleted(self, user: User):
        return f"Учетная запись пользователя {user.full_name()} удалена"

    def UserUnknownSpec(self):
        return "Неизвестная специализация"

    def UserUnknown(self):
        return "Пользователь не найден"

    def UserNotAllowedAction(self):
        return "Недопустимая операция"

    def UserNotAuth(self):
        return "Недоступно для неавторизированных пользователей"

    def UserWrongHashPassword(self):
        return "Неверный тип шифрования пароля"

    def UserEmailExists(self):
        return "Пользователь с таким email уже зарегистрирован"
