function launch {
	python ${PWD}/rock/app.py &
	echo $! > .server.pid
}

function terminate {
	kill `cat .server.pid`
	rm .server.pid
}

launch
gabbi-run 127.0.0.1:5000 < ${PWD}/rock/tests/gabbits/test_hello_endpoint.yaml
terminate
