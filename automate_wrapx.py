import argparse
import os

import errno


def find_obj_files(src):
    """
    Find valid files to process through Instant Meshes
    :param src: 
    :return: 
    """
    valid_files = []
    for file in os.listdir(src):
        if file.endswith(".ply") or file.endswith(".obj") or file.endswith(".aln"):
            valid_files.append(os.path.abspath(src + '/' + file))

    print('valid files: {}'.format(valid_files))
    return valid_files


def start():
    """
    Start entry funciton.
    :return: 
    """

    # Input Argument ("source image path and output path")
    ap = argparse.ArgumentParser(description='batching obj files through instant meshes')
    ap.add_argument("-m", "--meshes", required=True, help="Input meshes to need to process through Instant Meshes")
    ap.add_argument("-o", "--output", help="Writes to the specified PLY/OBJ output file in batch mode")

    args = vars(ap.parse_args())
    print('args: {}'.format(args))


if __name__ == '__main__':
    start()
