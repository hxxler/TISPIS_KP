const textarea = document.getElementById("id_text");

function autoResize() {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

const comments_field = document.querySelector('.comments')

let comments_part_number = 1
let post_id_ = Number(document.getElementById('like_btn').getAttribute('post-id'));

function addComments(){
    setTimeout(() => {
        fetch(`/api/get-comments?post_id=${post_id_}&part_number=${comments_part_number++}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
        }).then(response => response.json()).then(comments => {
            comments.forEach(comment_data => {
                console.log(comment_data);
                const comment_container = document.createElement('div');
                comment_container.className = 'comment_container';
                comments_field.appendChild(comment_container);

                const description_profile_photo_container = document.createElement('div');
                description_profile_photo_container.className = 'description_profile_photo_container';
                comment_container.appendChild(description_profile_photo_container);

                const photo_container = document.createElement('a');
                description_profile_photo_container.appendChild(photo_container);

                const description_profile_photo = document.createElement('img');
                description_profile_photo.className = 'description_profile_photo';
                description_profile_photo.src = comment_data.author.profile_image
                photo_container.appendChild(description_profile_photo);

                const username_description = document.createElement('div');
                username_description.className = 'username_description';
                comment_container.appendChild(username_description);

                const username_link = document.createElement('a');
                username_link.href = '/profile/' + comment_data.author.username;
                username_link.className = 'username description';
                username_link.textContent = comment_data.author.username;
                username_description.appendChild(username_link);

                const description = document.createElement('span');
                description.className = 'description';
                description.textContent = comment_data.text
                username_description.appendChild(description);
            })
        })
        comments_field.removeChild(stripe);
    }, 2000);
    comments_field.appendChild(stripe)
}

addComments();

// Обработчик прокрутки страницы
window.addEventListener('scroll', function () {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
    const clientHeight = document.documentElement.clientHeight;

    if (scrollTop + clientHeight >= scrollHeight) {
        addComments();
    }
});

window.onload = function () {
    stripe.classList.add('animate-stripe');
}