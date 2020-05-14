
## Setup
You can use Docker / docker-compose.

```sh
sudo docker-compose up -d # for background run and autostart on boot
sudo docker-compose up # for foreground run

sudo docker-compose down # stop and remove the docker container
```

X Window Authentication Setting is required.

For a temporal experiment, you can use `xhost local:` command (while some security issues remain).
