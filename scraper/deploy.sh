cd /home/TendersPlus

# fetch the latest files
git pull -X theirs

echo "git pulling"

cd scraper

# run the application
python3 main.py
