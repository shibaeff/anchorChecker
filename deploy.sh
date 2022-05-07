ssh $1 ls -l
ssh $1 git clone https://github.com/shibaeff/anchorChecker
scp -r .env $1:~/anchorChecker/.env
ssh $1 docker-compose -f ./anchorChecker/docker-compose.yaml up -d anchorbot
