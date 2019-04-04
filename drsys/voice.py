from drconf import dr
from web import utils
from models.token import Token
#baidu app setting
appid="11123308"
apikey="e1xRkZZcHh90C3NrN1kc9E9A"
secretKey="NfQCAfK9IjB99pXqFfDmof9wC2dr6oxX"

voiceParam = {}
voiceParam['lan'] = 'zh'
voiceParam['ctp'] = 1
voiceParam['cuid'] = 'abcdxxx'
voiceParam['spd'] = 4
voiceParam['vol'] = 5
voiceParam['pit'] = 5
voiceParam['per'] = 0


tokenUrl = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (apikey , secretKey)


makeUrl = "http://tsn.baidu.com/text2audio"

def getToken():
	import datetime
	now = datetime.datetime.now().strftime(dr.datefmt)
	try:
		token = Token.objects.get(platform="baidu")
		if( token.checkExpired() ):
			return token.token;
		else:
			tmp = utils.jsonHttp(tokenUrl)
			token.token = tmp['refresh_token']
			token.expires = tmp['expires_in']
			token.fetchTime = now
			token.save()
			return token.token
	except Token.DoesNotExist:
		token = Token(platform="baidu")
		tmp = utils.jsonHttp(tokenUrl)
		token.token = tmp['refresh_token']
		token.expires = tmp['expires_in']
		token.fetchTime = now
		token.save()
		return token.token



		
