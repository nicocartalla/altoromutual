#!/bin/bash
gradle sonar   -Dsonar.projectKey=$SONAR_PROJECT_KEY   \
    -Dsonar.projectName=$SONAR_PROJECT   \
    -Dsonar.host.url=$SONAR_URL  \
    -Dsonar.token=$SONAR_TOKEN \
    --no-daemon --stacktrace