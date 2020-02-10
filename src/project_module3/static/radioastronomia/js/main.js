function datev(thetime){
	if (thetime<10) {
		return '0'+ thetime;
	}
	else{return thetime}
}

var elementohora = document.getElementById('serverhour')

function mydatetime(){
    var v_horalocal = document.getElementById('v_horalocal');
    var today = new Date();
  
    elementohora.innerHTML = datev(today.getHours()) +':'+ datev(today.getMinutes())+':'+datev(today.getSeconds());

  
    // return datev(today.getHours()) +':'+ datev(today.getMinutes())+':'+datev(today.getSeconds());

    setTimeout(mydatetime, 1000);
  }
  

  mydatetime(); 

  