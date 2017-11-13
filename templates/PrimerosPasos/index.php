<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>My Saver - Gestiona tu dinero de manera fácil</title>
	<!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="../css/bootstrap.css">
    <link rel="stylesheet" href="../css/style-index.css">
    <link rel="stylesheet" href="css/style-Primeros-Pasos.css" />
    <script src="../js/jquery-3.2.1.min.js"></script>
    <script>
    	$(document).ready(function() {
			$("#marcador").html("<h2>Tu primer reto: 0 €</h2>");
			function moveSlider(e){
				var pos = $(e.currentTarget).offset();
				var posX = e.pageX - pos.left;
				var valor = Math.round(posX/2);
				
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
    </script>
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light">
      <a class="navbar-brand ml-5" href="#"><img src="../img/logo-banner-index.png" /></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse justify-content-end mr-5" id="navbarSupportedContent">
        <!-- <button type="button" class="btn btn-dark">Bienvenido Jose Carlos<img src="../img/flecha-abajo.png" class="ml-3" /></button> -->
        <nav class="navbar navbar-expand-lg ">
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
        
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
              <li class="nav-item dropdown" style="border:1px solid #000; border-radius:10px;">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <b> <?php echo($_COOKIE['nombre']);?></b>
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                  <a class="dropdown-item" href="#">Mi cuenta</a>
                  <a class="dropdown-item" href="#">Yo</a>
                  <div class="dropdown-divider"></div>
                  <a class="dropdown-item" href="#">Cerrar sesión</a>
                </div>
              </li>
            </ul>
          </div>
        </nav><!-- Cierre del Nav -->
      </div>
    </nav>
    <div id="content" class="container">
    	<form id="primerospasos" method="post" action="">
        	<div id="paso1" class="container pt-3" style="border:1px solid #000;">
            	<h1 class="mb-5">Te proponemos un juego, marca cual va a<br /> ser tu primer objetivo de ahorro y <br />nosotros
					nos encargamos del resto.</h1>
                <div id="marcador"></div>
                <div id="slider" class="mb-5">
                    <div id="progress"></div>
                    <div id="indicator"></div>
                </div>
                <div id="progreso" class="container justify-content-end mt-5">
                	<p>Paso 1 de 2 <button type="button" class="btn btn-outline-dark ml-3">Dark</button></p>
                </div>
            </div>
            
            
        </form>
        
    </div>

	<!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
    <script src="../js/bootstrap.js"></script>
</body>
</html>