// Get the CSRF token from the cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(";").shift();
}

addEventListener("DOMContentLoaded", () => {
    // Replace the contents of the post into textarea with the contents of the post
    document.querySelectorAll("#edit").forEach((button) => {
        button.onclick = () => {
            const post_id = button.dataset.post;
            const post = document.querySelector(`#post-${post_id}`);
            const post_content = post.innerHTML;

            // Replace the contents of the post into textarea with the contents of the post
            post.innerHTML = `<textarea id="post-${post_id}-edit" class="form-control mb-2">${post_content}</textarea>`;

            // Add a div to the post to hold the buttons
            const buttons_div = document.createElement("div");
            buttons_div.className = "d-flex justify-content-end";
            post.append(buttons_div);

            // Add a cancel button to the post
            const cancel_button = document.createElement("button");
            cancel_button.innerHTML = "Cancel";
            cancel_button.className = "btn btn-secondary mx-2";
            buttons_div.append(cancel_button);

            cancel_button.onclick = () => {
                post.innerHTML = post_content;
            };

            // Add a save button to the post
            const save_button = document.createElement("button");
            save_button.innerHTML = "Save";
            save_button.className = "btn btn-primary";
            buttons_div.append(save_button);

            save_button.onclick = () => {
                edited_post = document.querySelector(
                    `#post-${post_id}-edit`
                ).value;
                post.innerHTML = edited_post;

                // Send a POST request to the server to update the content
                fetch(`/edit/${post_id}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                    body: JSON.stringify({
                        content: edited_post,
                    }),
                }).then((response) => {
                    if (response.status != 200) {
                        alert("Error updating post");
                    }
                });
            };
        };
    });

    // Update the like count of each post
    document.querySelectorAll("#like_count").forEach((like_count) => {
        post_id = parseInt(like_count.dataset.post);

        // Send a GET request to the server to get the like count of the post
        fetch(`/like_count/${post_id}`).then((response) => {
            response.json().then((data) => {
                like_count.innerHTML = data.like_count;
            });
        });
    });

    // Like or Unlike button
    const like_button = document
        .querySelectorAll("#like_button")
        .forEach((button) => {
            button.onclick = () => {
                post_id = parseInt(button.dataset.post);
                user_id = button.dataset.user;

                // Send a GET request to the server to get the user's liked posts
                fetch(`/likes/${user_id}`)
                    .then((response) => response.json())
                    .then((data) => {
                        liked_posts = data.liked_posts;

                        // Check if post_id is in liked_posts
                        if (liked_posts.indexOf(post_id) >= 0) {
                            // Send a POST request to the server to remove a like
                            fetch(`/unlike/${post_id}`).then((response) => {
                                if (response.status != 200) {
                                    alert("Error unliking a post.");
                                }
                            });

                            // Change the button to "Like"
                            button.innerHTML = `<i class="bi bi-heart"></i>`;

                            // Update the like count of the post
                            like_count = document.querySelector(
                                `#like_count[data-post="${post_id}"]`
                            );
                            old_like_count = parseInt(like_count.innerHTML);
                            like_count.innerHTML = old_like_count - 1;
                        } else {
                            // Send a POST request to the server to add a like
                            fetch(`/like/${post_id}`).then((response) => {
                                if (response.status != 200) {
                                    alert("Error liking a post.");
                                }
                            });

                            // Change the button to "Unlike"
                            button.innerHTML = `<i class="bi bi-heart-fill text-danger"></i>`;

                            // Update the like count of the post
                            like_count = document.querySelector(
                                `#like_count[data-post="${post_id}"]`
                            );
                            old_like_count = parseInt(like_count.innerHTML);
                            like_count.innerHTML = old_like_count + 1;
                        }
                    });
            };
        });
});
