import os
import json
import sys
from jsonmerge import merge


def master_json(data, directory):
    for filename in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, filename)):
            data = master_json(data, os.path.join(directory, filename))
        elif filename.endswith('.json'):
            with open(os.path.join(directory, filename)) as node_file:
                data = merge(data, json.load(node_file))
    return data


def render_proofs(map_name):
    global PROOF_PDF_DIR
    PROOF_PDF_DIR = os.path.join('..', 'maps', map_name, 'proofs', 'pdfs')
    global PROOF_TEX_DIR
    PROOF_TEX_DIR = os.path.join('..', 'maps', map_name, 'proofs', 'tex')

    data = master_json({}, os.path.join(
        '..', 'maps', map_name, 'nodes', 'network'))
    for filename in os.scandir(PROOF_TEX_DIR):
        if not filename.is_file():
            continue
        if os.path.isfile(os.path.join(PROOF_PDF_DIR,
                                       filename.name.replace('.tex', '.pdf'))):
            continue
        ftex = open(filename.path, 'r')
        # make an auxiliary file
        faux = open('auxiliary.tex', 'w')
        template = open(os.path.join(
            '..', 'latex', 'proof_template.tex'), 'r').read()
        name = filename.name.replace('.tex', '')
        # write preamble
        preamble = open(os.path.join(
            '..', 'latex', 'preamble.tex'), 'r').read()
        template = template.replace('{{ preamble }}', preamble)
        # write theorem to be proved
        template = template.replace('{{ theorem }}', data[name]['tex'])
        template = template.replace('{{ proof }}', ftex.read())
        faux.write(template)
        faux.close()

        os.system("pdflatex auxiliary.tex")
        os.system("mv "+'auxiliary.pdf'+" " + os.path.join(PROOF_PDF_DIR,
                  filename.name.replace('.tex', '.pdf')))
        os.system("rm -rf auxiliary.*")


def main(map_name: str) -> None:
    render_proofs(map_name)


if __name__ == '__main__':
    main(sys.argv[1])
