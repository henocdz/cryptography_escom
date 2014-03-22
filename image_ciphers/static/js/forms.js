$(function(){
	$('.opmodes-sub').on('click', function(e){
		e.preventDefault();
		var $elf = $(this);
		var _type = $elf.data('type');
		var form  = $('#opmodes-form');
		if( _type === 'decrypt'){
			alert('Mostar tipos');
		}else{
			form.attr('action', $elf.data('action'))
			form.submit();
		}

	})
})