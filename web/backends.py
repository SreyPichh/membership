# from django.conf import settings
# #from django.contrib.auth.models import User

# url = "http://110.74.203.150"
# db = 'Asia2Asia'
# username = 'admin'
# password = 'admin73'

# common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
# uid = common.authenticate(db, username, password, {})
# models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

# class EmailAuth(object):
# 	def authenticate(self, username=None, password=None):
# 		try:
# 			user = Asia2Asia.objects.get(email=username)
# 			if user:
# 				return user
# 		except Asia2Asia.DoesNotExist:
# 			return None

# def get_user(self, user_id):
#     try:
#         return Asia2Asia.objects.get(pk=user_id)
#     except Asia2Asia.DoesNotExist:
#         return None
	
	
