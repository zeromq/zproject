#!/usr/bin/python
#   zproject API XML model generator
#
#   Syntax: mkapi.py project-header class1 class2...
#
#   This is a code generator built using the iMatix GSL code generation
#   language. See https://github.com/imatix/gsl for details.
#
#   Copyright (c) the Contributors as noted in the AUTHORS file.
#   This file is part of zproject.
#
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.


from __future__ import print_function

import argparse
import re
import os
import os.path
import sys

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

def s_comment_fill(comment):
    comment = re.sub(r' +(?=\n|$)', '', comment)
    return s_xml_escape(comment)

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
            last_comment += 6*' ' + line[2:]
            continue

        if last_comment:
            comments[i] = last_comment.rstrip()
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
        self._enums = set()

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
                if typ in self._enums:
                    xtra["enum"] = True
                ret.append((ArgDecl(n.name, typ, ptr, quals, xtra)))
            elif isinstance(n, c_ast.EllipsisParam):
                ret.append(ArgDecl("", "...", "", [], {}))
            else:
                raise NotImplementedError("%s is not supported in func_args" % (n.__class__.__name__))
        return tuple(ret)

    def decl_dict(self, node):
        typ, ptr, quals = FuncDeclVisitor.s_decl_type(node.type.type)
        rtyp = ArgDecl("", typ, ptr, quals, {})
        if typ in self._enums:
            rtyp.xtra["enum"] = True
        decl_dict = {
                    "return_type" : rtyp,
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
            decl_dict["args"][0].name == "self" and \
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
            self._enums.add(decl_dict["name"])
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



def s_decl_to_zproject_type(arg):
    class ZT(object):
        def __init__(self, name, size=None):
            self.name = name
            self.size = size
    dct = {
            ("void", "")  : ZT("nothing"),
            ("void", "*") : ZT("anything"),
            ("size_t", "") : ZT("size"),
            ("time_t", "") : ZT("time"),
            ("int64_t", "") : ZT("clock"),
            ("bool", "")  : ZT("boolean"),
            ("_Bool", "")  : ZT("boolean"),
            ("int", "")   : ZT("integer"),
            ("uint8_t", "") : ZT("number", 1),
            ("uint16_t", "") : ZT("number", 2),
            ("uint32_t", "") : ZT("number", 4),
            ("uint64_t", "") : ZT("number", 8),
            ("float", "") : ZT("real"),
            ("char", "*") : ZT("string"),
            ("byte", "*") : ZT("buffer"),
            ("off_t", "") : ZT("file_size"),
          }
    if hasattr(arg, "xtra") and "enum" in arg.xtra:
        return ZT(arg.xtra["enum_type"])
    if arg.type.endswith("_t") and arg.ptr in ("*", "**"):
        return ZT(arg.type[:-2])
    if arg.name == "format" and arg.type == "char" and arg.ptr == "*":
        return ZT("format")
    try:
        typ = dct[(arg.type, arg.ptr)]
    except KeyError:
        return ZT(arg.type)
    return typ

def s_arg_mutable(arg):
    """Return if attribute mutable should appear in API model
        -1 means no
        0  means mutable = "0"
        1  means mutable = "1"
    """
    if s_decl_to_zproject_type(arg).name in ("string", "format") or arg.ptr == "":
        return -1
    if "const" in arg.quals:
        return 0
    return 1

def s_show_zproto_model_arguments(fp, decl_dict, typ):
    was_format = False
    for arg in decl_dict["args"]:
        if arg.name in (None, "") and arg.type == "void":
            continue
        if arg.name == "self" and arg.type != "void":
            continue
        if typ == "destructor" and arg.name == "self_p" and arg.ptr == "**":
            continue
        if was_format and arg.type == "...":
            continue

        typ = s_decl_to_zproject_type(arg)
        was_format = (typ.name == "format")
        mut = s_arg_mutable(arg)

        print("""        <argument name = "%(name)s" type = "%(type)s"%(size)s%(byref)s%(mutable)s%(callback)s />""" %
                {   "name" : arg.name,
                    "type" : typ.name,
                    "size" : ' size = "%s"' % typ.size if typ.size is not None else "",
                    "byref" : ' by_reference = "1"' if arg.ptr == "**" else "",
                    "mutable" : ' mutable = "%s"' % mut if mut in (0, 1) else "",
                    "callback" : ' callback = "1"' if "callback" in arg.xtra else "",
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
    nam = decl_dict["name"][klass_l:] if decl_dict["name"] != klass else klass
    name = ' name = "%s"' % nam
    if decl_dict["name"] == klass + "_new":
        typ = "constructor"
        name = ""
    elif decl_dict["name"] == klass + "_destroy":
        typ = "destructor"
        name = ""
    elif typ == "singleton":
        typ = "method"
        singleton=' singleton = "1"'

    if typ == "method":
        arg = decl_dict["return_type"]
        if arg.ptr == "*" and not "const" in arg.quals:
            print("    <!-- function returns non const pointer, if it allocates new object, add fresh=\"1\" to <return/> -->",
                file=fp)


    print("""    <%s%s%s>""" % (typ, name, singleton), file=fp)
    s_show_zproto_model_comment(fp, decl_dict, comments)
    s_show_zproto_model_arguments(fp, decl_dict, typ)

    if typ not in ("constructor", "destructor") and \
        (decl_dict["return_type"].type != "void" or decl_dict["return_type"].ptr != ""):
        arg = decl_dict["return_type"]
        mut = s_arg_mutable(arg)
        ret_type = s_decl_to_zproject_type(arg)

        print("""        <return type = "%(type)s"%(size)s%(mutable)s />""" % {
                "size" : ' size = "%s"' % ret_type.size if ret_type.size is not None else "",
                "type" : ret_type.name,
                "mutable" : ' mutable = "%s"' % mut if mut in (0, 1) else "",
                }
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
<!---
    This api model is generated by mkapi.py
    please review the result carefully and especially don't forget
    to add fresh="1" to all methods allocating new functions
-->
<class name = "%s" >

""" % (klass, ), file=fp)

    klass_l = len(klass) + 1
    include = os.path.join("include", klass + ".h")

    for macro_decl in macros:
        print("""    <constant name = "%s" value = %s >%s</constant>""" % (
            macro_decl.name[klass_l:].lower(),
            s_xml_quoteattr(macro_decl.value),
            macro_decl.comment),
            file=fp)

    for decl_dict in (d for d in decls if os.path.normpath(d["coord"].file) == include):

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

def s_mangle_enum_type(arg, klass):
    typ = arg.type[len(klass)+1:]
    if typ.endswith("_t"):
        typ = typ[:-2]
    arg.xtra["enum_type"] = "enum:%(klass)s.%(type)s" % {
            "klass" : klass,
            "type"  : typ
            }

# brute force the enum type
# TODO: a saner approach would be to add klass name to each xtra first
#       and then reiterate once
def s_update_enum_type(decls):
    for klass in sorted(get_classes_from_decls(decls), reverse=True):
        for decl_dict in (d for d in decls if "args" in d):

            ret = decl_dict["return_type"]
            if ret.type.startswith(klass):
                s_mangle_enum_type(ret, klass)

            for arg in (a for a in decl_dict["args"] if "enum_type" not in a.xtra and "enum" in a.xtra and a.type.startswith(klass)):
                s_mangle_enum_type(arg, klass)


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
    if args.INCLUDE is None:
        return ret
    for d in args.INCLUDE:
        path = os.path.expandvars(
                os.path.expanduser(d))
        if not os.path.isdir(path):
            print("W: '%s' is not directory" % path)
        ret.append(path)
    return ret

def main(argv=sys.argv[1:]):

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("-D", "--define", help="extra defines, which will be passed to c preprocessor", dest="DEFINE", action='append')
    p.add_argument("-I", "--include", help="extra includes, which will be passed to c preprocessor", dest="INCLUDE", action='append')
    p.add_argument("--cpp", help="Define c preprocessor to use (gcc -E, clang -E, auto for autodetect and none for not calling preprocessor at all", default="auto")
    p.add_argument("header", help="main header file of the project")
    p.add_argument("klass", help="classes to process, default all", metavar="class", nargs='*')
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
    s_update_enum_type (decls)

    if len(args.klass) == 0:
        klasses = get_classes_from_decls(decls)
    else:
        decl_klasses = frozenset(get_classes_from_decls(decls))
        arg_klasses = frozenset(args.klass)
        klasses = decl_klasses.intersection(arg_klasses)
        if not arg_klasses.issubset(decl_klasses):
            print("W: following class declaration not found: %s" % ", ".join(arg_klasses.difference(decl_klasses)))
            print("I: hint add -DMYPROJ_BUILD_DRAFT_API if class is not yet marked as stable")
            sys.exit(1)

    for klass in klasses:
        print ("I: processing class %s" % klass)
        include = os.path.join("include", klass + ".h")
        comments, macros = parse_comments_and_macros(include)

        model = os.path.join(args.output, klass + ".xml")
        with open(model, 'wt') as fp:
            show_zproto_model(fp, klass, decls, comments, macros)

if __name__ == "__main__":
    main()
