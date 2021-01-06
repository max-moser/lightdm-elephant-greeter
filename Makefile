install:
	mkdir -p /etc/lightdm && cp max-moser-greeter.conf /etc/lightdm/
	mkdir -p /usr/local/share/lightdm/greeters && cp max-moser-greeter.desktop max-moser-greeter-x11.desktop /usr/local/share/lightdm/greeters/
	mkdir -p /usr/local/bin && cp max-moser-greeter.py /usr/local/bin/
	mkdir -p /usr/local/share/max-moser-greeter && cp max-moser-greeter.ui /usr/local/share/max-moser-greeter/
	mkdir -p /usr/local/share/max-moser-greeter/img && cp -r img /usr/local/share/max-moser-greeter/

uninstall:
	rm /usr/local/bin/max-moser-greeter.py
	rm -r /usr/local/share/max-moser-greeter/
	rm /usr/local/share/lightdm/greeters/max-moser-greeter.desktop
	rm /usr/local/share/lightdm/greeters/max-moser-greeter-x11.desktop 
	rm /etc/lightdm/max-moser-greeter.conf 

