
# fobbage
The ultimate quiz

## !! NO longer requires REDIS
- requires redis: `sudo docker run -p 6379:6379 -d redis:6`
- `scripts/setup`

cat fobbage.json | heroku run --no-tty --app fobbage -- python manage.py loaddata --format=json -

