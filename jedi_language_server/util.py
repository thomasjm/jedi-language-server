
import os
from subprocess import run

from pygls.types import (
    MarkupContent,
    MarkupKind,
)

def which(program):
    """ See if an executable exists on the PATH. From https://stackoverflow.com/a/377028/2659595. """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def docstring_to_markup_content(docstring):
    # By default, return the response as plaintext
    kind = MarkupKind.PlainText

    # If pandoc is on the path, use it to convert the response from reStructuredText to Markdown
    if which("pandoc"):
        kind = MarkupKind.Markdown
        p = run(["pandoc", "--from", "rst", "--to", "markdown"], check=True, input=docstring.encode(), capture_output=True)
        docstring = p.stdout.decode()

    return MarkupContent(kind=kind, value=docstring)
