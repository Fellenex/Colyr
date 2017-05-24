const KEYCODE_TAB = 9;

(function() {
	$(document).ready(function() {
		var currentColor = "#FFFFFF";
		$("#current-color").on("input", function(e) {
			if(this.value.length === 0) {
				$("#current-color").css("background-color", "#FFFFFF");
				return;
			}
			if(isHexFormat(this.value)) {
				console.log("new hex color: " + this.value.toUpperCase());
				currentColor = this.value.toUpperCase();
				$("#current-color").css("background-color", "#99FF99");
			} else { $("#current-color").css("background-color", "#FFB399"); }
		});
		$(window).keypress(function(e) {
			var ev = e || window.event;
			var key = ev.keyCode || ev.which;
			// key is now a code for which key was pressed
			if(key === KEYCODE_TAB) {
				// get highlighted text, and set to current color
				surroundSelection("color: " + currentColor + ";");
			}
		});
	});
	// determines if a given string falls within hex-color format
	function isHexFormat(hexString) {
		if(hexString.length !== 7)
			return false;
		if(hexString[0] !== "#")
			return false;
		for(var i = 1; i < hexString.length; i++) {
			if("0123456789ABCDEF".indexOf(hexString[i]) < 0
			&& "0123456789abcdef".indexOf(hexString[i]) < 0)
				return false;
		}
		return true;
	}
	// returns the user's selection
	function getSelection() {
		if (window.getSelection) {
			return window.getSelection();
		} else if (document.selection) {
			return document.selection;
		}
	}
	function surroundSelection(spanStyle) {
		var span = document.createElement("span");
		span.style = spanStyle;
		
		var sel = getSelection();
		span.textContent = sel.toString();
		
		var range = sel.getRangeAt(0);
		range.deleteContents();
		range.insertNode(span);
	}
})();