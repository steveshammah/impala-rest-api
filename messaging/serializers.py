import re

from rest_framework import serializers
# from django.utils.translation import ugettext_lazy as _


from .models import *


class SmsModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        max_length=8, required=True, help_text='Enter code')

    class Meta:
        model = SmsModel
        fields = ["code"]
        validators: list = []

    def validate_code(self, value):
        code_regex = "^[0-9]{6}$"
        regexed_code = re.search(code_regex, value)

        if regexed_code:
            value = re.sub(r'[^0-9]', '', value)
        else:
            raise serializers.ValidationError(
                "Code must be 6 digits.")
        return value
