Drake Style Guide
=================

![](https://github.com/RobotLocomotion/styleguide/workflows/CI/badge.svg?branch=gh-pages)

This repository is a fork of Google's style guide.  Drake's C++ style is a
small deviation from Google's, and approximately tracks Google's latest style
guidance at a small delay.

The README for Google's style guide follows after some Drake-specific notes
below.

Maintenance Philosophy
----------------------

This style guide should be updated in two cases:

 * The agreement of the Drake platform reviewers on a change to our style
   rules.

 * A change from the upstream Google style guide which has been reviewed (and
   altered if necessary) by the Drake platform reviewers.

Both sorts of updates should use ordinary Reviewable review for the platform
reviewer discussion.

When making a change, annotate an html tag surrounding the new material with
`class="drake"`.  This makes it easy for readers to see Drake-relevant
changes and for maintainers to understand our diffs.  Annotate Google material
that is superseded by Drake changes but is still useful for reference with
`class="nondrake"`.

When making a change, avoid changing whitespace or indentation unnecessarily.
Conflict resolution is difficult in prose text, and conflicts that are just
paragraph reflows make future maintainers cry.

Relevant Pages
--------------

The relevant modified style guides used by Drake are:

* [C++ Style Guide](./cppguide.html)
* [Python Style Guide](./pyguide.html) (*generation required*)

Making New Changes
------------------

Branch, update, and PR as you would any other Drake change.

Ensure that Drake is updated. See [Updating Drake](#updating-drake) for more
information.

Previewing Changes
------------------

Generally, you can preview changes locally without any build. However, if a page
is denoted as needing generation, you can view them locally by running this
script which will indicate necessary prereqs:

    ./preview_site_jekyll.py

You can alternatively preview them on your own GitHub fork.

<!-- TODO(eric): Document this workflow. -->

Pulling Upstream Changes
------------------------

A Drake style guide maintainer should keep a local clone of this repository.
This should be set up in the usual manner, but with remotes to both Google and
Drake as you will want to (a) merge from Google and (b) rebase onto Drake
updates:

 * Fork "styleguide" into your account, this is where all your branches will be

   * Go to https://github.com/RobotLocomotion/styleguide and press "Fork" in
     the top-right corner.  If prompted for the account to fork to, select
     your account.

 * Check out your own fork

   * Go to forked repository https://github.com/**USERNAME**/styleguide and
     press the green "Clone or download" button, then select "ssh" and copy
     ssh URL

   * Clone it on your local machine:

            git clone URL_YOU_JUST_COPIED
            cd styleguide

 * Add a "drake" remote for the Drake styleguide and make it the default
   upstream.  Note that for compatibility with Google, we use the branch
   `gh-pages` as our master:

        git remote add drake https://github.com/RobotLocomotion/styleguide.git
        git remote set-url --push drake no_push
        git fetch drake
        git branch --set-upstream-to drake/gh-pages

 * Add a "google" remote for the Drake styleguide:

        git remote add google https://github.com/google/styleguide.git
        git remote set-url --push google no_push

Now that you have a repository and remotes set up, you want to be up-to-date
with Drake and then pull Google's changes:

    git checkout gh-pages
    git pull --ff-only
    git checkout -b **NEW_BRANCH_NAME**
    git pull google gh-pages
    **RESOLVE CONFLICTS AND COMMIT**
    git push --set-upstream origin **NEW_BRANCH_NAME**
    **ORDINARY PR PROCESS**

There is a high likelihood that this merge will have conflicts.  These
conflicts represent google changes to or near Drake-specific style rules and
should be considered carefully rather than accepted or rejected blindly.

When you have resolved the merge you should commit, push, and PR in the usual
manner.  In creating the PR, double-check that you are PR'ing against
`RobotLocomotion/styleguide`, not `google/styleguide`.

You should add [all of the platform reviewers](http://drake.mit.edu/developers.html#review-process) to the resulting PR.

Ensure that Drake is updated. See [Updating Drake](#updating-drake) for more
information.

<a id="updating-drake"></a>

Updating Drake
--------------

Whenever a change to `styleguide` is made, be sure to submit a PR to `drake` to
bump the `styleguide` SHA.

If there are no changes to supporting code (e.g. `cpplint`):

1. Submit `styleguide` PR, and follow normal review process.
2. Submit `drake` PR, reference the `styleguide` PR, and follow normal review
process.

If there **are** changes to supporting code:

1. Submit the `styleguide` PR.
2. Submit the `drake` PR, reference the `styleguide` PR, and mark as
`do not merge`.
3. Wait until `drake` `*-release` tests pass.
4. Assign review for `styleguide` PR. Merge once review is done.
5. Update the `drake` PR to use the `styleguide` merge commit (from
`gh-pages`). Follow normal review process.

--


Google Style Guides
===================

Every major open-source project has its own style guide: a set of conventions
(sometimes arbitrary) about how to write code for that project. It is much
easier to understand a large codebase when all the code in it is in a
consistent style.

“Style” covers a lot of ground, from “use camelCase for variable names” to
“never use global variables” to “never use exceptions.” This project
([google/styleguide](https://github.com/google/styleguide)) links to the
style guidelines we use for Google code. If you are modifying a project that
originated at Google, you may be pointed to this page to see the style guides
that apply to that project.

This project holds the [C++ Style Guide][cpp], [Objective-C Style Guide][objc],
[Java Style Guide][java], [Python Style Guide][py], [R Style Guide][r],
[Shell Style Guide][sh], [HTML/CSS Style Guide][htmlcss],
[JavaScript Style Guide][js], [AngularJS Style Guide][angular],
[Common Lisp Style Guide][cl], and [Vimscript Style Guide][vim]. This project
also contains [cpplint][cpplint], a tool to assist with style guide compliance,
and [google-c-style.el][emacs], an Emacs settings file for Google style.

If your project requires that you create a new XML document format, the [XML
Document Format Style Guide][xml] may be helpful. In addition to actual style
rules, it also contains advice on designing your own vs. adapting an existing
format, on XML instance document formatting, and on elements vs. attributes.

The style guides in this project are licensed under the CC-By 3.0 License,
which encourages you to share these documents.
See [https://creativecommons.org/licenses/by/3.0/][ccl] for more details.

The following Google style guides live outside of this project:
[Go Code Review Comments][go] and [Effective Dart][dart].

<a rel="license" href="https://creativecommons.org/licenses/by/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/3.0/88x31.png" /></a>


[cpp]: https://google.github.io/styleguide/cppguide.html
[objc]: objcguide.md
[java]: https://google.github.io/styleguide/javaguide.html
[py]: https://google.github.io/styleguide/pyguide.html
[r]: https://google.github.io/styleguide/Rguide.xml
[sh]: https://google.github.io/styleguide/shell.xml
[htmlcss]: https://google.github.io/styleguide/htmlcssguide.html
[js]: https://google.github.io/styleguide/jsguide.html
[angular]: https://google.github.io/styleguide/angularjs-google-style.html
[cl]: https://google.github.io/styleguide/lispguide.xml
[vim]: https://google.github.io/styleguide/vimscriptguide.xml
[cpplint]: https://github.com/google/styleguide/tree/gh-pages/cpplint
[emacs]: https://raw.githubusercontent.com/google/styleguide/gh-pages/google-c-style.el
[xml]: https://google.github.io/styleguide/xmlstyle.html
[go]: https://golang.org/wiki/CodeReviewComments
[dart]: https://www.dartlang.org/guides/language/effective-dart
[ccl]: https://creativecommons.org/licenses/by/3.0/
