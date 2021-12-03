#!/usr/bin/env bash

## Author  : Aditya Shakya
## Mail    : adi1090x@gmail.com
## Github  : @adi1090x
## Twitter : @adi1090x

theme="style_12"
dir=$(dirname "$(readlink -f "$0")")
rofi -no-lazy-grab -show drun -modi drun -theme $dir/"$theme"
