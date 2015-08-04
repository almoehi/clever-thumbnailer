import sys
import os
import argparse
from ConfigParser import ConfigParser
import logging

from audioanalyser import AudioAnalyser
from cleverthumbnailer.exceptions import FileNotFoundException
from ctconstants import CONFIGFILE, DESCRIPTION, PROG

logging.basicConfig()
_logger = logging.getLogger()


def main(args, configFile):
    """Main routine to launch and run CleverThumbnailer

    Args:
        args(list): Command line arguments
        configFile(string): Location of config file
    Returns:
        exit code(int)

    Throws:
        SystemExit: if exit is invalid
    """

    if not os.path.isfile(configFile):
        raise FileNotFoundException('Config file not found')

    thumbnailerConfig = getConfig(configFile)
    parsedArgs = parseArgs(args, dict(thumbnailerConfig.items('DEFAULTS')))

    if parsedArgs.verbose == 0:
        _logger.setLevel(logging.WARN)
    elif parsedArgs.verbose == 1:
        _logger.setLevel(logging.INFO)
    elif parsedArgs.verbose >= 2:
        _logger.setLevel(logging.DEBUG)

    analyser = AudioAnalyser()
    analyser.loadAudio(parsedArgs.input)
    analyser.processAll()
    print(analyser.thumbnail)

    return 0  # success exit code


def getConfig(configFile):
    newConfig = ConfigParser()
    newConfig.read(configFile)
    return newConfig


def parseArgs(cmdargs, defaults):
    """
    Parse command line arguments for entry into application

    Args:
        args(list): list of string arguments to be parsed

    Throws:
        SystemExit: if arguments are not syntactically valid
    """

    p = argparse.ArgumentParser(prog=PROG, description=DESCRIPTION)
    p.add_argument(
        'input',
        help='WAVE / BWF file for processing',
        type=argparse.FileType('rb'),
        metavar='input')
    p.add_argument(
        '-v',
        '--verbose',
        help='Increase logging verbosity level',
        action='count')
    p.add_argument(
        '-f',
        '--fade',
        help='Fade in and out times (seconds)',
        nargs=2,
        type=float,
        metavar=('in', 'out'),
        default=(
            float(defaults['fadein']), float(defaults['fadeout'])
        ),
    )
    p.add_argument(
        '-c',
        '--crop',
        help='Crop time (seconds)',
        nargs=2,
        type=float,
        metavar=('in', 'out'),
        default=(
            float(defaults['cropstart']), float(defaults['cropend'])
        ),
    )

    p.add_argument(
        '-l',
        '--length',
        help='Thumbnail length (seconds)',
        nargs=1,
        type=float,
        metavar='seconds',
        default=float(defaults['thumbnaillength']),
    )
    p.add_argument(
        '-d', '--dynamic',
        help='Whether to use dynamic or loudest (default) metric for ' + \
    'choosing segments',
        action='store_true')
    p.add_argument(
        '-n',
        '--noapplause',
        help='Skip applause detection',
        action='store_true')
    p.add_argument(
        '-o',
        '--output',
        help='Output file path',
        type=argparse.FileType('wb'),
        metavar='wavfile')

    # parse args and throw SystemExit if invalid
    return p.parse_args(cmdargs)


if __name__ == '__main__':
    config = getConfig(CONFIGFILE)
    print os.getcwd()
    main(sys.argv[1:], 'config.ini')