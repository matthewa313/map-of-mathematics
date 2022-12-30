import os
import sys


def json_escape_characters(hjson_file: str) -> None:
    # change esc characters in hjson_file (\ -> \\) for json conversion
    with open(hjson_file, 'r') as f:
        lines = f.readlines()
        f.close()
    with open(hjson_file, 'w') as f:
        for line in lines:
            line = line.replace('\\', '\\\\')
            f.write(line)
        f.close()


def tex_escape_characters(hjson_file: str) -> None:
    # change esc characters in hjson_file (\\ -> \) for TeX-esque readability
    with open(hjson_file, 'r') as f:
        lines = f.readlines()
        f.close()
    with open(hjson_file, 'w') as f:
        for line in lines:
            line = line.replace('\\\\', '\\')
            line = line.replace('\\\\t', '\\t')
            f.write(line)
        f.close()


def convert_dfs(path: str) -> None:
    # convert all hjson files in path to json
    for f in os.listdir(path):
        if f.endswith('.hjson'):
            print('Converting ' + f + ' to json...')
            hjson_path = os.path.join(path, f)
            json_escape_characters(hjson_path)
            json_path = os.path.join(path, f[:-6] + '.json')
            os.system('hjson -j ' + hjson_path + ' > ' + json_path)
            tex_escape_characters(hjson_path)
        elif f.endswith('.json'):
            continue
        elif os.path.isdir(path + '/' + f):
            convert_dfs(path + '/' + f)


def hjson2json(map_name: str) -> None:
    # convert all hjson files in maps/map_name to json
    convert_dfs(os.path.join('..', 'maps', map_name))


def main(map_name: str) -> None:
    hjson2json(map_name)


if __name__ == '__main__':
    main(sys.argv[1])
