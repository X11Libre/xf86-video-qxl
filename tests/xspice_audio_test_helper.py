#!/usr/bin/python
# coding: utf-8
import os
import sys
import struct
from math import sin, pi

def produce_audio(basedir):
    filename = os.path.join(basedir, 'testaudio')
    os.system(u'mkfifo %s' % filename)
    if not os.path.exists(basedir):
        print "missing fifo dir %s" % repr(basedir)
    f=open(filename,'w')
    singen = lambda f: lambda t: (int(min(32767, 32768*sin(t*f/1000.0*pi))), int(min(32767, 32768*sin(t*f/1000.0*pi))))
    f.write(''.join( struct.pack('hh', *singen(40)(t)) for t in xrange(44100) ) )
    os.unlink(filename)

if __name__ == '__main__':
    produce_audio(sys.argv[-1] if len(sys.argv) > 1 else '/tmp/xspice-audio/')
