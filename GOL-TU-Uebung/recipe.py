import argparse
import sys,os

# release container from xeus-cling-cuda-container project
# https://github.com/ComputationalRadiationPhysics/xeus-cling-cuda-container
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'xeusClingCudaContainer'))
import generator as gn

from hpccm.primitives import copy, shell, runscript, environment, label
from hpccm.templates.CMakeBuild import CMakeBuild
from hpccm.building_blocks.packages import packages
from hpccm.templates.git import git

container_version = 1.0

def main():
    parser = argparse.ArgumentParser(
        description='Simple script for generating a singularity recipe for the GOL exercise.')
    parser.add_argument('--build_prefix', type=str, default='/tmp/GOL_example',
                        help='Define the path in which all projects will be built (default: /tmp/GOL_example).')
    parser.add_argument(
        '-j', type=str, help='number of build threads for make (default: -j)')
    parser.add_argument(
        '-l', type=str, help='number of linker threads for the cling build (default: -j)')
    parser.add_argument('-v ', '--version', action='store_true',
                        help='print version of the container')
    args = parser.parse_args()

    if args.version:
        print(container_version)
        sys.exit(0)

    if args.j:
        threads = int(args.j)
        if threads < 1:
            raise ValueError('-j have to be greater than 0')
    else:
        threads = None

    if args.l:
        linker_threads = int(args.l)
        if linker_threads < 1:
            raise ValueError('-l have to be greater than 0')
    else:
        linker_threads = None

    xcc_gen = gn.XCC_gen(build_prefix=args.build_prefix,
                         threads=threads,
                         linker_threads=linker_threads)
    stage = xcc_gen.gen_release_single_stage()

    stage += label(metadata={'EXAMPLE_CONTAINER_MAINTAINER': 'Simeon Ehrig'})
    stage += label(metadata={'EXAMPLE_CONTAINER_EMAIL': 's.ehrig@hzdr.de'})
    stage += label(metadata={'EXAMPLE_CONTAINER_Version': str(container_version)})

    # disable the xsrf check, which avoid some problems in Firefox
    stage += copy(src='jupyter_notebook_config.py', dest='/')

    # copy and build the pnwriter library
    stage += packages(ospackages=['libpng-dev'])
    png_git = git()
    stage += png_git.clone_step(repository='https://github.com/pngwriter/pngwriter.git',
                                branch='dev',
                                path='/opt/')
    png_cmake = CMakeBuild()
    stage += shell(commands=[png_cmake.configure_step(directory='/opt/pngwriter',
                                                  opts=['-DBUILD_SHARED_LIBS=ON']),
                             png_cmake.build_step(target='install')])

    # copy and install jitify
    jitify_git = git()
    stage += jitify_git.clone_step(repository='https://github.com/NVIDIA/jitify.git',
                                path='/opt/')
    png_cmake = CMakeBuild()
    stage += shell(commands=['cp /opt/jitify/jitify.hpp /usr/local/include'])

    stage += shell(commands=['rm -rf /opt/pngwriter',
                             'rm -rf /opt/jitify'])

    # check if the path to the notebook is specified, otherwise use the current directory
    stage += runscript(commands=['if [ $# -gt 0 ]',
                                 'then',
                                 'cd $1',
                                 'fi',
                                 'jupyter-notebook --config=/jupyter_notebook_config.py'])

    print(stage.__str__())


if __name__ == '__main__':
    main()
