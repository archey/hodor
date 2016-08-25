#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import argparse
import logging
import signal
import json
import sys


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    logger.log(logging.DEBUG, "Connected with result code {0}".format(rc))
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    try:
        topic = message.topic
        msg = json.loads(message.payload)
        logger.log(logging.INFO, "Topic: {0}\n\tMessage: {1}".format(topic, msg))
    except:
        pass


def setup_logging(v_lvl):
    global logger
    
    level = logging.WARN
    
    if v_lvl == 1:
        level = logging.INFO
    elif v_lvl == 2:
        level = logging.DEBUG


    # Set Logging to a file
    logger = logging.getLogger('hodor')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file, mode='a+')
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    

    # Set Logging to Screen
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(console)


def main():
    global log_file

    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', dest='tgtHost', required=True, help='specify target host')
    parser.add_argument('-f', '--filename', dest='tgtfile', default='hodor.log', help='specify file name to write data to') 
    parser.add_argument('-v', '--verbose', const=1, default=0, type=int, nargs='?', 
                        help='increase verbosity: 0 = only warnings, 1 = info, 2 = debug. No number means info. Default is no verbosity.') 
    
    options = parser.parse_args()
    tgtHost = options.tgtHost
    tgtfile = options.tgtfile
    
    log_file = tgtfile
    
    setup_logging(options.verbose)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(tgtHost, 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        print("[+] Interrupt recieved, closing request to %s" % tgtHost)

if __name__ =='__main__':
        main()

