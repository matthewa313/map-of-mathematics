import argparse
import sys
import os
import render_graph
import render_proofs

# argument parsing
parser = argparse.ArgumentParser(description='Process some integers.')

# list of subdirectories in maps/
supported_maps = [f.name for f in os.scandir(
    os.path.join('..', 'maps')) if f.is_dir()]
parser.add_argument('--map_name',
                    type=str,
                    nargs=1,
                    default='math',
                    choices=supported_maps,
                    help='name of the map to render (default: math)')


def main() -> None:
    args = parser.parse_args()
    render_graph.main(args.map_name)
    render_proofs.main(args.map_name)


if __name__ == '__main__':
    main()
