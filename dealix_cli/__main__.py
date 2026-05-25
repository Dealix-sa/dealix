import argparse
import os

from dealix_cli import commands


def main() -> None:
    parser = argparse.ArgumentParser(prog="dealix_cli", description="Dealix CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    productization = sub.add_parser(
        "productization",
        help="Generate productization review from private ops candidates.",
    )
    productization.add_argument(
        "--private-ops",
        default=os.environ.get("PRIVATE_OPS", "dealix-ops-private"),
    )

    args = parser.parse_args()

    if args.command == "productization":
        commands.productization(args.private_ops)


if __name__ == "__main__":
    main()
