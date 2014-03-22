$(function(){


	function sendForm(btn, form){
		var loader = btn.children('.loader');
		$.ajax({
			beforeSend: function(){
				loader.text('\\/')
			},
			url: btn.data('action'),
			type: 'POST',
			data: new FormData(form),
	        cache: false,
	        contentType: false,
	        processData: false,
	        dataType: 'json',
			success: function(res){
				console.log(res.code);
			},
			error: function(errs){
				console.log('Error en comunicación con el servidor');
			},
			complete: function(jqxhr, txt){
				loader.text('');
				$('.img-sd').text('No se ha selecc...')
				form.reset()
			}
		})
	}

	$('.opmodes-sub').on('click', function(e){
		e.preventDefault();
		var $elf = $(this);
		var _type = $elf.data('type');
		var form  = $('#opmodes-form');
		if( _type === 'decrypt'){
			alert('Mostar tipos');
		}else{
			form.attr('action', $elf.data('action'))
			form.submit()
			//sendForm($elf, form[0])
		}

	})

	$('.file_cvr').on('click', function(e){
		e.preventDefault();
		$elf = $(this);
		file_input = $($elf.data('input'))

		file_input.click()
		file_input.on('change', function(){
			$('.img-sd').text('Archivo: '+$(this).val().replace('C:\\fakepath','.../'))
		})
	})
})