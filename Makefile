default: all

all:
	cd agent; make
	cd collector; make
	cd kafka; make

clean:
	docker rm `docker ps -a -q -f status=exited`
