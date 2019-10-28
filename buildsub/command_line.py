import re

import click


def make_import_matcher(base):
    import_re = re.compile(
        f"from (?P<path>{base}(\\.\\w+)+)\\s+import\\s+\\*.*")

    def matcher(s):
        match = import_re.match(s)
        if match:
            # TODO: Use proper path tools
            return '/'.join(match.group('path').split(".")) + ".py"
        else:
            return None

    return matcher


def process(input, output, matcher, visited):
    for line in input:
        include = matcher(line)
        if include and include not in visited:
            visited.add(include)
            with open(include, "r") as include_input:
                process(include_input, output, matcher, visited)
        else:
            output.write(line)


@click.command()
@click.option('--base', required=True, help="Base module")
@click.argument('input', type=click.File('r'))
@click.argument('output', type=click.File('w'))
def main(base, input, output):
    process(input, output, make_import_matcher(base), set())
