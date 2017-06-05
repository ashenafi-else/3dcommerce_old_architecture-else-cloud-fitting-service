import os
import subprocess
import logging
import sys

logger = logging.getLogger(__name__)


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

BLENDER_PATH = '/usr/local/blender/2.78c/blender'
SCRIPTS_PATH = os.path.join(os.sep, BASE_PATH, 'blender_scripts')

BLENDER_MAPPING = [
    (BLENDER_PATH, 'Blender v2.78c with blend4web v17_02_1'),
]


def execute_blender_script(script, out_file, in_file=None, params=None, blender=None):
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
    print(arguments + ['--', out_file] + params)
    try:
        subprocess.call(arguments + ['--', out_file] + params)
    except:
        logger.debug(
            "execute_blender_script error {}/n{}".format(
                sys.exc_info()[0],
                arguments + ['--', out_file] + params
            )
        )
