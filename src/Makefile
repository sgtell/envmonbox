
build:

MONBOXBIN=/home/envmonbox/bin
MONBOXPLIB=/home/envmonbox/lib/python
CGIBIN=/usr/lib/cgi-bin

install-bin:
	mkdir -p 	 $(MONBOXBIN)
	sudo cp fs-lcdstats.py $(MONBOXBIN)
	cp mb-gather 	 $(MONBOXBIN)
	cp mb-forward 	 $(MONBOXBIN)
	cp mb-guilfred 	 $(MONBOXBIN)

install-cgi:
	sudo cp mb-status $(CGIBIN)

install-lib:
	mkdir -p   $(MONBOXPLIB)
	cp sgtmqtt.py  $(MONBOXPLIB)
	cp mbconfig.py  $(MONBOXPLIB)
	python mbconfig.py -q -o $(MONBOXPLIB)/mbconfig.yaml

