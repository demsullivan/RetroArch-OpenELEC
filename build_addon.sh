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
    if [[ "$selected_cores" == "all" ]]; then
	valid_core_selection="y"
	selected_cores="$real_cores"
    fi
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
exit 0

echo "CFG_CORES=\"$selected_cores\"" > packages/emulator/RetroArch/config

# copy files to OpenELEC source
cp -R tools/mkpkg/* $openelec_src_path/tools/mkpkg
mkdir -p $openelec_src_path/packages/emulator
cp -R packages/emulator/* $openelec_src_path/packages/emulator

# make packages
cd $openelec_src_path/tools/mkpkg
for [ i in "$selected_cores retroarch" ]; do
    ./mkpkg_$i
    echo "http://sources.openelec.tv/4.0.7/pkgname" > $openelec_src_path/sources/pkgname/pkgname
done

# build addon
PROJECT=$project ARCH=$arch ./scripts/create_addon RetroArch

exit 0
