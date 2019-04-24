




function myswitch (){

	var tswitch = document.getElementById('checkbox').checked;
	var titletext = document.getElementById('text')

	
	if (tswitch == false) {
		document.body.style.background = "#22282d"
		titletext.style.color = "#0efbd3"
	}

	else
	{
		document.body.style.background = "#fff";
		document.body.color = "#000";
		titletext.style.color = "#000";
	}

}


function mydatetime(){
  var v_horalocal = document.getElementById('v_horalocal');
  var today = new Date();
  v_horalocal.innerHTML = today.getHours() +':'+ today.getMinutes()+':'+ today.getSeconds();
  setTimeout(mydatetime, 1000);

}


mydatetime();
