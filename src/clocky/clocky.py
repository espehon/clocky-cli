#<--------------------- Dependencies --------------------------->
import argparse
from __init__ import __version__, timecard_file, timelog_file, default_break, target_hours, target_days, include_break
import json
import datetime
import copy
import time
import sys
import os

from colorama import Fore, init
init(autoreset=True)




if os.path.exists(timecard_file) == False: #Checks for timecard_file
    if timecard_file == "tutorial":
        print("\n\nWelcome to Clocky!\n\nTo begin, please open the clocky folder where ever you have this program installed.\n[Optional] Next, move the timecard.json and timelog.txt files to an easy access location like '~/.local/share/clocky/'.\nFinaly, open and update the __init__.py file so that timecard_file and timelog_file are set to the full path of the corresponding files.\n\nUse 'clocky -?' once done.\n")
    else:
        print(Fore.YELLOW + 'File: ' + timecard_file + " does not exist!\nPlease go to " + os.path.dirname(os.path.abspath(__file__)) + " and update __init__.py with correct file paths.")
    sys.exit(0)

if os.path.exists(timelog_file) == False: #Checks for timelog_file
    if timelog_file == "tutorial":
        print("\n\nWelcome to Clocky!\n\nTo begin, please open the clocky folder where ever you have this program installed.\n[Optional] Next, move the timecard.json and timelog.txt files to an easy access location like '~/.local/share/clocky/'.\nFinaly, open and update the __init__.py file so that timecard_file and timelog_file are set to the full path of the corresponding files.\n\nUse 'clocky -?' once done.\n")
    else:
        print(Fore.YELLOW + timelog_file + " does not exist!\nPlease go to " + os.path.dirname(os.path.abspath(__file__)) + " and update __init__.py with correct file paths.")
    sys.exit(0)

#<---------------------- Variables ----------------------------->
with open(timecard_file, 'r') as f:
    data = json.load(f)
with open(timelog_file, 'r') as arch:
        whole_log = arch.readlines()
todays_date = str(datetime.datetime.now().date())
current_time = str(datetime.datetime.now().time().strftime("%H:%M"))
debug = False
parser = argparse.ArgumentParser(description='Clocky: A timecard program!\n\nArguments are mutually exclusive. (Except --debug)', epilog="Try 'clocky --demo' for demonstrations.", add_help=False)
cli = parser.add_mutually_exclusive_group()
sys.stdout.reconfigure(encoding='utf-8')


colour_codes = {'red': Fore.RED,
                'green': Fore.GREEN,
                'yellow': Fore.YELLOW,
                'blue': Fore.BLUE,
                'cyan': Fore.CYAN,
                'magenta': Fore.MAGENTA,
                'white': Fore.WHITE,
                'none': Fore.RESET,
                'light_red': Fore.LIGHTRED_EX,
                'light_blue': Fore.LIGHTBLUE_EX,
                'light_yellow': Fore.LIGHTYELLOW_EX,
                'light_cyan': Fore.LIGHTCYAN_EX,
                'light_black': Fore.LIGHTBLACK_EX,
                'light_green': Fore.LIGHTGREEN_EX,
                'light_white': Fore.LIGHTWHITE_EX,
                'light_magenta': Fore.LIGHTMAGENTA_EX
                }

#<---------------------- Arguments ----------------------------->
parser.add_argument('-?', '--help', action='help', help='Show this help message and exit.')

parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Print debug information.')

cli.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=__version__))

cli.add_argument('-m', dest='minutes', action='store_true', help='Show minutes remaining.')

cli.add_argument('-i', '--in', dest='in_flag', action='store_true', help='Clock in.')

cli.add_argument('-o', '--out', dest='out_flag', action='store_true', help='Clock out.')

cli.add_argument('-t', '--toggle', dest='toggle_flag', action='store_true', help='Clock in if out, clock out if in.')

cli.add_argument('-b', '--break', dest='_break', metavar='M', action='append', type=int, nargs='?', const=default_break, help='Clock out for [M] minutes and clock back in. (default: ' + str(default_break) + ')')

cli.add_argument('-l', '--log', metavar='N', action='append', type=int, nargs='?', const=7, help='Print log for last [N] days. (default: 7)')

cli.add_argument('-s', '--sum', metavar='N', action='append', type=int, nargs='?', const=0, help='Print summary for [N]th week ago. (default: 0)')

cli.add_argument('-g', '--graph', metavar='N', action='append', type=int, nargs='?', const=0, help='Print graphical summary for [N]th week ago. (default: 0)')

cli.add_argument('-c', '--chart', metavar='N', action='append', type=int, nargs='?', const=0, help='Print chart summary for [N]th week ago. (default: 0)')

cli.add_argument('-gc', '-cg', metavar='N', action='append', type=int, nargs='?', const=0, help='Combines graph and chart for [N]th week ago. (default: 0)')

cli.add_argument('-h', '--hist', metavar=('I', 'N'), action='append', nargs='+', help='Chart history for last [N] [I]ntervals. (D=days W=weeks)')

cli.add_argument('--demo', dest='demo', action='store_true', help=argparse.SUPPRESS)

cli.add_argument('--edit', metavar='D', action='append', nargs='?', const='no_date', help='Edit timecard for [D]ate. (YYYY-MM-DD)')


#<---------------------- Functions ----------------------------->
def set_debug(): #Sets debug flag to True for the rest of the script
    global debug
    debug = True
    sop("\n        < < <  D E B U G  > > >\n")

def print_vars(): #Prints variables for --debug
    sop("    -------Function Variables-------")
    sop("    debug             = " + str(debug))
    sop("    timecard_file     = " + timecard_file)
    sop("    timelog_file      = " + timelog_file)
    sop("    todays_date       = " + todays_date)
    sop("    current_time      = " + current_time)
    try:
        sop("    data[todays_date] = " + str(data[todays_date]))
    except:
        sop("    data[todays_date] = None")
    print()

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def sop(text="", colour="blue", r=False): # StdOut with ANSI colour escapes.
    output = f'{colour_codes[colour]}{text}{colour_codes["none"]}'
    if r == False:
        print(output)
    else:
        return output


def today_exists(key=todays_date): #Checks if there is an entry for given date and returns True if there is.
    if key in data:
        output = True
    else:
        output = False
    if debug == True:
        sop("    today_exists() called and returned " + str(output))
    return output

def create_entry(key=todays_date): #This adds the key, value pair for today (will overwrite todays value if already exists!).
    #global data
    if debug == True:
        sop("    create_entry() called")
    if key not in data:
        data[key] = {"hrs": 0, "time": "None"}
    update_timecard()

def valid_date(d): #Checks if 'd' is a valid date
    if d == 'no_date':
        print("No date given.")
        return False
    else:
        try:
            return str(datetime.datetime.strptime(d, "%Y-%m-%d").date())
        except ValueError:
            print("Not a valid date: '{0}'.".format(d))
            return False

def is_clocked_in(): #Checks if there is a punch in already and returns True if there is.
    if data[todays_date]['time'] == "None":
        output = False
    else:
        output = True
    if debug == True:
        sop("    is_clocked_in() called and returned " + str(output))
    return output

def progressbar(it, prefix="", sufix=""): #progressbar -->  prefix: [############################.............................] i/it
    size = abs(os.get_terminal_size()[0] - len(prefix) - len(sufix) - 16)
    count = len(it)
    def show(j):
        x = int(size*j/count)
        sys.stdout.write("%s[%s%s] %i ← %i %s  \r" % (prefix, "#"*x, "."*(size-x), j, (count-j), sufix))
        sys.stdout.flush()
    show(0) #This prints the progressbar at 0 progress. Then next for loop renders the rest (stating at 1)
    for i, item in enumerate(it): #This is the 'i' in the comment on the 'def' line
        yield item
        show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()

def clock_in(): #Replaces todays time stamp with current_time.
    if debug == True:
        sop("    clock_in() called")
    if is_clocked_in() == False:
        if data[todays_date]['time'] == 'None' and data[todays_date]['hrs'] == 0.00: #Checks for first punch of the day
            first_punch = True
        else:
            first_punch = False
        data[todays_date]['time'] = current_time
        add_timestamp(current_time, "Clocked In")
        update_timecard()
        sop("\n[" + current_time + "] You are now clocked in.", colour='light_cyan')
        if first_punch == True:
            if include_break == True:
                target_time = datetime.datetime.now() + datetime.timedelta(hours=target_hours)
                target_time = target_time.strftime("%H:%M")
                output = sop('│ Working to ', colour='cyan', r=True) + sop(str(target_time), colour='light_magenta', r=True) + sop(' will put you at ', colour='cyan', r=True) + sop(str(target_hours), colour='light_green', r=True) + sop(' hours │', colour='cyan', r=True)
                output = sop('┌' + ('─'*(len(output)-51)) + '┐\n', colour='cyan', r=True) + output + sop('\n└' + ('─'*(len(output)-51)) + '┘', colour='cyan', r=True)
                print(output)
            else:
                target_time = datetime.datetime.now() + datetime.timedelta(minutes=default_break) + datetime.timedelta(hours=target_hours)
                target_time = target_time.strftime("%H:%M")
                output = sop('│ Working to ', colour='cyan', r=True) + sop(str(target_time), colour='light_magenta', r=True) + sop(' with a ', colour='cyan', r=True) + sop(str(default_break), colour='light_green', r=True) + sop(' minute break will put you at ', colour='cyan', r=True) + sop(str(target_hours), colour='light_green', r=True) + sop(' hours │', colour='cyan', r=True)
                output = sop('┌' + ('─'*(len(output)-71)) + '┐\n', colour='cyan', r=True) + output + sop('\n└' + ('─'*(len(output)-71)) + '┘', colour='cyan', r=True)
                print(output)
    else:
        sop("\nYou are already clocked in.", colour='light_red')
        print(last_timestamp())

def get_hrs(first_T, second_T): #Finds the number of hours between 2 times (second_T chronologically after first_T).
    T1 = datetime.datetime.strptime(first_T, '%H:%M')
    T2 = datetime.datetime.strptime(second_T, '%H:%M')
    H1 = T1.hour + (T1.minute / 60)
    H2 = T2.hour + (T2.minute / 60)
    hrs = round(H2 - H1, 2)
    if debug == True:
        sop("    get_hrs(" + first_T + ", " + second_T + ") called and returned " + str(hrs))
    return(hrs)

def clock_out(): #Finds the difference between the last time stamp and current_time; then adds it to the hrs.
    if debug == True:
        sop("    clock_out() called")
    if is_clocked_in() == True:
        #global data
        hrs = round(get_hrs(data[todays_date]['time'], current_time), 2)
        data[todays_date]['hrs'] = round(data[todays_date]['hrs'] + hrs, 2)
        data[todays_date]['time'] = "None"
        add_timestamp(current_time, "Clocked Out", hrs)
        update_timecard()
        sop("\n[" + current_time + "] You are now clocked out.", colour='light_yellow')
        print("You were clocked in for " + str(hrs) + " hours.")
    else:
        sop("\nYou are not clocked in.", colour='light_red')
        print(last_timestamp())

def take_break(M): #clocks out for M minutes, then clocks back in
    padding_v = int((os.get_terminal_size()[1] / 3)) # <-- Divide the console vertically by 1 / X
    padding_h = int((os.get_terminal_size()[0] / 2)) # <-- Divide the console horizontally by 1 / X
    msg1 = "<<< Clocked out for break >>>"
    msg2 = ("(" + str(M) + " minutes)")
    if debug == True:
        sop("    take_break() called")
    if is_clocked_in() == True:
        clock_out()
        try:
            if debug != True:
                clear()
                print("\n" * (padding_v + 4))
            print((" " * abs((padding_h-5) - int((len(msg1)/2)))) + msg1)
            print((" " * abs((padding_h-5) - int((len(msg2)/2)))) + msg2)
            print("\n" * abs(padding_v - 8))
            for s in progressbar(range(M), "Break: ", "(pass ← wait)"):
                time.sleep(60)
        except:
            print("\n[Progress interrupted]")
            print("\n" * padding_v)
        if debug == True:
            sop("    Updating current_time")
        global current_time #This lets the fuction update the variable so it can be used in other functions?
        current_time = str(datetime.datetime.now().time().strftime("%H:%M"))
        clock_in()
    else:
        print("\nYou are not clocked in.")
        print(last_timestamp())

def update_timecard(): #writes the new data stored in memory to file.
    with open(timecard_file, 'w') as tc:
        if debug == True:
            sop("    update_timecard() called")
            sop("        data[todays_date] = " + str(data[todays_date]))
            sop("        json.dump(data, timecard_file)")
        json.dump(data, tc)

def check_punch(): #Checks punch status and returns a string based on answer.
    if debug == True:
        sop("    check_punch() called")
    temp_data = copy.deepcopy(data) #Clones 'data' to keep it unchanged
    if temp_data[todays_date]['time'] == "None":
        fake_hrs = 0
    else:
        fake_hrs = round(get_hrs(temp_data[todays_date]['time'], current_time), 2)
    temp_data[todays_date]['hrs'] = temp_data[todays_date]['hrs'] + fake_hrs #Fake clocks out so today's hours can be live in case the date range covers today // bug updates data globaly
    hrs_remain = round(target_hours - temp_data[todays_date]['hrs'], 2)
    if hrs_remain > 0:
        if hrs_remain < 1:
            hrs_remain = "    " + str(round(hrs_remain * 60, 1)) + sop(text = " Minutes Remaining", colour = "cyan", r = True)
        else:
            hrs_remain = "    " + str(hrs_remain) + " Hours Remaining"
    else:
        hrs_remain = "    " + str(abs(hrs_remain)) + " Hours Over"
    if is_clocked_in() == True:
        hrs_ago = str(round(get_hrs(temp_data[todays_date]['time'], current_time), 2))
        print(sop("\nYou clocked in " + hrs_ago + " hours ago.    ", colour="light_blue", r=True) + sop("[Total: " + str(round(temp_data[todays_date]['hrs'], 2)) + "]", colour=colour_scale(temp_data[todays_date]['hrs']), r=True) + hrs_remain)
        print("Last entry: " + last_timestamp())
        #print("Last entry: " + last_timestamp())
    else:
        #sop("\nYou are not clocked in.    [Total: " + str(round(temp_data[todays_date]['hrs'], 2)) + "]    Last punch: " + last_timestamp(), colour='yellow')
        print(sop("\nYou are not clocked in.    ", colour="yellow", r=True) + sop("[Total: " + str(round(temp_data[todays_date]['hrs'], 2)) + "]", colour=colour_scale(temp_data[todays_date]['hrs']), r=True) + hrs_remain)
        print("Last entry: " + last_timestamp())
        #print("Last punch: " + last_timestamp())

def show_minutes():
    if debug == True:
        sop("    show_minutes() called")
    width = 96
    minPerHash = int((target_hours * 60) / width) # minutes per hash (how many minutes does one hash represent)
    temp_data = copy.deepcopy(data) #Clones 'data' to keep it unchanged
    if temp_data[todays_date]['time'] == "None":
        fake_hrs = 0
    else:
        fake_hrs = round(get_hrs(temp_data[todays_date]['time'], current_time), 2)
    temp_data[todays_date]['hrs'] = temp_data[todays_date]['hrs'] + fake_hrs #Fake clocks out so today's hours can be live in case the date range covers today // bug updates data globaly
    numHashes = int((temp_data[todays_date]['hrs'] * 60) / minPerHash) # gets hours worked and coverts to minutes then scales to fit width
    bar = '['
    for char in range(1, numHashes):
        bar = bar + (f'\033[{colour_codes[colour_scale(char, (width))]}m' + "#" + '\033[0m')
    bar = bar + ("-" * (width - numHashes)) + "]"
    if debug == True:
        sop("        minPerHash = " + str(minPerHash))
        sop("        numHashes = " + str(numHashes))
        sop("        numHashes / " + str(width) + "(width)  = " + str(round(numHashes / width, 2)))

    print(bar)

    

def add_timestamp(time, event, hrs=None): #adds the current event to timelog_file.
    if debug == True:
        sop("    add_timestamp() called")
    part1 = "[" + str(todays_date) + " " + str(time) + "]"
    if len(part1) < 24:
        part1 += " " * (24 - len(part1))
    part2 = event
    if len(part2) < 24:
        part2 += " " * (24 - len(part2))
    if hrs == None:
        part3 = " " * 24
    else:
        part3 = "(" + str(hrs) + " Hours)"
    if len(part3) < 24:
        part3 += " " * (24 - len(part3))
    new_line = part1 + part2 + part3 + "\n"
    if debug == True:
        sop("        new_line = " + new_line.strip('\n'))
    with open(timelog_file, 'a') as arch:
        if debug == True:
            sop("        arch.write(new_line)")
        arch.writelines(new_line)

def last_timestamp(): #Returns the last line from timelog_file.
    try:
        last_line = whole_log[-1]
        return last_line[:-25]
    except:
        return("No log found...")

def print_timelog(days_ago): #Prints out the last n days of the timelog (n = days_ago).
    starting_date = datetime.date.today() - datetime.timedelta(days = days_ago)
    print("\nTimestamp               Event                   Duration                \n------------------------------------------------------------------------")
    for entry in whole_log:
        if datetime.datetime.strptime(entry[1:11], '%Y-%m-%d') < datetime.datetime.combine(starting_date, datetime.datetime.min.time()):
            pass
        else:
            print(entry.strip("\n"))

def chart(render_date, sym='='):
    data_temp = copy.deepcopy(data) #Clones 'data' to keep it unchanged
    if render_date == todays_date:
        if data_temp[todays_date]['time'] == "None":
            hrs = 0
        else:
            hrs = round(get_hrs(data_temp[todays_date]['time'], current_time), 2)
        data_temp[todays_date]['hrs'] = round(data_temp[todays_date]['hrs'] + hrs, 2) #Fake clocks out so today's hours can be live in case the date range covers today
    try:
        chars = int(round((data_temp[render_date]['hrs']*4), 0) - 1)
        output = '[' + (sym*chars) + "]    " + str(data_temp[render_date]['hrs']) + " hours"
    except:
        chars = 0
        output = '[]    0 hours'
    return output

def graph(render_date): # render_date <string> Prints 'Mon |----------■■■■■■■■■■■■■■--■■■■■■■■■■■■■■■-------------------|' for given date
    if debug == True:
        sop("    graph() called")
    edit_flag = False #Used to let user know that day was modified
    log = []
    for line in whole_log:
        if ("Edited[" + render_date) in line: #ignores edited entries
            edit_flag = True
            break
    for line in whole_log:
        if render_date in line:
            if "Edited" not in line:
                log.append(line)
    quarters = {}
    try: #Builds a Boolean array where each key is 1/4 of an hour
        if "Clocked In" in log[0]:
            for h in range(0, 96):
                quarters[str(0.25*h)] = False
                on_clock = False
        elif "Clocked Out" in log[0]:
            for h in range(0, 96):
                quarters[str(0.25*h)] = True
                on_clock = True
    except: #Catches days with no entries
        for h in range(0, 96):
            quarters[str(0.25*h)] = False
            on_clock = False
    log_dict = {}
    for line in log: #converts time_log data to a dict
        dec_hrs = str(round((float(line[12:14]) + float(line[15:17])/60)*4)/4)
        if "Clocked In" in line:
            log_dict[dec_hrs] = "in"
        elif "Clocked Out" in line:
            log_dict[dec_hrs] = "out"
    if render_date == todays_date: #Fake clocks out if render_date is today and user is clocked in
        if is_clocked_in() == True:
            dec_hrs = str(round((float(current_time[0:2]) + float(current_time[3:5])/60)*4)/4)
            log_dict[dec_hrs] = "out"
    for quarter in quarters: #Writes the clocked in/out data to the array 'quarters'
        for entry in log_dict:
            if entry == quarter:
                if log_dict[entry] == 'in':
                    on_clock = True
                elif log_dict[entry] == 'out':
                    on_clock = False
        quarters[quarter] = on_clock
    output = '|'
    for q in quarters: #Uses the array to draw the chart
        if quarters[q] == True:
            output = output + "■"
        if quarters[q] == False:
            output = output + "-"
    output = output + '|'
    if edit_flag == True:
        output = output + "    [Edited]"
    if debug == True:
        sop("    log_dict = " + str(log_dict))
        sop("    edit_flag = " + str(edit_flag))
    return output

def get_sunday(): #Simply returns the date object of last Sunday
    today = datetime.date.today()
    offset = (today.weekday() + 1) % 7
    last_sunday = today - datetime.timedelta(days=offset)
    if debug == True:
        sop("    get_sunday() called and returned " + last_sunday.strftime('%Y-%m-%d'))
    return last_sunday

def plot(weeks_ago, g=False, c=False): #Iterates over the week, rendering graphs and/or charts
    starting_date = get_sunday()
    offset = datetime.timedelta(days = (7 * weeks_ago))
    count = 1
    if g == True and c == False:
        title = "Graph"
        padding = " " * 24
    elif g == False and c == True:
        title = "Chart"
        padding = " " * 3
    else:
        title = "Plots"
        padding = " " * 24
    head = ['Sun ', 'Mon ', 'Tue ', 'Wed ', 'Thu ', 'Fri ', 'Sat ']
    print("\n\n\n" + padding + "<<< " + title + " for pay period ending " + str(starting_date - datetime.timedelta(days = (7 * weeks_ago) - 6)) + " >>>")
    headline = "0---1---2---3---4---5---6---7---8---9---X---E---D---1---2---3---4---5---6---7---8---9---X---E---"
    data_temp = copy.deepcopy(data) #Clones 'data' to keep it unchanged
    if data_temp[todays_date]['time'] == "None":
        hrs = 0
    else:
        hrs = round(get_hrs(data_temp[todays_date]['time'], current_time), 2)
    data_temp[todays_date]['hrs'] = round(data_temp[todays_date]['hrs'] + hrs, 2) #Fake clocks out so today's hours can be live in case the date range covers today
    hrs_list = [] #This is used for the average and total hrs calculation
    rounded_target_hours = int(round(target_hours, 0))
    if g == True and c == False: # -g
        print("     " + headline)
        for day in head:
            try:
                colour = colour_scale(data_temp[str(starting_date - offset)]['hrs'])
                hrs_list.append(data_temp[str(starting_date - offset)]['hrs'])
            except:
                colour = 'light_black'
            sop(day + graph(str(starting_date - offset)), colour)
            offset = datetime.timedelta(days = (7 * weeks_ago) - count)
            count += 1
            time.sleep(0.02)
        average = sum(hrs_list)/len(hrs_list)
        print((" "*41) + "\u001b[7m" + sop("[Average : " + str(round(average, 2)) + "]", colour=colour_scale(average), r=True) + "\u001b[0m")
        blocks = round(sum(hrs_list)*4)
        output = "\r" + (" "*(48-(int(rounded_target_hours*4))))
        day_count = 1
        carage = 0
        print()
        for block in range(1, (blocks + 1)):
            output = output + sop(" ■", colour=colour_scale(block, custom=(rounded_target_hours*20)), r=True)
            if block == blocks:
                output = output + sop(" [Total : " + str(round(sum(hrs_list), 2)) + "]", colour=colour_scale(block, custom=(rounded_target_hours*20)), r=True)
                sys.stdout.write(output)
                sys.stdout.flush()
                print("\n")
                break
            carage += 1
            if carage == (int(rounded_target_hours*4)):
                str_day_count = str(day_count)
                if day_count == target_days:
                    str_day_count = sop(str_day_count, colour="light_magenta", r=True)
                if day_count == 1:
                    output = output + "  " + str(str_day_count) + " (" + str(rounded_target_hours) + " Hr Days)\n"
                else:
                    output = output + "  " + str(str_day_count) + "\n"
                day_count += 1
                carage = 0
                sys.stdout.write(output)
                sys.stdout.flush()
                output = "\r" + (" "*(48-(int(rounded_target_hours*4))))
            else:
                sys.stdout.write(output)
                sys.stdout.flush()
            time.sleep(0.005)

    elif g == False and c == True: # -c
        headline = "\033[30;1m-----\033[0m"
        for char in range(1, 51):
            headline = headline + (f'\033[{colour_codes[colour_scale(char, (target_hours*4))]}m' + "-" + '\033[0m')
        print(headline)
        for day in head:
            try:
                colour = colour_scale(data_temp[str(starting_date - offset)]['hrs'])
                hrs_list.append(data_temp[str(starting_date - offset)]['hrs'])
            except:
                colour = 'light_black'
            sop(day + chart(str(starting_date - offset)), colour)
            offset = datetime.timedelta(days = (7 * weeks_ago) - count)
            count += 1
            time.sleep(0.01)
        print()
        average = sum(hrs_list)/len(hrs_list)
        sop("Avg [" + "#"*round(average*4) + "]    " + str(round(average, 2)) + " Hours", colour=colour_scale(average))
        print("\u001b[7m" + sop("[Total : " + str(round(sum(hrs_list), 2)) + "]", colour=colour_scale(sum(hrs_list), custom=(target_hours*5)), r=True) + "\u001b[0m")
        print()

    elif g == True and c == True: # -gc
        new_headline = "     "
        for ch in range(0, len(headline)):
            new_headline = new_headline + (f'\033[{colour_codes[colour_scale(ch, (target_hours*4))]}m' + headline[ch] + '\033[0m')
        print(new_headline)
        for day in head:
            try:
                colour = colour_scale(data_temp[str(starting_date - offset)]['hrs'])
                hrs_list.append(data_temp[str(starting_date - offset)]['hrs'])
            except:
                colour = 'light_black'
            sop(day + graph(str(starting_date - offset)), colour)
            sop("    " + chart(str(starting_date - offset)), colour)
            print()
            offset = datetime.timedelta(days = (7 * weeks_ago) - count)
            count += 1
            time.sleep(0.02)
        average = sum(hrs_list)/len(hrs_list)
        sop("Avg [" + "#"*round(average*4) + "]    " + str(round(average, 2)) + " Hours", colour=colour_scale(average))
        blocks = round(sum(hrs_list)*4)
        day_count = 1
        output = "\r "
        carage = 0
        line_1 = True
        carage_limit = (int(96/(rounded_target_hours*4))*rounded_target_hours*4)
        for block in range(1, (blocks + 1)):
            output = output + sop("■", colour=colour_scale(block, custom=(rounded_target_hours*20)), r=True)
            if block == blocks:
                output = output + sop(" [Total : " + str(round(sum(hrs_list), 2)) + " Hrs]", colour=colour_scale(block, custom=(rounded_target_hours*20)), r=True)
                sys.stdout.write(output)
                sys.stdout.flush()
                print()
                break
            carage += 1
            if carage % (rounded_target_hours*4) == 0:
                str_day_count = str(day_count)
                if day_count == target_days:
                    str_day_count = sop(str_day_count, colour="light_magenta", r=True)
                output = output + ":" + str(str_day_count) + " "
                day_count += 1
            if carage == (carage_limit):
                if line_1 == True:
                    output = output + "(" + str(rounded_target_hours) + " Hr Days)\n"
                    line_1 = False
                else:
                    output = output + "\n"
                carage = 0
                sys.stdout.write(output)
                sys.stdout.flush()
                output = "\r "
            else:
                sys.stdout.write(output)
                sys.stdout.flush()
            time.sleep(0.005)

def colour_scale(number, custom=False): #Returns colour based on input hours
    if custom == False:
        number = number/target_hours
    else:
        number = number/int(custom)
    if number < 0.125:
        return 'light_black'
    elif number < 0.3:
        return 'white'
    elif number < 0.5:
        return 'light_white'
    elif number < 0.622917:
        return 'blue'
    elif number < 0.747917:
        return 'light_blue'
    elif number < 0.872917:
        return 'light_cyan'
    elif number < 0.96875:
        return 'cyan'
    elif number < 0.989583:
        return 'green'
    elif number < 1.03125:
        return 'light_green'
    elif number < 1.122917:
        return 'light_yellow'
    elif number < 1.247917:
        return 'yellow'
    elif number < 1.372917:
        return 'light_red'
    elif number < 1.5:
        return 'magenta'
    else:
        return 'red'

def print_summary(weeks_ago): #Prints summary of N weeks ago, formatted with ascii box drawing characters
    starting_date = get_sunday()
    offset = datetime.timedelta(days = (7 * weeks_ago))
    data_temp = copy.deepcopy(data) #Clones 'data' to keep it unchanged
    if data_temp[todays_date]['time'] == "None":
        hrs = 0
    else:
        hrs = round(get_hrs(data_temp[todays_date]['time'], current_time), 2)
    data_temp[todays_date]['hrs'] = data_temp[todays_date]['hrs'] + hrs #Fake clocks out so today's hours can be live in case the date range covers today
    var_if_none = " "
    total_hrs = 0
    count = 1
    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    output = "\n <<< Summary for pay period ending " + str(starting_date - datetime.timedelta(days = (7 * weeks_ago) - 6)) + " >>> \n┌────────────────┬────────────────┬────────────────┐\n│     DAY        │     DATE       │     HOURS      │\n╞════════════════╪════════════════╪════════════════╡\n"
    for day in day_names:
        try: #This block will catch future dates
            output = (output
                    + "│ "
                    + day
                    + (" " * (15 - len(day)))
                    + "│ "
                    + str(starting_date - offset)
                    + (" " * (15 - len(str(starting_date - offset))))
                    + "│ "
                    + str(round(data_temp[str(starting_date - offset)]['hrs'], 2))
                    + (" " * (15 - len(str(round(data_temp[str(starting_date - offset)]['hrs'], 2)))))
                    + "│\n")
            total_hrs = total_hrs + data_temp[str(starting_date - offset)]['hrs']
        except: #This block handles rows with future dates
            output = (output
                    + "│ "
                    + day
                    + (" " * (15 - len(day)))
                    + "│ "
                    + str(starting_date - offset)
                    + (" " * (15 - len(str(starting_date - offset))))
                    + "│ "
                    + var_if_none
                    + (" " * (15 - len(var_if_none)))
                    + "│\n")
        if count < 7:
            output = output + "├────────────────┼────────────────┼────────────────┤\n"
        else:
            output = output + "└────────────────┴────────────────┴────────────────┘\n"
        offset = datetime.timedelta(days = (7 * weeks_ago) - count)
        count += 1
    output = output + "                            Total:  " + str(round(total_hrs, 2)) + (" " * (15 - len(str(round(total_hrs, 2))))) + " \n════════════════════════════════════════════════════\n"
    print(output)

def edit_entry(key, new_hrs): # key = [D]ate (YYYY-MM-DD), new_hrs = float(input(<user's input>))
    #global data
    if today_exists(key) == False:
        create_entry(key)
    if debug == True:
        sop("    edit_entry(" + str(key) + ", " + str(new_hrs) + ") called")
    old_hrs = round(data[key]['hrs'], 2)
    new_hrs = round(new_hrs, 2)
    data[key]['hrs'] = new_hrs
    update_timecard()
    add_timestamp(current_time, "Edited[" + key + "]", str(old_hrs) + " -> " + str(new_hrs))
    print("Edited[" + key + "]    " + str(old_hrs) + " -> " + str(new_hrs))

def demo():#prints a demo
    print('\n')
    print('┎─────────────────────────────── clocky [--in | --out ] ────────────────────────────────\n┃')
    time.sleep(0.25)
    if (int(current_time[-1]) % 2) == 0:
        print( "┃" + sop("[" + current_time + "] You are now clocked in.", colour='light_cyan', r=True) + " (Example only)")
    else:
        print("┃" + sop("[" + current_time + "] You are now clocked out.", colour='light_yellow', r=True) + " (Example only)")
    time.sleep(0.25)
    print("┃" + (" "*3) + '↑' + (" "*24) + '↑')
    time.sleep(0.25)
    print("┃ Current Time              Event")
    time.sleep(0.25)
    input("┃\n┃ (Press enter for next demo)")
    print("\n")
    print("┎──────────────────────────────────── clocky --break ───────────────────────────────────\n┃")
    time.sleep(0.25)
    print("┃ The '--break' option will clock you out for the specified time and show a progress bar for the duration of the break.")
    time.sleep(0.25)
    print("┃ Once the break is over, you will be clocked back in automatically.")
    time.sleep(0.25)
    print("┃ A keyboard interrupt will stop the break and clocky you back in as well.")
    time.sleep(0.25)
    print("┃")
    time.sleep(0.25)
    input("┃ (Press enter to see an example of the progress bar that is used for this function.)")
    time.sleep(0.25)
    print("┃")
    time.sleep(0.25)
    print("┃ " + sop("[Clocked out]", colour='light_yellow', r=True) + " (Example only)")
    time.sleep(0.25)
    print("┃")
    try:
        for s in progressbar(range(40), prefix='┃    Break :', sufix="(pass ← wait)"):
            time.sleep(0.05)
    except:
        print("\n┃ [Progress interrupted]")
    print("┃")
    time.sleep(0.25)
    print("┃ " + sop("[Clocked in]", colour='light_cyan', r=True) + " (Example only)")
    time.sleep(0.25)
    print("┃")
    time.sleep(0.25)
    input("┃ (Press enter for next demo)")
    print("\n")
    print("┎────────────────────────────── clocky [--chart | --graph] ─────────────────────────────\n┃")
    time.sleep(0.25)
    print("┃ These options will graphically display hours per day. The following is a '--chart' example.\n┃")
    cust_hrs = 32
    chars = int(current_time[-1])
    if chars == 0:
        chars = 10
    chars = chars + 18
    print("┃ Day 1" + sop('[' + ("="*(chars-1)) + ']', colour=colour_scale(chars, cust_hrs), r=True))
    time.sleep(0.25)
    chars = int(current_time[-2])
    if chars == 0:
        chars = 10
    chars = chars + 38
    print("┃ Day 2" + sop('[' + ("="*(chars-1)) + ']', colour=colour_scale(chars, cust_hrs), r=True))
    time.sleep(0.25)
    chars = int(current_time[-4])
    if chars == 0:
        chars = 10
    chars = chars + 28
    print("┃ Day 3" + sop('[' + ("="*(chars-1)) + ']', colour=colour_scale(chars, cust_hrs), r=True))
    time.sleep(0.25)
    print("┃")
    time.sleep(0.25)
    output = "┃ Scale\033[30;1m[\033[0m"
    for char in range(1, 49):
        output = output + (f'\033[{colour_codes[colour_scale(char, cust_hrs)]}m' + "=" + '\033[0m')
    output = output + '\033[31m]\033[0m'
    print(output)
    time.sleep(0.25)
    print("┃" + " "*38 + sop("↑", colour="light_green", r=True))
    time.sleep(0.25)
    print("┃" + " "*36 + sop("Target", colour="light_green", r=True))
    time.sleep(0.25)
    print("\n")
    time.sleep(0.25)
    print("(End of demo)")
    time.sleep(0.25)
    print()



################## < < <  M A I N  > > > ########################
def clocky(argv=None):
    args = parser.parse_args(argv) #Execute parse_args()
    def print_args(): #prints argparse values for --debug
        sop("    --------Argument Values---------")
        sop("    args.debug          " + str(args.debug))
        sop("    args.minutes        " + str(args.minutes))
        sop("    args.in_flag        " + str(args.in_flag))
        sop("    args.out_flag       " + str(args.out_flag))
        sop("    args.toggle_flag    " + str(args.toggle_flag))
        sop("    args._break         " + str(args._break))
        sop("    args.log            " + str(args.log))
        sop("    args.sum            " + str(args.sum))
        sop("    args.edit           " + str(args.edit))
        sop("    args.chart          " + str(args.chart))
        sop("    args.graph          " + str(args.graph))
        sop("    args.gc             " + str(args.gc))
        sop("    args.hist           " + str(args.hist))
        sop("    args.demo           " + str(args.demo))
        print()

    if args.debug == True: # --debug info
        set_debug()
        print_args()
        print_vars()
        sop("    -----------Main Logic-----------")

    if args.debug == True:
        sop("    Checking if entry for today exists...")
    if today_exists() == False: #Add today's entry if none
        create_entry()
    
    if args.minutes == True: #clocky -m
        if args.debug == True:
            sop("\n    Argument -m passed...")
        show_minutes()

    elif args.in_flag == True: #clocky -i
        if args.debug == True:
            sop("\n    Argument --in passed...")
        clock_in()

    elif args.out_flag == True: #clocky -o
        if args.debug == True:
            sop("\n    Argument --out passed...")
        clock_out()

    elif args.toggle_flag == True: #clocky -t
        if args.debug == True:
            sop("\n    Argument --toggle passed...")
        if is_clocked_in() == True:
            clock_out()
        else:
            clock_in()

    elif args._break != None: #clocky -b [M]
        if args.debug == True:
            sop("\n    Argument --break passed...")
        take_break(args._break[0])

    elif args.log != None: #clocky -l [N]
        if args.debug == True:
            sop("\n    Argument --log passed...")
        print_timelog(args.log[0])

    elif args.sum != None: #clocky -s [N]
        if args.debug == True:
            sop("\n    Argument --sum passed...")
        print_summary(args.sum[0])

    elif args.graph != None: #clocky -g [N]
        if args.debug == True:
            sop("\n    Argument --graph passed...")
        plot(args.graph[0], g=True)

    elif args.chart != None: #clocky -c [N]
        if args.debug == True:
            sop("\n    Argument --chart passed...")
        plot(args.chart[0], c=True)

    elif args.gc != None: #clocky -gc [N]
        if args.debug == True:
            sop("\n    Argument -gc passed...")
        plot(args.gc[0], g=True, c=True)

    elif args.edit != None: #clocky -e [D]
        edit_date = str(valid_date(args.edit[0]))
        if edit_date == 'False':
            pass
        else:
            if debug == True:
                sop("    " + edit_date + " == " + todays_date + "?")
                sop("        " + str(edit_date == todays_date))
            if edit_date == todays_date: #Catch editing today's entry
                if is_clocked_in() == True:
                    clock_out() #just to be safe
                    sop("You were clocked out in order to edit today's entry.", colour='light_yellow')
            new_hrs = float(input("Enter hours for " + edit_date + " : "))
            edit_entry(edit_date, new_hrs)
            if edit_date == todays_date:
                time.sleep(2) #Helps get the users attention
                sop("\nToday's entry as been modified. Clock in to continue logging time for today\n", colour='light_magenta')
    
    elif args.demo == True:
        demo()

    else: #clocky [default]
        if args.debug == True:
            sop("\n    No argument passed...")
        check_punch()

    if args.debug == True: # --debug info
        sop("    ----------End of File-----------")