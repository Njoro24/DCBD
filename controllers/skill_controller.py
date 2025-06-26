from sqlalchemy.orm import Session
from models.skill import Skill
from typing import List, Dict

class SkillController:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def get_all_skills(self) -> List[Dict]:
        """
        Retrieve all skills from the database
        """
        skills = self.db.query(Skill).all()
        return [skill.to_dict() for skill in skills]
