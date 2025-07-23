#!/bin/bash
script_dir=$(dirname "$(readlink -f "$0")")
export KB_DEPLOYMENT_CONFIG=$script_dir/../deploy.cfg
export KB_AUTH_TOKEN=`cat /kb/module/work/token`
echo "Removing temp files..."
rm -rf /kb/module/work/tmp/*
echo "...done removing temp files."
export PYTHONPATH=$script_dir/../lib:$PATH:$PYTHONPATH
cd $script_dir/..
python3 -m nose --with-coverage --cover-package=kbase_protein_network_analysis_toolkit --cover-html --cover-html-dir=/kb/module/work/test_coverage --nocapture  --nologcapture test/unit_tests
