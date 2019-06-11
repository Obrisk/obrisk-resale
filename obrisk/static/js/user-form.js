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

$(document).ready(function () {
	function preselect() {
		if (!$("input[name='city']").val() && !$("input[name='province_region']").val()) {
			$("#province option[value='Zhejiang']").attr('selected', 'selected');
			helpers.city(geo_data[$("#province").prop('selectedIndex') - 1].cities, $city, "Select an option")
			$("#city option[value='Hangzhou']").attr('selected', 'selected');
		} else {
			province = "#province option[value=" + $("input[name='province_region']").val() + "]";
			city = "#city option[value=" + $("input[name = 'city']").val() + "]";
			$(province).attr('selected', 'selected');
			helpers.city(geo_data[$("#province").prop('selectedIndex') - 1].cities, $city, "Select an option")
			$(city).attr('selected', 'selected');
		}

	}
	$province = $("select[name='province']");
	$city = $("select[name='city']");
	helpers.province(geo_data, $province, "Select an option");
	preselect();
	$province.change(function () {
		helpers.city(geo_data[$("#province").prop('selectedIndex') - 1].cities, $city, "Select an option")
	});

});


$(function () {
	$("#submit").click(function (event) {
		if (!$("select[name='city']").val() || !$("select[name='province']")) {
			event.preventDefault();
			bootbox.alert("Please enter your address!");
		} else {
			$("input[name='city']").val($("select[name='city']").val());
			$("input[name='province_region']").val($("select[name='province']").val());
			$("#signup_form").submit();
		}
	});

	$(".update").click(function () {
		$("input[name='city']").val($("select[name='city']").val());
		$("input[name='province_region']").val($("select[name='province']").val());
		$("#update").submit();
	});
});


"use strict";
var iqwerty = iqwerty || {};
iqwerty.toast = (function () {
	function Toast() {
		var _duration = 3000;
		this.getDuration = function () {
			return _duration;
		};
		this.setDuration = function (time) {
			_duration = time;
			return this;
		};
		var _toastStage = null;
		this.getToastStage = function () {
			return _toastStage;
		};
		this.setToastStage = function (toastStage) {
			_toastStage = toastStage;
			return this;
		};
		var _text = null;
		this.getText = function () {
			return _text;
		};
		this.setText = function (text) {
			_text = text;
			return this;
		};
		var _textStage = null;
		this.getTextStage = function () {
			return _textStage;
		};
		this.setTextStage = function (textStage) {
			_textStage = textStage;
			return this;
		};
		this.stylized = false;
	};
	Toast.prototype.styleExists = false;
	Toast.prototype.initializeAnimations = function () {
		if (Toast.prototype.styleExists) return;
		var style = document.createElement("style");
		style.classList.add(iqwerty.toast.identifiers.CLASS_STYLESHEET);
		style.innerHTML = "." + iqwerty.toast.identifiers.CLASS_SLIDE_IN +
			"{opacity: 1; bottom: 10%;}" +
			"." + iqwerty.toast.identifiers.CLASS_SLIDE_OUT +
			"{opacity: 0; bottom: -10%;}" +
			"." + iqwerty.toast.identifiers.CLASS_ANIMATED +
			"{transition: opacity " + iqwerty.toast.style.TOAST_ANIMATION_SPEED + "ms, bottom " + iqwerty.toast.style.TOAST_ANIMATION_SPEED + "ms;}";
		document.head.appendChild(style);
		Toast.prototype.styleExists = true;
	};
	Toast.prototype.generate = function () {
		var toastStage = document.createElement("div");
		var textStage = document.createElement("span");
		textStage.innerHTML = this.getText();
		toastStage.appendChild(textStage);
		this.setToastStage(toastStage);
		this.setTextStage(textStage);
		this.initializeAnimations();
		return this;
	};
	Toast.prototype.show = function () {
		if (this.getToastStage() == null) {
			this.generate();
		}
		if (!this.stylized) {
			this.stylize();
		}
		var body = document.body;
		var before = body.firstChild;
		this.getToastStage().classList.add(iqwerty.toast.identifiers.CLASS_ANIMATED);
		this.getToastStage().classList.add(iqwerty.toast.identifiers.CLASS_SLIDE_OUT);
		body.insertBefore(this.getToastStage(), before);
		this.getToastStage().offsetHeight;
		this.getToastStage().classList.add(iqwerty.toast.identifiers.CLASS_SLIDE_IN);
		this.getToastStage().classList.remove(iqwerty.toast.identifiers.CLASS_SLIDE_OUT);
		setTimeout(this.hide.bind(this), this.getDuration());
		return this;
	};
	Toast.prototype.hide = function () {
		if (this.getToastStage() == null) return;
		this.getToastStage().classList.remove(iqwerty.toast.identifiers.CLASS_SLIDE_IN);
		this.getToastStage().classList.add(iqwerty.toast.identifiers.CLASS_SLIDE_OUT);
		setTimeout(function () {
			document.body.removeChild(this.getToastStage());
			this.setToastStage(null);
			this.setText(null);
			this.setTextStage(null);
		}.bind(this), iqwerty.toast.style.TOAST_ANIMATION_SPEED);
		return this;
	};
	Toast.prototype.stylize = function (style) {
		if (this.getToastStage() == null) {
			this.generate();
		}
		var toastStage = this.getToastStage();
		toastStage.setAttribute("style", iqwerty.toast.style.defaultStyle);
		if (arguments.length == 1) {
			var s = Object.keys(style);
			s.forEach(function (value, index, array) {
				toastStage.style[value] = style[value];
			});
		}
		this.stylized = true;
		return this;
	};
	return {
		Toast: Toast,
		style: {
			defaultStyle: "" +
				"background: rgba(0, 0, 0, .85);" +
				"box-shadow: 0 0 10px rgba(0, 0, 0, .8);" +
				"z-index: 99999;" +
				"border-radius: 3px;" +
				"color: rgba(255, 255, 255, .9);" +
				"padding: 10px 15px;" +
				"max-width: 40%;" +
				"word-break: keep-all;" +
				"margin: 0 auto;" +
				"text-align: center;" +
				"position: fixed;" +
				"left: 0;" +
				"right: 0;",
			TOAST_ANIMATION_SPEED: 400
		},
		identifiers: {
			CLASS_STYLESHEET: "iqwerty_toast_stylesheet",
			CLASS_ANIMATED: "iqwerty_toast_animated",
			CLASS_SLIDE_IN: "iqwerty_toast_slide_in",
			CLASS_SLIDE_OUT: "iqwerty_toast_slide_out"
		}
	};
})();

function uploadPreview(input) {
	console.log('clicked');
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			$('#avatar')
				.attr('src', e.target.result);
		};

		reader.readAsDataURL(input.files[0]);
	}
}