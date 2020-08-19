// set the number of stars to 0 at first
let num_stars = 0

document.addEventListener('DOMContentLoaded', () => {

    // does something for each click of the star
    document.querySelectorAll('.star').forEach(star => {
        star.addEventListener('click', (event) => {
            const clicked_star = event.target.id;
            console.log(clicked_star);
            if (clicked_star === '1') {
                clicked_one();
            } else if (clicked_star === '2') {
                clicked_two();
            }
            else if (clicked_star === '3') {
                clicked_three();
            }
            else if (clicked_star === '4') {
                clicked_four();
            }
            else if (clicked_star === '5') {
                clicked_five();
            }
        })
    });

    document.querySelector('.submit-btn').addEventListener('click', (event) => {
        if (num_stars > 0) {
            submit_feedback(event.target);
        } else {
            console.log('Sorry try again');
            return false;
        }
    })
});

function clicked_one() {
    console.log('Clicked 1st star');
    const stars = document.querySelectorAll('.star');
    // change the colors for the stars, only first one should be blue
    stars[0].className = 'fa fa-star fa-3x star star-rating-clicked';
    num_stars = 1;
    for (let i = 1; i < stars.length; i++) {
        stars[i].className = 'fa fa-star fa-3x star star-rating';
    }
}

function clicked_two() {
    console.log('Clicked 2nd star');
    const stars = document.querySelectorAll('.star');
    // change the colors for the stars, only first and second should be blue
    stars[0].className = 'fa fa-star fa-3x star star-rating-clicked';
    stars[1].className = 'fa fa-star fa-3x star star-rating-clicked';
    num_stars = 2;
    for (let i = 2; i < stars.length; i++) {
        stars[i].className = 'fa fa-star fa-3x star star-rating';
    }
}

function clicked_three() {
    console.log('Clicked 3rd star');
    const stars = document.querySelectorAll('.star');
    // change the colors for the stars, only first, second, and third should be blue
    stars[0].className = 'fa fa-star fa-3x star star-rating-clicked';
    stars[1].className = 'fa fa-star fa-3x star star-rating-clicked';
    stars[2].className = 'fa fa-star fa-3x star star-rating-clicked';
    num_stars = 3;
    for (let i = 3; i < stars.length; i++) {
        stars[i].className = 'fa fa-star fa-3x star star-rating';
    }
}

function clicked_four() {
    console.log('Clicked 4th star');
    const stars = document.querySelectorAll('.star');
    // change the colors for the stars, only first, second, third, and fourth should be blue
    for (let i = 0; i < 4; i++) {
        stars[i].className = 'fa fa-star fa-3x star star-rating-clicked';
    }
    num_stars = 4;
    stars[4].className = 'fa fa-star fa-3x star star-rating';
}

function clicked_five() {
    console.log('Clicked 5th star');
    const stars = document.querySelectorAll('.star');
    // change the colors for the stars, all five should be blue
    for (let i = 0; i < stars.length; i++) {
        stars[i].className = 'fa fa-star fa-3x star star-rating-clicked';
    }
    num_stars = 5;
}

function submit_feedback(target) {
    console.log(`Submitting feedback for ${target.id}`);
    // get the csrf token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // make sure to include csrf token when fetching
    const request = new Request(
        `/student/feedback/${target.id}/submit/`,
        {headers: {'X-CSRFToken': csrftoken}}
    );

    const commentsInput = document.querySelector(`#comments-form-input`);

    if ((num_stars > 0) && commentsInput.value.trim() !== '') {
        console.log('Submitting feedback');
        fetch(request, {
            method: 'POST',
            body: JSON.stringify({
                rating: num_stars,
                comments: commentsInput.value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        });
    } else {
        console.log('Sorry. Try again.');
    }
}