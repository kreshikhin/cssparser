#!/usr/bin/env python3
"""Build the cssparser extension.

Requires flex and bison (2.3 or newer). setuptools is used when it is
installed; otherwise ``python3 setup.py build_ext --inplace`` compiles the
extension directly.
"""

import os
import subprocess
import sys
import sysconfig

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")


def generate_sources():
    subprocess.check_call(["bison", "-d", "-o", "y.tab.c", "css.y"], cwd=SRC)
    subprocess.check_call(["flex", "-o", "lex.yy.c", "css.l"], cwd=SRC)


def python_includes():
    local_config = os.path.join(os.path.dirname(sys.executable), "python3-config")
    config = local_config if os.path.exists(local_config) else "python3-config"
    output = subprocess.check_output([config, "--includes"], text=True)
    return output.strip().split()


def build_inplace():
    generate_sources()
    suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    includes = python_includes()
    output = os.path.join(ROOT, "cssparser" + suffix)
    sources = [
        os.path.join(SRC, "cssparser.c"),
        os.path.join(SRC, "y.tab.c"),
        os.path.join(SRC, "lex.yy.c"),
    ]
    command = [
        "clang",
        "-bundle",
        "-undefined",
        "dynamic_lookup",
        "-Isrc",
        *includes,
        "-o",
        output,
        *sources,
    ]
    subprocess.check_call(command, cwd=ROOT)
    return output


def setuptools_main():
    from setuptools import Extension, setup
    from setuptools.command.build_ext import build_ext

    class BuildExt(build_ext):
        def run(self):
            generate_sources()
            super().run()

    generate_sources()
    setup(
        name="cssparser",
        version="1.0.0",
        description="CSS 2.1 parser for Python, based on the W3C lex/yacc grammar.",
        author="kreshikhin",
        author_email="denis@kreshikhin.com",
        url="https://github.com/kreshikhin/cssparser",
        ext_modules=[
            Extension(
                "cssparser",
                sources=["src/cssparser.c", "src/y.tab.c", "src/lex.yy.c"],
                include_dirs=["src"],
            )
        ],
        cmdclass={"build_ext": BuildExt},
    )


if __name__ == "__main__":
    try:
        import setuptools  # noqa: F401
    except ImportError:
        if len(sys.argv) == 1 or any(arg in sys.argv for arg in ("build", "build_ext", "install")):
            path = build_inplace()
            print("built", path)
        else:
            sys.exit("setuptools is required for this setup.py command")
    else:
        setuptools_main()
