#!/usr/bin/env bash

sleep 10
celery -A slack_client.celery beat -l debug
