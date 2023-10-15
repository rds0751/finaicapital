from django.core.management.base import BaseCommand
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
from users.models import User
from wallets.models import WalletHistory
import datetime
from datetime import timedelta
from level.models import LevelIncomeSettings, UserTotal
from users.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string


class Command(BaseCommand):
	help = "Send ROI Incomes"

	def handle(self, *args, **options):
		l = UserTotal.objects.filter(level__amount__gte=20)
		
		def generateid():
			txnid = get_random_string(8)
			try:
				txn = WalletHistory.objects.get(txnid = txnid)
			except WalletHistory.DoesNotExist:
				txn = 0
			if txn:
				generateid()
			else:
				return txnid
			
		def finduplines(user):  
			try:
				user = User.objects.get(username__iexact=str(user)) 
				upline = user.referral   
			except User.DoesNotExist:   
				upline = 'blank'
			return upline
		

		for x in l:
			directs = UserTotal.objects.filter(direct=x.user).count()
			time_difference = timezone.now() - x.activated_at
			days_difference = 5
			roi = x.level.amount * 0.1 / 30
			count = 0
			for d in range(0,days_difference):
				wallet = WalletHistory()
				wallet.comment = "ROI Income"
				wallet.user_id = x.user
				wallet.amount = roi
				wallet.type = "credit"
				wallet.created_at = timezone.now() - timedelta(days=count)
				wallet.save()
				user = User.objects.get(username=x.user)
				user.wallet += roi
				user.save()
				userid = User.objects.get(username=user.username)
				level = 0
				count += 1
				print(days_difference, count)