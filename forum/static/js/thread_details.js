
const toggleButtonPost = document.getElementById('post_button');
const formDivPost = document.getElementById('form-div');



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
const h2 = document.getElementById('h2');
const p = document.getElementById('p');


let editButtons = document.querySelectorAll("#edit-post-button");

form.addEventListener('submit', async (event) => {

    // stop form from submitting
    event.preventDefault();

    // value from form 
    const text = inputTextEl.value

    // reset input field to be blank
    inputTextEl.value = "";

    
    // get path/ action of form
    const action = form.getAttribute('action');
    
    // send info to django backend
    // await response
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

        // reset postContainer to have no posts
        postsContainer.innerHTML = '';

        // variable to hold list of posts
        const newPosts = data.posts;

        // create div for each post
        newPosts.forEach(post => {

            const postElement = document.createElement('div');


            let postHTML = `
                <p class="text-gray-700 text-sm inline pr-1">${post.username}</p>
            `;

            if (post.user === data.user_id) {
                postHTML += `
                    <p class="text-gray-400 text-sm inline pr-1">this is your post</p>
                    <button id="edit-post-button">&#9999;&#65039;</button>
                `
            }

            postHTML += `
                <div class="pl-2 my-0.5">
                <h2>${post.text}</h2>
            `

            if (post.user === data.user_id) {
                postHTML += `
                    <div id="edit-form-post" style="display: none;" class="bg-blue-500 text-center pt-6 pb-2">
                        <form id="form-post" action="/forum/${data.category_id}/${data.thread_id}/${post.id}/edit/" method="POST">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <p>

                                <textarea name="text" cols="40" rows="10" maxlength="3000" id="form_text" required>${post.text}</textarea> 
                            </p>
                            <input class="styled-button" type="submit" value="Update Post">
                        </form>

                        <a class="styled-button" href="/forum/${data.category_id}/${data.thread_id}/${post.id}/delete/">Delete This Post</a>
                    </div>
                `
            }

            postHTML += `
            </div>
            `

            postElement.innerHTML = postHTML
            postElement.id = "header"
        
            postsContainer.appendChild(postElement);
        });
    }

    } catch (error) {
        console.log(error)
    }

    editButtons = document.querySelectorAll("#edit-post-button");
    editButtons.forEach(editButton => {
        editButton.addEventListener("click", (event) => {

            const postContainer = event.target.closest('#header');

            const formDiv = postContainer.querySelector('#edit-form-post');
    
            // toggle form
            formDiv.style.display = formDiv.style.display === 'none' ? 'block' : 'none';

        });
    });

    // if first post delete the sample text
    if (h2) {
        h2.remove();
    }
    
    if (p) {
        p.remove();
    }
});

// 
editButtons.forEach(editButton => {
    editButton.addEventListener("click", (event) => {
      
        const postContainer = event.target.closest('#header');

        const formDiv = postContainer.querySelector('#edit-form-post');

        // toggle form
        formDiv.style.display = formDiv.style.display === 'none' ? 'block' : 'none';

    });
});

  