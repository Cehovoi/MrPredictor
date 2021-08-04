1. Create Dockerfile

2. docker build --tag python-docker .
	#docker build - build (creating an image) images from a Dockerfile and a 'context'
	#a build's context is the set of files located in the specified PATH or URL
	#--tag flag is used to set the name of the image 2218090394
	
	docker tag python-docker:latest python-docker:v1.0.0
	#to create a new tag for the image we’ve built above
	docker rmi python-docker:v1.0.0
	#remove the tag

3. docker run python-docker
	#in this case container run in isolation which includes networking

4. docker run --publish 5000:5000 python-docker
	#to publish a port --publish. The format command is [host port]:[container port]
	#-p for short 

5. docker run -d -p 5000:5000 python-docker
	#-d detached mode --detached

6. docker stop [container name] 
	docker restart [container name] 

7. docker ps -a
	#--all to see all conteiners on machine
	
8. docker rm hopeful_edison wizardly_solomon
	#can pass multiple container names

9. docker run -d -p 5000:5000 --name test-server python-docker
	#--name to specify conteiner name

10. docker volume create mysql
	#volume for data

11. docker volume create mysql_config
	#volume for config

12. docker network create mysqlnet

13. curl http://localhost:5000/widgets
	#check url from terminal

14. docker-compose -f docker-compose.yml up --build
	#build

15. docker-compose  -f docker-compose.dev.yml up -d
	#run

16. docker images
	docker image rm [OPTIONS] IMAGE [IMAGE...]

17. docker-compose up
	#run only .yml (not dev.yml)

18. docker system prune --all
