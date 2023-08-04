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

    // Button to send email
    document
        .querySelector("#compose-form")
        .addEventListener("submit", send_email);

    // By default, load the inbox
    load_mailbox("inbox");
});

function compose_email() {
    // Show compose view and hide other views
    document.querySelector("#emails-view").style.display = "none";
    document.querySelector("#compose-view").style.display = "block";

    // Clear out composition fields
    document.querySelector("#compose-recipients").value = "";
    document.querySelector("#compose-subject").value = "";
    document.querySelector("#compose-body").value = "";
}

function send_email(event) {
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
            // Print result
            console.log(result);

            // Load the sent mailbox
            load_mailbox("sent");
        });
}

function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector("#emails-view").style.display = "block";
    document.querySelector("#compose-view").style.display = "none";

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
                emailDiv.classList.add("p-1");

                // Add the email to the div
                emailDiv.innerHTML = `
                  <div class="row">
                    <span class="sender col-2">${email.sender}</span>
                    <span class="subject col-7">${email.subject}</span>
                    <span class="timestamp col-3 d-flex justify-content-end">${email.timestamp}</span>
                  </div>
                `;

                // Add the div to the view
                document.querySelector("#emails-view").append(emailDiv);

                // Add a click event listener to the div
                emailDiv.addEventListener("click", () => {
                    // Load the email
                    load_email(email.id, mailbox);
                });

                // If the email is read, add the class to the div
                if (!email.read) {
                    emailDiv.classList.add("bg-light-subtle");
                } else {
                    emailDiv.classList.add("read");
                    emailDiv.classList.add("bg-light");
                }
            });
        });
}
