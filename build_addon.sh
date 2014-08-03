#!/bin/bash

DIR=`pwd`

openelec_src_path=""
selected_cores=""
project=""
arch=""

echo "=================================="
echo "RetroArch/Lakka addon for OpenELEC"
echo "=================================="
echo
echo "This tool will walk you through the process of building a custom RetroArch/Lakka addon for OpenELEC."
echo
echo "First, please enter the path to your local OpenELEC source."
while [ -z "$openelec_src_path" ]; do
  echo -n "OpenELEC source path: "
  read openelec_src_path
  if [ ! -d "$openelec_src_path" ]; then
      echo "$openelec_src_path is an invalid directory!"
      openelec_src_path=""
  fi
done

echo "Cleaning $openelec_src_path..."
  cd $openelec_src_path
    git clean -df
    rm -rf sources
    rm -rf tools/mkpkg/*.git
    rm -rf tools/mkpkg/*.xz
  cd $DIR

# list of cores
valid_cores=""
real_cores=""
for i in `ls -1 packages/emulator`; do
    if [[ "$i" != "RetroArch" && "$i" != "retroarch-joypad-autoconfig" && "$i" != "retroarch-assets" ]]; then
	real_cores="$real_cores $i"
    fi
done
valid_cores="all $real_cores"
valid_core_selection="n"
echo "Next, which emulator cores would you like to build? Type 'all' for all."
echo "Valid cores: $real_cores"
while [[ $valid_core_selection != "y" ]]; do
    echo -n "Selected cores? "
    read selected_cores
    for i in $selected_cores; do
        if [[ $valid_cores != *$i* ]]; then
            valid_core_selection="n"
            break
        fi
        valid_core_selection="y"
    done
done

# project/architecture
echo "What target would you like to build for? Valid options are: ION, Fusion, Intel, Ultra, Generic, ATV"
valid_projects="ION Fusion Intel Ultra Generic ATV"
project="foobar"
while [[ $valid_projects != *$project* ]]; do
    echo -n "Target project? "
    read project
done

echo "What architecture would you like to build for? Valid options are: i386, x86_64"
valid_archs="i386 x86_64"
arch="foobar"
while [[ $valid_archs != *$arch* ]]; do
    echo -n "Target arch? "
    read arch
done

# apply options to in files
echo "Arch: $arch"
echo "Project: $project"
echo "Cores: $selected_cores"
echo "OE Source: $openelec_src_path"

echo "CFG_CORES=\"$selected_cores\"" > packages/emulator/RetroArch/config

# copy files to OpenELEC source
cp -R tools/mkpkg/* $openelec_src_path/tools/mkpkg
mkdir -p $openelec_src_path/packages/emulator
cp -R packages/emulator/* $openelec_src_path/packages/emulator
mkdir -p $openelec_src_path/packages/emulator/RetroArch/icon
cp icon/icon.png $openelec_src_path/packages/emulator/RetroArch/icon
cp changelog.txt $openelec_src_path/packages/emulator/RetroArch

. $openelec_src_path/config/version

# make packages
cd $openelec_src_path/tools/mkpkg
packages="$selected_cores RetroArch retroarch-assets common-shaders core-info"

if [ ! -d $openelec_src_path/sources/ ]; then
    mkdir $openelec_src_path/sources/
fi

export LAKKA_MIRROR="http://sources.openelec.tv/$OPENELEC_VERSION"

for i in $packages; do
    echo "Building $i package..."
    ./mkpkg_$i > /dev/null 2&>1
    package_file=`ls -1 $i*.tar.xz`

    if [ ! -d $openelec_src_path/sources/$i/ ]; then
	mkdir $openelec_src_path/sources/$i/
    fi
    mv $package_file $openelec_src_path/sources/$i/

    echo "Generating md5 and url files for $i..."
      md5sum $openelec_src_path/sources/$i/$package_file > $openelec_src_path/sources/$i/$package_file.md5
      echo "$LAKKA_MIRROR/$package_file" > $openelec_src_path/sources/$i/$package_file.url

    echo "Setting PKG_VERSION in $i package.mk..."
      package_ver=`echo $package_file | cut -f 2 -d - | cut -f 1 -d .`
      sed -i -e "s/PKG_VERSION=\".*\"/PKG_VERSION=\"$package_ver\"/" $openelec_src_path/packages/emulator/$i/package.mk
done

cd $openelec_src_path
# build addon
PROJECT=$project ARCH=$arch ./scripts/create_addon RetroArch

exit 0
