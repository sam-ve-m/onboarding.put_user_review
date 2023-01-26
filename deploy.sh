fission spec init
fission env create --spec --name onb-br-put-review-env --image nexus.sigame.com.br/fission-onboarding-br-put-review:0.1.0 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-put-review-fn --env onb-br-put-review-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-br-put-review-rt --method PUT --url /onboarding/put_user_review --function onb-br-put-review-fn
