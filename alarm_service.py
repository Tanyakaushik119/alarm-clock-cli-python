import datetime
import time
import uuid

from Domain.Infrastructure.clock import Clock
from Domain.Infrastructure.notifier import Notifier
from Domain.alarm import Alarm, JsonAlarmStore


class AlarmService:
    def __init__(
        self,
        store: JsonAlarmStore,
        clock: Clock,
        notifier: Notifier,
    ):
        self.store = store
        self.clock = clock
        self.notifier = notifier

    def add_alarm(self, trigger_time: str, message: str) -> Alarm:
        alarm_datetime = datetime.fromisoformat(trigger_time)

        alarm = Alarm(
            id=str(uuid.uuid4())[:8],
            trigger_time=alarm_datetime.isoformat(),
            message=message,
        )

        alarms = self.store.load()
        alarms.append(alarm)
        self.store.save(alarms)

        return alarm

    def list_alarms(self) -> list[Alarm]:
        return self.store.load()

    def delete_alarm(self, alarm_id: str) -> bool:
        alarms = self.store.load()

        filtered = [
            alarm
            for alarm in alarms
            if alarm.id != alarm_id
        ]

        deleted = len(filtered) != len(alarms)

        if deleted:
            self.store.save(filtered)

        return deleted

    def run_scheduler(self) -> None:
        print("Scheduler started...")
        print("Press CTRL+C to stop.\n")

        try:
            while True:
                alarms = self.store.load()
                now = self.clock.now()

                modified = False

                for alarm in alarms:
                    if (
                        alarm.enabled
                        and now >= alarm.trigger_datetime
                    ):
                        self.notifier.notify(alarm.message)
                        alarm.enabled = False
                        modified = True

                if modified:
                    self.store.save(alarms)

                time.sleep(1)

        except KeyboardInterrupt:
            print("\nScheduler stopped.")
