$( document ).ready(function() {
  $('.dropdown').dropdown();


  $('.ui.form')
	.form({
	  fields: {
		cid: {
		  identifier: 'cid',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入8位數統一編號'
		  }
		  ]
		},
		name : {
		  identifier: 'name',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入公司名稱'
		  }
		  ]
		},
		shortname: {
		  identifier: 'shortname',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入公司簡稱'
		  }
		  ]
		},
		password1: {
		  identifier: 'password1',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入密碼'
		  }
		  ]
		},
		password2: {
		  identifier: 'password2',
		  rules: [
		  {
			type   : 'match[password1]',
			prompt : '兩次密碼不一致'
		  }
		  ]
		},
		category: {
		  identifier: 'category',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入公司主事業類別'
		  }
		  ]
		},
		postal_code: {
		  identifier: 'postal_code',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入郵遞區號'
		  }
		  ]
		},
		address: {
		  identifier: 'address',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入公司地址'
		  }
		  ]
		},
		website: {
		  identifier: 'website',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入公司官網網址'
		  },
		  {
			type   : 'url',
			prompt : '公司官網網址格式錯誤'
		  }
		  ]
		},
		hr_name: {
		  identifier: 'hr_name',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入人資姓名'
		  }
		  ]
		},
		hr_fax: {
		  identifier: 'hr_fax',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入人資傳真號碼'
		  }
		  ]
		},
		hr_mobile: {
		  identifier: 'hr_mobile',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入人資手機號碼'
		  }
		  ]
		},
		hr_phone: {
		  identifier: 'hr_phone',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入人資電話號碼'
		  }
		  ]
		},
		hr_email: {
		  identifier: 'hr_email',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入人資Email'
		  },
		  {
			type   : 'email',
			prompt : '請輸入正確的人資Email'
		  }
		  ]
		},
		brief: {
		  identifier: 'brief',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入企業簡介'
		  }
		  ]
		},
		introduction: {
		  identifier: 'introduction',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入企業介紹'
		  }
		  ]
		},
	  }
	}) ;

});
