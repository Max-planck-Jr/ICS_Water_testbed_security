#!/bin/bash
(
cd "OpenPLC_v3_customized" || exit 1

# check if running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# create the docker network
sudo docker network inspect swat || sudo docker network create --subnet 172.18.0.0/24 --driver bridge swat



# build and run the plcs
for i in {11..16}
do
  sudo docker build -t plc"$i":oplcv3 .
  sudo docker run --net swat --ip 172.18.0."$i" -d  --privileged --name plc"$i" -p 100"$i":8080 plc"$i":oplcv3
done


)


# build and run scadaBR
(
cd scadabr || exit 1
sudo docker build -t scadabr:scadabr .
sudo docker run --net swat --ip 172.18.0.9 -d --privileged --name HMI-HIS -p 10010:8080 scadabr:scadabr
)



#  build and run the simulator
(
cd sim || exit 1
sudo docker build -t sim:sim .
sudo docker run --net swat --ip 172.18.0.10 -d --privileged --name MTU -h MTU sim:sim
)
