from app.models.activity_groups import ActivityGroup
from app.utils.database import get_db


class ActivityGroupsService:
    def __init__(self):
        self.cursor = get_db().cursor()
        self.columns = list(ActivityGroup.model_fields.keys())

    def get_all_activity_groups(self) -> list[ActivityGroup]:
        self.cursor.execute("SELECT * FROM activity_groups")
        rows = self.cursor.fetchall()
        activity_groups: list[ActivityGroup] = [
            ActivityGroup.model_validate(dict(zip(self.columns, row))) for row in rows
        ]
        return activity_groups
