# Image to gcode
Converts an image file to gcode.

## Project Rational
Typically printers will use color overlap to give the appearance of color gradients and continuity. This script is designed to avoid overlap for experiments requiring isolated depositions.

### Example applications
* Bacteria deposition
* Circuit board etch resist
* Circuit construction

## Compatible Firmwares
### Marlin
Use this branch for HPC6602 compatibility with the inkshield.
https://github.com/sjkelly/Marlin/tree/hpc6602


## How to use

positional arguments:
  input                 input file, defaults to stdin

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file, defaults to stdout
  -s SPREAD, --spread SPREAD
                        Nozzle spread (mm). Default: 3.175
  -n NOZZLES, --nozzles NOZZLES
                        Nozzle count. Default: 12
  -a AREA, --area AREA  Print area in millimeters. Default: [200, 200]
  -f FEEDRATE, --feedrate FEEDRATE
                        Print feedrate. Default: 1000
  --version             show program's version number and exit
  -r RED, --red RED     Head offset in millimeters. Default: [0, 0]
  -g GREEN, --green GREEN
                        Head offset in millimeters. Default: [30.5, 0.1]
  -b BLUE, --blue BLUE  Head offset in millimeters. Default: [0, 0]
  -k BLACK, --black BLACK
                        Head offset in millimeters. Default: [0, 0]


User interface is being updated.

## About
This project was started at AMRI at Rice University in August 2013.

## License
See LICENSE.txt

