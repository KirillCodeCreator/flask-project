class AppointmentMessages:

    def MissingFields(self):
        return "Отсутствуют обязательные поля"

    def AppointmentCreated(self):
        return f"Запись о приеме создана"

    def AppointmentCanceled(self):
        return f"Запись о приеме отменена"

    def AppointmentSaved(self):
        return f"Запись о приеме сохранена"

    def AppointmentUpdated(self):
        return f"Запись о приеме обновлена"

    def AppointmentDeleted(self):
        return f"Запись о приеме удалена"

    def AppointmentUnknownDoctor(self):
        return "Неизвестный доктор"

    def AppointmentUnknownPatient(self):
        return "Неизвестный пациент"

    def AppointmentUnknown(self):
        return "Запись о приеме не найдена"

    def AppointmentExists(self):
        return "Запись не может быть зарегистрирована, дата и время уже заняты"

    def AppointmentUnknownDateTime(self):
        return "Неверное дата или время приема"
