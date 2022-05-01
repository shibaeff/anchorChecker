ssh $1 ls -l
ssh $1 git clone https://github.com/shibaeff/anchorChecker
scp -r config.cfg $1:~/anchorChecker/config.cfg

