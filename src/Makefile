
build:

MONBOXBIN=/home/envmonbox/bin
MONBOXPLIB=/home/envmonbox/lib/python
CGIBIN=/usr/lib/cgi-bin

install:
	sudo cp fs-lcdstats.py $(MONBOXBIN)
	mkdir -p 	 $(MONBOXBIN)
	cp mb-gather 	 $(MONBOXBIN)
	cp mb-forward 	 $(MONBOXBIN)
	sudo cp mb-status $(CGIBIN)
	mkdir -p   $(MONBOXPLIB)
	cp sgtmqtt.py  $(MONBOXPLIB)
	cp mbconfig.py  $(MONBOXPLIB)
	python mbconfig.py -q -o $(MONBOXPLIB)/mbconfig.yaml

