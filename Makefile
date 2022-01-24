INSTALL_PATH=/usr/local
CONFIG_PATH=/etc
PKG_PREFIX=

lightdm-lightdm-unicorn-greeter.conf: lightdm-unicorn-greeter.conf.base
	sed -e "s|INSTALL_PATH|$(INSTALL_PATH)|" lightdm-unicorn-greeter.conf.base > lightdm-unicorn-greeter.conf

clean:
	rm lightdm-unicorn-greeter.conf

install: lightdm-unicorn-greeter.conf
	install -D -m 644 -t $(PKG_PREFIX)$(CONFIG_PATH)/lightdm/ lightdm-unicorn-greeter.conf
	install -D -m 755 -t $(PKG_PREFIX)$(INSTALL_PATH)/bin lightdm-unicorn-greeter.py
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/lightdm/greeters lightdm-unicorn-greeter.desktop lightdm-unicorn-greeter-x11.desktop
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/lightdm-unicorn-greeter lightdm-unicorn-greeter.ui
	install -D -m 644 -t $(PKG_PREFIX)$(INSTALL_PATH)/share/lightdm-unicorn-greeter/img img/*

uninstall:
	rm $(INSTALL_PATH)/bin/lightdm-unicorn-greeter.py
	rm -r $(INSTALL_PATH)/share/lightdm-unicorn-greeter/
	rm $(INSTALL_PATH)/share/lightdm/greeters/lightdm-unicorn-greeter.desktop
	rm $(INSTALL_PATH)/share/lightdm/greeters/lightdm-unicorn-greeter-x11.desktop
	rm $(CONFIG_PATH)/lightdm/lightdm-unicorn-greeter.conf

