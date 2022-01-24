#! /usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys
import cv2 as cv
import argparse
import termcolor
import ast
import copy

ignore_color = (255, 255, 255) #white
color_threshold = 10 #+- this color to be registered - might be needed due to compression alg

class ImageToGcode():
    def __init__(self,
                 img,
                 spread,
                 nozzles,
                 area,
                 feedrate,
                 offsets,
                 verbose=False):
        self.img = cv.imread(img)
        self.output = ""
        self.outFile = os.path.splitext(os.path.abspath(img))[0] + ".gco"
        self.spread = spread
        self.nozzles = int(nozzles)
        self.increment = spread/nozzles
        self.printArea = area
        self.feedrate = feedrate
        #change colors to sauces here
        self.red = (0, 0, 255)
        self.orange = (0, 152, 255)
        self.white = (255, 255, 255)
        self.black =(0, 0, 0)
        self.green = (0, 255, 0)
        self.offsets = offsets
        self.debug_to_terminal()
        self.make_gcode()

    def make_gcode(self):
        self.output = "M106\n"  # Start Fan
        nozzleFirings = [0 for x in range(0, self.img.shape[1])]
        nozzleFirings = [copy.copy(nozzleFirings) for x in range(0, self.nozzles)]
        scan = range(0, self.img.shape[0])
        scan = reversed(scan)
        for y in scan:
            for x in range(0, self.img.shape[1]):
                color = tuple(self.img[y, x])
               
                if color == ignore_color:
                    pass
                elif color == self.red:
                    nozzleFirings[0][x] += 1 << y % self.nozzles
                elif color == self.orange:
                    nozzleFirings[1][x] += 1 << y % self.nozzles
                elif color == self.green:
                    nozzleFirings[2][x] += 1 << y % self.nozzles
                elif color == self.black:
                    nozzleFirings[3][x] += 1 << y % self.nozzles
                else:
                    pass
            if y % self.nozzles == 0 and y > 0:
                for headNumber, headVals in enumerate(nozzleFirings):
                    for column, firingVal in enumerate(headVals):
                        if firingVal:
                            currentOffset = self.offsets[headNumber]
                            self.output += "G1 X"+str(self.increment*column-currentOffset[0])+" Y"+str(y/12*self.spread-currentOffset[1])+" F"+str(self.feedrate)+"\n"
                            self.output += "M400\n"
                            self.output += "M700 P"+str(headNumber)+" S"+str(firingVal)+"\n"
                #print(str(nozzleFirings))
                nozzleFirings = [0 for x in range(0, self.img.shape[1])]
                nozzleFirings = [copy.copy(nozzleFirings) for x in range(0, 4)]
        f = open(self.outFile, 'w')
        f.write(self.output)
        f.close()
        #print(self.output)

    def debug_to_terminal(self):
        print("Rows: "+str(self.img.shape[0]))
        print("Cols: "+str(self.img.shape[1]))
        print("Spread: "+str(self.spread)+"mm")
        print("Nozzles: "+str(self.nozzles))
        print("Print Area: "+str(self.printArea)+"mm")
        rowStr = ""
        for y in range(0, self.img.shape[0]):
            rowStr = ""
            for x in range(0, self.img.shape[1]):
                color = tuple(self.img[y, x])
                #print(color)
                #print(self.red)
                if color == self.red:
                    rowStr += termcolor.colored(" ", 'red', 'on_red')
                if color == self.green:
                    rowStr += termcolor.colored(" ", 'green', 'on_green')
                elif color == self.white:
                    rowStr += termcolor.colored(" ", 'white', 'on_white')
                elif color == self.orange:
                    rowStr += termcolor.colored(" ", 'yellow', 'on_yellow')
                elif color == self.black:
                    rowStr += " "
                else:
                    print(color)
                    rowStr += termcolor.colored(" ", 'white', 'on_white')
            print(rowStr)


if __name__ == "__main__":
    #Setup Command line arguments
    parser = argparse.ArgumentParser(prog="image_to_gcode.py",
                                     usage="%(prog)s [options] input...",
                                     description="Convert bitmaps to gcode."
                                     )
    parser.add_argument("-o", "--output",
                        default=sys.stdout,
                        help="Output file, defaults to stdout"
                        )
    parser.add_argument("-s", "--spread",
                        default="3.175",
                        help="Nozzle spread (mm). Default: %(default)s"
                        )
    parser.add_argument("-n", "--nozzles",
                        default="12",
                        help="Nozzle count. Default: %(default)s"
                        )
    parser.add_argument("-a", "--area",
                        default="[200, 200]",
                        help="Print area in millimeters. Default: %(default)s"
                        )
    parser.add_argument("-f", "--feedrate",
                        default="1000",
                        help="Print feedrate. Default: %(default)s"
                        )
    parser.add_argument("input",
                        help="input file, defaults to stdin"
                        )
    parser.add_argument('--version',
                        action='version',
                        version="%(prog)s 0.0.1-dev"
                        )
    parser.add_argument("-r", "--red",
                        default="[0, 0]",
                        help="Head offset in millimeters. Default: %(default)s"
                        )
    parser.add_argument("-g", "--green",
                        default="[30.5, 0.1]",
                        help="Head offset in millimeters. Default: %(default)s"
                        )
    parser.add_argument("-b", "--blue",
                        default="[0, 0]",
                        help="Head offset in millimeters. Default: %(default)s"
                        )
    parser.add_argument("-k", "--black",
                        default="[0, 0]",
                        help="Head offset in millimeters. Default: %(default)s"
                        )

    #Always output help by default
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)  # Exit after help display

    args = parser.parse_args()
    offsets = [ast.literal_eval(args.red),
               ast.literal_eval(args.green),
               ast.literal_eval(args.blue),
               ast.literal_eval(args.black)
               ]

    imageProcessor = ImageToGcode(img=args.input,
                                  spread=float(args.spread),
                                  nozzles=float(args.nozzles),
                                  area=ast.literal_eval(args.area),
                                  feedrate=float(args.feedrate),
                                  offsets=offsets
                                  )
