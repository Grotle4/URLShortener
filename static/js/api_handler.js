 const apiUrl = 'http://127.0.0.1:5000'

async function getEntry(){
    const rawString = document.getElementById('retrieve_shortcode').value;
    const shortcode = encodeURIComponent(rawString);
    const apiCall = `/shorten/${shortcode}`;

    try {
        const response = await fetch(apiUrl+apiCall);
        const data = await response.json()
        document.getElementById('responseOutput').innerText = data.message;
    }
    catch (error){
        console.error('Error communicating with API:', error)
    }
}

async function sendEntry(){
    const rawString = document.getElementById('url').value;
    const url = encodeURIComponent(rawString);
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