
<p align="center">
<a href="https://pypi.org/project/clocky-cli/">
<img align="center" src="https://raw.githubusercontent.com/espehon/clocky-cli/main/docs/images/firstClock.png"/>
</a>
</p>

# clocky
CLI for tracking hours worked
<br><br>
This was the first "installable" package I ever made. The code is very messy. It was originally used with easy install and I have used it for every work day since its conception. This is a great little program for keeping record of your punches in the event your company's system fails or you forget to punch-out at the end of the day. I have decided to publish the code and refactor it to be installable with pip.


# Install
Requires Python >= 3.8
```
pip install clocky-cli
```


# Features
- clocking in and out
- break timer that auto clocks back in
- output punches from timelog (similar to `tail` on Linux)
- output timecard for a given week
- various charts
- edit dates if you forget a punch



# Usage
```
usage: clocky [-?] [-d] [-v | -i | -o | -t | -b [M] | -l [N] | -s [N] | -g [N] | -c [N] | -gc [N] | -h
              I [N ...] | --edit [D]]

Clocky: A timecard program! Arguments are mutually exclusive. (Except --debug)

options:
  -?, --help                Show this help message and exit.
  -d, --debug               Print debug information.
  -v, --version             show program's version number and exit
  -i, --in                  Clock in.
  -o, --out                 Clock out.
  -t, --toggle              Clock in if out, clock out if in.
  -b [M], --break [M]       Clock out for [M] minutes and clock back in. (default: 30)
  -l [N], --log [N]         Print log for last [N] days. (default: 7)
  -s [N], --sum [N]         Print summary for [N]th week ago. (default: 0)
  -g [N], --graph [N]       Print graphical summary for [N]th week ago. (default: 0)
  -c [N], --chart [N]       Print chart summary for [N]th week ago. (default: 0)
  -gc [N], -cg [N]          Combines graph and chart for [N]th week ago. (default: 0)
  -h I [N], --hist I [N]    Chart history for last [N] [I]ntervals. (D=days W=weeks)  ← Not yet implemented 
  --edit [D]                Edit timecard for [D]ate. (YYYY-MM-DD)

Try 'clocky --demo' for demonstrations.
```
# Issues
- Be very careful about adding a `clocky -i` to your shell's profile. Sometimes shell profiles are reloaded which will cause unwanted punches. I experienced this firsthand in PowerShell: Took me way too long to debug. It's better to add `clocky -i` to a startup script that you run manually.

- If you are using Nerd Fonts or other fonts that support ligatures, you may experience rendering issues with some of the charts. (See Issue [#13](https://github.com/espehon/clocky-cli/issues/13))


# Author

- [@espehon](https://www.github.com/espehon)