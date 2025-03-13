let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    let userCredentials = {
        'username' : form.username.value,
        'password' : form.password.value
    }

    fetch('http://127.0.0.1:8000/api/users/token/', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(userCredentials)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.access)
        
        if (data.access){
            localStorage.setItem('token', data.access)
            window.location = 'file:///Users/anthoskountouris/Desktop/Front-end-api-test/projects-list.html'
        } else {
            alert('Username or password did not work')
        }
    })

})