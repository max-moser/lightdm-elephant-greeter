INSTALL_PATH=/usr/local
CONFIG_PATH=/etc
PKG_PREFIX=

unicorn-greeter.conf: unicorn-greeter.conf.base
	sed -e "s|INSTALL_PATH|$(INSTALL_PATH)|" unicorn-greeter.conf.base > unicorn-greeter.conf

clean:
	rm unicorn-greeter.conf

install: unicorn-greeter.conf
	install -D -m 644 -t $(PKG_PREFIX)$(CONFIG_PATH)/lightdm/ unicorn-greeter.conf
	install -D -m 755 -t $(PKG_PREFIX)$(INSTALL_PATH)/bin unicorn-greeter.py
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/lightdm/greeters unicorn-greeter.desktop unicorn-greeter-x11.desktop
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/unicorn-greeter unicorn-greeter.ui
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/unicorn-greeter/img img/*

uninstall:
	rm $(INSTALL_PATH)/bin/unicorn-greeter.py
	rm -r $(INSTALL_PATH)/share/unicorn-greeter/
	rm $(INSTALL_PATH)/share/lightdm/greeters/unicorn-greeter.desktop
	rm $(INSTALL_PATH)/share/lightdm/greeters/unicorn-greeter-x11.desktop
	rm $(CONFIG_PATH)/lightdm/unicorn-greeter.conf

