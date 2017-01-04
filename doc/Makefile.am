################################################################################
#  THIS FILE IS 100% GENERATED BY ZPROJECT; DO NOT EDIT EXCEPT EXPERIMENTALLY  #
#  Read the zproject/README.md for information about making permanent changes. #
################################################################################
# NOTE: stub doc/zproject.txt is generated by GSL from project.xml and
#       then comitted to SCM and maintained manually to describe the project.
MAN1 =
MAN3 =
MAN7 = zproject.7
MAN_DOC = $(MAN1) $(MAN3) $(MAN7)

# Assumption: the .7 pages only cover the project and are maintained manually
MAN_TXT = $(MAN7:%.7=%.txt)

EXTRA_DIST = asciidoc.conf mkman

if INSTALL_MAN
dist_man_MANS = $(MAN_DOC)
endif

if BUILD_DOC
MAN_TXT += $(MAN1:%.1=%.txt)
MAN_TXT += $(MAN3:%.3=%.txt)

DISTCLEANFILES = $(MAN_DOC)

dist-hook : $(MAN_DOC)

SUFFIXES=.txt .xml .1 .3 .7

$(builddir)/zproject.txt: $(srcdir)/zproject.txt
	if [ "$@" != "$<" ] || [ ! -s "$@" ] ; then \
		cp "$<" "$@" || exit ; \
	fi

.txt.xml:
	asciidoc -d manpage -b docbook -f $(srcdir)/asciidoc.conf \
        -azproject_version=@PACKAGE_VERSION@ -o$@ $<
.xml.1:
	xmlto man $<
.xml.3:
	xmlto man $<
.xml.7:
	xmlto man $<

GENERATED_DOCS =
.txt.doc:
# No-op, docs and texts are generated by mkman in one shot - just
# make a dependency that can not parallelize and break stuff


clean:
	rm -f *.1 *.3 *.7 $(GENERATED_DOCS)
doc: $(GENERATED_DOCS)

endif

EXTRA_DIST += $(MAN_TXT)
################################################################################
#  THIS FILE IS 100% GENERATED BY ZPROJECT; DO NOT EDIT EXCEPT EXPERIMENTALLY  #
#  Read the zproject/README.md for information about making permanent changes. #
################################################################################