#!/usr/bin/env python
# encoding: utf-8


def log(text):
    text = str(text)
    with open("debug.log", 'a') as fd:
        if text.endswith('\n'):
            fd.write(text)
        else:
            fd.write(text + "\n")
            
    
