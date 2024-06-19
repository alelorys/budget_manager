const url = 'http://127.0.0.1:2345'
function addOperation(){    
    const body = document.body;
    const userId = body.dataset.userId;
    const token =  body.dataset.token;

    console.log(userId);
    console.log(token);
    const formData = {
      user_id: userId,
      name: document.getElementById('name').value,
      amount: parseFloat(document.getElementById('amount').value),
      type: document.getElementById("type").checked,
      category: document.getElementById('category').value
    };
    console.log(formData);

    fetch(url+"/operations/add/",{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization':`Bearer ${token}`,
        'Accept':'*/*',
        'Connection':'keep-alive',
        'Accept-Encoding':'gzip, deflate, br'},
      body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error)
    });
  }

function addUser(){
  const registerData = {
    login: document.getElementById('login').value,
    name: document.getElementById('name').value,
    lastname: document.getElementById('lastname').value,
    password: document.getElementById('password').value
  };

  
  console.log(registerData);
  fetch(url+"/register",{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
        'Accept':'*/*',
        'Connection':'keep-alive',
        'Accept-Encoding':'gzip, deflate, br'
    },
    body: JSON.stringify(registerData)
  })
  .then(function(response){
    if (response.status === 422){
        alert("Użytkownik o tej nazwie już istnieje");
    }
    else if (response.status === 200){
      alert("Dodano pomyślnie")
    }
  })
  .then(data => console.log(data))
  .catch((error) => {
    console.error("Error:", error)
  });
}

/*document.getElementById('loginForm').addEventListener("submit", function(event){
  event.preventDefault();

  var loginData = new FormData(event.target);

  fetch('/token',{
      method:'POST',
      body: loginData
  })
  .then(response => response.json())
  .then(data =>{
      localStorage.setItem('token', data.access_token);
      window.location.href = '/services/list';
  })
  .catch(error => console.error('Error:', error));
});*/