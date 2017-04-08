#!/usr/bin/env bash
sleep 10
celery -A slack_client worker -l info -Q slack_update_db -n slack_update_db@%h -Ofair --autoscale=10,10 --maxtasksperchild=10