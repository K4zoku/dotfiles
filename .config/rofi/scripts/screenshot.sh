#!/usr/bin/env bash

rofi_command="rofi -theme themes/screenshotsmenu.rasi"

# Options
#     
screen=""
area=""
window=""
timer=""

# Variable passed to rofi
options="$screen\n$area\n$window\n$timer"

chosen="$(printf "$options" | $rofi_command -dmenu -selected-row 1)"
case $chosen in
    $screen)
        ~/.scripts/shot now
        ;;
    $area)
        sleep 0.2
        ~/.scripts/shot region
        ;;
    $window)
        ~/.scripts/shot window
        ;;
    $timer)
        ~/.scripts/shot timer 5
        ;;
esac
