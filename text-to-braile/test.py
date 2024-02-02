#!/usr/bin/env python3

import sys
import louis

def main(*args, **kwargs):
    louis.setLogLevel(louis.LOG_OFF)
    # check tables seperately cause it's better for memory (for some reason)
    louis.checkTable("en-gb-g1.utb")
    louis.checkTable("en-GB-g2.ctb")

    if args[0] == '1':
        table_list = "./en-gb-g1.utb"
    elif args[0] == '2':
        table_list = "./en-GB-g2.ctb"
    else:
        print("Invalid arguments. Grade: " + args[0])
        return

    print(louis.translateString(table_list, args[1], mode=68))


if __name__ == "__main__":
    main(*sys.argv[1:])
