---
Date: 2024-08-01 22:02
Tags: tutorial, linux, gaming
---

# Installing reshade for the steam version of Chrono Trigger on Linux

## Introduction

The title is quite the mouthful huh... but I didn't seem to find a good guide to do that easily on linux, so here I am consolidating this knowledge for future reference.

The steam version of Chrono Trigger is supposed to be the most feature complete if you don't count the DS version, that you can buy today. So I snatched it for what would
translate to 4 US bucks and started playing.

Out of the box, the experience is reasonable enough. You get a working game, that on linux and with proton 9 is very stable.

However those that are a little more... for a lack of a better word, discerning when it comes to pixel art and CRT, will find the steam version troublingly lacking in what
it delivers for a "high resolution" experience. It's basically what looks like 2xSal or Super Eagle... it's a mess. And it's either that or the original pixelated experience.

If you don't believe me, this is the original graphics:

![original](/images/chrono-trigger-reshade/original.png)

And this is with the "high resolution" option activated:

![high-res](/images/chrono-trigger-reshade/high-res.png)

That does no justice to how complex and interesting pixel art designed for CRT monitors actually is. If you want to have a look at it, I belive
[this post](https://www.datagubbe.se/crt/) is really interesting. There is a [comparison of different scaling algorithms](https://en.wikipedia.org/wiki/Pixel-art_scaling_algorithms)
on Wikipedia that also is worth taking a look.

This post tries to at least enable linux users looking to play this game and do its amazing pixel art some justice. It's not a definitive guide, and I don't claim to enable
a playing experience that is comparable to the original one on CRT monitors, but it's arguably better than the stock experience.

This is the end-result you should expect:

![with-reshade](/images/chrono-trigger-reshade/with-reshade.png)

## Installing reshade

So, ReShade and Windows is an unfortunate but understandable marriage. ReShade works on linux through compatibility layers, though. However the installation is delegated to
third party heroes, and the one go-to script for that is [kevinlekiller/reshade-steam-proton](https://github.com/kevinlekiller/reshade-steam-proton).

Installing it automatically for Chrono Trigger won't work though. It correctly identifies the architecture of the build, but fails to derive the graphics API.

Having that said, Chrono Trigger runs with a 32bit executable and used the OpenGL api, so when you run `reshade-linux.sh` you need to pass this information to the script:

```
$ reshade-linux.sh
Do you want to (i)nstall or (u)ninstall ReShade for a DirectX or OpenGL game?
(i/u): i
Supply the folder path where the main executable (exe file) for the game is.
(Control+c to exit)
Game path: /home/gchamon/.local/share/Steam/steamapps/common/Chrono Trigger
Is this path correct? "/home/gchamon/.local/share/Steam/steamapps/common/Chrono Trigger"
(y/n) y
Do you want /usr/bin/reshade-linux.sh to attempt to automatically detect the right dll files to use for ReShade?
(y/n) n
Specify if the game's EXE file architecture is 32 or 64 bits:
(32/64) 32
Manually enter the dll override for ReShade, common values are one of: d3d8 d3d9 d3d11 ddraw dinput8 dxgi opengl32
Override: opengl32
You have entered 'opengl32', is this correct?
(y/n): y
Linking ReShade files to game directory.
Linking ReShade32.dll to opengl32.dll.
ln: replace '/home/gchamon/.local/share/Steam/steamapps/common/Chrono Trigger/ReShade.ini'? N
------------------------------------------------------------------------------------------------
Done.
If you're using Steam, right click the game, click properties, set the 'LAUNCH OPTIONS' to: WINEDLLOVERRIDES="d3dcompiler_47=n;opengl32=n,b" %command%
If not, run the game with this environment variable set: WINEDLLOVERRIDES="d3dcompiler_47=n;opengl32=n,b"
The next time you start the game, open the ReShade settings, go to the 'Settings' tab, if they are missing, add the Shaders folder location to the 'Effect Search Paths', add the Textures folder to the 'Texture Search Paths', these folders are located inside the ReShade_shaders folder, finally go to the 'Home' tab, click 'Reload'.
```

After that, you add `WINEDLLOVERRIDES="d3dcompiler_47=n;opengl32=n,b" %command%` to steam command and you are done.

## Reshading

There is a good starting point for ReShade presets in [Chrono Trigger Retro Reshade](https://www.nexusmods.com/chronotrigger/mods/2?tab=posts) from Nexus Mods.

You just download the 7zip archive, decompress it in the Chrono Trigger folder and when launching the game, bring up the ReShade menu with the `Home` button, use the dropdown list on the top and
select the preset.

![select-ini](/images/chrono-trigger-reshade/select-ini.png)

I found that it's reasonably good out of the box. I just disable `Colorfulness` because I think it adds a little green tint I don't quite like.

![effect-selection](/images/chrono-trigger-reshade/effect-selection.png)
