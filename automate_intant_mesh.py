import argparse
import os, glob
import shlex
import sys
import errno
import subprocess
import threading
from datetime import datetime


def make_dir(output):
    """
    Make output folders on given path.
    :param output: 
    :return: 
    """
    print(os.path.dirname(output))
    if not os.path.exists(output):
        try:
            os.makedirs(output)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


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


def process_vertices_count(args):
    src = args["meshes"]
    args["meshes"] = None
    valid_files = find_obj_files(src)

    for file in valid_files:
        print('filename: {}, vertices: {}'.format(file, get_vertices(file)))


def process_instant_meshes(args):
    """
    Put the files through Instant Meshes
    :param args: 
    :return: 
    """
    src = args["meshes"]
    args["meshes"] = None
    make_dir(args["output"])
    valid_files = find_obj_files(src)

    command = ['Instant Meshes.exe']
    options = []

    # Add options to Instant meshes.exe
    for key in args.keys():
        if key == "output":
            continue
        if args[key] is not None:
            options.append("-" + key[0])
            options.append(args[key])

    command += options
    # print('Command to run: {}'.format(command))

    timestamp_start = datetime.now()
    for index, file in enumerate(valid_files):
        output_file = args["output"] + '/' + 'C59_IM-31110_F_' + str(index) + '.obj'
        command.append('-o')
        command.append(str(output_file))
        command.append(file)

        sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (results, errors) = sp.communicate()
        print('results: {}, errors: {}'.format(results, errors))
        del command[-1]
        del command[-1]
        del command[-1]

    timestamp_end = datetime.now()

    print('It takes {} to run whole process'.format(timestamp_end - timestamp_start))


def get_vertices(file):
    """
    Get vertices from obj file.
    :param file: 
    :return: 
    """
    count = 0
    with open(file, mode='r') as obj:
        content = obj.read()
        elements = content.split('\n')
        for item in elements:

            if item.split(' ')[0] == 'v':
                count += 1
    return count


def start():
    """
    Start entry funciton.
    :return: 
    """

    # Input Argument ("source image path and output path")
    ap = argparse.ArgumentParser(description='batching obj files through instant meshes')
    ap.add_argument("-m", "--meshes", required=True, help="Input meshes to need to process through Instant Meshes")
    ap.add_argument("-o", "--output", help="Writes to the specified PLY/OBJ output file in batch mode")
    ap.add_argument("-t", "--threads", default='10', help=" Number of threads used for parallel computations")
    ap.add_argument("-d", "--deterministic", help="Prefer (slower) deterministic algorithms")
    ap.add_argument("-c", "--crease", help="Dihedral angle threshold for creases")
    ap.add_argument("-S", "--smooth", default='0',
                    help="Number of smoothing & ray tracing reprojection steps (default: 2)")
    ap.add_argument("-D", "--dominant", help="Generate a tri/quad dominant mesh instead of a pure tri/quad mesh")
    ap.add_argument("-i", "--intrinstic", help="Intrinsic mode (extrinsic is the default)")
    ap.add_argument("-b", "--boundaries", help="Align to boundaries (only applies when the mesh is not closed)")
    ap.add_argument("-r", "--rosy", default='4', help="Specifies the orientation symmetry type (2, 4, or 6)")
    ap.add_argument("-p", "--posy", default='4', help="Specifies the position symmetry type (4 or 6)")
    ap.add_argument("-s", "--scale", help="Desired world space length of edges in the output")
    ap.add_argument("-f", "--faces", help="Desired face count of the output mesh")
    ap.add_argument("-v", "--vertices", default='31110', help="Desired vertex count of the output mesh")
    ap.add_argument("-C", "--compat", help="Compatibility mode to load snapshots from old software versions")
    ap.add_argument("-k", "--knn", help="Point cloud mode: number of adjacent points to consider")
    ap.add_argument("-F", "--fullscreen", help="Open a full-screen window")

    args = vars(ap.parse_args())
    print('args: {}'.format(args))

    # Get Arguments from command line
    # process_instant_meshes(args)
    process_vertices_count(args)

if __name__ == '__main__':
    # start function
    start()
