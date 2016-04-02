#!/usr/bin/env bash

#
# This script will regenerate several projects that use zproject
# and then configure, build, install and run tests on them.
# Correctness is up to the user by inspection of messages emitted.
#
# In case of error, log of last commands attempted can be found at files with extension .err.
# If completed without errors, there will not be any *.err file left and script exits with zero.
# Otherwise build area contains ${project}_${phase}.err files with error messages and script exits
# with non-zero value.
#
# Suggestion:
#   run the script prior to making changes to zproject and redirect to before.log
#     opedroso@OPLIN:~/git/zproject$ ./tstbldgen.sh > ../before.log
#   make your changes to zproject
#   run the script and redirect to after.log
#     opedroso@OPLIN:~/git/zproject$ ./tstbldgen.sh > ../after.log
#   compare before.log and after.log to check for any failures in build, install, or test results
#     opedroso@OPLIN:~/git/zproject$ meld ../before.log ../after.log

#
# Usage:
#   $ tstgenbld.sh [clean]
#
#     - if clean argument is present, the scrip will clean any git repository clones and re-clone them.
#       Clean does not apply to zproject itself, only to other repositories used in the process
#       such as gsl, libsodium, libzmq, czmq, malamute and zyre.
#
#     - Important to notice that if clean is used in command line, the script will ask for confirmation
#       that the ../gitprojects directory is actually gone. I have had some problems when using
#       git clones that were on location shared by different OS machines (Linux and Windows).
#

# set next line to "-o xtrace" if debugging
XTRACE="+o xtrace"
set ${XTRACE}

export STARTDATE=`date`

function loglogs() {
    echo ..Logfiles after ${phase} phase
    for err in "${BUILD_PREFIX}"/*.err
    do
        test -f "${err}" && ls "${err}"
    done
#    for ok in "${BUILD_PREFIX}"/*.ok
#    do
#        test -f "${ok}" && ls "${ok}"
#    done
    return 0
}

# cleanup previous build, if any
BUILD_PREFIX=$PWD/tmp
test -d ${BUILD_PREFIX} && find ${BUILD_PREFIX} | xargs rm -rf
mkdir ${BUILD_PREFIX}
test "${1,,}"=="clean" && test -d gitprojects && (find gitprojects | xargs rm -rf)
test "${1,,}"=="clean" && read -p "Check if ./gitprojects is gone then press ENTER: "
test -d gitprojects || mkdir gitprojects

# build zprojects with any changes made to it
phase=building
(
    cd ../zproject &&
    ./autogen.sh &&
    ./configure --prefix=${BUILD_PREFIX} &&
    make &&
    make install &&
    exit $?
) > ${BUILD_PREFIX}/zproject_${phase}.err 2>&1 && mv ${BUILD_PREFIX}/zproject_${phase}.err ${BUILD_PREFIX}/zproject_${phase}.ok
loglogs

# if errors from previous run, remove them before restarting
for project in gsl libsodium libzmq czmq malamute zyre; do
  for phase in gsl-generation building autogen-config make make-install make-check; do
    test -f ${BUILD_PREFIX}/${project}_${phase}.err && rm -f ${BUILD_PREFIX}/${project}_${phase}.err 
    test -f ${BUILD_PREFIX}/${project}_${phase}.ok  && rm -f ${BUILD_PREFIX}/${project}_${phase}.ok
  done
done
loglogs

# go where we will clone our target projects
pushd ./gitprojects > /dev/null 2>&1

# get required but not generated projects for zeromq stack
test -d gsl       || git clone --depth 1 https://github.com/imatix/gsl         gsl
test -d libsodium || git clone -b stable https://github.com/jedisct1/libsodium libsodium
test -d libzmq    || git clone --depth 1 https://github.com/zeromq/libzmq      libzmq
# get required projects for zeromq stack
test -d czmq      || git clone --depth 1 https://github.com/zeromq/czmq        czmq
test -d malamute  || git clone --depth 1 https://github.com/zeromq/malamute    malamute
test -d zyre      || git clone --depth 1 https://github.com/zeromq/zyre        zyre


# build gsl (the generator)
phase=building
(
    cd ../gitprojects/gsl/src &&
    make -j4 &&
    DESTDIR=${BUILD_PREFIX} make install &&
    exit $?
) > ${BUILD_PREFIX}/gsl_${phase}.err 2>&1 && mv ${BUILD_PREFIX}/gsl_${phase}.err ${BUILD_PREFIX}/gsl_${phase}.ok
loglogs


#regenerate projects
phase=gsl-generation
for project in czmq malamute zyre; do
    (
        pwd &&
        cd ../gitprojects/$project &&
        ${BUILD_PREFIX}/bin/gsl -target:* project.xml &&
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && test 0 -eq $? && mv ${BUILD_PREFIX}/${project}_${phase}.err  ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

# build zeromq stack including regenerated projects

# testing building
echo Building zeromq stack components
phase=autogen-config
for project in libsodium libzmq czmq malamute zyre; do
    (
        pwd &&
        cd ../gitprojects/$project &&
        ./autogen.sh &&
        ./configure --prefix=${BUILD_PREFIX} &&
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && mv ${BUILD_PREFIX}/${project}_${phase}.err  ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

phase=make
for project in libsodium libzmq czmq malamute zyre; do
    (
        cd ../gitprojects/$project &&
        make &&
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && mv ${BUILD_PREFIX}/${project}_${phase}.err  ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

phase=make-install
for project in libsodium libzmq czmq malamute zyre; do
    (
        cd ../gitprojects/$project &&
        DESTDIR=${BUILD_PREFIX} make install &&
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && mv ${BUILD_PREFIX}/${project}_${phase}.err  ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

# running tests
echo Running tests
phase=make-check
for project in libzmq czmq malamute zyre; do
    (
        cd ../gitprojects/$project &&
        DESTDIR=${BUILD_PREFIX} PATH=${BUILD_PREFIX}/bin:$PATH make check &&
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && mv ${BUILD_PREFIX}/${project}_${phase}.err  ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

# look for the word "FAIL" in .err files and report them
function logfailed() {
    echo Problems during $1:
    grep -iw -e fail $1 
    return 1
}

# inform user of final results
finalresult=0
for project in zproject gsl libsodium libzmq czmq malamute zyre; do
  for phase in gsl-generation building autogen-config make make-install make-check; do
    test -f ${BUILD_PREFIX}/${project}_${phase}.err && logfailed ${BUILD_PREFIX}/${project}_${phase}.err
  done
done
finalresult=$?

popd > /dev/null 2>&1

echo STOP__DATE: `date`
echo START_DATE: $STARTDATE

exit ${finalresult}