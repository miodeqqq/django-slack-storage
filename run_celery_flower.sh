#!/usr/bin/env bash
sleep 15
celery -A slack_client flower --basic_auth=slack:slack