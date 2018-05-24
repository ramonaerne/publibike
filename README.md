
## Cronjobs
The following cronjob crawls the data every 10 minutes

```
*/10 * * * * /Users/ramonaerne/anaconda3/bin/python /Users/ramonaerne/Code/Publibike/crawl_once.py >> ~/cron_output.log 2>&1
```

to create, simply edit via `crontab -e`


## Launchctl
More powerful on mac os, use the following plist file and put it in `/Library/LaunchAgents`, save it as `com.ramon.publibike.plist`

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ramon.publibike</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/ramonaerne/anaconda3/bin/python</string>
        <string>/Users/ramonaerne/Code/Publibike/crawl_once.py</string>
    </array>
    <key>StartInterval</key>
    <integer>600</integer>
    <key>StandardOutPath</key>
    <string>/tmp/publibike_launchctl.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/publibike_launchctl.err</string>
</dict>
</plist>
```
Launch it via
```
launchctl load /Library/LaunchAgents/com.ramon.publibike.plist
```
and unload via
```
launchctl unload /Library/LaunchAgents/com.ramon.publibike.plist
```
to see if it is running, run `launchctl list | grep com.ramon.publibike`
