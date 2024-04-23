class UserRequiredFields:
    def doctor_created_required_fields(self):
        return ["firstname", "lastname", "phone", "middlename", "specialization_id", "email",
                "hashed_password", "birthday", "location"]

    def doctor_update_required_fields(self):
        return ["firstname", "lastname", "phone", "middlename", "specialization_id",
                "hashed_password", "birthday", "location"]

    def patient_created_required_fields(self):
        return ["firstname", "lastname", "phone", "middlename", "polis", "email",
                "hashed_password", "birthday", "location"]

    def patient_update_required_fields(self):
        return ["firstname", "lastname", "middlename", "polis", "phone",
                "hashed_password", "birthday", "location"]
