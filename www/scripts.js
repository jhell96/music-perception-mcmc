$(document).ready(function() {

	var WHITE_KEYS = [1,3,5,6,8,10,12,13,15,17,18,20,22,24,25];
	var FREQ_DICT = {"1/4":"1","1/8":"0.5","1/16":"0.25","1/2":"2","1":"4"};
	var SOUND_DICT = {1:'c',2:'cis',3:'d',4:'es',5:'e',6:'f',7:'fis',8:'g',9:'gis',10:'a',11:'b',12:'h',13:'c1',
		14:'cis1',15:'d1',16:'es1',17:'e1',18:'f1',19:'fis1',20:'g1',21:'gis1',22:'a1',23:'b1',24:'h1',25:'c2'};
	var STYLE_DICT = {'to1':14,'l2':9,'r2':5,'to3':14,'l4':5,'r4':9,'to5':14,'to6':13,'l7':11,'r7':3,'to8':13,'l9':7,
		'r9':7,'to10':13,'l11':3,'r11':11,'to12':13,'to13':14,'l14':9,'r14':5,'to15':14,'l16':5,'r16':9,'to17':14,
		'to18':13,'l19':11,'r19':3,'to20':13,'l21':7,'r21':7,'to22':13,'l23':3,'r23':11,'to24':13,'to25':23,};

	function keywaspressed(e) {
		if (document.activeElement.nodeName == 'TEXTAREA') return;
		if (document.activeElement.nodeName == 'INPUT') return;

		switch(e.keyCode) {
			case 9: press(1); return false;
			case 49: press(2); break; //1
			case 81: press(3); break; //q
			case 50: press(4); break; //2
			case 87: press(5); break; //w
			case 69: press(6); break; //e
			case 52: press(7); break; //4
			case 82: press(8); break; //r
			case 53: press(9); break; //5
			case 84: press(10); break; //t
			case 54: press(11); break; //6
			case 89: press(12); break; //y
			case 85: press(13); break; //u
			case 56: press(14); break; //8
			case 73: press(15); break; //i
			case 57: press(16); break; //9
			case 79: press(17); break; //o
			case 80: press(18); break; //p
			case 189: press(19); break; //-
			case 173: press(19); break; //-
			case 219: press(20); break; //[
			case 187: press(21); break;
			case 61: press(21); break; //=
			case 221: press(22); break; //]
			case 8: press(23); return false; //backspace
			case 13: press(24); break; //enter
			case 220: press(25); break; //\

			case 90: cdur(); break; //z
			case 88: ddur(); break; //x
			case 67: edur(); break; //c
			case 86: fdur(); break; //v
			case 66: gdur(); break; //b
			case 78: adur(); break; //n
			case 77: bdur(); break; //m
			case 65: cmol(); break; //a
			case 83: dmol(); break; //s
			case 68: emol(); break; //d
			case 70: fmol(); break; //f
			case 71: gmol(); break; //g
			case 72: amol(); break; //h
			case 74: bmol(); break; 		
		}
	}

	function play(x) {
		var note = document.getElementById(SOUND_DICT[x]);
 		note.currentTime=0;
 		note.play(); 
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

	  		bottomHalf.style.backgroundColor = 'lightgray';
	  		topHalf.style.backgroundColor = 'lightgray';
	 	} else {
	  		var leftHalf = document.getElementById('l'+x);
	  		var rightHalf = document.getElementById('r'+x);

			leftHalf.style.backgroundColor = 'darkgray';
			rightHalf.style.backgroundColor = 'darkgray';
	 	}
	}

	function press(x) {
		$('#song').text(function(index, text) {
			return text+(parseInt(x)+27)+",";
		});

		$('#frequencies').text(function(index, text) {
			return text+FREQ_DICT[document.getElementById('freq').innerHTML]+",";
		});
	 	
	 	removeSelection();
	 	play(x);
	 	selectkey(x);  
	}


	function unselectkey(x) {
		if (WHITE_KEYS.indexOf(x) != -1) {
	 		$('#bo'+x).css("background-color", "white");
			$('#to'+x).css("background-color", "white");
	 	} else {
	 		$('#l'+x).css("background-color", "black");
			$('#r'+x).css("background-color", "black");
		}
	}

	function unselectall() {
		for (var x=1; x<=25; x++) unselectkey(x);
	}

	function cdur() { press(1); press(5); press(8); }
	function ddur() { press(3); press(7); press(10); }
	function edur() { press(5); press(9); press(12); }
	function fdur() { press(6); press(10); press(13); }
	function gdur() { press(8); press(12); press(15); }
	function adur() { press(10); press(14); press(17); }
	function bdur() { press(12); press(16); press(19); }
	function cmol() { press(1); press(4); press(8); }
	function dmol() { press(3); press(6); press(10); }
	function emol() { press(5); press(8); press(12); }
	function fmol() { press(6); press(9); press(13); }
	function gmol() { press(8); press(11); press(15); }
	function amol() { press(10); press(13); press(17); }
	function bmol() { press(12); press(15); press(19); }


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


/*	
	var freqs = ["1/16", "1/8", "1/4", "1/2", "1"];
  	var count = 0;
  	function frequp() {
	    if (count == 4) {
	      count = 0;
	    } else {
	      count += 1;
	    }
	    $('#freq').text(freqs[count]);
  	}*/
	

	function loadPianoMusic() {	
		var part1 = "<audio preload='auto' id='";
		var part2 = "' src='http://www.agnes-bruckner.com/apronus_static/music-lessons/sounds/";
		var part3 = ".mp3'></audio>";

		var ids = ["c", "cis", "d", "es", "e", "f", "fis", "g", "gis", "a", "b", "h", "c1",
			 "cis1", "d1", "es1", "e1", "f1", "fis1", "g1", "gis1", "a1", "b1", "h1", "c2"];

		var pianoMusicHtml = "";

		ids.forEach(function(id) {
			pianoMusicHtml += part1 + id + part2 + id + part3;
		});

		$("#pianomusic").html(pianoMusicHtml);
	}


	loadPianoMusic();

	$('#idbody').keydown(function(e) {
		keywaspressed(e);
	});

	$("#idbody").keyup(function() {
		unselectall();
	});

	$('#freq').click(function() {
		frequp();
	});
	$('#116').click(function() {
		$('#freq').text('1/16');
	});
	$('#18').click(function() {
		$('#freq').text('1/8');
	});
	$('#14').click(function() {
		$('#freq').text('1/4');
	});
	$('#12').click(function() {
		$('#freq').text('1/2');
	});
	$('#1').click(function() {
		$('#freq').text('1');
	});

	keyboardsize(0);

	[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25].forEach(function(k) {
		$('#bo'+k).mousedown(function() {
			press(k);
		});
		$('#bo'+k).mouseup(function() {
			unselectkey(k);
		});
		$('#to'+k).mousedown(function() {
			press(k);
		});
		$('#to'+k).mouseup(function() {
			unselectkey(k);
		});
		$('#r'+k).mousedown(function() {
			press(k);
		});
		$('#r'+k).mouseup(function() {
			unselectkey(k);
		});
		$('#l'+k).mousedown(function() {
			press(k);
		});
		$('#l'+k).mouseup(function() {
			unselectkey(k);
		});
	});

	$('#clear').click(function() {
		$('#frequencies').text('');
		$('#song').text('');
	});

	$('#delete').click(function() {
		$('#frequencies').text(function(index, text) {
			text = text.substring(0, text.length-1);

			var n = text.lastIndexOf(",");
			return text.substring(0,n+1);
		});
		$('#song').text(function(index, text) {
			text = text.substring(0, text.length-1);

			var n = text.lastIndexOf(",");
			return text.substring(0,n+1);
		});
	});


	$('#playback').click(async function() {
		var notes = $('#song').text().split(',');
		var frequencies = $('#frequencies').text().split(',');
		notes.pop();
		frequencies.pop();

		var count = 0;
		var current = 0;
		notes.forEach(function(note) {
			setTimeout(function () { 
				play(parseInt(note)-27)}, current);
			current += 500*parseFloat(frequencies[count]);
			count ++;

		});

	});


	$('#save').click(function() {
		console.log("trying save");
		var xhttp;
		var author = "Libby Aiello";
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



