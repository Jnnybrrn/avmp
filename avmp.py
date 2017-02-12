#!/usr/bin/env python

import argparse, sys, os, yaml, pprint, time

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
    global avmp
    avmp = yaml.safe_load(file('etc/avmp.conf', 'r'))
    avmp['WORK_DIR'] = os.path.expanduser(avmp['WORK_DIR'])

    # DEBUG - Remove
    global pp
    pp = pprint.PrettyPrinter(indent=4)

    # Do actions based on arguments
    # Filepath
    fileValid = checkFileValid(filepath)

    # Command
    if fileValid:
        #psuedo-code
        config = readYaml(filepath)
        verifyConfig(config) # i.e. check the essentials for life are there.
        checkVagrantFiles(config, filepath)
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
    # EnvironmentName must be set.
    try: config['avmpName']
    except NameError:
        print "avmpName not set. Exiting"
        exit(2)
    verbosePrint("avmpName set to " + config['avmpName'])
    # Minimum, each box must have..
        # box
        # hostname
        # network
    # Everything else is just extra.
    for box in config['boxes']:
        try:
            box['name']
            box['box']
            box['hostname']
            box['network']
        except:
            print "Missing essential information. Exiting"
            exit(2)
        print box['box'],'\n', box['name'],'\n', box['hostname'],'\n', box['network'],'\n'
    verbosePrint("All boxes have minimum required configuration")

def checkVagrantFiles( config, filepath ):
    # Check to see if existing WORK_DIR/name exists
    avmpPath = avmp['WORK_DIR']+config['avmpName']
    # If it does, check the difference between /lastmod file and os.path.getmtime(filepath)
    if os.path.exists(avmpPath):
        lastmodPath = avmpPath+"/lastmod"
        if checkFileValid(lastmodPath):
            lastmodfile = open(lastmodPath, "r")
            lastmod = lastmodfile.read()
            lastmodfile.close()
            if (lastmod < os.path.getmtime(filepath)):
                verbosePrint("Found new changes, updating Vagrant files")
                createVagrantFiles(config, filepath, avmpPath)
            else:
                # We're already up to date.
                return
        # No /lastmod file, assume old
        else:
            verbosePrint("No lastmod file found, updating Vagrant files")
            createVagrantFiles(config, filepath, avmpPath)
    # No directory, assume new .yaml, create dir + continue
    else:
        verbosePrint(avmpPath + " does not exist, creating it..")
        os.makedirs(avmpPath)
        verbosePrint("Updating Vagrant files")
        createVagrantFiles(config, filepath, avmpPath)

def createVagrantFiles( config, filepath, avmpPath ):
    # Run the templating functions to turn config into a vagrant file


    # And update /lastmod
    with open(avmpPath+"/lastmod", "w") as lastmod:
        lastmod.write("%s" % time.time())
    verbosePrint(avmpPath+"/lastmod updated.")

    return True

def checkFileValid( filepath ):
    # print "Filepath is: ", filepath
    # print "File is: ", os.path.basename(filepath)
    # print "Dirname is: ", os.path.dirname(filepath)
    if os.path.exists(filepath):
        if os.path.isfile(filepath):
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
        print "File", filepath," not found (or no access)."
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
        verbosePrint("The Command you entered was: Up")
        return
    print "Command:  Up"

def status():
    if verbose:
        verbosePrint("The Command you entered was: Status")
        return
    print "Command: Status"

def destroy():
    if verbose:
        verbosePrint("The Command you entered was: Destroy")
        return
    print "Command: Destroy"

def exit(code):
    # Do any shutdown steps here
    sys.exit(code)

def verbosePrint(string):
    if verbose:
        print string

if __name__ == "__main__":
    main()
