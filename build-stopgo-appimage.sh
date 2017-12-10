#! /usr/bin/bash
# based on plext build script

PKGDIR=${PKGDIR:-AppDir}
DOCDIR=${DOCDIR:-usr/doc}

set -x
set -e

# use RAM disk if possible
if [ -d /dev/shm ]; then
    TEMP_BASE=/dev/shm
else
    TEMP_BASE=/tmp
fi

BUILD_DIR=$(mktemp -d -p "$TEMP_BASE" Stopgo-AppImage-build-XXXXXX)

cleanup () {
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
    fi
}

#trap cleanup EXIT

# store repo root as variable
REPO_ROOT=$(readlink -f $(dirname $0))
OLD_CWD=$(readlink -f .)

pushd "$BUILD_DIR"

# install Miniconda, a self contained Python distribution, into AppDir
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
mkdir "$PKGDIR"
bash Miniconda3-latest-Linux-x86_64.sh -b -p "$PKGDIR"/usr -f

# activate Miniconda environment
. "$PKGDIR"/usr/bin/activate

# install dependencies
cp -rv "$OLD_CWD"/usr "$PKGDIR"
mkdir -p "$PKGDIR"/usr/"$LIB"/"$PYTHON"/site-packages/vlc
echo "vlc" > "$PKGDIR"/usr/"$LIB"/"$PYTHON"/site-packages/vlc.pth


# copy resources to AppDir
cp "$OLD_CWD"/usr/share/applications/stopgo.desktop "$PKGDIR"
cp "$OLD_CWD"/usr/share/icons/hicolor/scalable/stopgo.svg "$PKGDIR"
mkdir -p "$PKGDIR"/"$DOCDIR"/stopgo
cp "$OLD_CWD"/AUTHORS "$OLD_CWD"/TODO "$OLD_CWD"/COPYING "$PKGDIR"/"$DOCDIR"/stopgo

# precompile bytecode to speed up startup
pushd AppDir
python -m compileall . -fqb || true
popd

# copy in libraries
wget https://raw.githubusercontent.com/notklaatu/AppImages/klaatu/functions.sh
#https://raw.githubusercontent.com/AppImage/AppImages/master/functions.sh
(. ./functions.sh && cd "$PKGDIR" && set +x && copy_deps && copy_deps && copy_deps && delete_blacklisted)

# remove unnecessary libraries and other useless data
pushd "$PKGDIR"
find usr/lib \
    -iname '*Tk*' \
    -or -iname '*QtNetwork*' \
    -or -iname '*lib2to3*' \
    -or -iname '*ucene*' \
    -or -iname '*pip*' \
    -or -iname '*setuptools*' \
    -or -iname '*declarative*'  \
    -or -iname 'libkrb*.so*' \
    -or -iname 'libhcrypto*.so*' \
    -or -iname 'libheim*.so*' \
    -or -iname 'libroken*.so*' \
    -or -iname 'libreadline*.so*' \
    -delete
popd

# install AppRun
cat > "$PKGDIR"/AppRun <<EOF
#! /bin/sh

export LD_LIBRARY_PATH="\$APPDIR"/usr/lib:"\$APPDIR"/usr/lib/x86_64-linux-gnu/
export PYTHONPATH="\$APPDIR"/usr/lib/python3.5:"\$APPDIR"/usr/lib/python3.5/site-packages/

exec "\$APPDIR"/usr/bin/python "\$APPDIR"/usr/bin/stopgo
EOF

chmod +x "$PKGDIR"/AppRun

# get appimagetool
echo `pwd`
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage --appimage-extract

# build AppImage
squashfs-root/AppRun AppDir
# how I used to do it
#"$HOME"/bin/appimagetool-x86_64.AppImage "$PKGDIR"

# move AppImage back to old CWD
mv "$TEMP_BASE"/Stopgo-AppImage-build*/StopGo-*.AppImage "$OLD_CWD"/
