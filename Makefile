INSTALL_PATH=/usr/local
CONFIG_PATH=/etc
PKG_PREFIX=

elephant-greeter.conf: elephant-greeter.conf.base
	sed -e "s|INSTALL_PATH|$(INSTALL_PATH)|" elephant-greeter.conf.base > elephant-greeter.conf

clean:
	rm elephant-greeter.conf

install: elephant-greeter.conf
	install -D -m 644 -t $(PKG_PREFIX)$(CONFIG_PATH)/lightdm/ elephant-greeter.conf
	install -D -m 755 -t $(PKG_PREFIX)$(INSTALL_PATH)/bin elephant-greeter.py
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/lightdm/greeters elephant-greeter.desktop elephant-greeter-x11.desktop
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/elephant-greeter elephant-greeter.ui
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/elephant-greeter/img img/*

uninstall:
	rm $(INSTALL_PATH)/bin/elephant-greeter.py
	rm -r $(INSTALL_PATH)/share/elephant-greeter/
	rm $(INSTALL_PATH)/share/lightdm/greeters/elephant-greeter.desktop
	rm $(INSTALL_PATH)/share/lightdm/greeters/elephant-greeter-x11.desktop
	rm $(CONFIG_PATH)/lightdm/elephant-greeter.conf

