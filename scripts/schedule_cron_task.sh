cron_job="cd ~/Assigment; scripts/monitor_dashboard.sh -c configuration.json"
cron_time="* * * * *"
cron_task="$cron_time $cron_job"

crontab -l | { cat; echo "$cron_task"; } | crontab -
