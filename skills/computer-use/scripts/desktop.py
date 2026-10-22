#!/usr/bin/env python3
"""desktop.py — real desktop control for hosts without built-in computer-use.

Screenshots, mouse, keyboard and scroll from one dependency-light helper.
Requires: pip install pyautogui pillow

Safety: pyautogui FAILSAFE stays on — slam the mouse into a screen corner to
abort any running action. Coordinates are absolute screen pixels.

Usage:
  python desktop.py size
  python desktop.py screenshot [out.png]
  python desktop.py move <x> <y>
  python desktop.py click <x> <y> [--button left|right|middle] [--clicks N]
  python desktop.py drag <x1> <y1> <x2> <y2> [--seconds 0.4]
  python desktop.py type <text...>
  python desktop.py key <name>           # enter, tab, esc, backspace, ctrl+s ...
  python desktop.py scroll <clicks>      # positive=up, negative=down
  python desktop.py position
"""
import argparse
import sys


def _gui():
    try:
        import pyautogui as pag
    except ImportError:
        sys.exit("missing dependency: pip install pyautogui pillow")
    pag.FAILSAFE = True
    return pag


def main(argv=None):
    p = argparse.ArgumentParser(prog="desktop.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("size")
    sh = sub.add_parser("screenshot")
    sh.add_argument("out", nargs="?", default="screenshot.png")
    mv = sub.add_parser("move")
    mv.add_argument("x", type=int)
    mv.add_argument("y", type=int)
    ck = sub.add_parser("click")
    ck.add_argument("x", type=int)
    ck.add_argument("y", type=int)
    ck.add_argument("--button", default="left", choices=["left", "right", "middle"])
    ck.add_argument("--clicks", type=int, default=1)
    dg = sub.add_parser("drag")
    dg.add_argument("x1", type=int)
    dg.add_argument("y1", type=int)
    dg.add_argument("x2", type=int)
    dg.add_argument("y2", type=int)
    dg.add_argument("--seconds", type=float, default=0.4)
    ty = sub.add_parser("type")
    ty.add_argument("text", nargs="+")
    ky = sub.add_parser("key")
    ky.add_argument("name")
    sc = sub.add_parser("scroll")
    sc.add_argument("clicks", type=int)
    sub.add_parser("position")

    args = p.parse_args(argv)
    pag = _gui()

    if args.cmd == "size":
        w, h = pag.size()
        print(f"{w}x{h}")
    elif args.cmd == "screenshot":
        img = pag.screenshot()
        img.save(args.out)
        print(args.out)
    elif args.cmd == "move":
        pag.moveTo(args.x, args.y)
    elif args.cmd == "click":
        pag.click(args.x, args.y, clicks=args.clicks, button=args.button)
    elif args.cmd == "drag":
        pag.moveTo(args.x1, args.y1)
        pag.dragTo(args.x2, args.y2, duration=args.seconds, button="left")
    elif args.cmd == "type":
        pag.typewrite(" ".join(args.text), interval=0.02)
    elif args.cmd == "key":
        parts = args.name.lower().split("+")
        (pag.hotkey(*parts) if len(parts) > 1 else pag.press(parts[0]))
    elif args.cmd == "scroll":
        pag.scroll(args.clicks)
    elif args.cmd == "position":
        x, y = pag.position()
        print(f"{x},{y}")


if __name__ == "__main__":
    main()
