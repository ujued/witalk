#!/bin/sh
sudo spawn-fcgi -f `echo $PWD`/entry.py -p 5200 -P /run/witalk.pid -a 127.0.0.1