import json
import csv
import argparse
import os


def json2csv(directory: str) -> None:
    with open(os.path.join(directory, 'nodes.json')) as infile:
        data = json.load(infile)

    with open(os.path.join(directory, 'nodes.csv'), 'w') as outfile:
        csv_writer = csv.writer(outfile)
        # get header row
        keys = set()
        for key in data:
            for subkey in data[key].keys():
                keys.add(subkey)
        header: list = ['id'] + list(keys)
        print(header)
        csv_writer.writerow(header)
        header.pop(0)
        for row in data:
            addend = [row]
            for key in header:
                if key in data[row]:
                    addend.append(data[row][key])
                else:
                    addend.append('')
            csv_writer.writerow(addend)

    outfile.close()


def csv2json(directory: str) -> None:
    output_json: dict = {}
    with open(os.path.join(directory, 'nodes.csv'), mode='r') as infile:
        reader = csv.reader(infile)
        field_names = next(reader)
        reader = csv.DictReader(infile, field_names)
        for rows in reader:
            key = rows['name']
            output_json[key] = rows
            del output_json[key]['name']

    with open(os.path.join(directory, 'nodes.json'), 'w') as outfile:
        json.dump(output_json, outfile)

    outfile.close()


# argument parsing
parser = argparse.ArgumentParser(description='Process some integers.')

supported_files = [
    f.name + '/nodes.csv' for f in os.scandir() if f.is_dir()]
supported_files += [f.name + '/nodes.json' for f in os.scandir() if f.is_dir()]
parser.add_argument('file_path',
                    type=str,
                    nargs=1,
                    choices=supported_files,
                    help='path of the file to convert to csv/json \
                                (default: math/nodes.csv)')


def main():
    args = parser.parse_args()
    # if file extension is csv, convert to json
    print(args.file_path)
    directory = os.path.dirname(args.file_path[0])
    if args.file_path[0].endswith('nodes.csv'):
        print("Converting " + args.file_path[0] + " to nodes.json.\n\
            This will overwite the existing nodes.json file.")
        csv2json(directory)
    elif args.file_path[0].endswith('nodes.json'):
        print("Converting " + args.file_path[0] + " to nodes.csv.\n\
            This will overwite the existing nodes.csv file.")
        json2csv(directory)


if __name__ == '__main__':
    main()
