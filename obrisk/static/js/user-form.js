function sortList(id) 
{ 
		var lb = document.getElementById(id); 
		arrTexts = new Array(); 
		arrValues = new Array(); 
		arrOldTexts = new Array(); 

		for(i=0; i<lb.length; i++) 
		{ 
				arrTexts[i] = lb.options[i].text; 
				arrValues[i] = lb.options[i].value; 
				arrOldTexts[i] = lb.options[i].text; 
		} 

		arrTexts.sort(); 

		for(i=0; i<lb.length; i++) 
		{ 
				lb.options[i].text = arrTexts[i]; 
				for(j=0; j<lb.length; j++) 
				{ 
						if (arrTexts[i] == arrOldTexts[j]) 
						{ 
								lb.options[i].value = arrValues[j]; 
								j = lb.length; 
						} 
				} 
		} 
}

var helpers =
{
    province: function(result, dropdown, emptyMessage)
    {
        // Remove current options
        dropdown.html('');
        // Add the empty option with the empty message
        dropdown.append('<option value="">' + emptyMessage + '</option>');
        // Check result isnt empty
        if(result != '')
        {
            // Loop through each of the results and append the option to the dropdown
            $.each(result, function(k, v) {
                dropdown.append('<option value="' + v.name+ '">' + v.name + '</option>');
            });
        }
				
				
    },
		city: function(result, dropdown, emptyMessage)
    {
        // Remove current options
        dropdown.html('');
        // Add the empty option with the empty message
        dropdown.append('<option value="">' + emptyMessage + '</option>');
        // Check result isnt empty
        if(result != '')
        {
            // Loop through each of the results and append the option to the dropdown
            $.each(result, function(index, text) {
                dropdown.append('<option value="' + text + '">' + text + '</option>');
            });
        }
    }

}

const geo_data = [{"name":"Beijing","cities":["Beijing"]},{"name":"Tianjin","cities":["Tianjin"]},{"name":"Hebei","cities":["Zhangjiakou","Chengde","Baoding","Chuzhou","Hengshui","Shijiazhuang","Xingtai","Handan","Tangshan","Langfang","Qinhuangdao"]},{"name":"Shanxi","cities":["Taiyuan","Datong","Yangquan","Changzhi","Jincheng","Chuzhou","Jinzhong","Yuncheng","Chuzhou","Linyi","Lvliang"]},{"name":"Inner Mongolia","cities":["Hohhot","Hulunbeier","Xing'an","Tongliao","Chifeng","Xilinguol","Ulanchabu","Baotou","Ordos","Bayanmuer","U Sea","Alashan"]},
{"name":"Liaoning","cities":["Shenyang","Dalian","Anshan","Fushun","Benxi","Dandong","Jinzhou","Yingkou","Fuxin","Liaoyang","Panjin","Tieling","Chaoyang","Huludao"]},{"name":"Jilin","cities":["Changchun","Jilin","Siping","Tonghua","White Mountain","Liaoyuan","White City","Songyuan","Yanbian Korean Autonomous Prefecture"]},{"name":"Heilongjiang","cities":["Harbin","Qiqihar","Mudanjiang","Jiamusi","Daqing","Chixi","Shuangyashan","Yichun","Qitaihe","Hegang","Black River","Suihua","Daxinganling area"]},
{"name":"Shanghai","cities":["Shanghai"]},{"name":"Jiangsu","cities":["Nanjing","Wuxi","Xuzhou","Changzhou","Suzhou","Nantong","Lianyungang","Huai'an","Yancheng","Yangzhou","Zhenjiang","Taizhou","Suqian"]},{"name":"Zhejiang","cities":["Hangzhou","Huzhou","Shaoxing","Wenzhou","Jiaxing","Ningbo","Jinhua","Zhangzhou","Zhoushan","Taizhou","Lishui"]},{"name":"Anhui","cities":["Hefei","Wuhu","Bengbu","Huainan","Maanshan","Huaibei","Tongling","Anqing","Huangshan","Yangyang","Suzhou","Chuzhou","Lu'an","Xuancheng","Chizhou","Chuzhou"]},
{"name":"Fujian","cities":["Fuzhou","Quanzhou","Sanming","Nanping","Longyan","Zhangzhou","Ningde","Putian","Xiamen"]},{"name":"Jiangxi","cities":["Nanchang","Jiujiang","Jian","Chuzhou","Pingxiang","Xinyu","Yichun","Jingdezhen","Shangrao","Yingtan","Fuzhou"]},{"name":"Shandong","cities":["Jinan","Tai'an","Weifang","Dezhou","Binzhou","Laiwu","Qingdao","Yantai","Rizhao","Dongying","Jining","Heze","Liaocheng","Linyi","Zaozhuang","Zibo","Weihai"]},
{"name":"Henan","cities":["Zhengzhou","Kaifeng","Luoyang","Nanyang","Yuhe","Xuchang","Sanmenxia","Pingdingshan","Zhoukou","Zhumadian","Xinxiang","Hebi","Jiao Zuo","Yangyang","Anyang","Shangqiu","Xinyang","Jiyuan"]},
{"name":"Hubei","cities":["Wuhan","Shiyan","Xiangfan","Suizhou","Jingmen","Xiaogan","Yichang","Huanggang","Ezhou","Jingzhou","Yellowstone","Xianning"]},{"name":"Hunan","cities":["Changsha","Zhuzhou","Xiangtan","Hengyang","Shaoyang","Yueyang","Zhangjiajie","Yiyang","Changde","Loudi","Chenzhou","Yongzhou","Huaihua","Xiangxi Tujia and Miao Autonomous Prefecture"]},
{"name":"Guangdong","cities":["Guangzhou","Shenzhen","Zhuhai","Dongguan","Foshan","Zhongshan","Huizhou","Shantou","Jiangmen","Maoming","Zhaoqing","Zhanjiang","Meizhou","Iris","Heyuan","Qingyuan","Shaoguan","Jieyang","Yangjiang","Chaozhou","Yunfu"]},{"name":"Guangxi","cities":["Nanning","Guilin","Liuzhou","Chuzhou","Qinzhou","Beihai","Yulin","Guigang","Fangchenggang","Baise","Chongzuo","Guest ","Hezhou","Hechi"]},{"name":"Hainan","cities":["Haikou","Sanya","Qionghai","Chuzhou"]},
{"name":"Chongqing","cities":["Chongqing"]},{"name":"Sichuan","cities":["Chengdu","Zigong","Panzhihua","Chuzhou","Deyang","Mianyang","Guangyuan","Suining","Neijiang","Ziyang","Leshan","Meishan","Nan Chong","Yibin","Guangan","Dazhou","Bazhong","Ya'an","Ganzi Tibetan Autonomous Prefecture","Aba Tibetan and Qiang Autonomous Prefecture","Liangshan Yi Autonomous Prefecture"]},
{"name":"Guizhou","cities":["Guiyang","Zunyi","Anshun","Six Panshui","Duyun","Kerry","Tongren","Bijie","Xingyi","Chishui","Ren Huai","Qingzhen","Fuquan"]},{"name":"Yunnan","cities":["Kunming","Yuxi","Qujing","Pu'er","Baoshan","Lijiang","Linyi","Zhaotong"]},
{"name":"Tibet","cities":["Lhasa","Nagqu area","Changdu area","Nyingchi area","Shannam area","Shigatse area","Ali area"]},{"name":"Shaanxi","cities":["Xi'an","Baoji","Xianyang","Southern","Tongchuan","Yan'an","Yulin","Hanzhong","Ankang","Shangluo"]},{"name":"Gansu","cities":["Lanzhou","Jiayuguan", "Jinchang", "Wuwei", "Jiuquan", "Zhangye", "Baiyin", "Pingliang", "Qingyang", "Tianshui", "Longnan", " Dingxi","Linxia Autonomous Prefecture","Gannan Autonomous Prefecture"]},
{"name":"Qinghai","cities":["Xining","Haidong Area","Haixi Mongolian Tibetan Autonomous Prefecture","Hainan Tibetan Autonomous Prefecture","Haibei Tibetan Autonomous Prefecture","Huangnan Tibetan Autonomous Prefecture","Gaolu Tibetan Autonomous Prefecture","Yushu Tibetan Autonomous Prefecture"]},{"name":"Ningxia","cities":["Yinchuan","Shizuishan","Wu Zhong","Zhongwei","Guyuan"]},{"name":"Xinjiang","cities":["Urumqi","Karamai","Changji","Tulufan","Hami","Korla","Aksu","Atushi","Kash","Hetian","Yining","Kui Yu","Tacheng","Usu","Altay","Shihezi"]}
]



$(document).ready(function() {
		$province = $("select[name='province']");	
		$city = $("select[name='city']");
		helpers.province(geo_data,  $province, "Select an option");

		$province.change(function() {
				helpers.city(geo_data[$("#province").prop('selectedIndex')-1].cities ,  $city, "Select an option")
		});
		//sortList('province');
		
});


$(function () {
    $("#submit").click(function (event) {
		if (!$("select[name='city']").val() || !$("select[name='province']"))
		{
				event.preventDefault();
				alert("Please enter your address!");
		}
		else {
				$("input[name='city']").val( $("select[name='city']").val());
				$("input[name='province_region']").val($("select[name='province']").val());
				console.log("Shout out!");
				$("#signup_form").submit();
		}
    }); 
});
