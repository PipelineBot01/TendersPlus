cd /home/TendersPlus

git add .
git commit -m"update model"

echo "git pulling"
# fetch the latest files
git pull -X theirs

git add .
git commit -m"update model"
git push origin master

cd /home/TendersPlus/matcher

echo "run matcher"

# run the application
python3 main.py

