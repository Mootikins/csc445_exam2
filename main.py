import argparse

import yaml

from PushdownAutomata import PushdownAutomata


def parse_args():
    parser = argparse.ArgumentParser(
        description="A basic YAML-defined pushdown automata"
    )

    parser.add_argument(
        "-f, --yaml",
        required=True,
        type=str,
        dest="input",
        help="The YAML file to use as the automaton definition",
    )

    parser.add_argument(
        "word",
        nargs="+",
        type=str,
        help="Word(s) to try running through the defined automata",
    )

    parser.add_argument(
        "-d, --debug",
        default=False,
        action=argparse.BooleanOptionalAction,
        dest="debug",
        help="Print debug messages, which includes transitions",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    with open(args.input) as file:
        try:
            pda_def = yaml.full_load(file)
        except Exception as e:
            print(e)
            exit(1)

    pda = PushdownAutomata(pda_def, args.debug)
    for word in args.word:
        pda.run(word)


if __name__ == "__main__":
    main()
