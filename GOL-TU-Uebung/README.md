# Exercise "Game of Life" of the module "Hochparallele Programmierung von GPUs" of the TU Dresden

## Usage

1. Generate the singularity recipe with the python script
2. Build container
3. Run container

```bash
# run jupyter notebook server with the current directory as notebook root
singularity run --nv GOL-TU-ex.sif
# run jupyter notebook server with specific directory
singularity run --nv GOL-TU-ex.sif <path/to/notebook/directory>
```

## Software background

The notebook uses the NVIDIA CUDA driver API and [jitify](https://github.com/NVIDIA/jitify) to allow redefinition of kernels. The world of Game of Life is visualized with the [pngwriter](https://github.com/pngwriter/pngwriter) library. The software base stack uses [cling](https://github.com/root-project/cling) and [xeus-cling](https://github.com/QuantStack/xeus-cling).
