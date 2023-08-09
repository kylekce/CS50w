function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(";").shift();
}

// Replace the contents of the post into textarea with the contents of the post
addEventListener("DOMContentLoaded", () => {
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
});
