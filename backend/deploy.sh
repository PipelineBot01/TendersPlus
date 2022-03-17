cd /home/TendersPlus/backend

# fetch the latest files
git pull

echo "git pulling"

# install the requirements
pip3 install -r requirements.txt

echo "install requirements"

# run the application
python3 ./app/main.py

