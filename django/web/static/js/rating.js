document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.user-rating input');
    stars.forEach(star => {
        star.addEventListener('click', e => {
            const target = e.currentTarget;
            const value = target.value;
            const movieID = target.parentElement.parentElement.dataset.movieId;

            const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            $.ajax({
                type: 'POST',
                url: `/rating/`,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                data: {
                    'movie_id': movieID,
                    'rating': value
                },
                statusCode: {
                    401: () => {
                        window.location.href = `/accounts/login/?next=${window.location.pathname}`;
                    }
                },
                success: data => {
                    updateScore(data.value, data.count);
                    updateStars(value);
                    showDeleteRating();
                    try {
                        document.querySelector('#add-review').style.display = 'flex';
                    } catch (e) {

                    }
                }
            });
        });
    });

    const deleteRating = document.querySelectorAll('.delete-rating');
    deleteRating.forEach(elem => {
        elem.addEventListener('click', e => {
            const target = e.currentTarget;
            const parent = target.parentElement;
            const movieID = parent.dataset.movieId;
            console.log(movieID);

            const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            $.ajax({
                type: 'DELETE',
                url: `/rating/`,
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                },
                data: {
                    'movie_id': movieID
                },
                statusCode: {
                    401: () => {
                        window.location.href = `/accounts/login/?next=${window.location.pathname}`;
                    }
                },
                success: data => {
                    updateScore(data.value, data.count);
                    updateStars(0);
                    hideDeleteRating();
                    try {
                        document.querySelector('#add-review').style.display = 'none';
                    } catch (e) {
                        
                    }
                }
            });
        });
    });
});


function updateScore(score, count) {
    const backgroundStyle = `radial-gradient(closest-side, #222222 79%, transparent 80% 100%),conic-gradient(hsl(calc(${score} * 1.2), 100%, 50%) ${score}%, #606060 0)`;

    const scoreDiv = document.querySelector('#score');

    scoreDiv.querySelector('.score-text').innerHTML = score ? score : '-';
    scoreDiv.querySelector('.score-amount').innerHTML = count;
    
    const circle = scoreDiv.querySelector('.progress-circle');
    circle.setAttribute('aria-valuenow', score);
    circle.style.background = backgroundStyle;
}

function updateStars(score) {
    console.log(score);
    document.querySelectorAll('.user-rating input').forEach(input => {
        if (input.value == score) {
            input.checked = true;
        } else {
            input.checked = false;
        }
    });
}

function hideDeleteRating() {
    document.querySelectorAll('.delete-rating').forEach(elem => {
        elem.style.display = 'none';
    });
}

function showDeleteRating() {
    document.querySelectorAll('.delete-rating').forEach(elem => {
        elem.style.display = 'flex';
    });
}