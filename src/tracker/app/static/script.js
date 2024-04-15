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