cd /home/TendersPlus

# fetch the latest files
git pull -X theirs

echo "git pulling"

cd /home/TendersPlus/matcher
# install the requirements
pip3 install -r requirements.txt

echo "install requirements"


# run the application
python3 main.py

