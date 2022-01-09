#!/bin/bash

killall -q polybar

while pgrep -x polybar >/dev/null; do sleep 1; done

pkill -F /tmp/polybar-music.pid
rm /tmp/polybar-music.pid

polybar left 2>~/.config/polybar/left.log &
polybar right 2>~/.config/polybar/right.log &
~/.config/polybar/music_bar.py 2>~/.config/polybar/middle.log &