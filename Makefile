install:
	mkdir -p /etc/lightdm && cp elephant-greeter.conf /etc/lightdm/
	mkdir -p /usr/local/share/lightdm/greeters && cp elephant-greeter.desktop elephant-greeter-x11.desktop /usr/local/share/lightdm/greeters/
	mkdir -p /usr/local/bin && cp elephant-greeter.py /usr/local/bin/
	mkdir -p /usr/local/share/elephant-greeter && cp elephant-greeter.ui /usr/local/share/elephant-greeter/
	mkdir -p /usr/local/share/elephant-greeter/img && cp -r img /usr/local/share/elephant-greeter/

uninstall:
	rm /usr/local/bin/elephant-greeter.py
	rm -r /usr/local/share/elephant-greeter/
	rm /usr/local/share/lightdm/greeters/elephant-greeter.desktop
	rm /usr/local/share/lightdm/greeters/elephant-greeter-x11.desktop
	rm /etc/lightdm/elephant-greeter.conf

