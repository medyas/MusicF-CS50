
$(document).ready(function() {
  $(document).on ("click", "#close", function () {
        var player = document.getElementById("a");
        player.pause();
        player.src = player.src;
  });
    $(document).on ("click", ".vid", function () {
         var link = $(this).find('a').attr('href');
        var vid = 'https://www.youtube.com/embed/';
        var title = $(this).find('h5').html();

        var src = "../static/uploads/" + title.replace(/ /g, "-") + ".mp3";
        id = link.substring(link.length-11);
        src = src.replace(/&amp;/g, '&');


        $('.modal-title').html(title);
        $('.modal-body iframe').attr('src', vid+id);
        $('.modal-body audio').attr('src', src);
        $('.modal-body .wrapper a').attr('href', src);
        $('.modal-body .wrapper a').attr('download', title+".mp3");

        $('.rm_vid').click(function() {
              $("#audio").modal("hide");
              $(".loding").modal('show');
                link="/remove/"+id;
                $.getJSON(link,function(data,status) {
                	  if (status == "success") {
                	    $("#dmsg").text(data['msg']);
                	  } else {
                	    // request failed
                	    $("#dmsg").text("Error, Could not get data!").css("color","red");
                	  }
                });
              $(".list").text("");
              videos();
              $(".loding").modal('hide');
        });

        /************************************/
        $('#audio').click(function(){
            var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            var myAudio = document.querySelector('audio');
            var source ;
            var gainNode = audioCtx.createGain();
            var voiceSelect = document.getElementById("voice");
            var visualSelect = document.getElementById("visual");

            var drawVisual; // requestAnimationFrame
            var c = document.getElementById("visualizer");
            var canvasCtx = c.getContext("2d");
            var analyser = audioCtx.createAnalyser();
            var distortion = audioCtx.createWaveShaper();
            var biquadFilter = audioCtx.createBiquadFilter();


            function makeDistortionCurve(amount) { // function to make curve shape for distortion/wave shaper node to use
              var k = typeof amount === 'number' ? amount : 50,
                n_samples = 44100,
                curve = new Float32Array(n_samples),
                deg = Math.PI / 180,
                i = 0,
                x;
              for ( ; i < n_samples; ++i ) {
                x = i * 2 / n_samples - 1;
                curve[i] = ( 3 + k ) * x * 20 * deg / ( Math.PI + k * Math.abs(x) );
              }
              return curve;
            };

                source = audioCtx.createMediaElementSource(myAudio);
                source.connect(analyser);
                analyser.connect(distortion);
                distortion.connect(biquadFilter);
                biquadFilter.connect(gainNode);
                gainNode.connect(audioCtx.destination); // connecting the different audio graph nodes together

                visualize(myAudio);
                voiceChange();


            function visualize(myAudio) {
              WIDTH = 560;//canvasCtx.width;
              HEIGHT = 200;//canvasCtx.height;

                var visualSetting = visualSelect.value;

              if(visualSetting == "sinewave") {
                analyser.fftSize = 512;
                var bufferLength = analyser.frequencyBinCount; // half the FFT value
                var dataArray = new Uint8Array(bufferLength); // create an array to store the data

                canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);

                function draw() {

                  drawVisual = requestAnimationFrame(draw);

                  analyser.getByteTimeDomainData(dataArray); // get waveform data and put it into the array created above

                  canvasCtx.fillStyle = 'rgb(255, 255, 255)'; // draw wave with canvas
                  canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

                  canvasCtx.lineWidth = 2;
                  canvasCtx.strokeStyle = '#094377';

                  canvasCtx.beginPath();

                  var sliceWidth = WIDTH * 1.0 / bufferLength;
                  var x = 0;

                  for(var i = 0; i < bufferLength; i++) {

                    var v = dataArray[i] / 128.0;
                    var y = v * HEIGHT/2;

                    if(i === 0) {
                      canvasCtx.moveTo(x, y);
                    } else {
                      canvasCtx.lineTo(x, y);
                    }

                    x += sliceWidth;
                  }

                  canvasCtx.lineTo(WIDTH, HEIGHT/2);
                  canvasCtx.stroke();
                };

                draw();

              } else if(visualSetting == "frequencybars") {
                analyser.fftSize = 256;
                var bufferLength = analyser.frequencyBinCount;
                var dataArray = new Uint8Array(bufferLength);

                canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);

                function draw() {
                  drawVisual = requestAnimationFrame(draw);

                  analyser.getByteFrequencyData(dataArray);

                  canvasCtx.fillStyle = 'rgb(255, 255, 255)';
                  canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

                  var barWidth = (WIDTH / bufferLength) * 2.5;
                  var barHeight;
                  var x = 0;

                  for(var i = 0; i < bufferLength; i++) {
                    barHeight = dataArray[i];

                    canvasCtx.fillStyle = 'rgb( 9 ,67,119)';//50rgb(9,67,119),+ (barHeight+100) +
                    canvasCtx.fillRect(x,HEIGHT-barHeight/2,barWidth,barHeight/2);

                    x += barWidth + 1;
                  }
                };

                draw();
              }



            }

            function voiceChange() {
              distortion.curve = new Float32Array;
              biquadFilter.gain.value = 0; // reset the effects each time the voiceChange function is run
              distortion.curve = makeDistortionCurve(400); // apply distortion to sound using waveshaper node

            }
      });

    });

});



function validateSignin() {
    var a = true;
    var u = document.forms["signin"]["username"].value;
    var p = document.forms["signin"]["password"].value;

    if (u.length <6) {
        $('.col-md-6 .form_control:first-child span').addClass('glyphicon glyphicon-remove');
        a=false;
    }
    if (p.length <8) {
        $('.col-md-6 .form_control:last-child span').addClass('glyphicon glyphicon-remove');
            a=false;
    }
    return a;
}


function validateSignup() {
    var a = true;
    var u = document.forms["signup"]["username"].value;
    var p = document.forms["signup"]["password"].value;
    var c = document.forms["signup"]["confirmation"].value;
    var e = document.forms["signup"]["email"].value;

    if (c != p) {
        $('.col-md-6 .form_control:first-child span').addClass('glyphicon glyphicon-remove');
        a=false;
    }
    if (u.length <6) {
        $('.col-md-6 .form_control:first-child span').addClass('glyphicon glyphicon-remove');
        a=false;
    }
    if (p.length <8) {
        $('.col-md-6 .form_control:last-child span').addClass('glyphicon glyphicon-remove');
        a=false;
    }
    if(e.length < 10) {
        $('.col-md-6 .form_control:first-child span').addClass('glyphicon glyphicon-remove');
        a=false;
    }
    return a;
}

function validateLink() {
  $('#error').removeClass('glyphicon glyphicon-remove')
  $(".loader").show();
  $("#msg").text("");
  $("#form button").attr('disabled',true);
  $("#link").attr('disabled',true);
    var l = $("#link").val();

    if(l.length != 43 ) {
        $('#error').addClass('glyphicon glyphicon-remove').css( "color", "red" );
        $(".loader").hide();
        $("#form button").attr('disabled',false);
        $("#link").attr('disabled',false);
        return false;
    }
    else
        submitLink(l);
}
function submitLink(l) {
    var id = l.substring(l.length-11);

    link = "/addvideo/"+id;
    $.getJSON(link,function(data,status) {
    	  if (status == "success") {
    	    $("#msg").text(data["msg"]);
    	    videos();
    	  } else {
    	    // request failed
    	    $("#msg").text("Error, Could not get data!").css("color","red");
    	  }
    	  $(".loader").hide();
        $("#form button").attr('disabled',false);
        $("#link").attr('disabled',false);
    });
}


$(document).ready(function() {
    videos();
});

function videos() {
    var url = window.location.href;
    var site = url.substring('http://data-projects-medyas.c9users.io:8080/'.length);
    if(site == "dashboard" || site == 'admin') {
          $(".dataLoader").show();
          link = "/getvideos/";
          getData(link);
    }
    else if(site == "music") {
      $(".dataLoader").show();
          link = "/getvideos/"+$("#user").text();
          getData(link);
    }
}
function getData(link) {

    $.getJSON(link,function(data,status) {
        	  if (status == "success") {
        	    $(".list").text("")
        	    printData(data);
        	  } else {
        	    // request failed
        	    $(".list").text("Error, Could not get data!").css("color","red");
        	  }
        	  $(".dataLoader").hide();
        });
}
function printData(data) {

  if(data.length != 0) {
      for(var i=0; i<data.length; i++) {
        var temp = '<div class="vid" data-toggle="modal" data-target="#audio">'+
        '<center><img class="img-thumbnail" src="'+data[i].img+'"></img></center>'+
        '<a class="l" href="'+data[i].link+'"><h5>'+data[i].title+'</h5></a>'+
        '<p>Description :</p>'+
        '<ul><li>'+data[i].des+'</li>...</ul>'+
        '<p>Published on : '+data[i].date+'</p>'+
        '<a href="'+data[i].link+'">See More</a>'+
        '<p id="u">Added By '+data[i].username+'</p>'+
        '</div>';
        $(".list").append(temp);
    }
  }
  else
    $(".list").append('<center>Unbelievable.  No entries here so far</center>');

}


