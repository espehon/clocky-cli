__version__ = '1.12.1'

timecard_file = r"" # Example --> "C:/Users/User/.local/share/clocky/timecard.json"
timelog_file = r"" # Example --> "C:/Users/User/.local/share/clocky/timelog.json"

include_break = True # <-- Includes the default_break as time worked. Set to False if lunch is taken 'on the clock'
default_break = 15 # <-- Number of minutes. Best used as lunch duration
target_hours = 4 # <-- The number of hours you should be working. Use a positive integer for best results
target_days = 5 # <-- The number of days you should be working work