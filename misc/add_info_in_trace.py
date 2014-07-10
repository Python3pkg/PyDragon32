#!/usr/bin/env python
# encoding:utf-8

"""
    Filter Xroar trace files.

    see README for more information.

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import time
import sys
import argparse

class MemoryInfo(object):
    def __init__(self, rom_info_file):
        self.mem_info = self._get_rom_info(rom_info_file)
        self._cache = {}

    def eval_addr(self, addr):
        addr = addr.strip("$")
        return int(addr, 16)

    def _get_rom_info(self, rom_info_file):
        sys.stderr.write(
            "Read ROM Info file: %r\n" % rom_info_file.name
        )
        rom_info = []
        for line in rom_info_file:
            try:
                addr_raw, comment = line.split(";", 1)
            except ValueError:
                continue

            try:
                start_addr_raw, end_addr_raw = addr_raw.split("-")
            except ValueError:
                start_addr_raw = addr_raw
                end_addr_raw = None

            start_addr = self.eval_addr(start_addr_raw)
            if end_addr_raw:
                end_addr = self.eval_addr(end_addr_raw)
            else:
                end_addr = start_addr

            rom_info.append(
                (start_addr, end_addr, comment)
            )
        sys.stderr.write(
            "ROM Info file: %r readed.\n" % rom_info_file.name
        )
        return rom_info

    def get_shortest(self, addr):
        try:
            return self._cache[addr]
        except KeyError:
            pass

        shortest = None
        size = sys.maxint
        for start, end, txt in self.mem_info:
            if not start <= addr <= end:
                continue

            current_size = abs(end - start)
            if current_size < size:
                size = current_size
                shortest = start, end, txt

        if shortest is None:
            return "$%x: UNKNOWN" % addr

        start, end, txt = shortest
        if start == end:
            info = "$%x: %s" % (addr, txt)
        else:
            info = "$%x: $%x-$%x - %s" % (addr, start, end, txt)
        self._cache[addr] = info
        return info


class XroarTraceInfo(object):
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def add_info(self, rom_info):
        for line in self.infile:
            addr = line[:4]
            try:
                addr = int(addr, 16)
            except ValueError:
                self.outfile.write(line)
                continue

            addr_info = rom_info.get_shortest(addr)
            self.outfile.write(
                    "%s | %s" % (line.strip(), addr_info)
                )



def main(args):
    xt = XroarTraceInfo(args.infile, args.outfile)
    rom_info = MemoryInfo(args.infofile)
    xt.add_info(rom_info)


def get_cli_args():
    parser = argparse.ArgumentParser(description="Add info to Xroar traces")
    parser.add_argument("infile", nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Xroar trace file or stdin"
    )
    parser.add_argument("outfile", nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="If given: write output in a new file else: Display it."
    )
    parser.add_argument("--infofile", metavar="FILENAME",
        type=argparse.FileType("r"),
        help="ROM Info file from: https://github.com/6809/rom-info ;)",
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_cli_args()
    main(args)

