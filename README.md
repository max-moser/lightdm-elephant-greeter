# LightDM Elephant Greeter

A small and simple [LightDM](https://github.com/canonical/lightdm) greeter using Python and GTK that doesn't require an X11 server.

It is based on [Matt ~~Shultz's~~ Fischer's example LightDM greeter](http://www.mattfischer.com/blog/archives/5).


## Screenshot

![Screenshot](./screenshot.png?raw=true "Screenshot")


## Features

* optionally uses Wayland, via [Cage](https://www.hjdskes.nl/projects/cage/) (instead of X11)
* remembers the last authenticated user
* automatically selects the last used session per user

**Note**: The last authenticated user is stored in a cache file in the LightDM user's home directory (e.g. `/var/lib/lightdm/.cache/elephant-greeter/state`), similar to [Slick Greeter](https://github.com/linuxmint/slick-greeter/blob/ae927483c5dcf3ae898b3f0849e3770cfa04afa1/src/user-list.vala#L1026).


## Requirements

* LightDM
* Python 3.8+
* [Cage](https://www.hjdskes.nl/projects/cage/): small wayland compositor for the greeter

**Note**: Please make sure you have all requirements installed, as having a LightDM greeter constantly failing isn't as much fun as it sounds.


## Installation

The greeter can be installed by copying the files to the right places (`make install`) and updating LightDM's configuration file to register the greeter (`/etc/lightdm/lightdm.conf`):
```ini
[LightDM]
sessions-directory=/usr/share/lightdm/sessions:/usr/share/wayland-sessions:/usr/share/xsessions
greeters-directory=/usr/local/share/lightdm/greeters:/usr/share/xgreeters

[Seat:*]
greeter-session=lightdm-elephant-greeter
```

**Note**: If you wish to install the files somewhere else, specify them in the `make` command.  
For instance, to install the files into subdirectories of `/usr` instead of `/usr/local`, call `make INSTALL_PATH=/usr install`.
The `CONFIG_PATH` (default: `/etc`) can be overridden in the same fashion.


## Configuration

The greeter's configuration file (`/etc/lightdm/elephant-greeter.conf`) contains the sections `Greeter` and `GTK`.  
The former are basic configuration values that can determine the behavior of the greeter (e.g. override file locations), while the latter are passed directly to GTK (and can be used to e.g. set the GTK theme).

Example configuration file:
```ini
[GTK]
gtk-theme-name=Nordic
gtk-application-prefer-dark-theme=true

[Greeter]
default-session=sway
ui-file-location=/usr/local/share/elephant-greeter/elephant-greeter.ui
x-icon-location=/usr/local/share/elephant-greeter/img/X.png
wayland-icon-location=/usr/local/share/elephant-greeter/img/wayland.png
```


## Additional Notes

This project used to be called `max-moser-greeter`, until I could finally come up with a better name.


## Licenses

* `img/X.svg`: [CC-BY-SA, by Sven](https://commons.wikimedia.org/wiki/File:X.Org\_Logo.svg)
* `img/wayland.svg`: [CC-BY, by Kristian Høgsberg](https://commons.wikimedia.org/wiki/File:Wayland\_Logo.svg)

