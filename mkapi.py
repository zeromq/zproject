#!/usr/bin/python
# zproto API XML model generator
# licensed under MIT/X11

from __future__ import print_function

import argparse
import re
import os
import sys
import textwrap

from collections import namedtuple
from xml.sax.saxutils import quoteattr as s_xml_quoteattr
from xml.sax.saxutils import escape as s_xml_escape

from pycparser import c_parser, c_ast, parse_file

__doc__ = """
Generate zproto API XML model from CLASS compatible function declarations
"""

MacroDecl = namedtuple("MacroDecl", "name, value, comment")
TypeDecl  = namedtuple("TypeDecl", "type, ptr, quals")
ArgDecl   = namedtuple("ArgDecl", "name, type, ptr, quals, xtra")

COMMENTWRAPPER = textwrap.TextWrapper(
        width=80,
        initial_indent=8*' ',
        replace_whitespace=True,
        drop_whitespace=True,
        subsequent_indent=8*' ')

def s_comment_fill(comment):
    global COMMENTWRAPPER
    return COMMENTWRAPPER.fill(
            s_xml_escape(comment))

def s_parse_comments_and_macros(fp):

    interface_re = re.compile(r"^//\W*@interface\W*$")
    end_re = re.compile(r"^//\W*@end\W*$")
    macro_re = re.compile(r"^#define.*$")

    comments = dict()
    macros = list()

    is_interface = False
    last_comment = ""
    # go to @interface
    for i, line in enumerate(fp):
        if not is_interface:
            if not interface_re.match(line):
                continue
            is_interface = True
            continue

        if end_re.match(line):
            break

        if macro_re.match(line):
            try:
                _, name, value, comment = line.split(' ', 3)
                comment = comment.strip()[3:]
            except ValueError:
                _, name, value = line.split(' ', 2)
                value = value.strip()
                comment = ""
            macros.append(MacroDecl(name, value, comment))
            continue

        if line.startswith("//"):
            last_comment += line[2:].lstrip()
            continue

        if last_comment:
            comments[i] = last_comment
        last_comment = ""

    return comments, macros


def parse_comments_and_macros(filename):
    """Return comments, macros objects from file
    comments are tuple (line, comment)
    macros are (name, value, comment)

    Function use content between @interface @end lines only
    """

    with open(filename) as fp:
        return s_parse_comments_and_macros(fp)

class FuncDeclVisitor(c_ast.NodeVisitor):

    def __init__(self, *args, **kwargs):
        super(FuncDeclVisitor, self).__init__(*args, **kwargs)
        self._ret = list()
        self._callbacks = set()

    @staticmethod
    def s_decl_type(node):
        ptr = ''

        while isinstance(node, c_ast.PtrDecl):
            ptr = ptr + '*'
            node = node.type

        for attr in ("names", "name"):
            if not hasattr(node.type, attr):
                continue
            return TypeDecl(' '.join(getattr(node.type, attr)), ptr, node.quals)

        return TypeDecl("", "void", "")
        raise AttributeError("%s:%s:%s: %s do not have .type.names or .type.name" % (
            node.coord.file,
            node.coord.line,
            node.coord.column,
            node.__class__.__name__))

    def func_args(self, node):
        if node.args is None:
            return (ArgDecl('', "void", '', [], {}), )

        ret = list()
        for idx, n in node.args.children():
            if isinstance(n, (c_ast.Decl, c_ast.Typename)):
                typ, ptr, quals = FuncDeclVisitor.s_decl_type(n.type)
                xtra = {}
                if typ in self._callbacks:
                    xtra["callback"] = True
                ret.append((ArgDecl(n.name, typ, ptr, quals, xtra)))
            elif isinstance(n, c_ast.EllipsisParam):
                ret.append(ArgDecl("", "...", "", [], {}))
            else:
                raise NotImplementedError("%s is not supported in func_args" % (n.__class__.__name__))
        return tuple(ret)

    def decl_dict(self, node):
        decl_dict = {
                    "return_type" : FuncDeclVisitor.s_decl_type(node.type.type),
                    "name" : node.name,
                    "args" : self.func_args(node.type),
                    "coord" : node.coord,
                    }
        return decl_dict

    @staticmethod
    def s_enum_items(enumerators):
        return [MacroDecl(n.name, n.value.value if n.value is not None else "", "")
                for n in enumerators]

    @staticmethod
    def s_enum_dict(node):
        decl_dict = {
                "type" : "enum",
                "name" : node.name,
                "items" : FuncDeclVisitor.s_enum_items(node.type.type.values.enumerators),
                "coord" : node.coord
        }
        return decl_dict

    def visit_Decl(self, node):
        if not isinstance (node.type, c_ast.FuncDecl):
            return
        decl_dict = self.decl_dict(node)
        typ = "singleton"
        if  decl_dict["args"] and \
            decl_dict["args"][0].name in ("self", "self_p") and \
            decl_dict["args"][0].type.endswith("_t") and \
            decl_dict["args"][0].ptr == "*":
            typ = "method"
        decl_dict["type"] = typ
        self._ret.append(decl_dict)

    def visit_Typedef(self, node):
        if isinstance(node.type, c_ast.FuncDecl):
            decl_dict = self.decl_dict(node)
            decl_dict["type"] = "callback_type"
            self._ret.append(decl_dict)
            self._callbacks.add(decl_dict["name"])
            return
        elif isinstance(node.type.type, c_ast.Enum):
            decl_dict = FuncDeclVisitor.s_enum_dict(node)
            self._ret.append(decl_dict)
            return

def s_cpp_args(args):
    cpp_args = [args.cpp, ]
    try:
        for d in args.DEFINE:
            cpp_args.append("-D" + d)
    except TypeError:
        pass

    try:
        for d in args.INCLUDE:
            cpp_args.append("-I" + d)
    except TypeError:
        pass
    return cpp_args

def get_func_decls(filename, args):
    cpp_args = s_cpp_args(args)
    if args.cpp.lower() == "none":
        ast = parse_file(filename)
    else:
        ast = parse_file(filename,
                use_cpp=True,
                cpp_path=os.path.join(os.path.dirname(__file__), "fake_cpp"),
                cpp_args=cpp_args)
    v = FuncDeclVisitor()
    for idx, node in ast.children():
        v.visit(node)
    return v._ret

def s_decl_to_zproto_type(arg):
    dct = {
            ("void", "")  : "nothing",
            ("void", "*") : "anything",
            ("size_t", "") : "size",
            ("time_t", "") : "time",
            ("bool", "")  : "boolean",
            ("_Bool", "")  : "boolean",
            ("int", "")   : "integer",
            ("float", "") : "real",
            ("char", "*") : "string",
            ("byte", "*") : "buffer",
          }
    if arg.type.endswith("_t") and arg.ptr in ("*", "**"):
        return arg.type[:-2]
    return dct.get((arg.type, arg.ptr), arg.type)


def s_show_zproto_model_arguments(fp, decl_dict):
    was_format = False
    for arg in decl_dict["args"]:
        if (arg.name, arg.type) == ("", "void"):
            continue
        if arg.name in ("self", "self_p") and arg.type != "void":
            continue
        if was_format and arg.type == "...":
            continue
        if arg.name == "format" and arg.type == "char" and arg.ptr == "*":
            was_format = True
        print("""        <argument name = "%(name)s" type = "%(type)s"%(byref)s%(constant)s%(callback)s/>""" %
                {   "name" : arg.name,
                    "type" : s_decl_to_zproto_type(arg),
                    "byref" : """ by_reference="1" """ if arg.ptr == "**" else "",
                    "constant" : ' constant="1"' if "const" in arg.quals else "",
                    "callback" : ' callback="1"' if "callback" in arg.xtra else "",
                }, file=fp)

def s_show_zproto_model_comment(fp, decl_dict, comments):
    for i in range(3):
        if decl_dict["coord"].line -i in comments:
            print(s_comment_fill(comments[decl_dict["coord"].line-i]),
                    file=fp)


def s_show_zproto_mc(fp, klass, decl_dict, comments):
    """Show method or callback_type - they're mostly the same except tag name"""
    klass_l = len(klass) + 1
    typ = decl_dict["type"]
    singleton=''
    name = ' name="%s"' % decl_dict["name"][klass_l:]
    if decl_dict["name"] == klass + "_new":
        typ = "constructor"
        name = ""
    elif decl_dict["name"] == klass + "_destroy":
        typ = "destructor"
        name = ""
    elif typ == "singleton":
        typ = "method"
        singleton=""" singleton = "1" """

    if typ == "method":
        arg = decl_dict["return_type"]
        if arg.ptr == "*" and not "const" in arg.quals:
            print("    <!-- function returns non const pointer, if it allocates new object, add fresh=\"1\" to <return/> -->",
                file=fp)

    print("""    <%s%s%s>""" % (typ, name, singleton), file=fp)
    s_show_zproto_model_comment(fp, decl_dict, comments)
    s_show_zproto_model_arguments(fp, decl_dict)

    if typ not in ("constructor", "destructor") and decl_dict["return_type"].type != "void":
        arg = decl_dict["return_type"]
        constant = ' constant="1" ' if 'const' in arg.quals else ''
        print("""        <return type = "%(type)s"%(constant)s/>""" % {
                "type" : s_decl_to_zproto_type(arg),
                "constant" : constant}
             , file=fp)
    print("""    </%s>\n""" % (typ, ), file=fp)


def s_show_zproto_enum(fp, klass_l, decl_dict):
    print("""    <enum name="%s">""" % (decl_dict["name"][klass_l:-2].lower()), file=fp)
    for name, value, comment in decl_dict["items"]:
        name = name[klass_l:].lower()
        value = ' value="%s"' % value if value != "" else ""
        print ("""        <constant name="%s"%s />""" % (name, value), file=fp)
    print("""    </enum>""", file=fp)

def show_zproto_model(fp, klass, decls, comments, macros):
    print("""
<!--- WARNING: this api model is autogenerated by not yet finished
               [mkapi.py](https://github.com/zeromq/zproject/mkapi.py)
               please report all issues you have found to zeromq-dev
               or via github issue tracker (cc @vyskocilm)
-->
    <class name = "%s" >

    <include filename = "../license.xml" />
""" % (klass, ), file=fp)

    klass_l = len(klass) + 1
    include = os.path.join("include", klass + ".h")

    for macro_decl in macros:
        print("""    <constant name = "%s" value = %s >%s</constant>""" % (
            macro_decl.name[klass_l:].lower(),
            s_xml_quoteattr(macro_decl.value),
            macro_decl.comment),
            file=fp)


    for decl_dict in (d for d in decls if d["coord"].file == include):

        if decl_dict["type"] == "enum":
            s_show_zproto_enum(fp, klass_l, decl_dict)
            continue

        if decl_dict["name"].endswith("_test"):
            continue

        s_show_zproto_mc(fp, klass, decl_dict, comments)

    print("</class>", file=fp)

def get_classes_from_decls(decls):
    seen = set()
    for decl_dict in decls:
        name = decl_dict["name"]
        klass = name[:name.rfind('_')]
        include = os.path.join("include", klass + ".h")
        if not os.path.exists(include):
            continue
        if klass in seen:
            continue
        seen.add(klass)
        yield klass

def s_which(binary):
    for d in os.getenv("PATH").split(':'):
        full_path = os.path.join(d, binary)
        if os.path.isfile(full_path):
            return full_path
    return None

def s_detect_system_preprocessor():
    if sys.platform == "darwin":
        if s_which("clang") is None:
            return None
        return "clang -E"
    if s_which("gcc") is not None:
        return "gcc -E"
    if s_which("clang") is not None:
        return "clang -E"

    return None

def s_expand_dirs(args):
    ret = list()
    for d in args.INCLUDE:
        path = os.path.expandvars(
                os.path.expanduser(d))
        if not os.path.isdir(path):
            print("W: '%s' is not directory" % path)
        ret.append(path)
    return ret

def main(argv=sys.argv[1:]):

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("header", help="main header file of the project")
    p.add_argument("-D", "--define", help="extra defines, which will be passed to c preprocessor", dest="DEFINE", action='append')
    p.add_argument("-I", "--include", help="extra includes, which will be passed to c preprocessor", dest="INCLUDE", action='append')
    p.add_argument("--cpp", help="Define c preprocessor to use (gcc -E, clang -E, auto for autodetect and none for not calling preprocessor at all", default="auto")
    args = p.parse_args(argv)

    args.INCLUDE = s_expand_dirs(args)

    args.output = "api"

    if args.cpp == "auto":
        foo = s_detect_system_preprocessor()
        if foo is None:
            print ("E: Can't detect system preprocessor for platform '%s', neither gcc neither clang are found. Specify it via --cpp parameter" % sys.platform, file=sys.stderr)
            sys.exit(1)
        args.cpp = foo

    try:
        os.makedirs(args.output)
    except OSError as e:
        if e.errno != 17:   #file exists
            raise e

    decls = get_func_decls(args.header, args)
    for klass in get_classes_from_decls(decls):
        include = os.path.join("include", klass + ".h")
        comments, macros = parse_comments_and_macros(include)

        model = os.path.join(args.output, klass + ".xml")
        with open(model, 'wt') as fp:
            show_zproto_model(fp, klass, decls, comments, macros)

if __name__ == "__main__":
    main()
