---
Date: 2024-03-31 19:20
Tags: bugs, tech, linux
---

# Backups and bitrot

Last night I killed my linux installation. It refused to come back to life even after chrooting and reinstalling everything. Something broke irreparably, to the best of my knowledge.

And a backup, that should have prevented it, was the culprit. It was also what saved it.

## Context

The issue started showing its head about two weeks ago, when KDE decided it was time to push Plasma 6 and make my life miserable.
That made me switch to Gnome, and shortly after to Hyprland.

You can read more about this in my previous post: [Hyprland crash course](/2024/03/hyprland-crash-course).

At that time, while switching to these different environments, SDDM stopped working with a login loop, but I didn't give it much thought because GDM worked fine and I had work to do.
However I did some investigating and it turned out that SDDM and Hyprland would work OK if I had a fresh user. I couldn't look into it further, however odd it was.

Fast forward to yesterday, and having totally forgotten about this brief hickup I decided to give SDDM a try because I was purging Gnome from my system, having now
a very stable Hyprland setup.

And it worked! Well, it appeared to do so, because I installed SDDM, experimented with some themes, logging in and out...

All was well in Roswell.

Until I rebooted.

## Induced to error

Looking back with the benefit of foresight I should have remembered that ocasion where SDDM wasn't working, but I honestly thought it was something I did recently,
not a long running issue.

To add insult to injury, if I would login to another TTY and restart SDDM, the graphical login would start working again, which reinforced this false assumption.

So I started crippling my system, removing traces from X11 configuration files, looking for a culprit...

At one point, the login loop turned into this:

![tty1](/images/tty1-blank-white.jpg)

That bad image is a frame from a video I took to try to debug the fast vanishing logs that the tty was producing. It's a very small terminal with a white background.
I haven't figured out what exactly resulted in this symptom, only what was causing it. But not before killing my system.

This image was taken before my installation died on me. I think it was when I removed `/usr/share/X11`. You have to understand, at that time I thought it was a calculated
mangling of the system, because `/usr` is a folder I backup in its entirety to my separated storage system. But after that nothing could make the graphics system go back online again.

I had to reinstall and restore the backup yet again.

## The issue crops up

So I pulled my Ventoy USB containing the Archlinux install image and proceded with yet another system installation. Sure now with `archinstall` it has never been easier to install it,
it feels like an eternity when you are already past midnight and just want to go to bed...

So the installation went through without issues and booted fine, Hyprland + SDDM and all. There I thought all was well again... "I guess I really only had misconfigured something recently..."

That was before restoring my `/home` and `/etc/` folder...

I still need to lay out in details of how I backup my files, but the gist of it is I use borg with some [automation scripts](https://github.com/gchamon/borg-automated-backups)
and [this public gist](https://gist.github.com/gchamon/a10a23e258477e8eca67c4aa84aaccb5) for restoration instructions.

So after restoring my files and rebooting, there was it again, the nasty little white screen of pain and hopelessness.

My backups were tainted... Years of it.

They were not big, ~8GB for the home folder, but they were old... Maybe over 6 years of accumulating undocumented configurations.
This is a side effect from backups. They do exactly what they set out to do. To stand the test of time. And with that comes bitrot.

## Arriving at the solution

At this point I remembered the time when I tested with a fresh user, and sure enough logging in with the test user, untainted by the cursed backup, I could login to my graphical system.

Now I turn to my many dotfiles... first to the main ones. Removing `.local`, `.cache` and `.config`. They did nothing to the issue, which persisted.

That was actually a relief. The main configurations or data are in those folders (no not you `.cache` you could go away for all I care).

So I nuked all the other dot folders appart from some I knew couldn't be related and the issue went away.

But what was it? What caused it?

To figure it out, I listed the dot files/folders that remained and compared them against the inventory of dot files I extracted from my borg archive. These were the files that were deleted:

```
.aws
.bash_logout
.bash_profile
.cargo
.codetogether
.ctsystem
.dmrc
.docker
.exult
.gnupg
.helm
.helm-synth
.hyprland
.icons
.ideavimrc
.ipython
.jackdrc
.java
.mackup
.npm
.nv
.nvidia-settings-rc
.pki
.profile
.pulse-cookie
.python_history
.qt
.rnd
.steam
.steampath
.steampid
.subversion
.themes
.viminfo
.vscode-oss
.wget-hsts
.Xauthority
.zoom
.zprofile
```

So I did what every sane person would do and ~added one by one until the issue came back~ asked ChatGPT which files were more likely to be associated with the issue.

It produced a list of five files, from which I reduced to two, `.dmrc` and `.zprofile`.

## The issue

So...

What carried over years of neglect was `.zprofile`. It had these three nasty lines in it, from a time past memory, when things were simpler and the world was still young:

```bash
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  exec startx
fi
```

Why it was there, I will never know, the need for it being lost to time and buried in sand. But one lesson will remain, which is to **clean you HOME folder**.
