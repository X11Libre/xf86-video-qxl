#!/usr/bin/python

import os
from time import sleep
import subprocess
import atexit

class Process(object):
    processes = []
    @classmethod
    def new(clazz, *args, **kw):
        clazz.processes.append(subprocess.Popen(*args, **kw))
        return clazz.processes[-1]

    @classmethod
    def atexit(clazz):
        for p in reversed(clazz.processes):
            print "child %s" % p.pid
        if False:
            slp = subprocess.Popen(['/usr/bin/sleep', '10000'])
            print "wait on %d" % slp.pid
            slp.wait()
        if len(clazz.processes) == 0:
            return
        for p in reversed(clazz.processes):
            print "kill %s" % p.pid
            try:
                p.kill()
            except:
                pass
        if not any(p.poll() for p in clazz.processes):
            return
        sleep(1)
        for p in reversed(clazz.processes):
            if not p.poll():
                print "terminate %s" % p.pid
                try:
                    p.terminate()
                except:
                    pass

atexit.register(Process.atexit)

def which(prog):
    for path_element in os.environ['PATH'].split(':'):
        candidate = os.path.join(path_element, prog)
        if os.path.exists(candidate):
            return candidate
    return None

client_executable = which('remote-viewer')
if not client_executable:
    raise SystemExit('missing remote-viewer in path')

def launch_xspice(port):
    basedir = '/tmp/xspice_test_audio'
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    assert(os.path.exists(basedir))
    xspice = Process.new(['../scripts/Xspice', '--port', str(port), '--auto', '--audio-fifo-dir', basedir, '--disable-ticketing', ':15.0'])
    xspice.audio_fifo_dir = basedir
    return xspice

def launch_client(port):
    client = Process.new([client_executable, 'spice://localhost:%s' % port])
    return client

if __name__ == '__main__':
    launch_xspice(port=8000)
