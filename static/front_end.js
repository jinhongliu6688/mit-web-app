function update_page(response) {
  	document.getElementById('flex-container').innerHTML = response;
}


function search_by_title()
{
	var form = document.getElementById("form");
	const formData = new FormData(form);
	const searchParams = new URLSearchParams(formData);
	const queryString = searchParams.toString();
	xmlHttpRqst = new XMLHttpRequest( )
	xmlHttpRqst.onload = function(e) {update_page(xmlHttpRqst.response);}
	xmlHttpRqst.open( "GET", "/search-by-title?" + queryString);
	try {
		xmlHttpRqst.send( null );
	}
	catch(err)
	{
		alert(err);
	}
}


function search_by_author()
{
	var form = document.getElementById("form");
	const formData = new FormData(form);
	const searchParams = new URLSearchParams(formData);
	const queryString = searchParams.toString();
	xmlHttpRqst = new XMLHttpRequest( )
	xmlHttpRqst.onload = function(e) {update_page(xmlHttpRqst.response);}
	xmlHttpRqst.open( "GET", "/search-by-author?" + queryString);
	try {
		xmlHttpRqst.send( null );
	}
	catch(err)
	{
		alert(err);
	}
}