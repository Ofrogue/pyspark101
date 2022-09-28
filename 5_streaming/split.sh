#!/bin/bash

if [ -z "$1" ]; then
        echo "Missing file"
        exit 1
fi

dirname=$(echo "$1" | rev | cut -f 2- -d '.' | rev)
mkdir "$dirname"_cache
split -l 100  "$1" "$dirname"_cache/its1
