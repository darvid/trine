#!/usr/bin/env python
import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI, SCRIPT_PATH
from models import DBSession, initialize_db_connection


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def call_operation(session, script_name, operation):
    try:
        module = __import__("scripts." + script_name, fromlist=["scripts"])
        getattr(module, operation)(session)
        return True
    except AttributeError, err:
        print err
        print(bcolors.FAIL + "error: " + bcolors.ENDC + "invalid operation")
    except Exception, err:
        print err
        print(bcolors.FAIL + "error: " + bcolors.ENDC + err.message)


def main():
    parser = argparse.ArgumentParser(usage="%(prog)s [script] [operation]")
    parser.add_argument("script", help="name of script or 'all'")
    parser.add_argument("operation", help="[clean|merge]", nargs="?",
        default="merge")
    args = parser.parse_args()

    initialize_db_connection(create_engine(SQLALCHEMY_DATABASE_URI))
    session = DBSession

    if args.script == ["all"]:
        scripts = [f.get_name(False) for f in SCRIPT_PATH.glob("*.py")
            if not f.name.startswith("__init__")]
    else:
        scripts = [args.script]
    for script_name in scripts:
        if call_operation(session, script_name, args.operation):
            print(">> " + {
                "clean": bcolors.OKGREEN, 
                "merge": bcolors.OKBLUE,
            }[args.operation.lower()] + args.operation.lower() + bcolors.ENDC +
            " " + script_name)


if __name__ == "__main__":
    main()
