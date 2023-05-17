#Use 8.0.32 mysql version 
FROM mysql:8.0.32


#Define root password for mysql
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}

#Create classic user for mysql 
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}

#Add volume for database backup
COPY ./src/output_file.sql  /docker-entrypoint-initdb.d/
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/
CMD ["mysqld"]

EXPOSE ${MYSQL_PORT}