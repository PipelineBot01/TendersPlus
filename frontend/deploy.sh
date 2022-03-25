cd /home/TendersPlus

# fetch the latest files
git pull

echo "git pulling"

cd /home/TendersPlus/frontend

# install the dependency package
yarn

yarn build

serve -s buld -l 20221 -C


