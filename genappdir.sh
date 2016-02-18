#!/bin/sh
# 
#     Copyright (C) 2006 - 2009 Rick Helmus (rhelmus_AT_gmail.com) [Nixstaller]
#     Adapted for AppImage by Klaatu (klaatu@member.fsf.org)
#     
#     This program is free software; you can redistribute it and/or modify it under
#     the terms of the GNU General Public License as published by the Free Software
#     Foundation; either version 2 of the License, or (at your option) any later
#     version. 
#     
#     This program is distributed in the hope that it will be useful, but WITHOUT ANY
#     WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#     PARTICULAR PURPOSE. See the GNU General Public License for more details. 
#     
#     You should have received a copy of the GNU General Public License along with
#     this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
#     St, Fifth Floor, Boston, MA 02110-1301 USA

# Default settings
DEF_APPICON=""
DEF_APPDESK=""

usage()
{
    echo "Usage: $0 [options] <target dir>"
    echo
    echo "[options] can be one of the following things (all are optional):"
    echo
    echo " --help, -h             Print this message."
    echo " --icon, -i <file>      Path to icon PNG file. Default: generic icon."
    echo " --desktop, -d <file>   Path to .desktop filer. Default: minimal template file."
    echo " --name, -n <name>      Application name. Default: target basename."
    echo " --apprun, -a <file>    Path to AppRun binary. Default: `$pwd` or PATH"
    echo " --overwrite            Overwrite existing project dir."
    exit 1
}

error()
{
    echo "$*"
    exit 1
}

requiredcp()
{
    cp "$@" || error "Failed to copy file(s)"
}

checkargentry()
{
    if [ -z "$1" ]; then
        return 1
    fi
    
    case "$1" in
        -*)
            return 1
            ;;
        *)
            return 0
            ;;
    esac
}

# $1: Value to check
# $*: Valid values
verifyentry()
{
    VAL="$1"
    shift
    for o in $*
    do
        if [ $o = $VAL ]; then
            return 0
        fi
    done
    
    return 1
}

parseargs()
{
    while true
    do
        case "${1}" in
            --help | -h)
                usage
                ;;
            --name | -n)
                shift
                [ -z "${1}" ] && usage
                APPNAME="${1}"
                shift
                ;;
            --apprun | -a)
                shift
                [ -z "${1}" ] && usage
                APPRUNBIN="${1}"
                shift
                ;;
            --icon | -i)
                shift
                [ -z "${1}" ] && usage
                [ ! -f "${1}" ] && error "Couldn't find icon file ($1)"
                APPICON="${1}"
                shift
                ;;
            --desktop | -d)
                shift
                [ -z "${1}" ] && usage
                [ ! -f "${1}" ] && error "Couldn't find .desktop file ($1)"
                APPDESK="${1}"
                shift
                ;;
            --overwrite)
                shift
                OVERWRITE=1
                ;;
            -*)
                usage
                ;;
            *)
                break
                ;;
        esac
    done
    
    TARGETDIR=`echo "${1}" | sed 's/.appdir//'`.appdir
    DEF_APPNAME=`echo "${1}" | sed 's/.appdir//' | tr -d ' '`
    
    if [ -z "${TARGETDIR}" ]; then
        usage
    elif [ -d "${TARGETDIR}" ]; then
        if [ "$OVERWRITE" = 1 ]; then
	    if [ -z `which trashy` ]; then
		rm -rf "${TARGETDIR}"
	    else
		trash "${TARGETDIR}"
	    fi
	fi
    fi
    
    # Set defaults where necessary
    APPNAME=${APPNAME:=$DEF_APPNAME}
    # Brute-force a default icon if none exists
    if [ -z "${APPICON}" -o ! -e "${APPICON}" ]; then
	for SIZE in {512,256,128,96,72,64,48,32,24,16};
	do
	    DEF_APPICON=`find /usr/share/icons/ -type f -name "application-x-executable.png" | grep $SIZE | head -n1`
	    if [ -n "${DEF_APPICON}" ]; then
		APPICON=${APPICON:=$DEF_APPICON}
		break
	    fi
	done
    fi
}

createlayout()
{
    mkdir -p "${TARGETDIR}" || error "Failed to create target directory"
    mkdir -p "${TARGETDIR}/usr/bin" || error "Failed to create usr bin structure"
    mkdir -p "${TARGETDIR}/usr/lib" || error "Failed to create usr lib structure"
    mkdir -p "${TARGETDIR}/usr/lib64" || error "Failed to create usr lib64 structure"
}

copyappdesk()
{
    if [ -z "${APPDESK}" -o ! -e "${APPDESK}" ]; then
	printf "[Desktop Entry]\nName=%s\nExec=%s\nIcon=%s" \
	    "${APPNAME}" "${APPNAME}" "${APPNAME}" \
	    > "${TARGETDIR}"/"${APPNAME}".desktop
    else
	cp "${APPDESK}" "${TARGETDIR}"
    fi
}

copyappicon()
{
    if [ ! -z "${APPICON}" ]; then
        requiredcp "${APPICON}" "${TARGETDIR}"/"${APPNAME}".png
    fi
}

copyapprun()
{

    #if not defined, or is defined but does not exist
    if [ -z "${APPRUNBIN}" -o ! -e "${APPRUNBIN}" ]; then
	APPRUNBIN=`which AppRun 2>/dev/null` || APPRUNBIN=`find -O3 . -type f -maxdepth 1 -name "AppRun"`
    fi
    # still not exists
    if [ -z "${APPRUNBIN}" -o ! -e "${APPRUNBIN}" ]; then
	echo "Unable to locate a compiled AppRun binary."
	echo "If AppRun is not installed, or is not in your working directory, use -a to specify a path."
	echo
	echo "If you do not have AppRun, download it from https://github.com/probonopd/AppImageKit/"
	exit 1
    fi

    # ok i guess it exists
    requiredcp "${APPRUNBIN}" "${TARGETDIR}"
}


createprojdir()
{
    createlayout
    copyappdesk
    copyappicon
    copyapprun
}

hints()
{
    echo "Base project directory layout created in ${TARGETDIR}."
    echo
    echo "Now you need to.."
    echo "* Place your binar{y,ies) into their appropriate places."
    echo "* Place your libs into their appropriate places."
    echo
    echo "https://github.com/probonopd/AppImageKit/wiki/Creating-AppImages"

}

# main
parseargs "$@"
createprojdir
hints

