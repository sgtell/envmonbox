
build:

MONBOXBIN=/home/envmonbox/bin
MONBOXPLIB=/home/envmonbox/lib/python
CGIBIN=/usr/lib/cgi-bin

install:
	sudo cp fs-lcdstats.py $(MONBOXBIN)
	mkdir -p 	 $(MONBOXBIN)
	cp mb-gather 	 $(MONBOXBIN)
	cp mb-forward 	 $(MONBOXBIN)
	mkdir -p   $(MONBOXPLIB)
	cp sgtmqtt.py  $(MONBOXPLIB)
	sudo cp mb-status $(CGIBIN)
