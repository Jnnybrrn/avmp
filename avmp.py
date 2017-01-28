#!/usr/bin/python

import sys
import getopt

def main():
    try:
        options, args =  getopt.getopt(sys.argv[1:], '', [
        'help=', 'options=', 'here='])
    except getopt.error, inputErr:
        print str(inputErr)
        printUsage()
        exit(2)

    if len(args) > 2:
        print "Arguments: ", args, " not valid. See --help for info"


def up():
    print "Command:  Up"

def status():
    print "Command: Status"

def destroy():
    print "Command: Destroy"

def printUsage():
    print 'Usage: avmp <config file> <command>.'
    print 'Config file must point to a valid avmp .yaml file'
    print 'Available commands are:'
    print '\tup - create, and provision machines'
    print '\tstatus - display current status of machines'
    print '\tdestroy - shutdown and remove machines'

def exit(code):
    # Do any shutdown steps here
    sys.exit(code)

if __name__ == "__main__":
    main()
