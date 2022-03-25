cd /home/TendersPlus

# fetch the latest files
git pull

echo "git pulling"

cd /home/TendersPlus/fronend

# install the dependency package
yarn

echo "install dependency package"
yarn build

# launch app
serve -s build -l 20221 -C