# db urls

# current
postgres://sterre:figment-unleaded-spender@postgresql-sterre.alwaysdata.net/sterre_fobbage

postgres://pvbqjpjukoemho:ffde78ee01b3aecfd8c871bee98a4a39861ba3568e3aa00577f7ca37f0f4c029@ec2-63-35-156-160.eu-west-1.compute.amazonaws.com:5432/d7tc0lmp4lpjkv
postgres://jdcfgwqa:zvVxVM8OvP95YGcO2j7-WHcjbVqFcJQU@tyke.db.elephantsql.com/jdcfgwqa

# load data
cat fobbage290923.json | heroku run --no-tty --app fobbage -- python manage.py loaddata --format=json -
