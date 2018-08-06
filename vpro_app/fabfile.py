from fabric.api import *
env.hosts='127.0.0.1'
env.user='vagrant'
env.password='vagrant'

def if_condition():
    if sudo("uname -a | awk '{print $4}' | cut -b 5-10") == "ubuntu":
       print "THIS IS UBUNTU SERVER"
       ubuntu()
    else:
       print "THIS IS CENTOS SERVER" 
       centos()

   
def ubuntu():
    ciserver_u


def centos():
    ci_c()
    app_c()
    db_c()
    lb_c()
    memchace_c()
    rabbitmq_c()
######################################### 

def ciserver_u():
     sudo("apt-get update -y")
     sudo("add-apt-repository ppa:openjdk-r/ppa -y")
     #sudo("apt-get install java* -y")
     sudo("apt-get update")
     sudo("apt-get install openjdk-8-jdk -y ")
     sudo("apt-get  install git -y")
     with cd("/"):
         sudo("git clone -b vp-memcached-rabbitmq https://github.com/wkhanvisualpathit/VProfile.git")
         sudo("apt-get install maven -y")
     with cd("/VProfile"):
         sudo("sed -i 's/password=password/password=root/g' src/main/resources/application.properties")
         sudo("sed -i 's/newuser/root/g' src/main/resources/application.properties")
         sudo("sed -i 's/localhost:3306/db.com:3306/' src/main/resources/application.properties")
         sudo("sed -i 's/address=127.0.0.1/address='rmq.com'/' src/main/resources/application.properties")
         sudo("sed -i 's/active.host=127.0.0.1/active.host='memcache.com'/' src/main/resources/application.properties")
         sudo("mvn clean install")


def ci_c():
     sudo("yum update -y")
     sudo("yum install epel-release -y")
     sudo("yum install  java-1.8.0-openjdk -y")
     sudo("yum  install git -y")
     sudo("yum update -y")
     with cd("/vagrant/vpro_app"):
          sudo("git clone -b vp-memcached-rabbitmq https://github.com/wkhanvisualpathit/VProfile.git")
     with cd("/usr/local"):
          sudo("wget http://www-eu.apache.org/dist/maven/maven-3/3.5.4/binaries/apache-maven-3.5.4-bin.tar.gz")
          sudo("tar xzf apache-maven-3.5.4-bin.tar.gz")
          sudo("ln -s apache-maven-3.5.4 maven")
          sudo("echo #!/bin/bash > /etc/profile.d/maven.sh")
          sudo("echo export M2_HOME=/usr/local/maven >> /etc/profile.d/maven.sh")
          sudo("echo export PATH=$M2_HOME/bin:$PATH >> /etc/profile.d/maven.sh")
          sudo("chmod +x /etc/profile.d/maven.sh")
          sudo("source /etc/profile.d/maven.sh")
          sudo("mvn -version")
          #sudo("yum install maven -y")
     with cd("/vagrant/vpro_app/VProfile"):
          sudo("sed -i 's/password=password/password=root/g' src/main/resources/application.properties")
          sudo("sed -i 's/newuser/root/g' src/main/resources/application.properties")
          sudo("sed -i 's/localhost:3306/db.com:3306/' src/main/resources/application.properties")
          sudo("sed -i 's/address=127.0.0.1/address='rmq.com'/' src/main/resources/application.properties")
          sudo("sed -i 's/active.host=127.0.0.1/active.host='memcache.com'/' src/main/resources/application.properties")
          sudo("mvn clean install")



def app_c():
     sudo("yum update -y")
     sudo("yum install  java-1.8.0-openjdk -y")
     sudo("yum install wget -y")
     with cd("/root"):
         sudo("wget http://redrockdigimark.com/apachemirror/tomcat/tomcat-8/v8.5.32/bin/apache-tomcat-8.5.32.tar.gz")
         sudo("mv apache-tomcat-8.5.32.tar.gz /opt/apache-tomcat-8.5.32.tar.gz")
     with cd("/opt"):
          sudo("tar -xvzf apache-tomcat-8.5.32.tar.gz")
          sudo("rm -rf /opt/apache-tomcat-8.5.32/webapps/ROOT")
          sudo("cp /vagrant/vpro_app/VProfile/target/vprofile-v1.war /opt/apache-tomcat-8.5.32/webapps/ROOT.war")
          sudo("service iptables stop")
          sudo("chkconfig iptables off")
          sudo("/opt/apache-tomcat-8.5.32/bin/startup.sh")


def db_c():
     #sudo("debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'")
     #sudo("debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'")
     sudo("yum update -y")
     sudo("yum install mysql-server -y")
     sudo("service mysqld start")
     sudo("sed -i 's/127.0.0.1/0.0.0.0/' /etc/my.cnf")
     #sudo("mysql -u root -e \"create database accounts\" --password='root';")
     #sudo("mysql -u root -e \"create database accounts\";")
     #sudo("mysql -u root -e  \"grant all privileges on *.* TO 'root'@'app.com' identified by 'root'\"  --password='root';")
     sudo("mysql -u root -e  \"grant all privileges on *.* TO 'root'@'app.com' identified by 'root'\";")
     #sudo("mysql -u root --password='root' accounts < /root/VProfile/src/main/resources/db_backup.sql;")
     sudo("mysql -u root  accounts < /vagrant/vpro_app/VProfile/src/main/resources/db_backup.sql;")
    #sudo("mysql -u root -e \"FLUSH PRIVILEGES\" --password='root';")
     sudo("mysql -u root -e \"FLUSH PRIVILEGES\";")
     sudo("service mysqld restart")

def lb_c():
     sudo("yum install epel-release -y")
     sudo("yum install nginx -y")
     sudo("cat /vagrant/vproapp  > /etc/nginx/conf.d/vproapp.conf")
     sudo("service iptables stop")
     sudo("service nginx start")


def memcache_c():
    sudo("yum install memcached -y")
    sudo("memcached -p 11111 -U 11111 -u memcache -d")



def rabbitmq_c():
     sudo("yum update -y")
     sudo("yum install wget -y")
     sudo("yum install epel-release -y")
     sudo("rpm --import https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc")
     sudo("yum update -y")
     #sudo("echo 'deb http://www.rabbitmq.com/debian/ testing main' | sudo tee /etc/apt/sources.list.d/rabbitmq.list")
     #sudo("wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -")
     #sudo("wget -O- https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc| sudo apt-key add -")
     sudo("yum install rabbitmq-server -y")
     sudo("echo '[{rabbit, [{loopback_users, []}]}].' > /etc/rabbitmq/rabbitmq.config")
     sudo("rabbitmqctl add_user test test")
     sudo("rabbitmqctl set_user_tags test administrator")
