var helpers = {
	province: function (result, dropdown, emptyMessage) {
		// Remove current options
		dropdown.html('');
		// Add the empty option with the empty message

		dropdown.append('<option value="">' + emptyMessage + '</option>');
		// Check result isnt empty
		if (result != '') {
			// Loop through each of the results and append the option to the dropdown
			$.each(result, function (k, v) {
				dropdown.append('<option value="' + v.name + '">' + v.name + '</option>');
			});
		}


	},

	city: function (result, dropdown, emptyMessage) {
		// Remove current options
		dropdown.html('');
		// Add the empty option with the empty message
		dropdown.append('<option value="">' + emptyMessage + '</option>');
		// Check result isnt empty
		if (result != '') {
			// Loop through each of the sorted results and append the option to the dropdown
			result = result.sort();
			$.each(result, function (index, text) {
				dropdown.append('<option value="' + text + '">' + text + '</option>');
			});
		}
	}

}

const geo_data = [{
	"name": "Anhui",
	"cities": ["Hefei", "Wuhu", "Bengbu", "Huainan", "Maanshan", "Huaibei", "Tongling", "Anqing", "Huangshan", "Yangyang", "Suzhou", "Chuzhou", "Lu'an", "Xuancheng", "Chizhou", "Chuzhou"]
}, {
	"name": "Beijing",
	"cities": ["Beijing"]
}, {
	"name": "Chongqing",
	"cities": ["Chongqing"]
}, {
	"name": "Fujian",
	"cities": ["Fuzhou", "Quanzhou", "Sanming", "Nanping", "Longyan", "Zhangzhou", "Ningde", "Putian", "Xiamen"]
}, {
	"name": "Gansu",
	"cities": ["Lanzhou", "Jiayuguan", "Jinchang", "Wuwei", "Jiuquan", "Zhangye", "Baiyin", "Pingliang", "Qingyang", "Tianshui", "Longnan", " Dingxi", "Linxia Autonomous Prefecture", "Gannan Autonomous Prefecture"]
}, {
	"name": "Guangdong",
	"cities": ["Guangzhou", "Shenzhen", "Zhuhai", "Dongguan", "Foshan", "Zhongshan", "Huizhou", "Shantou", "Jiangmen", "Maoming", "Zhaoqing", "Zhanjiang", "Meizhou", "Iris", "Heyuan", "Qingyuan", "Shaoguan", "Jieyang", "Yangjiang", "Chaozhou", "Yunfu"]
}, {
	"name": "Guangxi",
	"cities": ["Nanning", "Guilin", "Liuzhou", "Chuzhou", "Qinzhou", "Beihai", "Yulin", "Guigang", "Fangchenggang", "Baise", "Chongzuo", "Guest ", "Hezhou", "Hechi"]
}, {
	"name": "Guizhou",
	"cities": ["Guiyang", "Zunyi", "Anshun", "Six Panshui", "Duyun", "Kerry", "Tongren", "Bijie", "Xingyi", "Chishui", "Ren Huai", "Qingzhen", "Fuquan"]
}, {
	"name": "Hainan",
	"cities": ["Haikou", "Sanya", "Qionghai", "Chuzhou"]
}, {
	"name": "Hebei",
	"cities": ["Zhangjiakou", "Chengde", "Baoding", "Chuzhou", "Hengshui", "Shijiazhuang", "Xingtai", "Handan", "Tangshan", "Langfang", "Qinhuangdao"]
}, {
	"name": "Heilongjiang",
	"cities": ["Harbin", "Qiqihar", "Mudanjiang", "Jiamusi", "Daqing", "Chixi", "Shuangyashan", "Yichun", "Qitaihe", "Hegang", "Black River", "Suihua", "Daxinganling area"]
}, {
	"name": "Henan",
	"cities": ["Zhengzhou", "Kaifeng", "Luoyang", "Nanyang", "Yuhe", "Xuchang", "Sanmenxia", "Pingdingshan", "Zhoukou", "Zhumadian", "Xinxiang", "Hebi", "Jiao Zuo", "Yangyang", "Anyang", "Shangqiu", "Xinyang", "Jiyuan"]
}, {
	"name": "Hubei",
	"cities": ["Wuhan", "Shiyan", "Xiangfan", "Suizhou", "Jingmen", "Xiaogan", "Yichang", "Huanggang", "Ezhou", "Jingzhou", "Yellowstone", "Xianning"]
}, {
	"name": "Hunan",
	"cities": ["Changsha", "Zhuzhou", "Xiangtan", "Hengyang", "Shaoyang", "Yueyang", "Zhangjiajie", "Yiyang", "Changde", "Loudi", "Chenzhou", "Yongzhou", "Huaihua", "Xiangxi Tujia and Miao Autonomous Prefecture"]
}, {
	"name": "Inner Mongolia",
	"cities": ["Hohhot", "Hulunbeier", "Xing'an", "Tongliao", "Chifeng", "Xilinguol", "Ulanchabu", "Baotou", "Ordos", "Bayanmuer", "U Sea", "Alashan"]
}, {
	"name": "Jiangsu",
	"cities": ["Nanjing", "Wuxi", "Xuzhou", "Changzhou", "Suzhou", "Nantong", "Lianyungang", "Huai'an", "Yancheng", "Yangzhou", "Zhenjiang", "Taizhou", "Suqian"]
}, {
	"name": "Jiangxi",
	"cities": ["Nanchang", "Jiujiang", "Jian", "Chuzhou", "Pingxiang", "Xinyu", "Yichun", "Jingdezhen", "Shangrao", "Yingtan", "Fuzhou"]
}, {
	"name": "Jilin",
	"cities": ["Changchun", "Jilin", "Siping", "Tonghua", "White Mountain", "Liaoyuan", "White City", "Songyuan", "Yanbian Korean Autonomous Prefecture"]
}, {
	"name": "Liaoning",
	"cities": ["Shenyang", "Dalian", "Anshan", "Fushun", "Benxi", "Dandong", "Jinzhou", "Yingkou", "Fuxin", "Liaoyang", "Panjin", "Tieling", "Chaoyang", "Huludao"]
}, {
	"name": "Ningxia",
	"cities": ["Yinchuan", "Shizuishan", "Wu Zhong", "Zhongwei", "Guyuan"]
}, {
	"name": "Qinghai",
	"cities": ["Xining", "Haidong Area", "Haixi Mongolian Tibetan Autonomous Prefecture", "Hainan Tibetan Autonomous Prefecture", "Haibei Tibetan Autonomous Prefecture", "Huangnan Tibetan Autonomous Prefecture", "Gaolu Tibetan Autonomous Prefecture", "Yushu Tibetan Autonomous Prefecture"]
}, {
	"name": "Shaanxi",
	"cities": ["Xi'an", "Baoji", "Xianyang", "Southern", "Tongchuan", "Yan'an", "Yulin", "Hanzhong", "Ankang", "Shangluo"]
}, {
	"name": "Shandong",
	"cities": ["Jinan", "Tai'an", "Weifang", "Dezhou", "Binzhou", "Laiwu", "Qingdao", "Yantai", "Rizhao", "Dongying", "Jining", "Heze", "Liaocheng", "Linyi", "Zaozhuang", "Zibo", "Weihai"]
}, {
	"name": "Shanghai",
	"cities": ["Shanghai"]
}, {
	"name": "Shanxi",
	"cities": ["Taiyuan", "Datong", "Yangquan", "Changzhi", "Jincheng", "Chuzhou", "Jinzhong", "Yuncheng", "Chuzhou", "Linyi", "Lvliang"]
}, {
	"name": "Sichuan",
	"cities": ["Chengdu", "Zigong", "Panzhihua", "Chuzhou", "Deyang", "Mianyang", "Guangyuan", "Suining", "Neijiang", "Ziyang", "Leshan", "Meishan", "Nan Chong", "Yibin", "Guangan", "Dazhou", "Bazhong", "Ya'an", "Ganzi Tibetan Autonomous Prefecture", "Aba Tibetan and Qiang Autonomous Prefecture", "Liangshan Yi Autonomous Prefecture"]
}, {
	"name": "Tianjin",
	"cities": ["Tianjin"]
}, {
	"name": "Tibet",
	"cities": ["Lhasa", "Nagqu area", "Changdu area", "Nyingchi area", "Shannam area", "Shigatse area", "Ali area"]
}, {
	"name": "Xinjiang",
	"cities": ["Urumqi", "Karamai", "Changji", "Tulufan", "Hami", "Korla", "Aksu", "Atushi", "Kash", "Hetian", "Yining", "Kui Yu", "Tacheng", "Usu", "Altay", "Shihezi"]
}, {
	"name": "Yunnan",
	"cities": ["Kunming", "Yuxi", "Qujing", "Pu'er", "Baoshan", "Lijiang", "Linyi", "Zhaotong"]
}, {
	"name": "Zhejiang",
	"cities": ["Hangzhou", "Huzhou", "Jiaxing", "Jinhua", "Lishui", "Ningbo", "Shaoxing", "Taizhou", "Wenzhou", "Zhangzhou", "Zhoushan"]
}]



document.addEventListener('DOMContentLoaded', function () {

    //Set the Province and city name defaults.
	function preselect() {
		if ( in_china ) {
            if (!document.getElementById('city').value && 
                !document.getElementById('province').value) {
                    $(`#province option[value=${province}]`).attr('selected', 'selected');
                    helpers.city(geo_data[$("#province").prop('selectedIndex') - 1].cities, $city, "Select an option")
                    $(`#city option[value=${city}]`).attr('selected', 'selected');
            }
		} else {
			province = "#province option[value=" + $("input[name='province_region']").val() + "]";
			city = "#city option[value=" + $("input[name='city']").val() + "]";
			$(province).attr('selected', 'selected');
            if (document.getElementById("province").value == '') {
                helpers.city('', $city, "Select an option");
            } else {
                helpers.city(geo_data[document.getElementById("province").selectedIndex - 1].cities, $city, "Select an option");
            }
			$(city).attr('selected', 'selected');
		}
	}
    
	$province = $("select[name='province_region']");
	$city = $("select[name='city']");

	helpers.province(geo_data, $province, "Select an option");
	preselect();
	$province.change(function () {
		helpers.city(geo_data[$("#province").prop('selectedIndex') - 1].cities, $city, "Select an option")
	});
});
