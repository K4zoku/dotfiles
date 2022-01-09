#!/usr/bin/env sh

#######################
# Turn off beep sound #
#######################
xset b off

########
# Path #
########
append_path() {
  if [ $# -eq "0" ]; then
    printf "Usage: $0 [path]\n"
    return 1
  fi
  for arg; do
    case ":$PATH:" in
    *:"$arg":*)
      ;;
    *)
      PATH="${PATH:+$PATH:}$arg"
    esac
  done
}

append_path "${HOME}/.local/bin"

export PATH

###############
# Text editor #
###############
export EDITOR=nvim
export VISUAL=subl

#############
# IM Module #
#############
export GTK_IM_MODULE=ibus
export QT_IM_MODULE=ibus
export QT4_IM_MODULE=ibus
export CLUTTER_IM_MODULE=ibus
export GLFW_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
# export IBUS_ENABLE_SYNC_MODE=1

#####################
# Network interface #
#####################
ETHERNET_INTERFACE="$(command ls /sys/class/net | grep "^e")"
WIRELESS_INTERFACE="$(command ls /sys/class/net | grep "wl")"
export ETHERNET_INTERFACE
export WIRELESS_INTERFACE

###########
# Theming #
###########
export THEME="ayu-dark" # TODO: Rofi theme chooser & theme changer script
export WALLPAPER_DIRECTORY="${HOME}/.wallpaper" # TODO: rofi wallpaper chooser
export WALLPAPER="ayu-dark.png" # TODO: Wallapaer changer
export WALLPAPER_MODE="fill"

#####################################
# Java application blank window fix #
#####################################
export AWT_TOOLKIT="MToolkit"
export _JAVA_AWT_WM_NONREPARENTING=1

#######################
# Android development #
#######################
export ANDROID_SDK_ROOT="/opt/android-sdk"

#########################
# Suppress wine message #
#########################
export WINEDEBUG="fixme-all"

######################
# Power Menu Command #
######################
export POWEROFF="systemctl poweroff"
export REBOOT="systemctl reboot"
export SLEEP="systemctl suspend"
export LOCK="i3lock-fancy"
