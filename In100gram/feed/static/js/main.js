function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0)
            return c.substring(name.length, c.length);
    }
    return "";
}

function LikeClick(element) {
    // if user like by double click on image
    if (element.classList.value === "content") {
        LikeClick(element.parentElement.parentElement.children[2].children[0].children[0].children[0])
        return;
    }

    var likes_count_el = element.parentElement.parentElement.parentElement.children[1].children[0];
    var regex = /^\d+/;
    var likes_count = Number(likes_count_el.textContent.match(regex)[0])

    if (!element.classList.replace('unactive', 'active')) {
        element.classList.replace('active', 'unactive');
        // отправляем запрос на снятие лайка
        fetch('/api/remove-like', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: Number(element.getAttribute('post-id'))
            })
        }).then(response => {
            likes_count_el.textContent = likes_count_el.textContent.replace(regex, String(likes_count - 1))
            if (!response.ok) {
                likes_count_el.textContent = likes_count_el.textContent.replace(regex, String(likes_count + 1))
                element.classList.replace('unactive', 'active');
            }
        });
    } else {
        // отправляем запрос на лайк
        fetch('/api/like-post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id: Number(element.getAttribute('post-id'))
            })
        }).then(response => {
            likes_count_el.textContent = likes_count_el.textContent.replace(regex, String(likes_count + 1))
            if (!response.ok) {
                likes_count_el.textContent = likes_count_el.textContent.replace(regex, String(likes_count - 1))
                element.classList.replace('active', 'unactive');
            }
        });
    }
}

const posts_field = document.querySelector('.posts')
const stripe = document.createElement('div');
stripe.className = 'stripe';

function GetNewPosts() {
    setTimeout(function () {
        fetch('/api/get-new-posts').then(response => response.json()).then(posts => {
            posts.forEach(post_data => {
                const postElement = document.createElement('div');
                postElement.className = 'post';
                postElement.id = 'post';

                const topElement = document.createElement('div');
                topElement.className = 'top';
                postElement.appendChild(topElement);

                const profilePhotoContainer = document.createElement('div');
                profilePhotoContainer.className = 'profile_photo_container';
                topElement.appendChild(profilePhotoContainer);

                const profilePhotoLink = document.createElement('a');
                profilePhotoLink.href = '/profile/' + post_data.user.username;
                profilePhotoContainer.appendChild(profilePhotoLink);

                const profilePhoto = document.createElement('img');
                profilePhoto.src = post_data.user.profile_image;
                profilePhoto.className = 'profile_photo';
                profilePhotoLink.appendChild(profilePhoto);

                const usernameContainer = document.createElement('div');
                usernameContainer.className = 'username_container';
                topElement.appendChild(usernameContainer);

                const usernameLink = document.createElement('a');
                usernameLink.href = '/profile/' + post_data.user.username;
                usernameLink.className = 'username';
                usernameLink.textContent = post_data.user.username;
                usernameContainer.appendChild(usernameLink);

                const contentContainer = document.createElement('div');
                contentContainer.className = 'content_container';
                postElement.appendChild(contentContainer);

                const contentImage = document.createElement('img');
                contentImage.src = post_data.content;
                contentImage.className = 'content';
                contentImage.setAttribute('ondblclick', 'LikeClick(this)');
                contentContainer.appendChild(contentImage);

                const reactionContainer = document.createElement('div');
                reactionContainer.className = 'reaction_container';
                postElement.appendChild(reactionContainer);

                const like_comment = document.createElement('div');
                like_comment.style.display = "flex";
                reactionContainer.appendChild(like_comment)


                const buttonContainer1 = document.createElement('div');
                buttonContainer1.className = 'button_container';
                like_comment.appendChild(buttonContainer1);

                const likeBtn = document.createElement('div');
                likeBtn.className = 'like_btn';
                likeBtn.classList.add(post_data.is_user_liked ? 'active' : 'unactive')
                likeBtn.id = 'like_btn';
                likeBtn.setAttribute('onclick', 'LikeClick(this)');
                likeBtn.setAttribute('post-id', post_data.id);
                buttonContainer1.appendChild(likeBtn);

                const buttonContainer2 = document.createElement('div');
                buttonContainer2.className = 'button_container';
                like_comment.appendChild(buttonContainer2);

                const commentsLink = document.createElement('a');
                commentsLink.href = '/post/' + String(post_data.id);
                buttonContainer2.appendChild(commentsLink);

                const commentsImage = document.createElement('img');
                commentsImage.src = 'static/img/comments.png';
                commentsImage.className = 'comments_btn';
                commentsLink.appendChild(commentsImage);

                const likesCount = document.createElement('div');
                likesCount.className = 'likes_count';
                reactionContainer.appendChild(likesCount);

                const likesCountLink = document.createElement('a');
                likesCountLink.href = '#';
                likesCountLink.textContent = post_data.likes_count + ' отметок \"Нравится\"';
                likesCount.appendChild(likesCountLink);

                const descriptionContainer = document.createElement('div');
                descriptionContainer.className = 'description_container';
                postElement.appendChild(descriptionContainer);

                const descriptionUsernameLink = document.createElement('a');
                descriptionUsernameLink.href = '/profile/' + post_data.user.username;
                descriptionUsernameLink.className = 'username description';
                descriptionUsernameLink.textContent = post_data.user.username;
                descriptionContainer.appendChild(descriptionUsernameLink);

                const descriptionSpan = document.createElement('span');
                descriptionSpan.className = 'description';
                descriptionSpan.textContent = post_data.description;
                descriptionContainer.appendChild(descriptionSpan);

                posts_field.appendChild(postElement)
            })
        })
        posts_field.removeChild(stripe);
    }, 2000);
    posts_field.appendChild(stripe);
}

function deletePost(post_id) {
    fetch('/api/post', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            id: post_id
        })
    }).then(response => {
        if (response.ok)
            window.location.href = '..'
        else
            console.log(response.json())

    })
}

// GetNewPosts();



window.onload = function () {
    stripe.classList.add('animate-stripe');
}

