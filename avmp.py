#!/usr/bin/python

import argparse, sys

def main():
    # Define arguments
    parser = argparse.ArgumentParser(description='avmp: Automated Virtual Machine Provisioner.')
    parser.add_argument('file', type=str, help='avmp yaml file')
    parser.add_argument('command', type=str, default='status',
        help='command: [up|status|destroy]')
    parser.add_argument('-v','--verbose', help='increase verbosity', action="store_true")
    args = parser.parse_args()

    # Store arguments
    global verbose, filename
    verbose = args.verbose
    filename = args.file
    command = args.command

    # Do actions based on arguments
    print "Filename is: ", filename
    switch(command)
    exit(1)

def switch( command ):
    if command == 'up':
        up()
    elif command == 'status':
        status()
    elif command == 'destroy':
        destroy()

def up():
    if verbose:
        print "The Command you entered was: Up"
        return
    print "Command:  Up"

def status():
    if verbose:
        print "The Command you entered was: Status"
        return
    print "Command: Status"

def destroy():
    if verbose:
        print "The Command you entered was: Destroy"
        return
    print "Command: Destroy"

def exit(code):
    # Do any shutdown steps here
    sys.exit(code)

if __name__ == "__main__":
    main()
