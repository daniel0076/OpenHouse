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
		phone: {
		  identifier: 'phone',
		  rules: [
		  {
			type   : 'regExp[/^0[0-9]-[0-9]*(#[0-9]+)?$/]',
			prompt : '公司電話格式錯誤'
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
		cid: {
		  identifier: 'cid',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入8位數統一編號'
		  }
		  ]
		},
		cid: {
		  identifier: 'cid',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入8位數統一編號'
		  }
		  ]
		},
		cid: {
		  identifier: 'cid',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入8位數統一編號'
		  }
		  ]
		},
		cid: {
		  identifier: 'cid',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入8位數統一編號'
		  }
		  ]
		},
		cid: {
		  identifier: 'cid',
		  rules: [
		  {
			type   : 'empty',
			prompt : '請輸入8位數統一編號'
		  }
		  ]
		},
	  }
	}) ;

});
