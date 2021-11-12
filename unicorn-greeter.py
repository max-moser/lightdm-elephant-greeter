#!/usr/bin/env python3
#
# Simple LightDM greeter, based on GTK 3.
#
# The code is based on the example greeter written and explained by
# Matt Fischer:
# http://www.mattfischer.com/blog/archives/5

import configparser
import gi
import os
import sys
from pathlib import Path

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("LightDM", "1")

from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import LightDM

DEFAULT_SESSION = "sway"
UI_FILE_LOCATION = "/usr/local/share/unicorn-greeter/unicorn-greeter.ui"
WAYLAND_ICON_LOCATION = "/usr/local/share/unicorn-greeter/img/wayland.png"
X_ICON_LOCATION = "/usr/local/share/unicorn-greeter/img/X.png"

# read the cache
cache_dir = (Path.home() / ".cache" / "unicorn-greeter")
cache_dir.mkdir(parents=True, exist_ok=True)
state_file = (cache_dir / "state")
state_file.touch()
cache = configparser.ConfigParser()
cache.read(str(state_file))
if not cache.has_section("greeter"):
    cache.add_section("greeter")

greeter = None
password_entry = None
message_label = None
login_clicked = False


def set_password_visibility(visible):
    """Show or hide the password entry field."""
    password_entry.set_sensitive(visible)
    password_label.set_sensitive(visible)
    if visible:
        password_entry.show()
        password_label.show()
    else:
        password_entry.hide()
        password_label.hide()


def read_config(gtk_settings, config_file="/etc/lightdm/unicorn-greeter.conf"):
    """Read the configuration from the file."""
    if not os.path.isfile(config_file):
        return

    config = configparser.ConfigParser()
    config.read(config_file)
    if "GTK" in config:
        # every setting in the GTK section starting with 'gtk-' is applied directly
        for key in config["GTK"]:
            if key.startswith("gtk-"):
                value = config["GTK"][key]
                gtk_settings.set_property(key, value)

    if "Greeter" in config:
        global DEFAULT_SESSION, UI_FILE_LOCATION, X_ICON_LOCATION, WAYLAND_ICON_LOCATION
        DEFAULT_SESSION = config["Greeter"].get("default-session", DEFAULT_SESSION)
        UI_FILE_LOCATION = config["Greeter"].get("ui-file-location", UI_FILE_LOCATION)
        X_ICON_LOCATION = config["Greeter"].get("x-icon-location", X_ICON_LOCATION)
        WAYLAND_ICON_LOCATION = config["Greeter"].get("wayland-icon-location", WAYLAND_ICON_LOCATION)


def write_cache():
    """Write the current cache to file."""
    with open(str(state_file), "w") as file_:
        cache.write(file_)


def auto_select_user_session(username):
    """Automatically select the user's preferred session."""
    users = LightDM.UserList().get_users()
    users = [u for u in users if u.get_name() == username] + [None]
    user = users[0]

    if user is not None:
        session_index = 0
        if user.get_session() is not None:
            # find the index of the user's session in the combobox
            session_index = [row[0] for row in sessions_box.get_model()].index(user.get_session())

        sessions_box.set_active(session_index)


def start_session():
    session = sessions_box.get_active_text() or DEFAULT_SESSION
    write_cache()
    if not greeter.start_session_sync(session):
        print("failed to start session", file=sys.stderr)
        message_label.set_text("Failed to start Session")


def dm_show_prompt_cb(greeter, text, prompt_type=None, **kwargs):
    """Respond to the password request sent by LightDM."""
    # this event is sent by LightDM after user authentication
    # started, if a password is required
    if login_clicked:
        greeter.respond(password_entry.get_text())
        password_entry.set_text("")

    if "password" not in text.lower():
        print(f"LightDM requested prompt: {text}", file=sys.stderr)


def dm_show_message_cb(greeter, text, message_type=None, **kwargs):
    """Show the message from LightDM to the user."""
    print(f"message from LightDM: {text}", file=sys.stderr)
    message_label.set_text(text)


def dm_authentication_complete_cb(greeter):
    """Handle the notification that the authentication is completed."""
    if not login_clicked:
        # if this callback is executed before we clicked the login button,
        # this means that this user doesn't require a password
        # - in this case, we hide the password entry
        set_password_visibility(False)

    else:
        if greeter.get_is_authenticated():
            # the user authenticated successfully:
            # try to start the session
            start_session()
        else:
            # autentication complete, but unsucessful:
            # likely, the password was wrong
            message_label.set_text("Login failed")
            print("login failed", file=sys.stderr)


def user_change_handler(widget, data=None):
    """Event handler for selecting a different username in the ComboBox."""
    global login_clicked
    login_clicked = False

    if greeter.get_in_authentication():
        greeter.cancel_authentication()

    username = usernames_box.get_active_text()
    greeter.authenticate(username)
    auto_select_user_session(username)

    set_password_visibility(True)
    password_entry.set_text("")
    cache.set("greeter", "last-user", username)


def login_click_handler(widget, data=None):
    """Event handler for clicking the Login button."""
    global login_clicked
    login_clicked = True

    if greeter.get_is_authenticated():
        # the user is already authenticated:
        # this is likely the case when the user doesn't require a password
        start_session()

    if greeter.get_in_authentication():
        # if we're in the middle of an authentication, let's cancel it
        greeter.cancel_authentication()

    # (re-)start the authentication for the selected user
    # this should trigger LightDM to send a 'show-prompt' signal
    # (note that this time, login_clicked is True, however)
    username = usernames_box.get_active_text()
    greeter.authenticate(username)


def poweroff_click_handler(widget, data=None):
    """Event handler for clicking the Power-Off button."""
    if LightDM.get_can_shutdown():
        LightDM.shutdown()


if __name__ == "__main__":
    builder = Gtk.Builder()
    greeter = LightDM.Greeter()
    settings = Gtk.Settings.get_default()
    read_config(settings)
    cursor = Gdk.Cursor(Gdk.CursorType.LEFT_PTR)
    greeter_session_type = os.environ.get("XDG_SESSION_TYPE", None)

    # connect signal handlers to LightDM
    # signals: http://people.ubuntu.com/~robert-ancell/lightdm/reference/LightDMGreeter.html#LightDMGreeter-authentication-complete
    greeter.connect("authentication-complete", dm_authentication_complete_cb)
    greeter.connect("show-message", dm_show_message_cb)
    greeter.connect("show-prompt", dm_show_prompt_cb)

    # connect builder and widgets
    ui_file_path = UI_FILE_LOCATION
    builder.add_from_file(ui_file_path)
    login_window = builder.get_object("login_window")
    password_entry = builder.get_object("password_entry")
    password_label = builder.get_object("password_label")
    message_label = builder.get_object("message_label")
    usernames_box = builder.get_object("usernames_cb")
    sessions_box = builder.get_object("sessions_cb")
    login_button = builder.get_object("login_button")
    poweroff_button = builder.get_object("poweroff_button")
    icon = builder.get_object("icon")

    # connect to greeter
    greeter.connect_to_daemon_sync()

    # set up the GUI
    login_window.get_root_window().set_cursor(cursor)
    password_entry.set_text("")
    password_entry.set_sensitive(True)
    password_entry.set_visibility(False)
    if greeter_session_type is not None:
        print(f"greeter session type: {greeter_session_type}", file=sys.stderr)
        message_label.set_text("Welcome Back!")
        if greeter_session_type.lower() == "wayland":
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(WAYLAND_ICON_LOCATION, 32, 32, False)
            icon.set_from_pixbuf(pixbuf)
        elif greeter_session_type.lower() == "x11":
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(X_ICON_LOCATION, 32, 32, False)
            icon.set_from_pixbuf(pixbuf)

    # register handlers for our UI elements
    poweroff_button.connect("clicked", poweroff_click_handler)
    usernames_box.connect("changed", user_change_handler)
    password_entry.connect("activate", login_click_handler)
    login_button.connect("clicked", login_click_handler)
    login_window.set_default(login_button)

    # make the greeter "fullscreen"
    screen = login_window.get_screen()
    login_window.resize(screen.get_width(), screen.get_height())

    # populate the combo boxes
    user_idx = 0
    last_user = cache.get("greeter", "last-user", fallback=None)
    for idx, user in enumerate(LightDM.UserList().get_users()):
        usernames_box.append_text(user.get_name())
        if last_user == user.get_name():
            user_idx = idx

    for session in LightDM.get_sessions():
        sessions_box.append_text(session.get_key())

    sessions_box.set_active(0)
    usernames_box.set_active(user_idx)

    # if the selected user requires a password, (i.e the password entry
    # is visible), focus the password entry -- otherwise, focus the
    # user selection box
    if password_entry.get_sensitive():
        password_entry.grab_focus()
    else:
        usernames_box.grab_focus()

    login_window.show()
    login_window.fullscreen()
    GLib.MainLoop().run()
