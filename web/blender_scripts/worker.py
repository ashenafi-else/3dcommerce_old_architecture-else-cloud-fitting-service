import os
import subprocess
import logging
import sys

logger = logging.getLogger(__name__)


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
BLENDER_PATH = '/usr/local/blender/2.78c/blender'
SCRIPTS_PATH = os.path.join(os.sep, BASE_PATH, 'scripts')


def execute_blender_script(script, out_file=None, in_file=None, params=[], blender=None):
    if params is None:
        params = []
    if blender is None:
        blender = BLENDER_PATH
    script_path = os.path.join(os.sep, SCRIPTS_PATH, script)
    arguments = [blender, '--background']
    if in_file is not None:
        arguments.append(in_file)
    arguments.append('--python')
    arguments.append(script_path)
    if out_file is not None:
        params = [out_file,] + params

    print(arguments + ['--',] + params)
    try:
        subprocess.call(arguments + ['--'] + params)
    except:
        logger.debug(
            "execute_blender_script error {}/n{}".format(
                sys.exc_info()[0],
                arguments + ['--', out_file] + params
            )
        )