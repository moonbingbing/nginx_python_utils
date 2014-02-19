#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0'
__author__  = 'moonbingbing at gmail.com'

import os
import re
import sys
try:
    import multiprocessing #new in python 2.6
except ImportError:
    multiprocessing = None

def get_worker_cpu_affinity(worker_processes):
    worker_cpu_affinity = []
    for i in range(0, worker_processes):
        c = bin(2 ** i)
        c = c.replace('0b', '0' * (worker_processes - len(c) + len('0b')))
        worker_cpu_affinity.append(c)
    return ' '.join(worker_cpu_affinity)

def get_cpu_processor_count():
    '''NOTICE: If you are using Windows and python versions lower than 2.6, the function can not get cpu count '''
    cpu_processor_count = 1 #default is 1 
    try: 
        if multiprocessing:
            cpu_processor_count = multiprocessing.cpu_count()
        else:
            cpu_processor_count = os.sysconf("SC_NPROCESSORS_CONF") # not available in windows
    except Exception, e:
        print "Could not get cpu_processor_count,return the default value. error info: %s" % str(e)
    return cpu_processor_count

def auto_modify_nginx_cpu_conf(filepath):
    ''' auto modify worker_processes and worker_cpu_affinity in nginx.conf according to the number of cpu.
        filepath: where's nginx.conf. default is /etc/nginx.conf '''
    if not os.path.exists(filepath):
        print 'nginx.conf not exist : %s' % filepath
        return False
    
    nginx_conf = ''
    with open(filepath) as f:
        nginx_conf = f.read()
        
    cpu_processor_count = get_cpu_processor_count()
    worker_cpu_affinity = get_worker_cpu_affinity(cpu_processor_count)
    
    cpu_affinity_conf = 'worker_cpu_affinity %s;' % worker_cpu_affinity
    p = re.compile('worker_cpu_affinity[\d\s]+?;')
    nginx_conf, sub_number = p.subn(cpu_affinity_conf, nginx_conf)
    #if worker_cpu_affinity is not yet configured, auto add to the begin of nginx.conf
    if sub_number == 0:
        nginx_conf = cpu_affinity_conf + '\r\n' + nginx_conf
        
    cpu_processes_conf = 'worker_processes %s;' % cpu_processor_count
    p = re.compile('worker_processes[\d\s]+?;')
    nginx_conf, sub_number = p.subn(cpu_processes_conf, nginx_conf)
    if sub_number == 0:
        nginx_conf = cpu_processes_conf + '\r\n' + nginx_conf
        
    with open(filepath, 'w') as f:
         f.write(nginx_conf)
         
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = '/etc/nginx.conf'
    print auto_modify_nginx_cpu_conf(filepath)