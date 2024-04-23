class AppointmentPatientsRequiredFields:
    def create_required_fields(self):
        return ["appointment_id", "patient_id"]

    def update_required_fields(self):
        return ["result"]