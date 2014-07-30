#!/bin/sh


DIR=`pwd`

# ask for path to OpenELEC source
# lakka or no?
# list of cores or "all"
# project/arch
# apply changes to in files, copy to OpenELEC source, begin building
# copy addon package back to this dir

openelec_src_path=""
use_lakka=""
core_list=""
project=""
arch=""

echo "=================================="
echo "RetroArch/Lakka addon for OpenELEC"
echo "=================================="
echo
echo "This tool will walk you through the process of building a custom RetroArch/Lakka addon for OpenELEC."
echo
echo "First, please enter the path to your local OpenELEC source."
while [ ! -d $openelec_src_path ]; do
  echo -n "OpenELEC source path: "
  read openelec_src_path
done

echo "Great! Now, would you like to build plain RetroArch, or include the Lakka menu driver?"
echo "The Lakka menu driver provides a nice interface for loading ROMs. Take a look at"
echo "http://lakka.tv/ for more information."
while [ "$use_lakka" -ne "y" -o "$use_lakka" -ne "n" ]; do
    echo -n "Use lakka? [y/n] "
    read use_lakka
done

# list of cores

# project/architecture
echo "What target would you like to build for? Valid options are: ION, Fusion, Intel, Ultra, Generic, ATV"
valid_projects="ION Fusion Intel Ultra Generic ATV"
while [[ $project != *$valid_projects* ]]; do
    echo -n "Target project? "
    read project
done

echo "What architecture would you like to build for? Valid options are: i386, x86_64"
valid_archs="i386 x86_64"
while [[ $arch != *$valid_archs* ]]; do
    echo -n "Target arch? "
    read arch
done

# apply options to in files

# copy files to OpenELEC source

# make packages

# build addon

exit 0
cp tools/mkpkg/mkpkg_retroarch $1/tools/mkpkg
mkdir -p $1/packages/emulator
cp -R packages/emulator/retroarch $1/packages/emulator

cd $1/tools/mkpkg
  ./mkpkg_retroarch
echo "http://sources.openelec.tv/4.0.7/retroarch-1.0.tar.xz" > $1/sources/retroarch/retroarch-1.0.tar.xz.url

cd $1
if [ -z $2 ]; then
    PROJECT=Generic
else
    PROJECT=$2
fi

if [ -z $3 ]; then
    ARCH=x86_64
else
    ARCH=$3
fi

PROJECT=$PROJECT ARCH=$ARCH ./scripts/create_addon retroarch
cp target/addons/$PROJECT/$ARCH/4.0.7/emulator.retroarch/emulator.retroarch-4.0.7.zip .
