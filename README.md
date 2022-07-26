# Map Visualizer

Simple python script that uses [StellaVSLAM Python Bindings](https://github.com/Squiro/StellaVSLAM-Python-bindings) to open the viewer and visualize a map.

## Usage

Execute with:

    python3 visualizer.py -p path/to/your/map.msg

## Considerations

You have to include a config.yaml inside stella_bindings folder, and also the .so library of the bindings.