# stasi

Collect data from various sensors (see [`gan`](https://github.com/ibz/gan)) and use [`rrdtool`](https://oss.oetiker.ch/rrdtool/doc/rrdtool.en.html) to generate graphs.

My own home monitoring setup involves one instance of `stasi` running directly on a Raspberri Pi, which syncs data from multiple Raspberry Pi Zero devices that collect data using `gan`.

## Running stasi

The ideal way is to start from a `gan` instance, as built by [`gan-gen`](https://github.com/ibz/gan-gen).

1. Clone the `stasi` repo
1. Create the config file
1. `sudo apt install python3-rrdtool nginx`
1. Run the commands manually for the first time - both to make sure it works, and because it will take a long time to sync if you have a lot of data
   * `mkdir /home/gan/stasi-data/`
   * `/home/gan/stasi/scripts/sync.sh`
   * `python3 /home/gan/stasi/scripts/rrd_import.py /home/gan/stasi-data/`
   * `/home/gan/stasi/scripts/graph.sh`
1. Set up a cron job to do this periodically
   * `sudo touch /var/log/cron.log && chmod a+w /var/log/cron.log`
   * `crontab -e`
   * `* * * * * /home/gan/stasi/scripts/sync.sh >> /var/log/cron.log 2>&1 && python3 /home/gan/stasi/scripts/rrd_import.py /home/gan/stasi-data/ >> /var/log/cron.log 2>&1 && /home/gan/stasi/scripts/graph.sh >> /var/log/cron.log 2>&1`

## TODO

I use this system for my own home monitoring setup and it works fine, but it might not work for everyone nor is it easy enough to install for everyone.
