#!/usr/bin/python

from time import sleep
from xspice_audio_test_helper import produce_audio
from xspice_util import launch_xspice, launch_client

def main():
    port = 8000
    xspice = launch_xspice(port)
    sleep(2)
    client = launch_client(port)
    sleep(1)
    produce_audio(xspice.audio_fifo_dir)
    sleep(2)
    client.kill()
    xspice.kill()

if __name__ == '__main__':
    main()
