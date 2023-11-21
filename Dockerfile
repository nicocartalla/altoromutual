# Etapa de build
FROM openjdk:17-buster as build
RUN apt-get update && apt-get install -y \
    curl unzip \
    && rm -rf /var/lib/apt/lists/*
ENV GRADLE_VERSION=8.4
RUN curl -L https://services.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip -o gradle-$GRADLE_VERSION-bin.zip \
    && unzip gradle-${GRADLE_VERSION}-bin.zip \
    && rm -f gradle-${GRADLE_VERSION}-bin.zip
ENV PATH=$PATH:/gradle-${GRADLE_VERSION}/bin
ENV GRADLE_USER_HOME /cache
WORKDIR /app
COPY . /app
RUN gradle clean build


FROM tomcat:8.5.96-jre17-temurin-focal
COPY --from=build /app/build/libs/*.war /usr/local/tomcat/webapps/AltoroJ.war

EXPOSE 8080
CMD ["catalina.sh", "run"]
