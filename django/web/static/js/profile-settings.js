function changeUsername(url) {
    const username_input = document.getElementById("username_input")
    const formData = {
      'username': username_input.value,
    }
    $.ajax({
      url: url,
      type: 'PUT',
      headers: {
          'X-CSRFToken': Cookies.get('csrftoken')
      },
      data: formData,
      success: function(response) {
        window.location.reload();
      },
      error: function(response) {
        username_input.style.background_color = "red";
      },
    })
  }