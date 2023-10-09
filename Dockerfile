# Etapa de build
FROM openjdk:8-jdk as build
RUN curl -L https://services.gradle.org/distributions/gradle-3.0-bin.zip -o gradle-3.0-bin.zip \
    && unzip gradle-3.0-bin.zip \
    && rm -f gradle-3.0-bin.zip
ENV PATH=$PATH:/gradle-3.0/bin
ENV GRADLE_USER_HOME /cache
WORKDIR /app
COPY . /app
RUN gradle build

FROM tomcat:8-jre8
COPY --from=build /app/build/libs/*.war /usr/local/tomcat/webapps/AltoroJ.war

EXPOSE 8080
CMD ["catalina.sh", "run"]
