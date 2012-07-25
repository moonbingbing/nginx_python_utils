nginx-python-utils
=========
nginx-python-utils is a collection of useful python scripts about nginx.

python-utils
=========
1.auto_modify_nginx_cpu_conf.py
---------
If nginx deployed in a cluster of servers, the server's CPU configuration may be different.So set **worker_processes** and **worker_cpu_affinity** according to *the number of CPU process number* is a very troublesome thing.     
If you used [Tengine](http://tengine.taobao.org/), it has a great feature is just set **worker_processes** and **worker_cpu_affinity** to "auto", nginx will be able to adjust automatically according to the number of cpu.     
The purpose of this python script is to implement this feature of Tengine.    
When configured nginx.conf, run the python script, the above two parameters will be automatically modified.    
License
=========
(The MIT License)

Copyright (c) 2012 WenMing <moonbingbing@gmail.com> 
