---
Date: 2024-03-18 13:53
Tags: tutorial, tech, linux
---

# Hyprland crash course

**EDIT** I made my config files available here: [gchamon/.config](https://github.com/gchamon/.config).

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
- How to screenshot;
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
- [Clipboard managers](https://wiki.hyprland.org/Useful-Utilities/Clipboard-Managers/)
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

This way you can have a separate history with frequency tracking for rofi:

![rofi-shell-history](https://raw.githubusercontent.com/gchamon/xd1.dev/main/images/hyprland-crash-course/rofi-shell-history.png)

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

### Dunst notification sounds

You can configure dunst to play notification sounds by following [this comment](https://github.com/dunst-project/dunst/issues/257) on github.
However powersaving policies, most likely from the bluetooth protocol, prevents my headphones to play music straight away. It would only play
the end of the audio from *A link to the past*. To work around this I use [this 500ms silent mp3 file](https://github.com/anars/blank-audio/blob/master/500-milliseconds-of-silence.mp3)
to warm up my device. Needless to say it introduces a half-second latency to every notification sound, but it does the job. The script will then look like this:

```shell
#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source "$HOME/.zshenv"

if [[ "$DUNST_QUIET" != "true" ]]; then
    # warm up audio device in case of powersave policies (like bluetooth)
    pw-play $SCRIPT_DIR/../assets/500-milliseconds-of-silence.mp3
    pw-play $SCRIPT_DIR/../assets/link.mp3
fi
```

As you can see I also implemented a quiet mode by setting `DUNST_QUIET=true` in `.zshenv`. Yes, bash and zsh shouldn't mix but let this slide, please :D

### Wayland lock screen

I use [sawlock-effects](https://aur.archlinux.org/packages/swaylock-effects) for locking my screen. The script looks like this
(just so that it doesn't clutter the hyprland config file):

```shell
#!/usr/bin/env bash

swaylock \
    --image /usr/share/backgrounds/archlinux/split.png \
    --clock \
    --indicator \
    --indicator-radius 100 \
    --indicator-thickness 7 \
    --effect-blur 7x5 \
    --effect-vignette 0.5:0.5 \
    --ring-color bb00cc \
    --key-hl-color 880033 \
    --line-color 00000000 \
    --inside-color 00000088 \
    --separator-color 00000000 \
    --fade-in 1

```

And I invoke it with `bind = $mainMod, L, exec, ~/.config/hypr/scripts/wayland-lock.sh`.

### Screenshot with editor

I use [grimblast](https://github.com/hyprwm/contrib/tree/main/grimblast) from [aur](https://aur.archlinux.org/packages/grimblast-git)
together with [ksnip](https://github.com/ksnip/ksnip), which is available from the `extra` packages.

There is a `captureArea.sh` script:

```shell
#!/bin/bash

export GRIMBLAST_EDITOR=ksnip
grimblast --cursor edit area
```

And a `captureAll.sh` script:

```shell
#!/bin/bash
set -euo pipefail

SCREENSHOT_FILENAME=$(date +'%Y-%m-%dT%H:%M:%S%z_grim.png')
SCREENSHOT_FILENAME_ABSOLUTE=$HOME/Pictures/Screenshots/$SCREENSHOT_FILENAME

notify-send --app-name=grim --urgency=normal --category=screenshot "Capturing entire screen to $SCREENSHOT_FILENAME_ABSOLUTE"
grim $SCREENSHOT_FILENAME_ABSOLUTE
```

Which I launch with

```conf
bind = SHIFT, 107, exec, ~/.config/hypr/scripts/screenshot/captureAll.sh
bind = , 107, exec, ~/.config/hypr/scripts/screenshot/captureArea.sh
```

The number `107` being the PrintScreen key. It can also be referenced by `Print`, but for some reason I left it with the code.

**BTW** you can use `wev` and get codes from keys you press and just use them in hyprland config.

### Kill hyprland if stuck on exit

Hyprland, at least for me, will randomly freeze on a blackscreen upon exit. [This issue](https://github.com/hyprwm/Hyprland/issues/3558) covers the problem
and also offers a workaround by using this script:

```
echo "Hyprland exit" | systemd-cat -t coffebar -p info
hyprctl dispatch exit &
sleep 10
echo "Hyprland failed to exit" | systemd-cat -t coffebar -p err
killall -9 Hyprland
```

You can then just call it with `SUPER+M` instead of dispatching exit directly. It won't solve the problem, but at least you don't need to reboot everytime it happens.

## Quick tips

These are some quick references to tips and tricks I came across during this last few days.

### Multiple keyboard layouts

Since I have two keyboards with two different layouts (a us mx-keys and a br-abnt2 built-in keyboard on my notebook) it wasn't clear for me how I should configure hyprland.
At first I was looking for a way to display the current keyboard and maybe toggle it with waybar, but I quickly realised that hyprland toggle will work only for the keyboard which
pressed the toggle key.

However you can set different layouts for different devices in `hyprland.conf`. My configuration looks like this:

```conf
input {
    kb_layout = br
    kb_variant = abnt2
    # ...
}

device {
    name = logitech-mx-keys
    kb_layout = us
    kb_variant = intl
}

```

This is nice because I get consistent layout configuration with whatever keyboard I use. You can find which input devices you have with `hyprctl devices`.

### Waybar on-click actions

After applying [cjbassi's theme](https://github.com/cjbassi/config/tree/master/.config/waybar) I wanted more functionality for my bar.
**BTW** you can find more themes [here](https://github.com/Alexays/Waybar/wiki/Examples).

First, you should install `pamixer` so that clicking on the volume to mute works.
Oh, and install `otf-font-awesome`, otherwise the nice icons won't render.

Then I mapped:

- pulseaudio
  - Right click: `pavucontrol`
- memory
  - Left click: `gnome-system-monitor --show-processes-tab`
- cpu
  - Right click: `kitty top`
  - Left click: `gnome-system-motnitor --show-resources-tab`
- battery
  - Left click: `tlpui`
- disk
  - Left click: `kitty ncdu ~`
  - Right click: `gnome-system-monitor --show-file-systems-tab`

I thought about leaving right-click on disk to open `ncdu` on root, but it takes an ungodly amount of time to go through the files in my NAS, but you could do that
if this isn't a problem for you.


### gnome-keyring

Just a headsup: if you enter a wrong password for your ssh keys, it won't complain, there won't be a warning, `ssh-add` will just gobble 100% cpu and `ssh` or `git clone`
will just hang there. You will have to kill it with `pkill ssh-add`. To fix this, open `seahorse`, go to `Login` and remove the offending ssh key password there.
Just **don't** remove it from `OpenSSH Keys` tab as it will delete the keys themselves.

Also, either use this or [keychain](https://wiki.archlinux.org/title/SSH_keys#Keychain), never both.

