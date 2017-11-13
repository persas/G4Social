// JavaScript Document
var valor = 0;
$(document).ready(function() {
	$("#marcador").html("<h2>Tu primer reto: 0 €</h2>");
	function moveSlider(e){
		var pos = $(e.currentTarget).offset();
		var posX = e.pageX - pos.left;
		valor = Math.round(posX/2);
		
		if(posX >= 0 && posX <= $(e.currentTarget).outerWidth()){
			$("#slider #progress").css("width", posX+"px");
			$("#slider #indicator").css("left", posX+"px");
			$("#marcador").html("<h2>Tu primer reto: "+valor+" €</h2>");
			
		}	
	}

	
	$("#slider").on("mousedown",function(e){					
		moveSlider(e);
		$(this).on("mousemove",function(e){
			moveSlider(e);
		});
	}).on("mouseup",function(){
		$(this).off("mousemove");
	});
	
});
function ponerValor(){
	alert(valor);	
}