#!/usr/bin/env python3

"""
Previews site using a consolidated version of instructions from:

https://help.github.com/en/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll
"""

import os
import platform
import shlex
from subprocess import run, PIPE
import sys

PREREQS = "ruby-full build-essential zlib1g-dev"

INSTALL_TEXT = f"""
Missing prerequisites. Please run:

    sudo apt install {PREREQS}
""".lstrip()

# TODO(eric.cousineau): Figure out right theme / layout for plain site.
# TODO(eric.cousineau): If/when we figure out how to fully sync up output with
# gh-pages, commit `Gemfile` and `_config.yml` to Git.
GEMFILE_CONTENT = """
# For more information: https://bundler.io/gemfile.html
source 'https://rubygems.org'
gem 'github-pages', '~> 212'
""".lstrip()

CONFIG_CONTENT = """
# For more information: https://jekyllrb.com/docs/
title: Style Guide
theme: minima
""".lstrip()

GEMRC_CONTENT = """
# For more information: https://guides.rubygems.org/command-reference/
gem: --no-document
"""


def which(prog):
    return run(["which", prog]).returncode == 0


def shlex_join(argv):
    # TODO(eric.cousineau): Replace this with `shlex.join` when we exclusively
    # use Python>=3.8.
    return " ".join(map(shlex.quote, argv))


def main():
    if platform.linux_distribution() != ("Ubuntu", "18.04", "bionic"):
        print("Only supported on Ubuntu 18.04")
        sys.exit(1)

    package_check = run(
        ["dpkg", "-s"] + PREREQS.split(), stdout=PIPE, stderr=PIPE)
    if package_check.returncode != 0:
        print(INSTALL_TEXT)
        sys.exit(1)

    # TODO(eric.cousineau): Try to contain generated files within a single
    # directory.
    os.chdir(os.path.dirname(__file__))

    # Isolate the environment.
    # N.B. I (Eric) briefly looked at the following options for virtualenv-like
    # solutions (https://stackoverflow.com/q/486995/7829525):
    # - bundler - Still requires modifying user Gems. Dunno if this can be
    #   configured better.
    # - rbenv: Can handle different ruby versions, and isolates gems. However,
    #   may clobber user's setup for rbenv, and is not constrained to a single
    #   directory by default. (TODO(eric): Try it out, and see if it simplifies
    #   anything).
    # - rvm: Scary, large, and hard-to-read docs. Don't know how to install in
    #   a contained fashion.
    # - sandbox: Old. Suuuuper old.
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": os.environ["HOME"],
        "USER": os.environ["USER"],
        "SHELL": os.environ["SHELL"],
        "TERM": os.environ["TERM"],
        "PWD": os.getcwd(),
    }

    # Isolate environment.
    gem_home = os.path.join(os.getcwd(), "_gems")
    print(f"Setting GEM_HOME to tmpdir: {gem_home}")
    env["GEM_HOME"] = gem_home
    fake_home = os.path.join(gem_home, "fake_home")
    os.makedirs(fake_home, exist_ok=True)
    print(f"Setting HOME to {fake_home}")
    env["HOME"] = fake_home

    with open(os.path.join(fake_home, ".gemrc"), "w") as f:
        f.write(GEMRC_CONTENT)

    # Hoist path. We need this so that we can access `bundle` correctly.
    gem_bin = os.path.join(gem_home, "bin")
    path = env.get("PATH", "").split(":")
    if gem_bin not in path:
        path.insert(0, gem_bin)
    env["PATH"] = ":".join(path)

    # Set up config.
    with open("Gemfile", "w") as f:
        f.write(GEMFILE_CONTENT)
    with open("_config.yml", "w") as f:
        f.write(CONFIG_CONTENT)

    print("\n\nSetting up site. May take a while the first time...\n")

    def run_env(args):
        # Runs a command with our isolated environment.
        cmd = shlex_join(args)
        print(f"+ {cmd}", file=sys.stderr)
        run(args, env=env, check=True)

    # Show environment in case debugging is needed.
    run_env(["bash", "-c", "export -p"])

    # Bionic's version of bundler (1.16) is reportedly too old for this
    # setup (it says bundler>=2 needed).
    run_env(["gem", "install", "-v", "~> 2.2", "bundler"])

    # Without this `--local` command, then an Ubuntu-installed version of
    # jekyll may leak through into `jekyll serve`.
    run_env(["bundle", "config", "set", "--local", "path", gem_home])

    run_env(["bundle", "install"])

    # Use --no-watch because using the gem tmpdir under this folder may
    # overload inotify.
    run_env(["bundle", "exec", "jekyll", "serve", "--no-watch", "--port", "8000"])


assert __name__ == "__main__"
main()
