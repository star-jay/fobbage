
# fobbage
The ultimate quiz

## !! NO longer requires REDIS
- requires redis: `sudo docker run -p 6379:6379 -d redis:6`
- `scripts/setup`

cat fobbage.json | heroku run --no-tty --app fobbage -- python manage.py loaddata --format=json -

heroku run python manage.py dumpdata --indent=2 --natural-foreign --natural-primary accounts quizes > fobbage4.json
