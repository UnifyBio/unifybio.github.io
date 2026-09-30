"""Makes ```edn fenced code blocks highlight.

Pygments has no EDN lexer, but EDN is a subset of Clojure syntax, so alias `edn`
to the Clojure lexer. Existing ```clojure blocks keep working.
"""
from pygments.lexers import LEXERS


def on_startup(command, dirty, **kwargs):
    module, name, aliases, filenames, mimetypes = LEXERS["ClojureLexer"]
    if "edn" not in aliases:
        LEXERS["ClojureLexer"] = (module, name, tuple(aliases) + ("edn",), filenames, mimetypes)
