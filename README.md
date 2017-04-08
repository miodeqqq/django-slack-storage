DJANGO SLACK STORAGE
========================

**Django Slack Storage** uses `slackclient` package and provides simple app for storing Slack Team data:

* channels data (channel id, channel name, channel members, number of members, channel description);
* users data (user name, user email, user avatar path);
* users posted files (user name, file URL, timestamp)
* channels posted messages (channel name, user name, message, timestamp)

**Current stable version:** v1.0

**Release date:** 08.04.2017

### Author:

* Maciej Januszewski (maciek@mjanuszewski.pl)

### Running:

* **Build Dockerfile:** 
```
docker build . -t slack-client
```

* **Run docker-compose (docker-compose.yml):**
```
docker-compose up -d
```


### From now:

* **Application can be found at:** 
```
http://localhost:1111
```

* **Celery flower can be found at (auth=slack/slack):** 
```
http://localhost:1112
```

**For a proper app working, you're supposed to provide Slack team API Token.**