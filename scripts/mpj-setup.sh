#!/bin/sh

apt-get update
apt-get install -y default-jdk

sudo su

mkdir -p /home/root/.ssh

ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -P ""
cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys
ssh-keyscan localhost > /root/.ssh/known_hosts

cat /clonedssh >> /root/.ssh/authorized_keys

export MPJ_HOME=/mpj
export PATH=$MPJ_HOME/bin:$PATH
export CLASSPATH=.:$MPJ_HOME/lib/mpj.jar
export PATH=/usr/lib/jvm/java-1.7.0-opendjk-amd64/jre/bin/:$PATH

echo "export MPJ_HOME=/mpj" >> /root/.bashrc
echo "export PATH=$MPJ_HOME/bin:$PATH" >> /root/.bashrc
echo "export CLASSPATH=.:$MPJ_HOME/lib/mpj.jar" >> /root/.bashrc
echo "export PATH=/usr/lib/jvm/java-1.7.0-opendjk-amd64/jre/bin/:$PATH" >> /root/.bashrc

mpjdaemon -boot localhost
