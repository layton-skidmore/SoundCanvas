
const toggleButton = document.getElementById('post_button');
const formDiv = document.getElementById('form-div');

toggleButton.addEventListener('click', function() {
    formDiv.style.display = formDiv.style.display === 'none' ? 'block' : 'none';

});


const form = document.getElementById('form');
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const postsContainer = document.getElementById('posts-container');
const textEl = document.getElementById('id_text');


form.addEventListener('submit', async (event) => {

    const text = textEl.value

    // supposed to reset input field to be blank
    // does not work because of browser caching
    textEl.value = "";

    formDiv.style.display = formDiv.style.display === 'none' ? 'block' : 'none';

    

    // stop form from submitting
    event.preventDefault();
    
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

        

        postsContainer.innerHTML = '';

        // add the new posts to the posts container
        const newPosts = data.posts;
        // create div for each post
        newPosts.forEach(post => {

            const postElement = document.createElement('div');


            postElement.innerHTML = `
                <h2>${post.text}</h2>
                <p>${post.upvotes}</p>
                <button>&#8679;</button><button>&#8681;</button>
            `;
            postElement.id = `${post.id}`
        
            postsContainer.appendChild(postElement);
        });
    }

    } catch (error) {
        console.log(error)
    }
});

  