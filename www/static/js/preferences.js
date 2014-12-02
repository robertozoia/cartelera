 	$(document).ready(function(){
       
        $('[rel="in-app"]').on('click', function(event) {
            // this is needed to prevent iOS app mode to leave app mode when
            // clicking links
            var baseurl = 'http://carteleraperu.com';
            event.preventDefault();
            location.href = $(this).attr("href");
        });
        
 		var cookieName = 'cartelera';
 		var cookieVersion = 1.2;
	
		function initialize(data) {
			if (data['version']==cookieVersion) {
				delete data['version'];
				for (var key in data) {
					if (data[key]) {
						$('#'+ key).attr('checked', '');
						
					} else {
						$('#'+ key).removeAttr('checked');
					}
				}
			}
		}
		function writeCookie()  {
			// no cookie set, initialize defaults and set cookie
			var data = new Object();
			
			data['version'] = cookieVersion;  // data format version
			// iterate checkboxes and retrive values
			$("[rel='filter-action']").map(function(){
				data[this.id]=this.checked;
			});
			// set cookie
			$.cookie(cookieName, data, { expires: 360 });
		}
		$.cookie.json = true;
		if ($.cookie(cookieName) ) {
			// cookie exists, read contents
			var data = $.cookie(cookieName);
			initialize(data);
		} else {
			writeCookie();
		}

		var elems = Array.prototype.slice.call(document.querySelectorAll('.js-switch'));

		elems.forEach(function(html) {
		  var switchery = new Switchery(html);
		});

		$(':checkbox').change(function() {
			writeCookie();
		});

        /* $(':checkbox').iphoneStyle({
              checkedLabel: 'SI',
              uncheckedLabel: 'NO',
              onChange: function(elem, value) {
                writeCookie();
              },
        });
 	*/
	});