import uuid

from ...utils.result import Result

class RoadStretch():
    def __init__(self, id: uuid.UUID, code: str, 
                 lat_initial: float, long_initial: float, 
                 lat_final: float, long_final: float):
        self.id = id
        self.code = code
        self.initial_point = [lat_initial, long_initial]
        self.final_point = [lat_final, long_final]
        self.visual_surveys = None
    
    def load_surveys(self, surveys):
        self.visual_surveys = surveys
        return self
    
    def get_last_visual_survey(self) -> Result:
        if self.visual_surveys == None or len(self.visual_surveys) == 0:
            return Result.failure("Nenhum levantamento realizado!")
        
        last_survey = self.visual_surveys.sort(key=lambda e: e.suyvey_date, reverse=True)[0]

        return Result.success(last_survey)
    
    def has_open_survey(self) -> bool:
        return self.visual_surveys != None \
            and any(vs.is_open for vs in self.visual_surveys)