#!/usr/bin/env python

import argparse, sys, os, yaml

def main():
    # Define arguments
    parser = argparse.ArgumentParser(description='avmp: Automated Virtual Machine Provisioner.')
    parser.add_argument('file', type=str, help='avmp yaml file')
    parser.add_argument('command', type=str, default='status',
        help='command: [up|status|destroy]')
    parser.add_argument('-v','--verbose', help='increase verbosity', action="store_true")
    args = parser.parse_args()

    # Store arguments
    global verbose
    verbose = args.verbose
    filepath = args.file
    command = args.command

    # Load avmp config
    avmp = yaml.safe_load(file('etc/avmp.conf', 'r'))

    # Do actions based on arguments
    # Filepath
    fileValid = checkFileValid(filepath)

    # Command
    if fileValid:
        #psuedo-code
        config = readYaml(filepath)
        verifyConfig(config) # i.e. check the essentials for life are there.
        createVagrantFiles(config, filepath)
        switch(command)
        # Finished
        exit(1)
    else:
        exit(2)

def readYaml( filepath ):
    try:
        config = yaml.safe_load(file(filepath, 'r'))
    except yaml.YAMLError, err:
        print filepath, "contains error(s).", err
        exit(2)

    return config

def verifyConfig( config ):
    # Minimum, each box must have..
        # box
        # hostname
        # network
    # Everything else is just extra.
    for box in config['boxes']:
        try:
            box['box']
            box['hostname']
            box['network']
        except:
            print "Missing essential information. Exiting"
            exit(2)
        print box['box'],'\n', box['hostname'],'\n', box['network'],'\n'
    print "All boxes have minimum required configuration"

def createVagrantFiles( config, filepath ):
    # Check to see if existing WORK_DIR/name exists
    # If it does, check the difference between /lastmod file and os.path.getmtime(filepath)
    # If it requires changing, run the templating functions to turn config into a vagrant file
    # If it doesn't, or after completion, return/end/whatever.
    return True

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
