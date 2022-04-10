# LightDM Unicorn Greeter

.75 Update: I'm currently working migrating the UI from GTK3 to GTK4.
In early development, but expect a release in the next few weeks.

Latest Version: .60

* Developer's note:  this release is mainly focused on hammering down the layout that I envision the greeter to have. Refinements and features will come in the next few releases.

A more feature rich [LightDM](https://github.com/canonical/lightdm) greeter using Python and GTK that doesn't require an X11 server.

It's forked from Max Moser's LightDM Elephant Greeter (https://github.com/max-moser/lightdm-elephant-greeter) which is based on [Matt Fischer's example LightDM greeter](http://www.mattfischer.com/blog/archives/5).  My goal is to make it a more feature rich alternative to LightDM Elephant Greeter.

I prefer to use a greeter, and LightDm is my preferred. I wanted a Wayland native greeter and came across the elephant Greeter. I loved it, but felt it was missing some options that other greeters for X offer, such as customizable backgrounds, changing keyboard layouts and other things. My goal with this project is to flesh it out a bit more to bring it more on par with native X greeters.

## Screenshot

![Screenshot](./default.png?raw=true "Screenshot")


## Features

* Optionally uses Wayland, via [Cage](https://www.hjdskes.nl/projects/cage/) (instead of X11)
* Remembers the last authenticated user
* Automatically selects the last used session per user
* Can set background image in the config file
* Supports GTK themes, and cursors.

**Note**: The last authenticated user is stored in a cache file in the LightDM user's home directory (e.g. `/var/lib/lightdm/.cache/lightdm-unicorn-greeter/state`), similar to [Slick Greeter](https://github.com/linuxmint/slick-greeter/blob/ae927483c5dcf3ae898b3f0849e3770cfa04afa1/src/user-list.vala#L1026).


## Requirements

* LightDM
* Python 3.8+
* [PyGObject](https://pygobject.readthedocs.io/en/latest/index.html): GObject bindings for Python
* [Cage](https://www.hjdskes.nl/projects/cage/): small wayland compositor for the greeter
* XWayland (Only if you don't build cage from source, or enable cage's XWayland support during the build)

**Note**: Please make sure you have all requirements installed, as having a LightDM greeter constantly failing isn't as much fun as it sounds.


## Installation

```ini
git clone https://github.com/FlirtatiousMule/lightdm-unicorn-greeter.git
make install or sudo make install for non root

Update LightDM's configuration file to register the greeter (`/etc/lightdm/lightdm.conf`):

[LightDM]
sessions-directory=/usr/share/lightdm/sessions:/usr/share/wayland-sessions:/usr/share/xsessions
greeters-directory=/usr/local/share/lightdm/greeters:/usr/share/xgreeters

[Seat:*]
greeter-session=lightdm-unicorn-greeter
```

**Note**: If you wish to install the files somewhere else, specify them in the `make` command.  
For instance, to install the files into subdirectories of `/usr` instead of `/usr/local`, call `make INSTALL_PATH=/usr install`.
The `CONFIG_PATH` (default: `/etc`) can be overridden in the same fashion.


## Configuration

The greeter's configuration file (`/etc/lightdmlightdm-unicorn-greeter.conf`) contains the sections `Greeter` and `GTK`.  
The former are basic configuration values that can determine the behavior of the greeter (e.g. override file locations), while the latter are passed directly to GTK (and can be used to e.g. set the GTK theme).  I recommend /usr/share/pixmaps for custom background image location.

Example configuration file:
```ini
[GTK]
gtk-theme-name=Ultimate-Dark-Red
gtk-application-prefer-dark-theme=true
gtk-cursor-theme-name=Bibata-Rainbow-Modern

[Greeter]
ui-file-location=/usr/local/share/lightdm-unicorn-greeter/lightdm-unicorn-greeter.ui
background-file-location=/usr/local/share/lightdm-unicorn-greeter/img/back.jpg
```


## Changelog

.60
* Developer's note:  this release is mainly focused on hammering down the layout that I envision the greeter to have. Refinements and features will come in the next few releases.
* Added a keyboard layout menu (work in progress) placeholder
* Added headerbar to login dialog
* Added a session type display to the headerbar
* Removed Login text
* Removed Restart text
* Removed Shutdown text
* Added Login icon
* Added Restart icon
* Added Shutdown icon
* Added tooltips to the interace
* Added user icon (eventually will support user images)
* Added password icon
* Moved the session selection to the headerbar (upper left of login dialog)

.52
* Fixed a bug that would cause the login window to be behind the background

.51
* Initial release
* Added support for a custom background file
* Fixed a bug that caused the background to not fill the screen

.50
* Renamed all instances of elephant-greeter
* Shrunk the login dialog and made it, you know, a dialog
* Added a window to handle the background image as well as a menubar (menubar coming in the future)
* Added a Restart button to the login screen
* Removed instances of X.png X.svg Wayland.png Wayland.svg and associated code

## Licenses

* Max Moser's LightDM Elephant Greeter (https://github.com/max-moser/lightdm-elephant-greeter)
* Matt Fischer's example LightDM greeter](http://www.mattfischer.com/blog/archives/5)
