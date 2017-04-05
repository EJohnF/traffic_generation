#!/bin/bash
sudo apt-get install rsyslog
# Install elasticsearch
sudo dpkg -i elasticsearch-1.0.1.deb
# Start elasticsearch service:
sudo service elasticsearch restart

# Unpack logstash
tar -xvzf logstash-1.4.0.tar.gz
# Move to opt:
sudo mv logstash-1.4.0 /opt/logstash

# Configure logstash as a service
sudo cp ./configs/logstash-syslog.conf /etc/
sudo cp ./configs/logstash /etc/init.d/
sudo chmod +x /etc/init.d/logstash

# Start logstash service
sudo service logstash start

# Add elasticsearch and logstash to init script   
sudo update-rc.d elasticsearch defaults 95 10
sudo update-rc.d logstash defaults 95 10

# Update syslog configuration
sudo cp ./configs/30-prcss.conf /etc/rsyslog.d/
sudo sed -ie 's/#$ModLoad imudp/$ModLoad imudp/g' /etc/rsyslog.conf
sudo sed -ie 's/#$UDPServerRun 514/$UDPServerRun 514/g' /etc/rsyslog.conf
sudo sed -ie 's/$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat/$ActionFileDefaultTemplate RSYSLOG_SyslogProtocol23Format/g' /etc/rsyslog.conf
sudo service rsyslog restart
sudo touch /var/log/prcss.log
sudo chmod +r /var/log/prcss.log
sudo chown syslog /var/log/prcss.log
sudo chgrp adm /var/log/prcss.log
