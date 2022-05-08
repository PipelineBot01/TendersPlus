cd /home/TendersPlus


git reset --hard origin/master:

echo "git pulling"

git pull -X theirs

cd /home/TendersPlus/matcher

echo "run matcher"

# run the application
python3 main.py

