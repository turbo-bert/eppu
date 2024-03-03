import requests
import subprocess
import sys
import rich
from rich.pretty import pprint as PP
from rich.console import Console
from rich.table import Table
CONSOLE = Console()

import argparse
parser = argparse.ArgumentParser(prog="eppu", description="Easy Python Package Updater.", epilog="Useful? Donate: https://www.paypal.com/donate/?hosted_button_id=4EZE2QKKG29JE THANK YOU")
parser.add_argument("pkg", metavar="PACKAGE_NAME", type=str, help="Lowercase name of the package to update")
parser.add_argument("--pip", nargs=1, type=str, default=["pip"], help="Default: use 'pip', place your own pip here if you want")

args = parser.parse_args()
pip_to_use = args.pip[0]

def runpip_uninstall(pkgname):
    global pip_to_use
    global args
    subprocess.call("%s uninstall -y %s" % (pip_to_use, pkgname), shell=True, universal_newlines=True)

def runpip_install(pkgname, pkgver):
    global pip_to_use
    global args
    cmd = "%s install %s==%s" % (pip_to_use, pkgname, pkgver)
    CONSOLE.print(cmd)
    CONSOLE.input(">> press RETURN to execute that # ")
    subprocess.call(cmd, shell=True, universal_newlines=True)
    CONSOLE.input(">> DONE - press RETURN to continue # ")

def runpip_getlocalversion(pkgname):
    global pip_to_use
    lines = subprocess.check_output("%s freeze" % pip_to_use, shell=True, universal_newlines=True).strip().replace("\r", "").split("\n")
    local_versions = [x for x in lines if x.startswith('%s==' % pkgname)]
    local_version = None
    if len(local_versions) > 0:
        local_version = local_versions[0].split("==")[1]
    return local_version

latest_online = requests.get('https://pypi.org/pypi/%s/json' % args.pkg).json()["info"]["version"]

local_version = runpip_getlocalversion(args.pkg)
installed = True
if local_version == None:
    installed = False
    local_version = "NOT INSTALLED"

CONSOLE.print("Latest ONLINE Version is %s" % latest_online)
CONSOLE.print("Local Version is %s" % local_version)

if local_version == latest_online:
    CONSOLE.print("No updates available.")
    sys.exit(0)

if installed:
    runpip_uninstall(args.pkg)

while True:
    runpip_install(args.pkg, latest_online)
    if runpip_getlocalversion(args.pkg) != None:
        break

CONSOLE.print("Updated %s to %s" % (args.pkg, latest_online))
sys.exit(0)
