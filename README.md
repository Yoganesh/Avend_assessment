# Avendus Assessment

### Procedure to run this code

    Before that make sure you have docker and python installed in your system

    docker run --name run-mysql -e MYSQL_ROOT_PASSWORD="secret" -e MYSQL_USER="avend" -e MYSQL_PASSWORD="secret" -e MYSQL_DATABASE="avend_db" -p "3306:3306" mysql:5.7

    docker-machine ip dev

    Use the above output in the files app.py line no 10 and web_scrap.py line no 9. It is done inorder to connect the mysql database

    docker build -t avend_ass .

    docker run -d -p 6655:6655 --name=avendus_container avend_ass:latest

###For logs

    docker logs -f <container-id>
    
