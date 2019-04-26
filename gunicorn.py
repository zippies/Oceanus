# -*- encoding:utf-8 -*-
import multiprocessing

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
backlog = 2048
reload = False
debug = False
