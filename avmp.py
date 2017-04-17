#!/usr/bin/env python

# TODO: Maybe only bring in what we really need
import argparse, sys, os, yaml, pprint, time, jinja2, subprocess

def main():
    # Define arguments
    parser = argparse.ArgumentParser(description='avmp: Automated Virtual Machine Provisioner.')
    parser.add_argument('file', type=str, help='avmp yaml file')
    parser.add_argument('command', type=str, default='status',
        help='command: [up|status|destroy]')
    parser.add_argument('-v','--verbose', help='increase verbosity', action="store_true")
    parser.add_argument('-f','--force', help='force regeneration of vagrantfile', action="store_true")
    args, options = parser.parse_known_args()

    # Store arguments
    global verbose, force
    verbose = args.verbose
    force = args.force
    filepath = args.file
    command = args.command

    # Load avmp config
    global avmp, avmpPath
    avmp = yaml.safe_load(file('avmp.conf', 'r'))
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
        avmpPath = avmp['WORK_DIR']+config['avmpName']
        checkVagrantFiles(config, filepath)
        runCommand(command, options)
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
        # name
        # box
        # network
    # Everything else is just extra.
    for machine in config['machines']:
        try:
            machine['name']
            machine['box']
            machine['network']
        except:
            print "Missing essential information. Exiting"
            exit(2)
    verbosePrint("All machines have minimum required configuration")

def checkVagrantFiles( config, filepath ):
    # Check to see if existing WORK_DIR/name exists
    # If it does, check the difference between /lastmod file and os.path.getmtime(filepath)
    if os.path.exists(avmpPath):
        lastmodPath = avmpPath+"/lastmod"
        if (force):
            verbosePrint("Forced regeneration of vagrantfile")
            createVagrantFiles(config, filepath)
        else:
            if checkFileValid(lastmodPath):
                lastmodfile = open(lastmodPath, "r")
                lastmod = lastmodfile.read()
                lastmodfile.close()
                if (float(lastmod) < float(os.path.getmtime(filepath))):
                    verbosePrint("Found new changes, updating Vagrant files")
                    createVagrantFiles(config, filepath)
                else:
                    # We're already up to date.
                    return
            # No /lastmod file, assume old
            else:
                verbosePrint("No lastmod file found, updating Vagrant files")
                createVagrantFiles(config, filepath)
    # No directory, assume new .yaml, create dir + continue
    else:
        verbosePrint(avmpPath + " does not exist, creating it..")
        os.makedirs(avmpPath)
        verbosePrint("Updating Vagrant files")
        createVagrantFiles(config, filepath)

def createVagrantFiles( config, filepath ):
    # Symlink local scripts/ to WORK_DIR/scripts
    if not os.path.islink(avmpPath+'/scripts'):
        os.symlink(os.getcwd()+'/scripts', avmpPath+'/scripts')

    # Symlink local sync/ to WORK_DIR/sync
    if not os.path.islink(avmpPath+'/sync'):
        os.symlink(os.getcwd()+'/sync', avmpPath+'/sync')

    # Run the templating functions to turn config into a vagrant file
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates')
    )
    template = env.get_template('vagrantfile.template')

    with open(avmpPath+"/vagrantfile", "w") as outputfile:
        outputfile.write(template.render(machines=config['machines']));
    verbosePrint("Written new vagrantfile from template");

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

def runCommand(command, options):
    arguments = []
    arguments.extend(['vagrant'])
    arguments.extend([command])
    arguments.extend(options)
    command = subprocess.check_call(arguments, cwd=avmpPath)

def exit(code):
    # Do any shutdown steps here
    sys.exit(code)

def verbosePrint(string):
    if verbose:
        print string

if __name__ == "__main__":
    main()
