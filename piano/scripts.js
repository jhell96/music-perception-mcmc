$(document).ready(function() {

	var WHITE_KEYS = [1,3,5,6,8,10,12,13,15,17,18,20,22,24,25];
	var SOUND_DICT = {1:'c',2:'cis',3:'d',4:'es',5:'e',6:'f',7:'fis',8:'g',9:'gis',10:'a',11:'b',12:'h',13:'c1',
		14:'cis1',15:'d1',16:'es1',17:'e1',18:'f1',19:'fis1',20:'g1',21:'gis1',22:'a1',23:'b1',24:'h1',25:'c2'};
	var STYLE_DICT = {'to1':14,'l2':9,'r2':5,'to3':14,'l4':5,'r4':9,'to5':14,'to6':13,'l7':11,'r7':3,'to8':13,'l9':7,
		'r9':7,'to10':13,'l11':3,'r11':11,'to12':13,'to13':14,'l14':9,'r14':5,'to15':14,'l16':5,'r16':9,'to17':14,
		'to18':13,'l19':11,'r19':3,'to20':13,'l21':7,'r21':7,'to22':13,'l23':3,'r23':11,'to24':13,'to25':23,};
	var MIDI_DICT = {65:1, 87:2, 83:3, 69:4, 68:5, 70:6, 84:7, 71:8, 89:9, 72:10, 85:11, 74:12, 75:13, 79:14, 76:15, 
		80:16, 186:17, 222:18, 219:19}

	function keywaspressed(e) {
		if (document.activeElement.nodeName == 'TEXTAREA') return;
		if (document.activeElement.nodeName == 'INPUT') return;

		switch(e.keyCode) {
			case 65: press(1); break; //a
			case 87: press(2); break; //w
			case 83: press(3); break; //s
			case 69: press(4); break; //e
			case 68: press(5); break; //d
			case 70: press(6); break; //f
			case 84: press(7); break; //t
			case 71: press(8); break; //g
			case 89: press(9); break; //y
			case 72: press(10); break; //h
			case 85: press(11); break; //u
			case 74: press(12); break; //j
			case 75: press(13); break; //k
			case 79: press(14); break; //o
			case 76: press(15); break; //l
			case 80: press(16); break; //p
			case 186: press(17); break; //;
			case 222: press(18); break; //'
			case 219: press(19); break; //[
		}
	}

	function play(x) {
 		x = parseInt(x)+59;
 		document.getElementById(x.toString()).play();
	}

	function removeSelection() {
		if (window.getSelection().empty) {
    		window.getSelection().empty();
    	}
	}

	function selectkey(x) {
		if (WHITE_KEYS.indexOf(x) !== -1) {
	 		var bottomHalf = document.getElementById('bo'+x);
	  		var topHalf = document.getElementById('to'+x);

	  		bottomHalf.style.backgroundColor = 'lightblue';
	  		topHalf.style.backgroundColor = 'lightblue';

	 	} else {
	  		var leftHalf = document.getElementById('l'+x);
	  		var rightHalf = document.getElementById('r'+x);

			leftHalf.style.backgroundColor = 'lightblue';
			rightHalf.style.backgroundColor = 'lightblue';
	 	}
	}

	var trials = []
	function press(x) {
		$('#song').text(function(index, text) {
			trials.push("[" + Object.keys(heldKeys)+"]")
			return trials.toString()
		});

		$('#frequencies').text(function(index, text) {
			return text+FREQ_DICT[document.getElementById('freq').innerHTML]+",";
		});
	 	
	 	removeSelection();
	 	play(x);
	 	selectkey(x);  
	}


	function unselectkey(x) {
		y = parseInt(x)+59;
		document.getElementById(y.toString()).pause();
		document.getElementById(y.toString()).currentTime = 0;


		if (WHITE_KEYS.indexOf(x) != -1) {
	 		$('#bo'+x).css("background-color", "white");
			$('#to'+x).css("background-color", "white");

	 	} else {
	 		$('#l'+x).css("background-color", "black");
			$('#r'+x).css("background-color", "black");
		}
	}

	var currentSize = 2;
	function keyboardsize(x) {
		if (x==0) x = 2;
		currentSize = x;
		var unit = 'px';

		$('#to1').height(''+100*x+unit);
		$('#bo1').height(''+50*x+unit);
		
		for (var id in STYLE_DICT) {
			$('#'+id).width(''+STYLE_DICT[id]*x+unit);
		}
	}	

	function loadPianoMusic() {	
		var part1 = "<audio id=";
		var part2 = " src=../resources/keys_wav/";
		var part3 = ".wav></audio>"

		var ids = ["60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74",
					"75", "76", "77", "78"];

		var pianoMusicHtml = "";

		ids.forEach(function(id) {
			pianoMusicHtml += part1 + id + part2 + id + part3;
		});

		$("#pianomusic").html(pianoMusicHtml);
	}


	loadPianoMusic();


	var heldKeys = {};

	$('#idbody').keydown(function(e) {
		console.log("down")
		if (e.keyCode in heldKeys) {
			return false;
		}
		heldKeys[e.keyCode]=true;
		keywaspressed(e);
	});

	$("#idbody").keyup(function() {
		console.log("up")
		lastState=null;
		delete heldKeys[event.keyCode];
		id = MIDI_DICT[event.keyCode];
		unselectkey(id);
	});

	keyboardsize(0);

	$('#clear').click(function() {
		$('#frequencies').text('');
		$('#song').text('');
	});


	$('#save').click(function() {
		console.log("trying save");
		var xhttp;
		var author = "Christie Hong";
		var songName = "Simple";
		xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
		  if (this.readyState == 4 && this.status == 200) {
		    console.log(this.responseText);
		  }
		};
		xhttp.open("GET", "https://iesc-s2.mit.edu/6S08dev/abertics/final/sb1.py?ADD=1&name="+songName+
				"&author="+author+"&notes="+$('#song').text()+"&frequencies="+$('#frequencies').text(), true);
		xhttp.send();

	});



});



