#!/usr/bin/python
# -*- coding:utf-8 -*-

REGION = "cn-hangzhou"
PRODUCT_NAME = "SMSapi"
DOMAIN = "dysmsapi.aliyuncs.com"
ACCESS_KEY_ID = 'akid'   # 必填
ACCESS_KEY_SECRET = 'akst'  # 必填

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider


acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.modify_point(PRODUCT_NAME, REGION, DOMAIN)


from aliyunsdkcore.request import RpcRequest


class SendSmsRequest(RpcRequest):
    def __init__(self):
        RpcRequest.__init__(self, 'Dysmsapi', '2017-05-25', 'SendSms')

    def set_TemplateCode(self, TemplateCode):
        """ Template Code """
        self.add_query_param('TemplateCode', TemplateCode)

    def set_TemplateParam(self, TemplateParam):
        """ Template parameters, variables """
        self.add_query_param('TemplateParam', TemplateParam)

    def PhoneNumbers(self, PhoneNumbers):
        """Phone number to send """
        self.add_query_param('PhoneNumbers', PhoneNumbers)

    def set_SignName(self, SignName):
        """ SMS Signature Name """
        self.add_query_param('SignName', SignName)

def send_sms(phone_numbers, sign_name='The signature name', template_code='template code',
             template_param='{"template_param_name":"value"}'):
    """
    Call the SMS interface and return the result
    :param phone_numbers:  phone number
    :param sign_name:   SMS Signature Name
    :param template_code:   Template CODE
    :param template_param:  Template parameters, variables
    """
    sign_name = sign_name
    sms_request = SendSmsRequest()
    sms_request.set_TemplateCode(template_code)  # SMS templateCODE
    if template_param:
        sms_request.set_TemplateParam(template_param) # SMS template parameters.
    sms_request.set_SignName(sign_name)  # 
    sms_request.set_PhoneNumbers(phone_numbers)  #Phone number to send
    sms_response = acs_client.do_action_with_exception(sms_request)  # Call the SMS send interface and return json
    return sms_response


if __name__ == '__main__':
    print(send_sms('Please enter phone number to send'))

