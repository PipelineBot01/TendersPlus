cd /home/TendersPlus

# fetch the latest files
git pull -X theirs

echo "git pulling"

cd /home/TendersPlus/scraper

# run the application
python3 tenders/main.py
