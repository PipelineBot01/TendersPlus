cd /home/TendersPlus

git add .
git commit -m"update log"

echo "git pulling"

git pull -X theirs

git add .
git commit -a
git push origin master

cd /home/TendersPlus/matcher

echo "run matcher"

# run the application
python3 main.py

