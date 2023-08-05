#!/bin/bash

for dir in $(ls -d */); do
  cd $dir
  echo $PYTHONPATH
  echo ${PWD/tests/src}
  export PYTHONPATH="$PYTHONPATH:${PWD/tests/src}"
  echo $PYTHONPATH
  cd ..
done

pytest
