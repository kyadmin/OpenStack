var Lock = function () {

    return {
        //main function to initiate the module
        init: function () {

             $.backstretch([
		        "/static/images/1.jpg",
		        "/static/images/2.jpg",
		        "/static/images/3.jpg",
		        "/static/images/4.jpg"
		        ], {
		          fade: 1000,
		          duration: 8000
		      });
        }

    };

}();