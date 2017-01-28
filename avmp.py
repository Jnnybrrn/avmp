#!/usr/bin/python

import argparse, sys, os

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
    filepath = args.file
    command = args.command

    # Do actions based on arguments
    # Filepath
    fileValid = checkFileValid(filepath)

    # Command
    if fileValid:
        switch(command)
    else:
        # Finished
        exit(1)

def checkFileValid( filepath ):
    # print "Filepath is: ", filepath
    # print "File is: ", os.path.basename(filepath)
    # print "Dirname is: ", os.path.dirname(filepath)
    if os.path.exists(filepath):
        if os.path.isfile(filepath):
            print "This file exists"
            print "LastModifiedTime is: ", os.path.getmtime(filepath)
            try:
                with open(filepath) as tempFile:
                    return True
            except Exception as err:
                print "File is not readable,", err
                return False
        elif os.path.isdir(filepath):
            # TODO: Implement passing a folder (and it searching for .yaml)
            print "Passing a folder not implemented"
            return False
        else:
            print "Something went wrong; I don't know what file is."
            return False
    else:
        print "File", filepath," not found (or no access). Exiting"
        return False


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
