# CronTab

Mac and Linux users can use CronTab to schedule Python scripts!
CronTab is preinstalled on MacOS.

## Give CronTab access to File Disk

    > Open System Preferences
    > Click Security and Privacy
    > Click File Disk Access
    > Click the + button
    > Press Command + Shift + G
    > Type /usr/sbin/cron
    > Click Open

## Schedule the script to run every hour

 1. Launch Terminal.
 2. Type `crontab -e` to launch CronTab editor.
 3. Press `i` to edit
 4. Type `0 * * * * cd ~/Documents/portfolio/craigslist_chairs && /Users/taekunkim/opt/anaconda3/bin/python3 script.py`

> * `0 * * * *` sets the schedule to every hour of every day
> * `cd ~/Documents/portfolio/craigslist_chairs` brings CronTab to the directory where my script is saved
> * `/Users/taekunkim/opt/anaconda3/bin/python3 script.py` is the same as typing in `python3 script.py`. However, CronTab may not recognize `python3`, so we must type in the directory where `python3` is saved. You can find the directory by typing `which python3` into Terminal.
>
 5. Press `esc`
 6. Enter `:wq`

That's it!
