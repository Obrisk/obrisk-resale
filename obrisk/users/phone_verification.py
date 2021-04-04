import os
from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.request import RpcRequest


class SendSmsRequest(RpcRequest):
    """This class has been taken from the python module aliyunsdkdysmsapi
       that is not an aliyun PyPI package. If this module is built manually
       in the project then can be easily imported as
       from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest"""

    def __init__(self):
        RpcRequest.__init__(self, 'Dysmsapi', '2017-05-25', 'SendSms')

    def get_TemplateCode(self):
        return self.get_query_params().get('TemplateCode')

    def set_TemplateCode(self,TemplateCode):
        self.add_query_param('TemplateCode',TemplateCode)

    def get_PhoneNumbers(self):
        return self.get_query_params().get('PhoneNumbers')

    def set_PhoneNumbers(self,PhoneNumbers):
        self.add_query_param('PhoneNumbers',PhoneNumbers)

    def get_SignName(self):
        return self.get_query_params().get('SignName')

    def set_SignName(self,SignName):
        self.add_query_param('SignName',SignName)

    def get_ResourceOwnerAccount(self):
        return self.get_query_params().get('ResourceOwnerAccount')

    def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
        self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

    def get_TemplateParam(self):
        return self.get_query_params().get('TemplateParam')

    def set_TemplateParam(self,TemplateParam):
        self.add_query_param('TemplateParam',TemplateParam)

    def get_ResourceOwnerId(self):
        return self.get_query_params().get('ResourceOwnerId')

    def set_ResourceOwnerId(self,ResourceOwnerId):
        self.add_query_param('ResourceOwnerId',ResourceOwnerId)

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self,OwnerId):
        self.add_query_param('OwnerId',OwnerId)

    def get_SmsUpExtendCode(self):
        return self.get_query_params().get('SmsUpExtendCode')

    def set_SmsUpExtendCode(self,SmsUpExtendCode):
        self.add_query_param('SmsUpExtendCode',SmsUpExtendCode)

    def get_OutId(self):
        return self.get_query_params().get('OutId')

    def set_OutId(self,OutId):
        self.add_query_param('OutId',OutId)

def send_sms(business_id, phone_numbers, sign_name,
        template_code,template_param=None):
    """
    Call the SMS interface and return the result
    :param phone_numbers:  phone number
    :param sign_name:   SMS Signature Name
    :param template_code:   Template CODE
    :param template_param:  Template parameters, variables
    """

    REGION = os.getenv('SMS_REGION')
    PRODUCT_NAME = "SMSapi"
    SMS_DOMAIN = os.getenv('SMS_DOMAIN')
    ACCESS_KEY_ID = os.getenv('RAM_USER_ID')
    ACCESS_KEY_SECRET = os.getenv('RAM_USER_S3KT_KEY')

    verify_counter = 0

    if getattr(settings, 'PHONE_SIGNUP_DEBUG', False):
        print("Setting up local env...")

    else:
        acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
        region_provider.modify_point(PRODUCT_NAME, REGION, SMS_DOMAIN)


    sign_name = sign_name
    sms_request = SendSmsRequest()
    sms_request.set_TemplateCode(template_code)  # SMS templateCODE

    # SMS template variable parameters
    if template_param is not None:
        sms_request.set_TemplateParam(template_param)

    # Set up the business request flow number, required.
    sms_request.set_OutId(business_id)

    sms_request.set_SignName(sign_name)  # 
    sms_request.set_PhoneNumbers(phone_numbers)  #Phone number to send

    # 数据提交方式
	# sms_request.set_method(MT.POST)

	# 数据提交格式
    # sms_request.set_accept_format(FT.JSON)

    # Call the SMS send interface and return json
    sms_response = acs_client.do_action_with_exception(sms_request)
    return sms_response
