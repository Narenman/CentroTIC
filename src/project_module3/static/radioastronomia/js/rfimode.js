function openMode(evt, modeName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(modeName).style.display = "block";
    evt.currentTarget.className += " active";
  }




var nnfft_fs = {};
nnfft_fs['1024'] = [250000, 500000, 1000000, 2000000, 4000000, 8000000, 16000000];
nnfft_fs['2048'] = [250000, 500000, 1000000, 2000000, 4000000, 8000000, 16000000];


function torbw(){
  nfft_fs = {};
  nfft_fs['1024']=[];
  nfft_fs['2048']=[];

  for(var i=1; i<nnfft_fs['1024'].length; i++){
    // nfft_fs['2048'][i] = Math.floor(nnfft_fs['2048'][i]*(1/2048));
    // nfft_fs['1024'][i] = Math.floor(nnfft_fs['2048'][i]*(1/1024));

    nfft_fs['2048'][i] = nnfft_fs['2048'][i]*(1/2048);
    nfft_fs['1024'][i] = nnfft_fs['2048'][i]*(1/1024);
  }
    
}
torbw();

function rbwlist(){

      var nfftlist = document.getElementById('nFFT_LIST');
      var rbwlist  = document.getElementById('RBW_LIST');
      var selnfft  = nfftlist.options[nfftlist.selectedIndex].value;
    
      while(rbwlist.options.length){
        rbwlist.remove(0);
      }
      var nffts = nfft_fs[selnfft];
      
      if (nffts){
        var j;
        for(j = 0; j<nffts.length; j++){
            var rbw = new Option(nffts[j], nffts[j]);
            rbwlist.options.add(rbw);
        }
        rbwlist.options.remove(0);
    }

}

function rbwlistM(){

  var nfftlist = document.getElementById('nFFT_LIST_M');
  var rbwlist  = document.getElementById('RBW_LIST_M');
  var selnfft  = nfftlist.options[nfftlist.selectedIndex].value;

  while(rbwlist.options.length){
    rbwlist.remove(0);
  }
  var nffts = nfft_fs[selnfft];
  
  if (nffts){
    var j;
    for(j = 0; j<nffts.length; j++){
        var rbw = new Option(nffts[j], nffts[j]);
        rbwlist.options.add(rbw);
    }
    rbwlist.options.remove(0);
}

}

formobjectA = document.getElementById('Af');

formobjectA.addEventListener('submit', function(event){
  event.preventDefault();
  
  f1 = document.getElementsByName('finicial')[0].value;
  f2 = document.getElementsByName('ffinal')[0].value;
  console.log(f1, f2)

  if(f2-f1<0){
    window.alert("Rango de frecuencia inconsistente");
  }
  else
  {
    var Af = new FormData(document.getElementById('Af'));
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "control-automatico", true); 
  
    xhr.send(Af);
    
  }


})

formobject = document.getElementById('Mf');

formobject.addEventListener('submit', function(event){
  event.preventDefault();
  var Mf = new FormData(document.getElementById('Mf'));
  var Mxhr = new XMLHttpRequest();
  Mxhr.open("POST", "control-manual", true);
  Mxhr.send(Mf);


})
