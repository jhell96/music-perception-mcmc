Storage.prototype.setObj = function(key, obj) {
    return this.setItem(key, JSON.stringify(obj))
};
Storage.prototype.getObj = function(key) {
    return JSON.parse(this.getItem(key))
};

$(document).ready(function() {

	// ----------- PIANO CODE -----------
	var WHITE_KEYS = [1,3,5,6,8,10,12,13,15,17,18,20,22,24,25];

	var SOUND_DICT = {1:'C',2:'C#',3:'D',4:'E♭',5:'E',6:'F',7:'F#',8:'G',9:'A♭',10:'A',11:'B♭',12:'B',13:'1C',
		14:'1C#',15:'1D',16:'1E♭',17:'1E',18:'1F',19:'1F#'};

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
	var interface_trials = []
	function press(x) {
		$('#song').text(function(index, text) {
			interface_trials.push("[" + Object.keys(heldKeys)+"]")
			trials.push(Object.keys(heldKeysMidi))
			return interface_trials.toString()
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
		var part2 = " src=resources/keys_wav/";
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


	var heldKeys = {}; // SOUND_DICT for UI purposes
	var heldKeysMidi = {}; // MIDI_DICT for vector purposes 
	$('#idbody').keydown(function(e) {
		// console.log("down")
		key = SOUND_DICT[MIDI_DICT[e.keyCode]]
		if (key in heldKeys) {
			return false;
		}
		heldKeys[key]=true;
		heldKeysMidi[MIDI_DICT[e.keyCode]] = true;
		keywaspressed(e);

	});

	$("#idbody").keyup(function(e) {
		// console.log("up")
		key = SOUND_DICT[MIDI_DICT[e.keyCode]];
		delete heldKeys[key];
		delete heldKeysMidi[MIDI_DICT[e.keyCode]];
		id = MIDI_DICT[e.keyCode];
		unselectkey(id);
	});


	keyboardsize(0);


	// ----------- BUTTON CODE -----------

	$('#clear').click(function() {
		$('#song').text('');
	});


	// user_tests = []
	$('#save').click(function() {
		console.log(trials)
		var vectors = [] // holds 20len vectors for each trial
		for (var i=0; i<trials.length; i++) {
			vector = []
			for (var x=0; x<20; x++){
				vector.push(0)
			}
			for (var j=0; j<trials[i].length; j++) {
				vector[trials[i][j]-1] = 1
			}
			vectors.push(vector)
		}

		var pages = window.location.pathname.split("/");
		localStorage.setObj(pages[pages.length-1], vectors);

		if (pages[pages.length-1] === "test5.html") {
			$('#submit').prop('disabled', false)
		}

	});

	$('#submit').click(function() {
		test1=localStorage.getObj("test1.html")
		test2=localStorage.getObj("test2.html")
		test3=localStorage.getObj("test3.html")
		test4=localStorage.getObj("test4.html")
		test5=localStorage.getObj("test5.html")
		console.log(test5)

		$.ajax({
            type: "POST",
            url: "post_data",
            data: 'test1='+test1+'&test2='+test2+'&test3='+test3+'&test4='+test4+'&test5='+test5
        }).then(function(data) {
            console.log(data);
        });

	})

	// Get the modal
	var modal = document.getElementById('myModal');

	// Get the button that opens the modal
	var btn = document.getElementById("submit");

	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];

	// When the user clicks on the button, open the modal 
	btn.onclick = function() {
	  modal.style.display = "block";
	}

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	  modal.style.display = "none";
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	    modal.style.display = "none";
	  }
}

});



