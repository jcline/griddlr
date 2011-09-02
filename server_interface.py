from flup.server.fcgi import WSGIServer

def servcont(environ, start_response):
	print 'got request: %s' % environ
	start_response('200 OK', [('Content-Type', 'text/plain')])
	return ['Hello World!\n']


if __name__ == '__main__':
	from flup.server.fcgi import WSGIServer
	WSGIServer(servcont, umask=0, bindAddress = '/tmp/fcgi.sock').run()
