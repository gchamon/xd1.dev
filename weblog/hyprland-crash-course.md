---
Date: 2024-03-18 13:53
---

# Hyprland crash course

For the past week I have been configuring hyprland and using it as my daily driver.
Coming from major Desktop Environments like KDE or Gnome, this was definitely quite challanging,
specially when implementing features that we take it for granted on these DEs, like screen sharing or screenshot annotating.

In this post I will be going through all the tools and scripts I have been creating to configure this amazing Window Manager to my liking.

## Introduction

First things first, the system I daily drive is Archlinux, and it comes with its own set of pros and cons.
However specially for hyprland, everything is available from the package manager. Apparently nix configurations are also very well supported.
Other system architectures might not have such a thorough support from the distro.

All of this to say, I am going to assume you are using arch.

Hyprland itself has a nice [Master tutorial](https://wiki.hyprland.org/Getting-Started/Master-Tutorial/) which I recommend you to follow.
I believe this gets you 90% of the way there. This post aims to polish the rough edges after installing it successfully.

Your mileage may vary, but it took me maybe two days to get a functional installation and maybe four more days of polishing until I felt
I could just ditch GNOME.

### Things I'll cover here

So what I really aim to do after you have a working hyprland setup is the following:

- My scripts;
- My shortcuts;
- How to screenshot;
- Theming;
- Some tips and tricks I came across;

## The master tutorial

So basically after installing hyprland with:

```shell
sudo pacman -S hyprland kitty
```

You get to a nice window manager environment. For a quick introduction about the difference between Desktop environments and Window managers,
try [this blog post](https://www.linuxfordevices.com/tutorials/linux/desktop-environment-vs-window-manager) by the nice folks from
[linuxfordevices.com](https://www.linuxfordevices.com/).

Launching hyprland from GDM worked flawlessly for me, so you can try that. Now you can boot into it and start configuring it.

After the master tutorial you should take a look at:

- [Screen sharing](https://wiki.hyprland.org/Useful-Utilities/Screen-Sharing/)
- [App launchers](https://wiki.hyprland.org/Useful-Utilities/App-Launchers/)
- [Status bars](https://wiki.hyprland.org/Useful-Utilities/Status-Bars/)
- [gnome-keyring SSH Keys](https://wiki.archlinux.org/title/GNOME/Keyring#SSH_keys)

You would probably also need [nm-applet and blueman-applet](https://www.reddit.com/r/hyprland/comments/165hhd9/comment/jye2bhm/).

## My scripts

These scripts aim to extend functionality and work around problems of hyprland and its applications.

### Rofi

Rofi is nice in that it presents you with a couple of options. You can install it from [the AUR](https://aur.archlinux.org/packages/rofi-lbonn-wayland-git).
You can configure hyprland to use it by setting `$menu = rofi -show drun` and running it with `SUPER+R`.

What was missing for me is the ability to launch programs in a shell, in or outside a terminal emulator, using rofi.

This can be easily achieved with a command like `kitty bash -c $(rofi -dmenu -p terminal)`. However Rofi won't remember the commands.
I found [frece](https://github.com/YodaEmbedding/frece) from [this issue](https://github.com/davatorium/rofi/issues/747) and used the example scripts as a reference
to add history to rofi commands:

```shell
#!/bin/bash
set -euo pipefail

# this adds frequency sorted history to rofi -dmenu

if [[ -z "$1" ]]; then
    echo Usage ./launch-rofi-frece.sh {ROFI_TYPE}
    echo Rofi type can be anything describing the rofi usage, for instance shell or terminal
fi

ROFI_TYPE="$1"
DB_FILE="$HOME/.cache/rofi.$ROFI_TYPE.db"
if ! [[ -f "$DB_FILE" ]]; then
    frece init "$DB_FILE" /dev/null
fi

item=$(frece print "$DB_FILE" | rofi "$@" -dmenu -p $ROFI_TYPE)
[[ -z $item ]] && exit 1

if ! frece increment "$DB_FILE" "$item" >/dev/null 2>&1; then
    frece add "$DB_FILE" "$item"
fi

echo "$item"
```

This will initialize an empty frece database with the context type I am using rofi (either shell or terminal).
Then I can use this script from hyprland:

```conf
$shellMenu = bash -c "$(~/.config/hypr/scripts/launch-rofi-frece.sh shell)"
$terminalMenu = kitty bash -c "$(~/.config/hypr/scripts/launch-rofi-frece.sh terminal)"
bind = $mainMod SHIFT, R, exec, $shellMenu
bind = $mainMod CTRL SHIFT, R, exec, $terminalMenu
```

### Waybar

You can just start using waybar, but if you want to customize it, it won't reload by itself. I use [this script](https://github.com/Alexays/Waybar/issues/961#issuecomment-753533975)
to reload waybar whenever I want to change the theme:

```shell
#!/bin/bash

CONFIG_FILES="$HOME/.config/waybar/config $HOME/.config/waybar/style.css"

trap "killall waybar" EXIT

while true; do
    waybar &
    inotifywait -e create,modify $CONFIG_FILES
    killall waybar
done
```

Which you can launch by changing how you launch waybar with hyprland to `exec-once = ~/.config/hypr/scripts/launch-waybar.sh`.
