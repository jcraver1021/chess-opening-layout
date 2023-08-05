#!/bin/bash

for dir in $(ls -d */); do
  cd $dir
  export PYTHONPATH="$PYTHONPATH:${PWD/tests/src}"
  cd ..
done

pytest
