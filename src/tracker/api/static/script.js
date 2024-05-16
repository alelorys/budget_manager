function addOperation(){
              
    const formData = {
      name: document.getElementById('name').value,
      amount: parseFloat(document.getElementById('amount').value),
      type: document.getElementById("type").checked,
      category: document.getElementById('category').value
    };
    console.log(formData);

    fetch("http://127.0.0.1:2345/operations/add/",{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
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
  fetch("http://127.0.0.1:2345/register",{
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

