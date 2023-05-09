# import os
# import pyotp
# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException
# from rest_framework import serializers
#
# client = Client(os.environ['TWILIO_ACCOUNT_SID'],
#                 os.environ['TWILIO_AUTH_TOKEN'])
# verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])
#
#
# def send(phone):
#     verify.verifications.create(to=phone, channel='sms')
#
#
# def check(phone, code):
#     try:
#         result = verify.verification_checks.create(to=phone, code=code)
#     except TwilioRestException:
#         raise serializers.ValidationError("Invalid code.")
#     return result.status == 'approved'
#
#
# class GenerateKey:
#     @staticmethod
#     def returnValue():
#         secret = pyotp.random_base32()
#         totp = pyotp.TOTP(secret, interval=86400)
#         otp = totp.now()
#         return {"totp": secret, "OTP": otp}
