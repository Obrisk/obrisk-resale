from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from obrisk.notifications.models import Notification, notification_handler

PROVINCE_CHOICES = (
    ('q', 'anhui'),
    ('w', 'beijing'),
    ('e', 'chongqing'), 
    ('r', 'fujian'),
    ('t', 'gansu'),   
    ('y', 'guangdong'),   
    ('u', 'guangxi'),   
    ('i', 'guizhou'),   
    ('o', 'hainan'),    
    ('p', 'hebei'),     
    ('a', 'heilongjiang'),   
    ('s', 'henan'),  
    ('d', 'hongkong'),  
    ('f', 'hubei'),  
    ('g', 'hunan'),  
    ('h', 'inner_mongolia'),  
    ('j', 'jiansu'),
    ('k', 'jiangxi'),
    ('l', 'jilin'),  
    ('z', 'liaoning'),
    ('x', 'macau'),
    ('c', 'ningxia'),  
    ('v', 'qinghai'), 
    ('b', 'shaanxi'),   
    ('n', 'shadong'),   
    ('m', 'shanxi'),  
    ('as', 'sichuan'),
    ('dd', 'tianjin'),  
    ('sd', 'tibet'),  
    ('hb', 'xinjiang'),   
    ('jj', 'yunan'),    
    ('ll', 'zhejiang'),


)

CITY_CHOICES = (
    ('Q', 'Aba'),
    ('W', 'Aksu'),
    ('E', 'Alxa League'),
    ('R', 'Ankang'),
    ('T', 'Anqing'),
    ('Y', 'Anshan'),
    ('U', 'Anshun'),
    ('I', 'Anyang'),
    ('O', 'Baicheng'),
    ('P', 'Baise'),
    ('Z', 'Baishan'),
    ('ZX', 'Baiyin'),
    ('ZA', 'Baoding'),
    ('ZS', 'Baoji'),
    ('ZW', 'Baoshan'),
    ('ER', 'Baotou'),
    ('RE', 'Bayan Nur'),
    ('XZ', 'Bayingholin'),
    ('ZQ', 'Bazhong'),
    ('QZ', 'Beihai'),
    ('SZ', 'Beijing'),
    ('AZ', 'Bengbu'),
    ('WZ', 'Benxi'),
    ('QW', 'Bijie'),
    ('WQ', 'Binzhou'),
    ('EW', 'Börtala'),
    ('EQ', 'Bozhou'),
    ('QE', 'Cangzhou'),
    ('WE', 'Chamdo'),
    ('AS', 'Changchun'),
    ('SA', 'Changde'),
    ('AD', 'Changji'),
    ('DA', 'Changsha'),
    ('AQ', 'Changzhi'),
    ('QA', 'Changzhou'),
    ('A', 'Chaohu'),
    ('S', 'Chaoyang'),
    ('D', 'Chaozhou'),
    ('F', 'Chengde'),
    ('G', 'Chengdu'),
    ('H', 'Chenzhou'),
    ('J', 'Chifeng'),
    ('K', 'Chizhou'),
    ('L', 'Chongqing'),
    ('LO', 'Chongzuo'),
    ('KI', 'Chuxiong'),
    ('JU', 'Chuzhou'),
    ('HY', 'Dali'),
    ('GT', 'Dalian'),
    ('FR', 'Dandong'),
    ('DE', 'Daqing'),
    ('SW', 'Datong'),
    ('PL', 'Daxinganling'),
    ('IK', 'Daye'),
    ('UJ', 'Dazhou'),
    ('YH', 'Dehong'),
    ('TG', 'Deyang'),
    ('RF', 'Dezhou'),
    ('SX', 'Dingxi'),
    ('DC', 'Diqing'),
    ('FV', 'Dongguan'),
    ('GB', 'Dongying'),
    ('HN', 'Enshi'),
    ('JM', 'Ezhou'),
    ('KM', 'Fangchenggang'),
    ('LM', 'Foshan'),
    ('ML', 'Fushun'),
    ('MK', 'Fuxin'),
    ('MJ', 'Fuyang'),
    ('MH', 'Fuzhou'),
    ('MG', 'Fuzhou Jiangxi'),
    ('MF', 'Gannan'),
    ('MD', 'Ganzhou'),
    ('MS', 'Garzê'),
    ('MA', 'Golog'),
    ('QG', 'Guangan'),
    ('WG', 'Guangyuan'),
    ('EG', 'Guangzhou'),
    ('RG', 'Guigang'),
    ('GY', 'Guilin'),
    ('YG', 'Guiyang'),
    ('UG', 'Guyuan'),
    ('IG', 'Haibei'),
    ('OG', 'Haidong'),
    ('PG', 'Haikou'),
    ('GQ', 'Hainan'),
    ('GW', 'Haixi'),
    ('GE', 'Hami'),
    ('GR', 'Handan'),
    ('GU', 'Hangzhou'),
    ('GI', 'Hanzhong'),
    ('GO', 'Harbin'),
    ('GP', 'Hebi'),
    ('ZG', 'Hechi'),
    ('XG', 'Hefei'),
    ('CG', 'Hegang'),
    ('VG', 'Heihe'),
    ('BG', 'Hengshui'),
    ('NG', 'Hengyang'),
    ('MG', 'Heyuan'),
    ('GM', 'Heze'),
    ('GN', 'Hezhou'),
    ('GV', 'Hinggan'),
    ('GC', 'Hohhot'),
    ('GX', 'Huaibei'),
    ('GZ', 'Huaihua'),
    ('FQ', 'Huainan'),
    ('FW', 'Huanggang'),
    ('FE', 'Huangnan'),
    ('FT', 'Huangshan'),
    ('FY', 'Huangshi'),
    ('FU', 'Huizhou'),
    ('FI', 'Huludao'),
    ('FO', 'Hulunbuir'),
    ('FP', 'Huzhou'),
    ('PF', 'Ili'),
    ('OF', 'Ili Kazakh'),
    ('IF', 'Jian'),
    ('UF', 'Jiamusi'),
    ('YF', 'Jiangmen'),
    ('TF', 'Jiaozuo'),
    ('RF', 'Jiaxing'),
    ('EF', 'Jiayuguan'),
    ('WF', 'Jieyang'),
    ('QF', 'Jilin'),
    ('AV', 'Jinan'),
    ('SV', 'Jinchang'),
    ('DV', 'Jincheng'),
    ('FV', 'Jingdezhen'),
    ('GV', 'Jingmen'),
    ('HB', 'Jingzhou'),
    ('HV', 'Jinhua'),
    ('JV', 'Jining'),
    ('KV', 'Jinzhong'),
    ('LV', 'Jinzhou'),
    ('VL', 'Jiujiang'),
    ('VK', 'Jiuquan'),
    ('VJ', 'Jixi'),
    ('VH', 'Jiyuan'),
    ('VF', 'Kaifeng'),
    ('VD', 'Karamay'),
    ('VS', 'Kashgar'),
    ('VA', 'Khotan'),
    ('Z', 'Kizilsu'),
    ('X', 'Kunming'),
    ('C', 'Laibin'),
    ('V', 'Laiwu'),
    ('B', 'Langfang'),
    ('N', 'Lanzhou'),
    ('M', 'Leshan'),
    ('CQ', 'Lhasa'),
    ('CW', 'Liangshan'),
    ('CE', 'Lianyungang'),
    ('CR', 'Liaocheng'),
    ('CT', 'Liaoyang'),
    ('CY', 'Liaoyuan'),
    ('CU', 'Lijiang'),
    ('CI', 'Lincang'),
    ('CO', 'Linfen'),
    ('CP', 'Linxia'),
    ('CA', 'Linyi'),
    ('CS', 'Lishui'),
    ('CD', 'Liupanshui'),
    ('CF', 'Liuzhou'),
    ('CH', 'Longnan'),
    ('CJ', 'Longyan'),
    ('CK', 'Loudi'),
    ('CL', 'Luan'),
    ('XA', 'Lüliang'),
    ('XS', 'Luohe'),
    ('DX', 'Luoyang'),
    ('XD', 'Luzhou'),
    ('XF', 'Maanshan'),
    ('XG', 'Macau'),
    ('XH', 'Maoming'),
    ('XJ', 'Meishan'),
    ('XK', 'Meizhou'),
    ('XL', 'Mianyang'),
    ('XM', 'Mudanjiang'),
    ('XN', 'Nagchu'),
    ('XB', 'Nanchang'),
    ('XV', 'Nanchong'),
    ('XC', 'Nanjing'),
    ('XX', 'Nanning'),
    ('XZ', 'Nanping'),
    ('QQ', 'Nantong'),
    ('WW', 'Nanyang'),
    ('EE', 'Nanyang'),
    ('RR', 'Neijiang'),
    ('TT', 'Ngari'),
    ('YY', 'Ningbo'),
    ('UU', 'Ningde'),
    ('II', 'Nujiang'),
    ('OO', 'Nyingchi'),
    ('PP', 'Ordos'),
    ('AA', 'Panjin'),
    ('SS', 'Panzhihua'),
    ('DD', 'Pingdingshan'),
    ('FF', 'Pingliang'),
    ('GG', 'Pingxiang'),
    ('HH', 'Puer'),
    ('JJ', 'Putian'),
    ('KK', 'Puyang'),
    ('LL', 'Qiandongnan'),
    ('qjg', 'Qianjiang'),
    ('CC', 'Qiannan'),
    ('VV', 'Qianxinan'),
    ('BB', 'Qingdao'),
    ('NN', 'Qingyang'),
    ('MM', 'Qingyuan'),
    ('AW', 'Qinhuangdao'),
    ('AE', 'Qinzhou'),
    ('AR', 'Qiqihar'),
    ('AT', 'Qitaihe'),
    ('AY', 'Quanzhou'),
    ('AU', 'Qujing'),
    ('AI', 'Quzhou'),
    ('AO', 'Rizhao'),
    ('AP', 'Sanmenxia'),
    ('WA', 'Sanming'),
    ('EA', 'Sanya'),
    ('RA', 'Shanghai'),
    ('TA', 'Shangluo'),
    ('YAA', 'Shangqiu'),
    ('UA', 'Shangrao'),
    ('IA', 'Shannan'),
    ('OA', 'Shantou'),
    ('PA', 'Shanwei'),
    ('BA', 'Shaoguan'),
    ('NA', 'Shaoxing'),
    ('MA', 'Shaoyang'),
    ('SQ', 'Shennongjia'),
    ('SWW', 'Shenyang'),
    ('SE', 'Shenzhen'),
    ('SR', 'Shijiazhuang'),
    ('ST', 'Shiyan'),
    ('SY', 'Shizuishan'),
    ('SU', 'Shuangyashan'),
    ('SI', 'Shuozhou'),
    ('SO', 'Siping'),
    ('SP', 'Songyuan'),
    ('SA', 'Suihua'),
    ('SD', 'Suining'),
    ('SF', 'Suizhou'),
    ('SG', 'Suqian'),
    ('SH', 'Suzhou'),
    ('SJ', 'Suzhou Anhui'),
    ('SK', 'Taian'),
    ('SL', 'Taiyuan'),
    ('xp', 'Taizhou'),
    ('SXX', 'Taizhou Zhejiang'),
    ('SCS', 'Tangshan'),
    ('SVS', 'Tianjin'),
    ('SB', 'Tianmen'),
    ('SN', 'Tianshui'),
    ('SSM', 'Tieling'),
    ('SM', 'Tongchuan'),
    ('QAZ', 'Tonghua'),
    ('WSX', 'Tongliao'),
    ('EDC', 'Tongling'),
    ('RFV', 'Tongren'),
    ('TGB', 'Turfan'),
    ('YHN', 'Ulanqab'),
    ('UJM', 'Ürümqi'),
    ('IKM', 'Weifang'),
    ('OLM', 'Weihai'),
    ('PLM', 'Wenzhou'),
    ('PKM', 'Wuhai'),
    ('POM', 'Wuhan'),
    ('OKM', 'Wuhu'),
    ('IKM', 'Wuwei'),
    ('PJM', 'Wuxi'),
    ('MLP', 'Wuzhong'),
    ('MLO', 'Wuzhou'),
    ('MKI', 'Xian'),
    ('MJU', 'Xiamen'),
    ('NHY', 'Xiangtan'),
    ('BGT', 'Xiangxi'),
    ('VFR', 'Xiangyang'),
    ('CDE', 'Xianning'),
    ('XSW', 'Xiantao'),
    ('ZAQ', 'Xianyang'),
    ('AQZ', 'Xiaogan'),
    ('SWX', 'Xigazê'),
    ('DEC', 'Xilin Gol'),
    ('FRV', 'Xingtai'),
    ('GTB', 'Xining'),
    ('HHYN', 'Xinxiang'),
    ('JUM', 'Xinyang'),
    ('KIM', 'Xinyu'),
    ('KOM', 'Xinzhou'),
    ('KPM', 'Xishuangbanna'),
    ('LPM', 'Xuancheng'),
    ('AOM', 'Xuchang'),
    ('ASZ', 'Xuzhou'),
    ('SDX', 'Yaan'),
    ('DFC', 'Yanan'),
    ('FGV', 'Yanbian'),
    ('GHB', 'Yancheng'),
    ('HJN', 'Yangjiang'),
    ('JKM', 'Yangquan'),
    ('KLM', 'Yangzhou'),
    ('QWA', 'Yantai'),
    ('WES', 'Yibin'),
    ('ERD', 'Yichang'),
    ('FGF', 'Yichun'),
    ('RTF', 'Yichun Heilongjiang'),
    ('RTG', 'Yinchuan'),
    ('TYG', 'Yingkou'),
    ('YUH', 'Yingtan'),
    ('UIJ', 'Yiyang'),
    ('UIK', 'Yongzhou'),
    ('IOK', 'Yueyang'),
    ('OPL', 'Yulin'),
    ('LOK', 'Yulin Shaanxi'),
    ('KIJ', 'Yuncheng'),
    ('JUH', 'Yunfu'),
    ('HYG', 'Yushu'),
    ('GTF', 'Yuxi'),
    ('FRD', 'Zaozhuang'),
    ('DES', 'Zhangjiajie'),
    ('SWA', 'Zhangjiakou'),
    ('AZS', 'Zhangye'),
    ('SXD', 'Zhangzhou'),
    ('DCF', 'Zhanjiang'),
    ('FVG', 'Zhaoqing'),
    ('GBH', 'Zhaotong'),
    ('HNJ', 'Zhengzhou'),
    ('JMK', 'Zhenjiang'),
    ('KKL', 'Zhongshan'),
    ('LLP', 'Zhongwei'),
    ('QWE', 'Zhoukou'),
    ('WER', 'Zhoushan'),
    ('ERT', 'Zhuhai'),
    ('RTY', 'Zhumadian'),
    ('TYU', 'Zhuzhou'),
    ('UII', 'Zibo'),
    ('III', 'Zigong'),
    ('OPJ', 'Ziyang'),
    ('Z', 'Zunyi'),
)

class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = models.CharField(_("Full name"), blank=True, max_length=255)
    picture = models.ImageField(
        _('Profile picture'), upload_to='profile_pics/', null=True, blank=True)
    job_title = models.CharField(
        _('Job title'), max_length=50, null=True, blank=True)
    personal_url = models.URLField(
        _('Personal URL'), max_length=555, blank=True, null=True)
    facebook_account = models.URLField(
        _('Facebook profile'), max_length=255, blank=True, null=True)
    instagram_account = models.URLField(
        _('Instagram account'), max_length=255, blank=True, null=True)
    linkedin_account = models.URLField(
        _('LinkedIn profile'), max_length=255, blank=True, null=True)
    short_bio = models.CharField(
        _('Describe yourself'), max_length=60, blank=True, null=True)
    bio = models.CharField(
        _('Short bio'), max_length=280, blank=True, null=True)
    country = models.CharField(
        _('Country'), max_length=100, default="China")
    province_region = models.CharField (_('Province/Region'), max_length=100, choices=PROVINCE_CHOICES)
    city = models.CharField  (  _('City'), max_length=100, choices=CITY_CHOICES) 
    points = models.IntegerField(  _('Points'), default=0)
    nationality = models.CharField (_('Nationality'), max_length=100, blank=True, null=True )
    phone_number = PhoneNumberField (_('Phone number'), default="Unknown_phone_no")  #Needs a country's code 
    is_official = models.BooleanField (default=False)      #For the use of published posts
    is_seller = models.BooleanField (default=False)  #For sellers in Classifieds.
    # near future please add unique 12 digit ID to use instead of username for url's especially in chat.
    #https://stackoverflow.com/questions/42703059/how-to-create-a-8-digit-unique-id-in-python

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_profile_name(self):
        if self.name:
            return self.name

        return self.username


def broadcast_login(sender, user, request, **kwargs):
    """Handler to be fired up upon user login signal to notify all users."""
    notification_handler(user, "global", Notification.LOGGED_IN)


def broadcast_logout(sender, user, request, **kwargs):
    """Handler to be fired up upon user logout signal to notify all users."""
    notification_handler(user, "global", Notification.LOGGED_OUT)


# user_logged_in.connect(broadcast_login)
# user_logged_out.connect(broadcast_logout)
