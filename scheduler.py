import datetime

from Domain.alarm import Alarm


class Scheduler:
    def is_due(
        self,
        alarm: Alarm,
        now: datetime
    ) -> bool:
        ...