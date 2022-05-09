ssh $1 ls -l
ssh $1 git clone https://github.com/shibaeff/anchorChecker
scp -r .env $1:~/anchorChecker/.env
ssh $1 pybabel compile -D bot -d po -l ru
ssh $1 cd ./anchorChecker &&  docker-compose up -d anchorbot
