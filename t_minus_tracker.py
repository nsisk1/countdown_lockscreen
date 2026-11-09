#!/usr/bin/env python3
"""
T-Minus Pacing & Telemetry Tracker
Tracks daily and weekly progress toward a 40-hour work week by Friday.
Calculates exact remaining hours, intra-day check-in milestones, and generates an .ics calendar file.
"""

from datetime import datetime, date, time, timedelta

class TMinusTracker:
    def __init__(self, target_hours=40.0, start_date=date(2026, 11, 9), deadline_date=date(2026, 11, 13)):
        self.target_hours = target_hours
        self.start_date = start_date
        self.deadline_date = deadline_date
        self.days = [
            ("T-5D", "Monday", date(2026, 11, 9), 8.0, 40.0),
            ("T-4D", "Tuesday", date(2026, 11, 10), 8.0, 32.0),
            ("T-3D", "Wednesday", date(2026, 11, 11), 8.0, 24.0),
            ("T-2D", "Thursday", date(2026, 11, 12), 8.0, 16.0),
            ("T-1D", "Friday", date(2026, 11, 13), 8.0, 8.0),
        ]
        self.intraday_schedule = [
            ("T-8:00:00", time(8, 30), "Shift Launch & Deep Work Sprint 1"),
            ("T-6:00:00", time(10, 30), "2.0h Logged — 10m Micro-Break & Focus Sprint 2"),
            ("T-4:00:00", time(13, 0), "4.0h Logged (Midpoint) — Lunch & Midday Recharge"),
            ("T-2:00:00", time(15, 30), "6.0h Logged — Afternoon Final Sprint & Admin Wrap"),
            ("T-0:00:00", time(17, 30), "8.0h Daily Objective Completed — Time Logged"),
        ]

    def status_summary(self, hours_logged_so_far=0.0):
        hours_remaining = max(0.0, self.target_hours - hours_logged_so_far)
        pct_complete = (hours_logged_so_far / self.target_hours) * 100.0
        print("=" * 60)
        print(" T-MINUS 40-HOUR TELEMETRY DASHBOARD")
        print("=" * 60)
        print(f" Target Goal:      {self.target_hours:.1f} Hours by Friday")
        print(f" Hours Logged:     {hours_logged_so_far:.1f} Hours ({pct_complete:.1f}%)")
        print(f" Hours Remaining:  T-{hours_remaining:.1f} Hours")
        print("-" * 60)
        print(" WEEKLY MILESTONES:")
        for code, day_name, d_date, target_day, rem_start in self.days:
            rem_end = rem_start - target_day
            print(f"  [{code}] {day_name} ({d_date.strftime('%b %d')}): Target {target_day:.1f}h | Start: T-{rem_start:.1f}h -> End: T-{rem_end:.1f}h")
        print("-" * 60)
        print(" DAILY INTRA-DAY CHECK-IN TEMPLATE:")
        for t_code, t_val, desc in self.intraday_schedule:
            print(f"  {t_code} ({t_val.strftime('%I:%M %p')}): {desc}")
        print("=" * 60)

    def export_ics(self, output_path="t_minus_accountability.ics"):
        """Generates an RFC 5545 iCalendar file for calendar integration."""
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//T-Minus Milestone Tracker//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
        ]
        
        for code, day_name, d_date, target_day, rem_start in self.days:
            dt_start = datetime.combine(d_date, time(8, 30)).strftime("%Y%m%dT%H%M%S")
            dt_end = datetime.combine(d_date, time(9, 0)).strftime("%Y%m%dT%H%M%S")
            rem_end = rem_start - target_day
            uid = f"tminus-{d_date.strftime('%Y%m%d')}@gemini.local"
            
            lines.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
                f"DTSTART:{dt_start}",
                f"DTEND:{dt_end}",
                f"SUMMARY:[{code}] T-{rem_start:.0f}h Remaining — Target {target_day:.0f}h Today",
                f"DESCRIPTION:Daily accountability check-in. Target: {target_day:.0f}h. Projected end-of-day milestone: T-{rem_end:.0f}h remaining.",
                "STATUS:CONFIRMED",
                "END:VEVENT"
            ])
            
        lines.append("END:VCALENDAR")
        content = "\r\n".join(lines) + "\r\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Exported iCalendar schedule to: {output_path}")

if __name__ == "__main__":
    tracker = TMinusTracker()
    tracker.status_summary(hours_logged_so_far=0.0)
    tracker.export_ics("artifacts/file_generation/ttl=63d/output/t_minus_accountability.ics")