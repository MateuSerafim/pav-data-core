class VisualRegister():
    def __init__(self, id, image_url, lat, long, process_status, survey_id):
        self.id = id
        self.image_url = image_url
        self.lat = lat
        self.long = long
        self.process_status = process_status
        self.visual_survey_id = survey_id

        self.objects = None

    def load_objects_registers(self, registers):
        self.objects = registers
        return self