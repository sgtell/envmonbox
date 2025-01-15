#!/home/tell/venv/bin/python3
# -*- coding: utf-8 -*-

import time
import os
from perlish import *
import paho.mqtt.client as mqtt

class sgtmqtt():

    def __init__(self, mqhost="localhost", port=1833):
        self.periodic_callback = None
        self.nomqtt_callback = None
        
        self.mq = mqtt.Client()
#        mq.on_connect = self.on_connect
        self.mq.on_discconnect = lambda mq,userdata : self.on_disconnect()
        self.mq.on_message = lambda mq,userdata,msg : self.on_message(msg)
        self.mq.connect(mqhost, port, keepalive=90)
        self.mq.reconnect_delay_set(min_delay=1, max_delay=120);

# user should do mq.on_connect directly, and use it to subscribe to topics they want
#    def on_connect(mq, userdata, flags, rc):
#        print("Connected with result code "+str(rc))
#        # Subscribing in on_connect() means that if we lose the connection and
#        # reconnect then subscriptions will be renewed.
#        if(self.mq):
#            self.mq.subscribe("omnistat/#")

    def on_disconnect(self):
        if(self.verbose):
            printf("on_disconnect\n");
        self.mqtt_reconnect()
    
    def mqtt_reconnect(self):
        try:
            self.mq.reconnect()
        except ConnectionRefusedError:
            # if the server is not running,
            # then the host rejects the connection
            # and a ConnectionRefusedError is thrown
            # getting this error > continue trying to
            # connect
            pass
        
        # The callback for when a PUBLISH message is received from the server.
        # NB:  somehow the mqtt stuff catches and supresses exeptions from these
        # callbacks, so if there are any errors, they fail silently.
        #  keeps things running, but difficult to debug.
    def on_message(self, client, userdata, msg):
        try:
            if(self.on_message_inner):
                on_message_inner(client, userdata, msg)
        except Exception as e:
            #printf("Exception in on_message: %s\n", str(e))
            traceback.print_exc()

    def selectloop(self, timeout=10.0):
        t0 = time.time();
        t_alive = t0;
        while(True):
            any_mq = False
            if(self.mq):
                mqsocket = self.mq.socket()
                rlist = []
                t_now = time.time();
                if(mqsocket):
                    rlist.append(mqsocket)
                    t0 = t_now
            else:
                t1 = t_now
                if(t1 - t0 > 2):
                    t0 = t1
                    printf("mqsocket is %s, attempting reconnect\n", mqsocket)
                    self.mqtt_reconnect()
                
            wlist = [];
            xlist = [];
            if(self.mq.want_write()):
                wlist.append(mqsocket)

            try:
                (rlist, wlist, xlist) = select(rlist, wlist, xlist, timeout)
            except TypeError as e:
                print(e)
                print(rlist, wlist, xlist)
                exit(1)

            for fd in rlist:
                if(fd is mqsocket):
                    self.mq.loop_read()
                    any_mq = True

            for fd in wlist:
                if(fd is mqsocket):
                    self.mq.loop_write()
                    any_mq = True

            if(not any_mq):
                if(self.nomqtt_callback):
                    self.nomqtt_callback()

            if(self.periodic_callback):
                self.periodic_callback()
