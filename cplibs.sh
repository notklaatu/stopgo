#!/bin/bash
# Copy libs needed to run a binary

VERSION=0.8.0
SCR=`echo $0 | rev | cut -f1 -d"/" |rev`
ACT=`which cp`

usage(){
    echo "Analyse BASIS for required libs, and copy those libs to DEST"
    echo " "
    echo "$SCR [OPTIONS] BASIS DEST"
    echo "     --version | -w   print version"
    echo "     --help    | -h   print help and exit"
    echo "     --verbose | -v   be verbose"
    echo "     --dry-run | -d   don't actually perform the copy"
    version
    echo " "
    exit
}

version() {
    echo $SCR" version $VERSION GPLv3"
}

type_test() {
    local ITEM="$1"
    echo "type_testing $ITEM"
    local FTYPE="$2"
    echo "type_testing $FTYPE"
    echo $FTYPE
    local TESTD=$(echo `file -b "$ITEM"` | grep $FTYPE)

    if [ -z "$TESTD" ]; then
	echo "Wrong file type detected:"
	echo "$FTYPE was expected."
	exit 1
    fi
}

# ripped off shamelessly from
# cyberciti.biz/tips/linux-shared-library-management.html
cp_support_shared_libs(){
        DEST="$2"
	echo "dest is $DEST" #debug
	type_test $DEST "directory"

	BASIS="$1"
	echo "basis is $BASIS" #debug
	type_test $BASIS "dynamically"
	
	local files=""
        files="$(ldd $BASIS | awk '{ print $3 }' | sed  '/^$/d')"
 
        for i in $files
        do
          dcc="${i%/*}" # get dirname only
          [ ! -d ${DEST}${dcc} ] && mkdir -p ${DEST}${dcc}
          "${ACT}" -f $VERBOSE $i ${DEST}${dcc}
        done
 
        # Works with 32 and 64 bit ld-linux
        sldl="$(ldd $BASIS | grep 'ld-linux' | awk '{ print $1}')"
        sldlsubdir="${sldl%/*}"
        [ ! -f ${DEST}${sldl} ] && ${ACT} -f $VERBOSE ${sldl} ${DEST}${sldlsubdir}
}

# process verbose and help and dryrun options
while [ True ]; do
    if [ "$1" = "--help" -o "$1" = "-h" ]; then
	usage
	exit
    elif [ "$1" = "--verbose" -o "$1" = "-v" ]; then
	VERBOSE="-v"
	shift 1
    elif [ "$1" = "--list" -o "$1" = "-l" ]; then
	# NOT implemented YET
	list
	shift 1
    elif [ "$1" = "--version" -o "$1" = "-w" -o "$1" = "--which" ]; then
	version
	shift 1
    elif [ "$1" = "--dryrun" -o "$1" = "-d" -o "$1" = "--dry-run" ]; then
	ACT="echo"
	DRYRUN=1
	shift 1
    else
	break
    fi
done

echo "i see $1 as 1" #debug
echo "i see $2 as 2" #debug

# call to main
cp_support_shared_libs $1 $2
