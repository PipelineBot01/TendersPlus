cd /home/TendersPlus

# fetch the latest files
git pull -X theirs

echo "git pulling"

cd /home/TendersPlus/matcher

echo "run matcher"

# run the application
python3 main.py

