from hjson2json import *
from fancy_namer import fancy_namer
from latex2svg import latex2svg
from color_themer import color_themer
import json

FONT_SIZE = 12
COLOR_ON = False


def traverse_jsons(statements: dict, path: str) -> None:
    # traverse jsons recursively
    # for each folder or json, create a group
    # for each key-value pair in each json, create a statement
    for f in os.listdir(path):
        if f.endswith('.json'):  # json
            with open(os.path.join(path, f), 'r') as f:
                json_dict = json.load(f)
            statements[os.path.split(f.name)[-1][:-5]] = json_dict
        elif os.path.isdir(os.path.join(path, f)):  # directory
            statements[f] = {}
            traverse_jsons(statements[f], os.path.join(path, f))


def already_rendered(name: str, tex: dict) -> bool:
    if name not in render_log:
        return False
    return tex == render_log[name]


def render_node(name: str, data: dict) -> None:
    # if node already rendered, skip
    if already_rendered(name, data['tex']):
        return
    # compute tex of node
    tex = ''
    if data['type'] in ['fact', 'formula', 'example', 'note']:
        # no name
        tex = '\\textbf{' + data['type'].capitalize() + '.} ' + \
            data['tex']
    else:
        tex = '\\textbf{' + data['type'].capitalize() + '} (' + \
            data['name'] + ')' + '\\textbf{. }' + data['tex']
    # try rendering node
    try:
        output = latex2svg(tex,
                           color=color_themer(data) if COLOR_ON else "white")
    except Exception:
        print("LaTeX error while rendering: " + name)
    else:
        # write output to render file
        outpath = os.path.join('..', 'maps', map_name, 'nodes',
                               'renders', name + '.svg')
        with open(outpath, 'w') as f_read:
            print('Rendered ' + name)
            f_read.writelines(output["svg"])
            data["width"] = round(output["width"] * FONT_SIZE, 2)
            data["height"] = round(output["height"] * FONT_SIZE, 2)
            dimensions[name] = (data["width"], data["height"])
        # log that node is written
        render_log[name] = data['tex']


def write_preamble(graph) -> None:
    with open('../graphml/preamble.txt', 'r') as file:
        graphml_preamble = file.read()
    graph.write(graphml_preamble)


def write_group(graph, group_name: str, fancy_name: str) -> None:
    with open('../graphml/group.txt', 'r') as file:
        graphml_group = file.read()
    graph.write(graphml_group.format(
        id=group_name+'_group', group_label=fancy_namer(fancy_name)))
    pass


def write_subgraph(graph, id: str, statement: dict) -> None:
    # write node
    with open('../graphml/node_statement.txt', 'r') as file:
        graphml_node = file.read()
    graph.write(graphml_node.format(node=id, id=id,
                                    height=dimensions[id][1],
                                    width=dimensions[id][0]))
    # write predec node
    if 'predec' not in statement:
        return
    for predec in statement['predec']:
        if statement['type'] in ['definition', 'note', 'example']:
            with open('../graphml/node_definition.txt', 'r') as file:
                graphml_predec = file.read()
            graph.write(graphml_predec.format(name=predec))
        elif statement['type'] != 'axiom':
            with open('../graphml/node_proof.txt', 'r') as file:
                graphml_predec = file.read()
            proof_link = os.path.join(
                '..', 'maps', map_name, 'proofs', 'pdfs', predec + '.pdf')
            graph.write(graphml_predec.format(
                name=predec, link=proof_link))


def write_nodes(graph, statements: dict) -> None:
    # loop through statements
    for statement in statements:
        if 'name' in statements[statement]:  # statement
            render_node(statement, statements[statement])
            # write_group(graph, statement +
            #            '_nodegroup', statements[statement]['name'])
            write_subgraph(graph, statement, statements[statement])
            # graph.write('</graph></node>')
        else:  # directory
            write_group(graph, statement, statement)
            write_nodes(graph, statements[statement])
            graph.write('</graph></node>')


def write_edges(graph, id: str, statements: dict) -> None:
    # loop through statements
    for statement in statements:
        if 'name' in statements[statement]:
            id = statement
            statement = statements[statement]
            if 'predec' in statement and statement['predec'] != 'None':
                with open('../graphml/edge.txt', 'r') as file:
                    edge = file.read()
                for key in statement['predec']:
                    for predec in statement['predec'][key]:
                        style = 'standard'
                        if statement['type'] in ['definition', 'note',
                                                 'example']:
                            style = 't_shape'
                        graph.write(edge.format(id=predec+'_'+id,
                                                source=predec,
                                                target=id +
                                                '_predec',
                                                style=style))
                graph.write(edge.format(id=id + '_predec',
                                        source=id +
                                        '_predec',
                                        target=id,
                                        style='standard'))
        else:  # directory
            write_edges(graph, statement, statements[statement])


def write_svgs(graph, id: str, statements: dict) -> None:
    svg_text = '<y:Resource id="{id}" xml:space="preserve">{svg}</y:Resource>'
    for statement in statements:
        if 'name' in statements[statement]:  # statement
            svg_path = os.path.join('..', 'maps', map_name,
                                    'nodes', 'renders', statement+'.svg')
            svg = open(svg_path).read()
            svg = svg.replace("<", "&lt;").replace(">", "&gt;")
            graph.write(svg_text.format(id=statement, svg=svg))
        else:  # directory
            write_svgs(graph, statement, statements[statement])


def render_graph() -> None:
    # read in jsons to statement and proof nodes
    hjson2json(map_name)
    statements: dict = {}
    traverse_jsons(statements, os.path.join(
        '..', 'maps', map_name, 'nodes', 'network'))
    # render pdfs

    # write graphml file from statement and proof nodes
    # write graphml_text to file in output/
    with open(os.path.join('..', 'output', map_name + '.graphml'), 'w') as f:
        write_preamble(f)
        write_nodes(f, statements)
        write_edges(f, None, statements)
        f.write('\n</graph>\n<data key="d7">\n<y:Resources>')
        write_svgs(f, None, statements)
        f.write("\n</y:Resources>\n</data>\n</graphml>")
        f.close()


def main(map_name_in: str) -> None:
    global map_name
    map_name = map_name_in

    global render_log
    render_log_path = os.path.join('..', 'maps', map_name, 'nodes',
                                   'renders', '.log.json')
    with open(render_log_path, 'r') as f:
        render_log = json.load(f)

    global dimensions
    dimensions_path = os.path.join('..', 'maps', map_name, 'nodes',
                                   'renders', '.dimensions.json')
    with open(dimensions_path, 'r') as f:
        dimensions = json.load(f)

    render_graph()

    with open(render_log_path, 'w') as f:
        json.dump(render_log, f)
    with open(dimensions_path, 'w') as f:
        json.dump(dimensions, f)


if __name__ == '__main__':
    main(sys.argv[1])
