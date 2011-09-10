from flup.server.fcgi import WSGIServer

import urlparse
import time
import json
import norse
import os.path

auther = None

beg = ""
end = ""

http_codes = {
			'404': '404 Not Found',
			'303': '303 See Other',
			'503': '503 Service Unavailable'
	}

threezerothree = http_codes['303']
fourzerofour = http_codes['404']
fivezerothree = http_codes['503']

text_plain = [('Content-Type', 'text/plain')]

def servcont(environ, start_response):
	start = time.time()
	addr = environ['REMOTE_ADDR']
	path = environ['PATH_INFO']
	try:
		tmp = distribute(environ, start_response, addr, path)
	except Exception, e:
		print e
		end = time.time()
		print time.time(), "\t", addr, "\t", path, "\t", end-start
		start_response(fivezerothree, text_plain)
		return [fivezerothree]

	end = time.time()
	print time.time(), "\t", addr, "\t", path, "\t", end-start
	return tmp

def distribute(environ, start_response, addr, path):
	if environ['REQUEST_METHOD'] != 'GET':
		start_response(fourzerofour, text_plain)
		return [fourzerofour]

	if path == '/':
		start_response(fourzerofour, text_plain)
		return [fourzerofour]
	elif path == '/dash.do':
		return contentrequest(environ, start_response, addr)
	elif path == '/login.do':
		return beginauthuser(environ, start_response, addr)
	elif path == '/callback.do':
		if environ['REDIRECT_STATUS'] == '200':
			return endauthuser(environ, start_response, addr)
		else:
			start_response(fivezerothree, text_plain)
			return [fivezerothree]
	# Default error page
	start_response(fourzerofour, text_plain)
	return [fourzerofour]

def beginauthuser(environ, start_response, addr):
	ident = [addr,None]
	ret = auther.authreq(ident)
	if ret[0]:
		# Redirect the user to tumblr w/ the oauth request token
		start_response(threezerothree, [('Content-Type', 'text/plain'),
							('Location', '%s?oauth_token=%s' % (ret[1], ret[2])),
							('Authorization', ret[2])
							])
		return ['Success']
	else:
		start_response(fivezerothree, text_plain)
		return ret[1]

def endauthuser(environ, start_response, addr):
	response = dict(urlparse.parse_qsl(environ['QUERY_STRING']))
	
	ident = [addr,response['oauth_verifier']]
	auther.authconf(ident)
	start_response(threezerothree, [('Content-Type', 'text/plain'),
		            ('Location', 'dash.do')])
	return ['Success']
	
def contentrequest(environ, start_response, addr):
	ident = [addr]
	env = urlparse.parse_qs(environ['QUERY_STRING'])
	#try:
	#	num = int(env['num'][0])
	#except Exception, e:
	#	num=20
	try:
		off = int(env['off'][0])
	except Exception, e:
		off=0
	num = 40
	
	num = num + off
	mod = num % 20
	if mod:
		num = num + mod

	uri_form = 'http://api.tumblr.com/v2/user/dashboard?type=photo&offset=%s' 
	clist = []
	first = None

	start = time.time()
	
	for i in xrange(off, num, 20):
		response = auther.signreq(ident, uri_form % str(i))
		parsed = json.loads(str(response))
		parsedrp = parsed['response']['posts']

		if i == off:
			first = parsedrp[0]['id']
		elif parsedrp[0]['id'] == first:
			break

		clist.extend(
				[k 
				for i in parsedrp
				for j in i['photos'] 
				for k in j['alt_sizes']
				if k['width'] == 400
				]
				)
	stop = time.time()
	print stop-start
	
	#stop = true
	#clist = 
	posts = "".join(['<div class=\"post\"><div class=\"meta\"><img src=\"%s\" alt="" /></div></div>' % (i['url']) for i in clist])

	content = '%s%s%s' % (beg,posts,end)

	start_response('200 OK', [('Content-Type', 'text/html')])
	return str(content)

if __name__ == '__main__':
	from flup.server.fcgi import WSGIServer
	auther = norse.TumblrAuth()
	if os.path.exists("index.html.beg") and	os.path.exists("index.html.end"):
		beg = open("index.html.beg","r").read()
		end = open("index.html.end","r").read()
		WSGIServer(servcont, umask=0, bindAddress = '/tmp/fcgi.sock').run()
	else:
		print 'COULD NOT READ TEMPLATE'
