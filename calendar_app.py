import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import calendar
from datetime import date, datetime, timedelta
from event_scheduler import EventScheduler
from plyer import notification  # Make sure to install plyer

class RecurringEventScheduler:
    def __init__(self, event_scheduler):
        self.event_scheduler = event_scheduler

    def schedule_recurring_event(self, event, start_date, end_date, frequency):
        current_date = start_date
        while current_date <= end_date:
            self.event_scheduler.schedule_event(current_date.isoformat(), event, is_recurring=True)
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

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Calendar")

        self.selected_date = date.today()
        self.cal = calendar.TextCalendar()
        self.event_scheduler = EventScheduler()
        self.recurring_event_scheduler = RecurringEventScheduler(self.event_scheduler)

        self.create_widgets()

        # Check for birthdays, recurring events, and highlight present day when the app starts
        self.check_birthdays_today()
        self.recurring_event_scheduler.check_recurring_events_today(date.today().isoformat())
        self.highlight_present_day()

        # Set up alarm scheduler
        self.root.after(1000, self.check_events_today)  # Check events every second

    def create_widgets(self):
        self.month_label = ttk.Label(self.root, text="")
        self.month_label.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Date", "Event"), show="tree", selectmode="none")
        self.tree.heading("#0", text="Day")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Event", text="Event")

        self.tree.pack(padx=20, pady=10)

        self.update_calendar()

        self.next_month_button = ttk.Button(self.root, text="Next Month", command=self.next_month)
        self.next_month_button.pack(side=tk.RIGHT, padx=10)

        self.prev_month_button = ttk.Button(self.root, text="Previous Month", command=self.prev_month)
        self.prev_month_button.pack(side=tk.LEFT, padx=10)

        self.schedule_button = ttk.Button(self.root, text="Schedule Event", command=self.schedule_event)
        self.schedule_button.pack(pady=10)

        self.delete_button = ttk.Button(self.root, text="Delete Event", command=self.delete_event)
        self.delete_button.pack(pady=10)

        self.save_button = ttk.Button(self.root, text="Save Events", command=self.save_events)
        self.save_button.pack(pady=10)

        self.load_button = ttk.Button(self.root, text="Load Events", command=self.load_events)
        self.load_button.pack(pady=10)

        self.set_alarm_button = ttk.Button(self.root, text="Set Alarm", command=self.set_alarm)
        self.set_alarm_button.pack(pady=10)

    def update_calendar(self):
        month_text = self.cal.formatmonth(self.selected_date.year, self.selected_date.month)
        self.month_label.config(text=month_text)

        self.tree.delete(*self.tree.get_children())

        events = self.event_scheduler.get_events_for_month(self.selected_date.year, self.selected_date.month)
        for day, event in events.items():
            tags = ()
            if datetime.now().date() == date(self.selected_date.year, self.selected_date.month, int(day)):
                tags = ("today",)
            if int(day) == datetime.now().day:
                tags += ("present_day",)
            self.tree.insert("", "end", text=day, values=(day, event), tags=tags)

    def next_month(self):
        if self.selected_date.month == 12:
            self.selected_date = self.selected_date.replace(year=self.selected_date.year + 1, month=1)
        else:
            self.selected_date = self.selected_date.replace(month=self.selected_date.month + 1)

        self.update_calendar()

    def prev_month(self):
        if self.selected_date.month == 1:
            self.selected_date = self.selected_date.replace(year=self.selected_date.year - 1, month=12)
        else:
            self.selected_date = self.selected_date.replace(month=self.selected_date.month - 1)

        self.update_calendar()

    def schedule_event(self):
        date_prompt = "Enter date (YYYY-MM-DD):"
        date_str = self.get_input_from_dialog(date_prompt)
        if date_str:
            try:
                event_date = date.fromisoformat(date_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                return

            if self.selected_date.month == event_date.month:
                event_prompt = "Enter event/task:"
                event = self.get_input_from_dialog(event_prompt)
                is_birthday = messagebox.askyesno("Birthday", "Is this a birthday?")
                is_recurring = messagebox.askyesno("Recurring Event", "Is this a recurring event?")
                if event:
                    self.event_scheduler.schedule_event(date_str, event, is_birthday, is_recurring)
                    messagebox.showinfo("Scheduled", f"Event scheduled on {date_str}: {event}")
                    self.update_calendar()
            else:
                messagebox.showerror("Error", "Selected date is not in the current month.")

    def delete_event(self):
        date_prompt = "Enter date to delete (YYYY-MM-DD):"
        date_str = self.get_input_from_dialog(date_prompt)
        is_birthday = messagebox.askyesno("Birthday", "Is this a birthday?")
        if date_str:
            self.event_scheduler.delete_event(date_str, is_birthday)
            messagebox.showinfo("Deleted", f"Event on {date_str} deleted.")
            self.update_calendar()

    def save_events(self):
        filename = simpledialog.askstring("Save Events", "Enter filename to save events:")
        if filename:
            self.event_scheduler.save_events(filename)
            messagebox.showinfo("Saved", f"Events saved to {filename}.")

    def load_events(self):
        filename = simpledialog.askstring("Load Events", "Enter filename to load events:")
        if filename:
            self.event_scheduler.load_events(filename)
            messagebox.showinfo("Loaded", f"Events loaded from {filename}.")
            self.update_calendar()

    def set_alarm(self):
        alarm_time = self.get_input_from_dialog("Enter alarm time (HH:MM AM/PM):")
        alarm_event = self.get_input_from_dialog("Enter alarm event:")
        if alarm_time and alarm_event:
            # Add logic to set an alarm using the chosen time and event details
            print(f"Alarm set for {alarm_time}: {alarm_event}")

    def get_input_from_dialog(self, prompt):
        user_input = simpledialog.askstring("Input", prompt)
        return user_input

    def check_birthdays_today(self):
        today_str = self.get_date_string(date.today().day)
        self.event_scheduler.check_birthdays_today(today_str)

    def check_events_today(self):
        today_str = self.get_date_string(date.today().day)
        self.event_scheduler.check_events_today(today_str)
        self.root.after(1000, self.check_events_today)

    def get_date_string(self, day):
        return f"{self.selected_date.year}-{self.selected_date.month:02d}-{day:02d}"

    def highlight_present_day(self):
        present_day = datetime.now().day
        present_day_str = self.get_date_string(present_day)

        for item_id in self.tree.get_children():
            self.tree.item(item_id, tags=())

        for item_id in self.tree.get_children():
            item_date = self.tree.item(item_id, "text")
            if int(item_date) == present_day:
                self.tree.item(item_id, tags=("present_day",))
            elif datetime.now().date() == date(self.selected_date.year, self.selected_date.month, int(item_date)):
                self.tree.item(item_id, tags=("today",))

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
