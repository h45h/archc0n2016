# build.py
# Ash Holtz 2016
# Build a CrowdResponse exe with embedded config
# Run instructions:
# Put the resource hacker exe in the same directory as this script.
# Run build.py <project_name>

import argparse
import sys
import win32api
from datetime import datetime
from os import path, listdir, getcwd, mkdir, remove
from os.path import join
from subprocess import call


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller - from the internet!"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


def clean(outpath):
    """
    Delete copied files from target output folder
    :param outpath: Directory to clean
    :return:
    """
    clean_files = ['CrowdResponse.exe']
    for f in listdir(outpath):
        for q in clean_files:
            if q in f:
                try:
                    remove(path.join(outpath,f))
                except:
                    pass


def encode(infile, outfile, eng_name):
    """
    Replace project token with project name
    :param infile: user specified or embedded config
    :param outfile: replaced config
    :param eng_name: project name
    :return:
    """
    with open(infile, 'rb') as inf:
        with open(outfile, 'wb') as outf:
            outf.write(inf.read().replace('<project>', eng_name.lower()))


def main():
    parser = argparse.ArgumentParser(
    description='Welcome to the cr builder. Give me some'\
                'options and I can build you something. '\
                'Only engagement name is required.'
                ,formatter_class=argparse.RawTextHelpFormatter
                )

    parser.add_argument('engagement_name', action="store", default=None)
    parser.add_argument('-f', action="store", dest="cr_exe_loc", default=None,
                        help="Location of the CrowdResponse executable you want to use. If not provided,"
                             " I'll use the one that lives inside of me.")
    parser.add_argument('-c', action="store", dest="master_config_path", default=None,
                        help="Path to configuration file. If not provided, I use the one from box or my embedded default.")
    parser.add_argument('-o', action="store", dest='out_path', default=getcwd(),
                        help="Output location. I default to the directory you're running me from.")
    parser.add_argument('-v', action="store_true", dest='version', default=False,
                        help="Lists the version of python, CrowdResponse, and other tools that I'm using.")
    parser.add_argument('-n', action="store", dest='out_name', default=None,
                        help="What you want me to name the exe. I default to <engagement>_<date>.exe.")
    parser.add_argument('-r', action="store", dest='resource_hacker_path', default=None,
                        help="Where the ResourceHacker.exe lives. I default to my directory.")
    args = parser.parse_args()

    if args.version:
        print 'Using Python version {0}.{1}.{2}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
        cr_location = resource_path('cr')
        info = win32api.GetFileVersionInfo(path.join(cr_location, 'CrowdResponse.exe'), "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        vers = "%d.%d.%d.%d" % (win32api.HIWORD(ms), win32api.LOWORD (ms),
                                     win32api.HIWORD (ls), win32api.LOWORD (ls))
        print 'CrowdResponse exe packaged version {0}'.format(vers)
        print 'Config file: crowdresponse_config.txt'
        sys.exit(0)

    today = datetime.now().strftime('%Y_%m_%d')
    eng_name = args.engagement_name.lower().replace(' ', '_')
    out_base = args.out_path
    out_path = path.join(out_base,eng_name)
    master_config_out_path = path.join(out_path,'crowdresponse_config_enc.txt')
    master_config_path = args.master_config_path
    cr_exe = args.cr_exe_loc
    cr_out = path.join(out_path, '{0}_{1}.exe'.format(eng_name, today))
    if not path.isdir(out_path):
        mkdir(out_path)

    if args.out_name:
        n = args.out_name.replace('.exe','')
        cr_out = path.join(out_path, '{0}.exe'.format(n))

    if not master_config_path or not cr_exe:
        # Defaults to the embedded resource
        cr_location = resource_path('cr')
        if not master_config_path:
            master_config_path = path.join(cr_location,'crowdresponse_config.txt')
        if not cr_exe:
            cr_exe = path.join(cr_location, 'CrowdResponse.exe')
    print cr_exe
    encode(master_config_path, master_config_out_path, eng_name)
    resource_hacker = args.resource_hacker_path
    if not resource_hacker:
        resource_hacker = join(getcwd(),'ResourceHacker.exe')
    call([resource_hacker,
        '-addoverwrite',  '{0}, {1}, {2}, CONFIG, 105, 1033'.format(
        cr_exe, cr_out, master_config_out_path
    )])
    clean(out_path)


if __name__ == "__main__":
    main()



