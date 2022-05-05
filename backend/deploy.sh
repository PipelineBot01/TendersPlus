cd /home/TendersPlus

# fetch the latest files
git pull -X theirs

echo "git pulling"

cd /home/TendersPlus/backend
# install the requirements
pip3 install -r requirements.txt --user

echo "install requirements"

cd /home/TendersPlus/backend/app


# run the application
python3 main.py --env_path=./.env

