class VisualRegister():
    def __init__(self, id, image_url, lat, long, process_status, survey_id):
        self.id = id
        self.image_url = image_url
        self.lat = lat
        self.long = long
        self.process_status = process_status
        self.visual_survey_id = survey_id

        self.objects = []

    def load_objects_registers(self, registers):
        self.objects = registers
        return self
    
    def quant_item_by_class(self, item_class) -> int:
        return len([o for o in self.objects if o.class_type.value == item_class])