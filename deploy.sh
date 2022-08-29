#!/bin/bash
fission spec init
fission env create --spec --name user-review-env --image nexus.sigame.com.br/fission-async-cx:0.0.1 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name user-review-fn --env user-review-env --src "./func/*" --entrypoint main.update_user_review_data --executortype newdeploy --maxscale 1
fission route create --spec --name user-review-rt --method PUT --url /onboarding/put_user_review --function user-review-fn
