#!/usr/bin/env bash
sleep 10
celery -A slack_client worker -l info -Q slack_download_posted_files -n slack_download_posted_files@%h -Ofair --autoscale=10,10 --maxtasksperchild=10