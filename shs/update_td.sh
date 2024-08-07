#!/bin/bash
cd $HOME
# cd /data/project/mdwiki/

rm -rf tdx

# Download the wd-core repository from GitHub.
git clone https://github.com/MrIbrahem/Translation-Dashboard.git tdx
# git clone -b update --single-branch https://github.com/MrIbrahem/Translation-Dashboard.git tdx

# delete composer.json and composer.lock
rm -rf tdx/composer.json tdx/composer.lock -v

# delete all json files in all subdirectories
find tdx -name *.json -delete

# delete vendor
rm -rf tdx/vendor -v

# copy all files to public_html
cp -rf -v tdx/* public_html/Translation_Dashboard -v

# Remove the `tdx` directory.
rm -rf tdx

echo ">>> Script execution completed successfully."
