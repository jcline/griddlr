
import oauth2 as oauth
import time
import urlparse

class TumblrAuth:
	identities = dict()

	def __init__(self):
		self.req_url = "http://www.tumblr.com/oauth/request_token"
		self.acc_url = "http://www.tumblr.com/oauth/access_token"
		self.auth_url = "http://www.tumblr.com/oauth/authorize" 

		self.cons_key = ""
		self.sec_key = ""

		self.consumer = oauth.Consumer(key=self.cons_key, secret=self.sec_key)

	def authreq(self,ident):
		client = oauth.Client(self.consumer)
		response, content = client.request(self.req_url, "GET")
		if response['status'] != '200':
			return [False,'Failed to authenticate. Please try again.']

		request_token = dict(urlparse.parse_qsl(content))
		TumblrAuth.identities[ident[0]] = oauth.Token(request_token['oauth_token'],
				request_token['oauth_token_secret'])

		return [True, self.auth_url, request_token['oauth_token']]

	def authconf(self, ident):
		TumblrAuth.identities[ident[0]].set_verifier(ident[1])

		client = oauth.Client(self.consumer, TumblrAuth.identities[ident[0]])

		response, content = client.request(self.acc_url, "POST")
		keys = dict(urlparse.parse_qsl(content))

		TumblrAuth.identities[ident[0]] = oauth.Token(keys['oauth_token'],
				keys['oauth_token_secret'])

	def signreq(self, ident, url):
		client = oauth.Client(self.consumer, TumblrAuth.identities[ident[0]])
		response, content = client.request(url)
		if response['status'] == '200':
			return content
		return None
		

# Set up instances of our Token and Consumer. The Consumer.key and 
# Consumer.secret are given to you by the API provider. The Token.key and
# Token.secret is given to you after a three-legged authentication.
#token = oauth.Token(key="tok-test-key", secret="tok-test-secret")
#consumer = oauth.Consumer(key="con-test-key", secret="con-test-secret")

# Set our token/key parameters
#params['oauth_token'] = token.key
#params['oauth_consumer_key'] = consumer.key

# Create our request. Change method, etc. accordingly.
#req = oauth.Request(method="GET", url=url, parameters=params)

# Sign the request.
#signature_method = oauth.SignatureMethod_HMAC_SHA1()
#req.sign_request(signature_method, consumer, token)

