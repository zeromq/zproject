#!/usr/bin/env bash

#
# This script will regenerate several projects that use zproject
# and then configure, build, install and run tests on them.
#
# Correctness is up to the user by inspection of messages emitted.
#
# In case of error, a log of last commands attempted can be found at files
# with extension .err in the build area (i.e. zproject/tmp).
#
# When it completes without errors, there will not be any *.err file
# left and the script exits with zero.
#
# Otherwise build area contains ${project}_${phase}.err files with error
# messages and script exits with non-zero value.
#
# Suggestion:
#   - Run the script prior to making changes to zproject and save output
#     to before.log:
#       opedroso@OPLIN:~/git/zproject$ ./tstbldgen.sh > ../before.log
#
#   - Make your changes to zproject
#
#   - Run the script and redirect to after.log:
#       opedroso@OPLIN:~/git/zproject$ ./tstbldgen.sh > ../after.log
#
#   - Compare before.log and after.log to check for any failures in
#     build, install, or test results:
#       opedroso@OPLIN:~/git/zproject$ meld ../before.log ../after.log
#
# Usage:
#   $ tstgenbld.sh [clean] [> results.log]
#
#     - if clean argument is present, the script will clean any git
#       repository clones and exit.
#     - Clean does not apply to zproject itself, only to other
#       repositories used in the process such as gsl, libsodium, libzmq,
#       czmq, malamute and zyre.
#
#     - Important to notice that if clean is used in command line, the
#       script will ask for confirmation that the ../gitprojects
#       directory is actually gone. I have had some problems when using
#       git clones that were on location shared by different OS machines
#       (Linux and Windows).
#

# Set this to enable verbose profiling
[ -n "${CI_TIME-}" ] || CI_TIME=""
case "$CI_TIME" in
    [Yy][Ee][Ss]|[Oo][Nn]|[Tt][Rr][Uu][Ee])
        CI_TIME="time -p " ;;
    [Nn][Oo]|[Oo][Ff][Ff]|[Ff][Aa][Ll][Ss][Ee])
        CI_TIME="" ;;
esac

# Set this to enable verbose tracing
[ -n "${CI_TRACE-}" ] || CI_TRACE="no"
# set next line to "-o xtrace" if debugging
# note that to simplify such tracing, some loops below explicitly "exit $?"
XTRACE="+o xtrace"
case "$CI_TRACE" in
    [Nn][Oo]|[Oo][Ff][Ff]|[Ff][Aa][Ll][Ss][Ee])
        XTRACE="+o xtrace" ;;
    [Yy][Ee][Ss]|[Oo][Nn]|[Tt][Rr][Uu][Ee])
        XTRACE="-o xtrace" ;;
esac
set ${XTRACE}

export STARTDATE="`date`"

# directory where products will be installed
BUILD_PREFIX=${PWD}/tmp
echo "Projects will be built and installed to here: ${BUILD_PREFIX}"
#read -p "Press ENTER to continue: "

# directory where git projects will be cloned will be ${GITPROJECTS}
GITROOT=${PWD}
GITPROJECTS=${GITROOT}/gitprojects
echo "Projects will be cloned to here: ${GITPROJECTS}"
#read -p "Press ENTER to continue: "

# user to get the zeromq projects on github
ZEROMQ=zeromq
JEDISCT1=jedisct1

function cleanRepositories() {
    find ${GITPROJECTS} | xargs rm -rf
    test -d ${GITPROJECTS} && \
            read -p "Error: Manually delete ${GITPROJECTS} then press ENTER: "
    test -d ${GITPROJECTS} && return 1 || return 0
}

# cleanup previous build, if any
test -d ${BUILD_PREFIX} && find ${BUILD_PREFIX} | xargs rm -rf
test -d ${BUILD_PREFIX} && \
            read -p "Error: Manually delete ${BUILD_PREFIX} then press ENTER: "
mkdir ${BUILD_PREFIX}

# only clean the repositories if using temporary repository area
test "${1,,}" == "clean" && test -d ${GITPROJECTS} && \
(
    test "${PWD}" == "${GITROOT}" && cleanRepositories || \
            read -p "Warning: Please do the clean manually."
    test "${PWD}" != "${GITROOT}" && echo "Clean done, exiting."
    exit 0
) && exit 0

# create repository area
test -d ${GITPROJECTS} || mkdir ${GITPROJECTS}

# define function used later in processing
function loglogs() {
    echo "..Logfiles after ${phase} phase"
    ls ${BUILD_PREFIX}/*.err > /dev/null 2>&1 && ls ${BUILD_PREFIX}/*.err || echo '..None for *.err'
#   ls ${BUILD_PREFIX}/*.ok  > /dev/null 2>&1 && ls ${BUILD_PREFIX}/*.ok  || echo '..None for *.ok'
    #read -p "Press ENTER to continue: "
    return 0
}

# if errors from previous run, remove them before restarting
for project in gsl libsodium libzmq czmq malamute zyre; do
  for phase in gsl-generation building autogen-config make make-install make-check; do
    test -f ${BUILD_PREFIX}/${project}_${phase}.err && rm -f ${BUILD_PREFIX}/${project}_${phase}.err
    test -f ${BUILD_PREFIX}/${project}_${phase}.ok  && rm -f ${BUILD_PREFIX}/${project}_${phase}.ok
  done
done
phase="initial cleanup"
loglogs

# build zproject with any changes made to it
echo "Building zproject"
phase=building
(
    cd ../zproject && \
    $CI_TIME ./autogen.sh && \
    $CI_TIME ./configure && \
    $CI_TIME make && \
    $CI_TIME make install
    exit $?
) > ${BUILD_PREFIX}/zproject_${phase}.err 2>&1 && \
    mv -f ${BUILD_PREFIX}/zproject_${phase}.err ${BUILD_PREFIX}/zproject_${phase}.ok
loglogs


# go where we will clone our target projects
pushd ${GITPROJECTS} > /dev/null 2>&1
echo "Projects will be cloned to here: ${PWD}"
#read -p "Press ENTER to continue: "

# get required but not generated projects for zeromq stack
test -d gsl       || git clone --depth 1 https://github.com/${ZEROMQ}/gsl             gsl
test -d libsodium || git clone -b stable https://github.com/${JEDISCT1}/libsodium     libsodium
test -d libzmq    || git clone --depth 1 https://github.com/${ZEROMQ}/libzmq          libzmq
# get required projects for zeromq stack
test -d czmq      || git clone --depth 1 https://github.com/${ZEROMQ}/czmq            czmq
test -d malamute  || git clone --depth 1 https://github.com/${ZEROMQ}/malamute        malamute
test -d zyre      || git clone --depth 1 https://github.com/${ZEROMQ}/zyre            zyre

# build gsl (the generator)
echo "Building gsl"
phase=building
(
    cd ${GITPROJECTS}/gsl/src && \
    $CI_TIME make -j4 && \
    DESTDIR=${BUILD_PREFIX} $CI_TIME make install
    exit $?
) > ${BUILD_PREFIX}/gsl_${phase}.err 2>&1 && \
    mv -f ${BUILD_PREFIX}/gsl_${phase}.err ${BUILD_PREFIX}/gsl_${phase}.ok
loglogs


#regenerate projects
phase=gsl-generation
for project in czmq malamute zyre; do
    (
        echo "Regenerating projects: $project"
        cd ${GITPROJECTS}/$project && \
        ${BUILD_PREFIX}/bin/gsl project.xml
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && \
        mv -f ${BUILD_PREFIX}/${project}_${phase}.err ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs


echo "All projects have been regenerated. Good time for a backup if you want."
read -p "Press ENTER to continue: "


# build zeromq stack including regenerated projects

# testing building
echo "Building zeromq stack components"
phase=autogen-config
for project in libsodium libzmq czmq malamute zyre; do
    (
        echo "Configuring projects: $project"
        cd ${GITPROJECTS}/$project && \
        $CI_TIME ./autogen.sh && \
        $CI_TIME ./configure --prefix=${BUILD_PREFIX}
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && \
        mv -f ${BUILD_PREFIX}/${project}_${phase}.err ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

phase=make
for project in libsodium libzmq czmq malamute zyre; do
    (
        echo "Building projects: $project"
        cd ${GITPROJECTS}/$project && \
        $CI_TIME make
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && \
        mv -f ${BUILD_PREFIX}/${project}_${phase}.err ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

phase=make-install
for project in libsodium libzmq czmq malamute zyre; do
    (
        echo "Installing projects: $project"
        cd ${GITPROJECTS}/$project && \
        DESTDIR=${BUILD_PREFIX} $CI_TIME make install
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && \
        mv -f ${BUILD_PREFIX}/${project}_${phase}.err ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

# running tests
echo Running tests
phase=make-check
for project in libzmq czmq malamute zyre; do
    (
        echo "Checking projects: $project"
        cd ${GITPROJECTS}/$project && \
        DESTDIR=${BUILD_PREFIX} PATH=${BUILD_PREFIX}/bin:$PATH $CI_TIME make check
        exit $?
    ) > ${BUILD_PREFIX}/${project}_${phase}.err 2>&1 && \
        mv -f ${BUILD_PREFIX}/${project}_${phase}.err ${BUILD_PREFIX}/${project}_${phase}.ok
done
loglogs

# look for the word "FAIL" in .err files and report them
function logfailed() {
    echo "Problems during $1:"
    grep -iw -e fail "$1"
    return 1
}

# inform user of final results
finalresult=0
for project in zproject gsl libsodium libzmq czmq malamute zyre; do
  for phase in gsl-generation building autogen-config make make-install make-check; do
    test -f ${BUILD_PREFIX}/${project}_${phase}.err && \
            finalresult=1 && \
            logfailed ${BUILD_PREFIX}/${project}_${phase}.err
  done
done

popd > /dev/null 2>&1

echo "STOP__DATE: `date`"
echo "START_DATE: $STARTDATE"

exit ${finalresult}
