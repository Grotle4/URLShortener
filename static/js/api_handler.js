const apiUrl = 'http://127.0.0.1:5000'

async function sendEntry(){
    const url = document.getElementById('url').value;
    const urlData = {"url": url}
    const apiCall = '/shorten'

    const response = await fetch(apiUrl+apiCall,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(urlData)
    })
    .then (response =>{
        if (!response.ok){
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data =>{
        console.log('Success from API', data);
    })
    .catch(error =>{
        console.error('Error:', error);
    })
    
}

async function getEntry(){
    const shortcode = document.getElementById('retrieve_shortcode').value;
    const apiCall = `/shorten/${shortcode}`;

    const response = await fetch(apiUrl+apiCall,{
        method: 'GET',
    })
    .then (response =>{
        if (!response.ok){
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data =>{
        console.log('Success from API', data);
        localStorage.setItem("recieved_data", JSON.stringify(data));
        window.location.href = "entry_page.html";
    })
    .catch(error =>{
        console.error('Error:', error);
    })
}

async function updateEntry(){
    const shortcode = document.getElementById('update_shortcode').value;
    const url = document.getElementById('update_url').value;
    const apiCall = `/shorten/${shortcode}`;
    const urlData = {"url": url}

    const response = await fetch(apiUrl+apiCall,{
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(urlData)
    })
    .then (response =>{
        if (!response.ok){
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data =>{
        console.log('Success from API', data);
    })
    .catch(error =>{
        console.error('Error:', error);
    })
}

async function deleteEntry(){
    const shortcode = document.getElementById('delete_shortcode').value;
    const apiCall = `/shorten/${shortcode}`;

    const response = await fetch(apiUrl+apiCall,{
        method: 'DELETE',
    })
    .then (response =>{
        if (!response.ok){
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data =>{
        console.log('Success from API', data);
    })
    .catch(error =>{
        console.error('Error:', error);
    })
    
}

async function getEntryStats(){
    //Need to remove access_count from dict if not loading stats menu.
    const shortcode = document.getElementById('retrieve_shortcode').value;
    const apiCall = `/shorten/${shortcode}/stats`;

    const response = await fetch(apiUrl+apiCall,{
        method: 'GET',
    })
    .then (response =>{
        if (!response.ok){
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data =>{
        console.log('Success from API', data);
        localStorage.setItem("recieved_data", JSON.stringify(data));
        window.location.href = "entry_page.html";
    })
    .catch(error =>{
        console.error('Error:', error);
    })
}