# event_scheduler.py

from datetime import datetime

class EventScheduler:
    def __init__(self):
        self.events = {}

    def schedule_event(self, date_str, event, is_birthday=False, is_recurring=False):
        if date_str not in self.events:
            self.events[date_str] = {"events": [], "is_birthday": is_birthday, "is_recurring": is_recurring}

        self.events[date_str]["events"].append(event)

    def check_birthdays_today(self, today_str):
        if today_str in self.events and self.events[today_str]["is_birthday"]:
            print("Birthday Today!")

    def check_events_today(self, today_str):
        if today_str in self.events:
            for event in self.events[today_str]["events"]:
                print(f"Event Today: {event}")

    def get_events_for_month(self, year, month):
        events_for_month = {}
        for date_str, data in self.events.items():
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if date.year == year and date.month == month:
                events_for_month[date.day] = ", ".join(data["events"])
        return events_for_month

    def save_events(self, filename):
        with open(filename, 'w') as file:
            for date_str, data in self.events.items():
                file.write(f"{date_str}|{data['is_birthday']}|{data['is_recurring']}|{','.join(data['events'])}\n")

    def load_events(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                date_str, is_birthday, is_recurring, *events = line.strip().split('|')
                self.events[date_str] = {"events": events, "is_birthday": is_birthday == 'True', "is_recurring": is_recurring == 'True'}

    def get_recurring_events_for_today(self, today_str):
        recurring_events = []
        for date_str, data in self.events.items():
            if data["is_recurring"] and today_str in self.get_recurring_dates(date_str):
                recurring_events.extend(data["events"])
        return recurring_events

    def get_recurring_dates(self, start_date):
        recurring_dates = []
        date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        current_date = date_obj
        while current_date <= datetime.now().date():
            recurring_dates.append(current_date.isoformat())
            current_date = self.get_next_recurring_date(current_date, date_obj)
        return recurring_dates

    def get_next_recurring_date(self, current_date, start_date):
        # Adjust this function according to your recurring event logic
        return current_date + timedelta(days=7)  # For weekly recurring events
