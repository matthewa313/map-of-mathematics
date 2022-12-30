colors_by_type = {
    "axiom": "#f00",
}


def color_themer(type: str) -> str:
    if type in colors_by_type:
        return colors_by_type[type]
    else:
        return "#fff"
