import argparse

from dealix_cli.commands import finance


def main():
    parser = argparse.ArgumentParser(prog="dealix_cli", description="Dealix CEO CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    finance_parser = subparsers.add_parser(
        "finance",
        help="Generate finance review from private ops.",
    )
    finance_parser.add_argument("--private-ops", required=True)

    args = parser.parse_args()

    if args.command == "finance":
        finance(args.private_ops)


if __name__ == "__main__":
    main()
