#!/bin/sh
docker build -t fission-onboarding-br-put-review --secret id=pipconfig,src=$HOME/.pip.conf .
