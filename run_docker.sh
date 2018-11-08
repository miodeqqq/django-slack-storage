#!/usr/bin/env bash

clear;docker build . -t slack-client && docker-compose -f docker-compose.yml up --build --remove-orphans