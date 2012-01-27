$(function(){
	$("#accordion").accordion({collapsible: true, autoHeight:false});
	$('dt').css('font-size', '14px');
    var mostrar = true;
	$('.borde').each(function(){
		$(this).find('dd').hide().end().find('dt').click(function(){
			$(this).next().slideToggle();
		});
		$(this).addClass('ui-corner-all').css({"border": "1px solid grey",
											   "padding": "5px"});
		$(this).find('.details').addClass('ui-corner-all').css({"border": "1px solid grey",
			   "padding": "5px", "margin-bottom": '10px'});
	});
	$('.manage a').button();
});