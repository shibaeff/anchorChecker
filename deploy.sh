ssh $1 ls -l
ssh $1 git clone https://github.com/shibaeff/anchorChecker
ssh pybabel compile -D bot -d po -l ru
scp -r .env $1:~/anchorChecker/.env
scp ./po/ru/LC_MESSAGES/bot.mo $1:~/anchorChecker/po/ru/LC_MESSAGES/bot.mo
ssh $1 docker-compose -f ./anchorChecker/docker-compose.yaml up -d
