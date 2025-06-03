# TO_DO-Flask-app
# TIMETABLE Web App

A simple, modern web-based agenda and Pomodoro timer built with Flask and Bootstrap.  
Features a calendar view, daily task slots, and persistent storage in `task.json`.

---

## Features

- **Agenda View**: See all your tasks grouped by day.
- **Calendar Popup**: Click "Show Calendar" to view tasks on a monthly calendar (FullCalendar).
- **Daily View**: Click a date to see and manage tasks in 30-minute slots (like Outlook).
- **Add/Edit/Complete Tasks**: Inline editing and completion for each task.
- **Pomodoro Timer**: Built-in timer for productivity.
- **Persistent Storage**: All tasks are saved in `task.json`.
- **Responsive Design**: Works on desktop and mobile.

---

## Getting Started

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
python app.py
```

### 3. Open in Browser

Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## File Structure

- `app.py` — Flask backend
- `templates/index.html` — Main agenda and calendar view
- `templates/day.html` — Per-day slot/task view
- `task.json` — Persistent storage for tasks

---

## Customization

- **Slot Duration**: Change the `slot` query parameter for different time slot lengths.
- **Styling**: Edit the CSS in `index.html` for your own look.
- **Notifications**: Uses browser notifications for Pomodoro timer.

---

## Credits

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [FullCalendar](https://fullcalendar.io/)

---

## License

MIT License
