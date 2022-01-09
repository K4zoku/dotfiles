#!/bin/bash

sxhkdrc=$1
[ -z "${sxhkdrc}" ] && sxhkdrc="${HOME}/.config/sxhkd/sxhkdrc"

awk '/^[a-z]/ && last {print "<small>",$0,"\t",last,"</small>"} {last=""} /^#/{last=$0}' "${sxhkdrc}" |\
column -t -s $'\t' |\
rofi -dmenu -i -markup-rows -no-show-icons -theme themes/textlistinput.rasi
