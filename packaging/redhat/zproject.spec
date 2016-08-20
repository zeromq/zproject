#
#    zproject - Project
#
#    Copyright (c) the Contributors as noted in the AUTHORS file.       
#    This file is part of CZMQ, the high-level C binding for 0MQ:       
#    http://czmq.zeromq.org.                                            
#                                                                       
#    This Source Code Form is subject to the terms of the Mozilla Public
#    License, v. 2.0. If a copy of the MPL was not distributed with this
#    file, You can obtain one at http://mozilla.org/MPL/2.0/.           
#

%global debug_package %{nil}
Name:           zproject
Version:        1.1.0
Release:        1
Summary:        project
License:        MPLv2
URL:            https://github.com/zeromq/zproject
Source0:        %{name}-%{version}.tar.gz
Group:          System/Libraries
# Note: ghostscript is required by graphviz which is required by
#       asciidoc. On Fedora 24 the ghostscript dependencies cannot
#       be resolved automatically. Thus add working dependency here!
BuildRequires:  ghostscript
BuildRequires:  asciidoc
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  xmlto
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
zproject project.


%prep
%setup -q

%build
sh autogen.sh
%{configure}
make %{_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# remove static libraries
find %{buildroot} -name '*.a' | xargs rm -f
find %{buildroot} -name '*.la' | xargs rm -f

%files
%defattr(-,root,root)
%doc README.md
%doc README.txt
%{_bindir}/zproject.gsl
%{_bindir}/zproject_projects.gsl
%{_bindir}/zproject_class_api.gsl
%{_bindir}/zproject_skeletons.gsl
%{_bindir}/zproject_bench.gsl
%{_bindir}/zproject_class.gsl
%{_bindir}/zproject_git.gsl
%{_bindir}/zproject_valgrind.gsl
%{_bindir}/zproject_android.gsl
%{_bindir}/zproject_autotools.gsl
%{_bindir}/zproject_cmake.gsl
%{_bindir}/zproject_cygwin.gsl
%{_bindir}/zproject_debian.gsl
%{_bindir}/zproject_docker.gsl
%{_bindir}/zproject_gyp.gsl
%{_bindir}/zproject_java.gsl
%{_bindir}/zproject_java_lib.gsl
%{_bindir}/zproject_java_msvc.gsl
%{_bindir}/zproject_mingw32.gsl
%{_bindir}/zproject_nodejs.gsl
%{_bindir}/zproject_nuget.gsl
%{_bindir}/zproject_obs.gsl
%{_bindir}/zproject_python.gsl
%{_bindir}/zproject_python_cffi.gsl
%{_bindir}/zproject_qml.gsl
%{_bindir}/zproject_qt.gsl
%{_bindir}/zproject_redhat.gsl
%{_bindir}/zproject_rpi.gsl
%{_bindir}/zproject_ruby.gsl
%{_bindir}/zproject_travis.gsl
%{_bindir}/zproject_vagrant.gsl
%{_bindir}/zproject_vs2008.gsl
%{_bindir}/zproject_vs20xx.gsl
%{_bindir}/zproject_vs20xx_props.gsl
%{_bindir}/zproject_known_projects.xml
%{_bindir}/mkapi.py
%{_bindir}/fake_cpp

%changelog
