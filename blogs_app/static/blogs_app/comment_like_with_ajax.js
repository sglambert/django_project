$(function(){

	var test = $('#like_status').text();
	$('#like_status').hide();
	
	if(test == 'True'){
		$('#like_unlike_btn').text('unlike');
		$('#like_status').text('You liked this Post').show();
	} else {
		$('#like_unlike_btn').text('Like');

	};


	$('#like_unlike_btn').click(function(){
		console.log('clicked');
		$.ajax({
			url:'',	
			type:'get', //defines the type of request
			data:{      //'data' defines the data being sent to the server with request
				button_text: $(this).text()
				//gets the text of selected item and stores it in 'button_text'
			},

			//When the server responds successfully i.e status code = '200'
			success: function(response){
				$('#totalLikes').text(response.post_likes)
				$('#like_unlike_btn').text(response.text)
				if (response.text == 'Like'){
					$('#like_status').text('')
				} else {
					$('#like_status').text('You liked this post')
				}
			}

		});
	});

	var csrf = $('input[name=csrfmiddlewaretoken]').val()

	$('#commentForm').on('submit', function(e){
		e.preventDefault()
		console.log($('#commentIn').val())
		$.ajax({
			url:'',
			type:'post',
			data:{
				formData:$('#commentIn').val(),
				csrfmiddlewaretoken: csrf
			},
			success:function(response) {
				console.log(response.new_comment)
				var commentFormat = `<img class="img-thumbnail article-img"
				src="${response.new_comment.commentator.profile.image.url }">
				<a class="mr-2" >${ response.new_comment.commentator }</a>
				<p class="article-content">${ response.new_comment.comment }</p><hr>`
				$('#commentDiv').append(commentFormat)
			}
		});
	});
		
});