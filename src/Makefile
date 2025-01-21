
build:

BINDIR=/usr/local/sbin
MONBOXBIN=/home/envmonbox/bin
MONBOXPLIB=/home/envmonbox/lib/python

install:
	sudo cp fs-lcdstats.py $(BINDIR)
	mkdir -p 	 $(MONBOXBIN)
	cp mb-gather 	 $(MONBOXBIN)
	cp mb-forward 	 $(MONBOXBIN)
	mkdir -p   $(MONBOXPLIB)
	cp sgtmqtt.py  $(MONBOXPLIB)
