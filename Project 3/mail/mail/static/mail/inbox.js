document.addEventListener("DOMContentLoaded", function () {
    // Use buttons to toggle between views
    document
        .querySelector("#inbox")
        .addEventListener("click", () => load_mailbox("inbox"));
    document
        .querySelector("#sent")
        .addEventListener("click", () => load_mailbox("sent"));
    document
        .querySelector("#archived")
        .addEventListener("click", () => load_mailbox("archive"));
    document.querySelector("#compose").addEventListener("click", compose_email);

    // Add a click event listener to the submit button
    document
        .querySelector("#compose-form")
        .addEventListener("submit", send_email);

    // By default, load the inbox
    load_mailbox("inbox");
});

function compose_email() {
    // Show compose view and hide other views
    document.querySelector("#emails-view").style.display = "none";
    document.querySelector("#email-details-view").style.display = "none";
    document.querySelector("#compose-view").style.display = "block";

    // Clear out composition fields
    document.querySelector("#compose-recipients").value = "";
    document.querySelector("#compose-subject").value = "";
    document.querySelector("#compose-body").value = "";
}

function send_email(event) {
    // Prevent the form from submitting
    event.preventDefault();

    // Get the values from the form
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    // Send the email
    fetch("/emails", {
        method: "POST",
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body,
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            // Load the sent mailbox
            load_mailbox("sent");
        });
}

function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector("#emails-view").style.display = "block";
    document.querySelector("#compose-view").style.display = "none";
    document.querySelector("#email-details-view").style.display = "none";

    // Show the mailbox name
    document.querySelector("#emails-view").innerHTML = `<h3>${
        mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
    }</h3>`;

    // Get the emails
    fetch(`/emails/${mailbox}`)
        .then((response) => response.json())
        .then((emails) => {
            // loop through the emails
            emails.forEach((email) => {
                // Create a div for the email
                const emailDiv = document.createElement("div");

                // Add classes to the div
                emailDiv.classList.add("email");
                emailDiv.classList.add("border");
                emailDiv.classList.add("border-dark");
                emailDiv.classList.add("p-1");

                // Add the email to the div
                emailDiv.innerHTML = `
                  <div class="row">
                    <span class="sender col-3"><i class="bi bi-person-circle"></i> &nbsp; ${email.sender}</span>
                    <span class="subject col-6"><i class="bi bi-envelope"></i> &nbsp; ${email.subject}</span>
                    <span class="timestamp col-3 d-flex justify-content-end"><i class="bi bi-calendar"></i> &nbsp; ${email.timestamp}</span>
                  </div>
                `;

                // Add the div to the view
                document.querySelector("#emails-view").append(emailDiv);

                // Add a click event listener to the div
                emailDiv.addEventListener("click", () => {
                    // View the email
                    view_email(email.id, mailbox);
                });

                // Change the class, border, and bg of the div if the email is read or unread
                if (email.read) {
                    emailDiv.classList.add("read");
                    emailDiv.classList.add("bg-secondary");
                    emailDiv.classList.add("text-body");
                } else {
                    emailDiv.classList.remove("read");
                    emailDiv.classList.remove("bg-secondary");
                    emailDiv.classList.remove("text-body");
                }
            });
        });
}

function view_email(email_id, mailbox) {
    // Get the email
    fetch(`/emails/${email_id}`)
        .then((response) => response.json())
        .then((email) => {
            // Mark the email as read
            fetch(`/emails/${email_id}`, {
                method: "PUT",
                body: JSON.stringify({
                    read: true,
                }),
            });

            // Show the email details and hide other views
            document.querySelector("#emails-view").style.display = "none";
            document.querySelector("#compose-view").style.display = "none";
            document.querySelector("#email-details-view").style.display =
                "block";

            // Inside the email view
            document.querySelector("#email-details-view").innerHTML = `
                <h3>${email.subject}</h3>
                <div class="row">
                  <div class="d-flex flex-column col-8">
                    <span><strong>From:</strong> ${email.sender}</span>
                    <span><strong>To:</strong> ${email.recipients}</span>
                    <span><strong>Timestamp:</strong> ${email.timestamp}</span>
                  </div>

                  <div class="col-4 d-flex justify-content-end">
                    <div>
                      <div class="btn-group" role="group">
                        <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
                        <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
                      </div>
                    </div>
                  </div>
                </div>

                <hr>

                <div>${email.body}</div>
            `;

            console.log(email);

            // Change the archive button text depending on the mailbox
            if (email.archived === true) {
                document.querySelector("#archive").innerHTML = "Unarchive";
            } else {
                document.querySelector("#archive").innerHTML = "Archive";
            }

            // Add a click event listener to the archive button
            document.querySelector("#archive").addEventListener("click", () => {
                // Archive or unarchive the email
                archive_email(email_id, email.archived);
            });

            // Add a click event listener to the reply button
            document.querySelector("#reply").addEventListener("click", () => {
                // Show the compose view and hide other views
                compose_email();

                // Pre-fill the composition fields
                document.querySelector("#compose-recipients").value =
                    email.sender;
                document.querySelector(
                    "#compose-subject"
                ).value = `Re: ${email.subject}`;
                document.querySelector(
                    "#compose-body"
                ).value = `"On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n\n"`;
            });
        });
}

function archive_email(email_id, archived) {
    // Archive or unarchive the email
    fetch(`/emails/${email_id}`, {
        method: "PUT",
        body: JSON.stringify({
            archived: !archived,
        }),
    }).then(() => {
        // Load the inbox
        load_mailbox("archive");
    });
}
