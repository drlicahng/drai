# -*- encoding:utf-8 -*-
from threading import Thread
from time import sleep

def drSyn(func,params=()):
	t = Thread(target = func , args=params )
	t.start()
	
