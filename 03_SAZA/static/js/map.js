function GpsGetCurrentPosition(){
    $('#check_location').css('display', 'none');
    $('#result_location').css('display', 'block');
    $('.restaurant_list_box').css('display', 'block');
    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition (function (pos)
        {
            lat = pos.coords.latitude; 
            lng = pos.coords.longitude;
            data = {
                'user_lat' : lat,
                'user_lng' : lng
            };
  
            var mapOptions = {
                zoom: 16,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                center: new google.maps.LatLng(lat, lng)
            };
  
            map = new google.maps.Map(document.getElementById('map'),mapOptions);
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(lat,lng),
                map: map
            });
            
            // var map = new google.maps.Map('map', mapOptions);

            console.log(lat);
            console.log(lng);
            
            $.ajax({
                type:'POST',
                url:'/get-current-coordinate/',
                data: JSON.stringify(data),
                success: function(json){
                    console.log('data pass success');
                },
                error: function(json){
                    console.log('data pass failed');
                },
                complete: function(json){
                    console.log('complete');
                }
            });

            },function(error)
            {
                switch(error.code)
                {
                    case 1:
                        $("#errormsg").html("User denied the request for Geolocation.");
                        break;
                    case 2:
                        $("#errormsg").html("Location information is unavailable.");
                        break;
                    case 3:
                        $("#errormsg").html("The request to get user location timed out.");
                        break;
                    case 0:
                        $("#errormsg").html("An unknown error occurred.");
                        break;
                }
            });
        }
        else
        {
            $("#errormsg").html("Geolocation is not supported by this browser.");
        }
}
