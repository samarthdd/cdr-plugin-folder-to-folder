echo "\n\n**** Connects to QA server and binds local ports *****\n"
echo "API - http://localhost:8000/docs"
echo "Jupyter -  http://localhost:8001/"
echo "Elastric - http://localhost:8002/"
echo "Minio - http://localhost:8003/"
echo "\n"
echo "usage: bin/dev-connect-to-qa-server.sh packer 34.253.17.169"
echo "note that these ports are a different from the ones used by DockerCompose"
echo "\n\n"
export SSH_KEY=$1
export SERVER_IP=$2
ssh -L 8000:127.0.0.1:8880 -L 8001:127.0.0.1:8888 -L 8002:127.0.0.1:5601 \
    -L 8003:127.0.0.1:9000 -L 8004:127.0.0.1:1313 -L 8005:127.0.0.1:8866 \
    -i $SSH_KEY ubuntu@$SERVER_IP