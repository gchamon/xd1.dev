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

### Things I'll cover here

So what I really aim to do after you have a working hyprland setup is the following:

- Quickly go over some confusing points in the Master tutorial;
- My shortcuts;
- My scripts;
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


