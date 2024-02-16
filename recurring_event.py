from datetime import timedelta, date
from event_scheduler import EventScheduler
from plyer import notification  # Make sure to install plyer

class RecurringEventScheduler:
    def __init__(self, event_scheduler):
        self.event_scheduler = event_scheduler

    def schedule_recurring_event(self, event, start_date, end_date, frequency):
        current_date = start_date
        while current_date <= end_date:
            self.event_scheduler.schedule_event(current_date.isoformat(), event)
            current_date += timedelta(days=frequency)

    def check_recurring_events_today(self, today_str):
        recurring_events = self.event_scheduler.get_recurring_events_for_today(today_str)
        for event in recurring_events:
            notification.notify(
                title='Recurring Event Notification',
                message=f"Reminder: {event}",
                app_name='Desktop Calendar App',
                timeout=10
            )

if __name__ == "__main__":
    # Example usage:
    event_scheduler = EventScheduler()
    recurring_event_scheduler = RecurringEventScheduler(event_scheduler)

    # Schedule a weekly meeting for the next 4 weeks
    start_date = date.today()
    end_date = start_date + timedelta(weeks=4)
    recurring_event_scheduler.schedule_recurring_event("Weekly Meeting", start_date, end_date, frequency=7)

    # Schedule a monthly task for the next 6 months
    start_date = date.today()
    end_date = start_date + timedelta(weeks=4 * 6)
    recurring_event_scheduler.schedule_recurring_event("Monthly Task", start_date, end_date, frequency=30)

    # Check for recurring events today
    today_str = date.today().isoformat()
    recurring_event_scheduler.check_recurring_events_today(today_str)
