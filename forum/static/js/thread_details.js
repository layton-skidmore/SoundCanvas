
const toggleButtonPost = document.getElementById('post_button');
const formDivPost = document.getElementById('form-div');

toggleButtonPost.addEventListener('click', function() {
    formDivPost.style.display = formDivPost.style.display === 'none' ? 'block' : 'none';

});

const toggleButtonThread = document.getElementById('thread_button');

const formDivThread = document.getElementById('form-div-thread');

const title_val = document.getElementById('title').textContent;
const text_val = document.getElementById('text').textContent;

const titleEl = document.getElementById('form_title');
const textEl = document.getElementById('form_text');

if (formDivThread) {

    toggleButtonThread.addEventListener('click', function() {
        formDivThread.style.display = formDivThread.style.display === 'none' ? 'block' : 'none';
        titleEl.value = title_val
        textEl.innerHTML = text_val
    });

}
    

const form = document.getElementById('form');
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const postsContainer = document.getElementById('posts-container');
const inputTextEl = document.getElementById('id_text');

let editButtons = document.querySelectorAll("#edit-post-button");

form.addEventListener('submit', async (event) => {

    // stop form from submitting
    event.preventDefault();

    // value from form 
    const text = inputTextEl.value

    console.log(text)

    // supposed to reset input field to be blank
    // does not work because of browser caching
    inputTextEl.value = "";

    formDivPost.style.display = formDivPost.style.display === 'none' ? 'block' : 'none';

    

    
    
    // get path/ action of form
    const action = form.getAttribute('action');
    
    try {
        const response = await fetch(action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
            }),
    });

    
    const data = await response.json();

    if (data.message === 'Post added successfully') {

        console.log("here")

        postsContainer.innerHTML = '';

        // add the new posts to the posts container
        const newPosts = data.posts;
        // create div for each post
        newPosts.forEach(post => {

            const postElement = document.createElement('div');


            let postHTML = `
                <h2>${post.text}</h2>
                <p>${post.upvotes}</p>
                <button>&#8679;</button><button>&#8681;</button>
            `;

            if (post.user === data.user_id) {

                postHTML += `
                    <button id="edit-post-button">&#9999;&#65039;</button>

                    <div id="edit-form-post" style="display: none;">
                        <form id="form-post" action="/forum/${data.category_id}/${data.thread_id}/${post.id}/edit/" method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <p>
                            <label>Text:</label>
                            <textarea name="text" cols="40" rows="10" maxlength="3000" id="form_text" required>${post.text}</textarea> 
                        </p>
                            <input type="submit" value="Update Post">
                        </form>

                        <a href="/forum/${data.category_id}/${data.thread_id}/${post.id}/delete/">Delete This Post</a>
                    </div>
                `;
            }

            postElement.innerHTML = postHTML
            postElement.id = `${post.id}`
        
            postsContainer.appendChild(postElement);
        });
    }

    } catch (error) {
        console.log(error)
    }

    editButtons = document.querySelectorAll("#edit-post-button");
    editButtons.forEach(editButton => {
        editButton.addEventListener("click", (event) => {
            const formDiv = event.target.nextElementSibling;
    
            // Show or hide the form div based on your logic
            formDiv.style.display = formDiv.style.display === 'none' ? 'block' : 'none';

        });
    });
});


editButtons.forEach(editButton => {
    editButton.addEventListener("click", (event) => {
        const formDiv = event.target.nextElementSibling;

        // Show or hide the form div based on your logic
        formDiv.style.display = formDiv.style.display === 'none' ? 'block' : 'none';

    });
});

// function showForm(event) {

// }

  