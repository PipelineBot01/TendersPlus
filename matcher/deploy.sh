cd /home/TendersPlus
git add .
git commit -m"update model"
git push

# fetch the latest files
git pull -X theirs

echo "git pulling"

cd /home/TendersPlus/matcher

echo "run matcher"

# run the application
python3 main.py

