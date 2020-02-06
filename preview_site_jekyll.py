#!/usr/bin/env python3

"""
Preview site using a consolidated version of instructions from:

https://help.github.com/en/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll
"""

import os
import platform
from subprocess import run
import sys

INSTALL_TEXT = """
Missing prerequisites. Please run:

    sudo apt install ruby-full build-essential zlib1g-dev
""".lstrip()

# TODO(eric.cousineau): Figure out right theme / layout for plain site.
GEMFILE_CONTENT = """
source "https://rubygems.org"
gem "minima", "~> 2.5"
gem "github-pages", group: :jekyll_plugins
""".lstrip()

CONFIG_CONTENT = """
title: Style Guide
theme: minima
""".lstrip()

GEM_HOME_DEFAULT = os.path.expanduser("~/.local/opt/ruby/gems")


def which(prog):
    return run(["which", prog]).returncode == 0


def main():
    if platform.linux_distribution() != ("Ubuntu", "18.04", "bionic"):
        print("Only tested on Ubuntu 18.04")
        sys.exit(1)

    has_prereqs = which("gem")
    if not has_prereqs:
        print(INSTALL_TEXT)
        sys.exit(1)

    env = dict(os.environ)
    if "GEM_HOME" not in env:
        print(f"Setting GEM_HOME to: {GEM_HOME_DEFAULT}")
        env["GEM_HOME"] = GEM_HOME_DEFAULT
    gem_home = env["GEM_HOME"]
    gem_bin = os.path.join(gem_home, "bin")
    path = env.get("PATH", "").split(":")
    if gem_bin not in path:
        path.insert(0, gem_bin)
    env["PATH"] = ":".join(path)

    os.chdir(os.path.dirname(__file__))
    with open("Gemfile", "w") as f:
        f.write(GEMFILE_CONTENT)
    with open("_config.yml", "w") as f:
        f.write(CONFIG_CONTENT)

    def run_env(args):
        run(args, env=env, check=True)

    print("\n\nSetting up site. May take a while the first time...\n\n")

    run_env(["gem", "install", "bundle"])
    run_env(["bundle", "update"])
    run_env(["bundle", "exec", "jekyll", "serve"])


assert __name__ == "__main__"
main()
