#!/bin/bash

NAME='de.lukass.appstore_search'
VERSION=$(head -1 VERSION)
EXTENSION='alfredworkflow'

FILENAME=$NAME.$VERSION.$EXTENSION

# create build dir if it doesnt exist
[ ! -d build ] && mkdir build > /dev/null

# if build/tmp exists, remove contents
[ -d build/tmp ] && rm -rf build/tmp/* > /dev/null
# if it doesn't, create it
[ ! -d build/tmp ] && mkdir build/tmp > /dev/null

# copy necessary files into build/tmp
cp -RH alp requests build/tmp/ > /dev/null
cp appsearch.py iaprefs.py prefs.py build/tmp/ > /dev/null
cp icon.png info.plist build/tmp/ > /dev/null

# zip it's contents into build
pushd build/tmp > /dev/null
zip -r ../$FILENAME * > /dev/null
popd > /dev/null

# remove tmp dir
rm -rf build/tmp > /dev/null