import argparse
from .app import run_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--passwd", "-p", help="passwd filepath", default="/etc/passwd")
    parser.add_argument("--group", "-g", help="group filepath", default="etc/group")
    parser.add_argument("--run", "-r", action="store_true", help="run program")
    parser.add_argument("--version", "-v", action="store_true", help="show version")
    parser.add_argument("--port", help="specify port number", default=8080)
    args = parser.parse_args()

    if args.version:
        print("1.0.0")
    elif args.run:
        run_app(passwd_path=args.passwd, group_path=args.group, port=args.port)
    else:
        print("no arguments given--nothing to do!")
