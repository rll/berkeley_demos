#!/usr/bin/env bash

FOLDING_ROOT=`rosstack find visual_feedback`/..
echo "Using folding_root $FOLDING_ROOT"

CVGREYC_DIR="$FOLDING_ROOT/visual_feedback/thirdparty/python-cvgreyc/cvgreyc/build/lib.linux-x86_64-2.6"
export PYTHONPATH="$CVGREYC_DIR:$PYTHONPATH"
echo "python path is now $PYTHONPATH"

