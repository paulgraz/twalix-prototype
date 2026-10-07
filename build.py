#!/usr/bin/env python3
"""Build the standalone prototype page.

Takes the design canvas artboard (src/Main.dc.html) and the host page
(src/shell.html) and writes index.html: one self-contained file that can be
opened locally or put on any static hosting.

Usage: python3 build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_OLD = '<div style="width: 100%; max-width: {{w}}px; height: 100vh; max-height: {{h}}px; overflow: hidden">'
ROOT_NEW = '<div style="width: 100%; height: 100%; overflow: hidden">'


def between(text, start, end):
    a = text.index(start) + len(start)
    return text[a:text.index(end, a)]


def main():
    src = (HERE / 'src' / 'Main.dc.html').read_text(encoding='utf-8')
    shell = (HERE / 'src' / 'shell.html').read_text(encoding='utf-8')

    template = between(src, '</helmet>', '</x-dc>')
    if ROOT_OLD not in template:
        raise SystemExit('root element of Main.dc.html changed; update ROOT_OLD in build.py')
    template = template.replace(ROOT_OLD, ROOT_NEW, 1)

    script_open = src.index('data-dc-script')
    logic = between(src[script_open:], '>', '</script>')

    out = shell.replace('<!--TEMPLATE-->', template.strip(), 1).replace('/*LOGIC*/', logic.strip(), 1)
    (HERE / 'index.html').write_text(out, encoding='utf-8')
    print('index.html: %d KB' % (len(out.encode('utf-8')) // 1024))


if __name__ == '__main__':
    main()
