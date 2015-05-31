 	$(document).ready(function(){

        $('[rel="in-app"]').on('click', function(event) {
            // this is needed to prevent iOS app mode to leave app mode when
            // clicking links
            var baseurl = 'http://carteleraperu.com';
            event.preventDefault();
            location.href = $(this).attr("href");
        });


        addToHomescreen();
 		var cookieName = 'cartelera';
 		var cookieVersion = 1.2;
		$.cookie.json = true;

	
		function initialize(data) {

			if (data['version']==cookieVersion) {
				delete data['version'];
				for (var key in data) {
					$('#'+key+'-box').toggle(data[key]);
				}
			}
		}

		if ($.cookie(cookieName) ) {
			// cookie exists, read contents
			var data = $.cookie(cookieName);
			initialize(data);

		} else {
			$('[rel="theater-box"]').show();
		}

	});