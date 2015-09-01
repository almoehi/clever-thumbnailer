"""Audio thumbnail creator, powered by calling SoX subprocess"""

import os
import logging
import subprocess

import ctexceptions

_logger = logging.getLogger(__name__)


def createThumbnail(inFile, outFile, startSeconds, durationSeconds, fade):
    """Create an audio thumbnail from an input file

    Args:
        inFile(string): Input file name
        outFile(string): Output file name
        startSeconds(float): Start time in seconds
        durationSeconds(float): duration in seconds
        fadeIn(float): fade up time in seconds
        fadeOut(float): fade out time in seconds
    """
    _logger.debug('Creating thumbnail from track {0} to track {1} with fade'
                  ' times {2}. Starting at {3:.1f}s, duration {'
                  '4:.1f}s.'.format(
        inFile, outFile, fade, startSeconds, durationSeconds)
    )

    # pre-emptively check for file's existence
    if not os.path.isfile(inFile):
        raise ctexceptions.FileNotFoundError('Input file not found when '
                                'creating thumbnail')

    # build sox subprocess parameters
    s = ['sox', str(inFile), str(outFile), 'trim', str(startSeconds),
         str(durationSeconds), 'fade', 't', str(fade[0]), str(durationSeconds),
         str(fade[1])]

    # call SoX to create new file
    _logger.debug('Calling sox with parameters: {0}'.format(' '.join(s)))
    try:
        # call subprocess, and throw exception on non-zero exit code.
        subprocess.check_call(s)
    except subprocess.CalledProcessError:
        _logger.error('Error using SoX to create thumbnail, using '
                      'parameters: {0}'.format(s))
        raise ctexceptions.SoxError('Error creating thumbnail')
