
<p align="center">
<a href="https://pypi.org/project/clocky-cli/">
<img align="center" src="https://raw.githubusercontent.com/espehon/clocky-cli/main/docs/images/firstClock.png"/>
</a>
</p>

# clocky
CLI for tracking hours worked


# Install
Requires Python >= 3.8
```
pip install clocky-cli
```


# Features
- 


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

# Author

- [@espehon](https://www.github.com/espehon)