const apiUrl = 'http://127.0.0.1:5000'

async function sendEntry(){
    const url = document.getElementById('url').value;
    const urlData = {"url": url}
    const apiCall = '/shorten'

    try {
        const response = await fetch(apiUrl+apiCall,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(urlData)
        });
        const data = await readApiResponse(response);

        if (!response.ok){
            throw new Error(getApiMessage(data, `Request failed (${response.status})`));
        }

        console.log('Success from API', data);
        document.getElementById("status_message").textContent =
            getApiMessage(data, "Request completed successfully.");
        clearElements();
    } catch (error) {
        console.error(error);
        document.getElementById("status_message").textContent =
            error instanceof Error ? error.message : String(error);
    }
}

async function getEntry(){
    const shortcode = document.getElementById('retrieve_shortcode').value;
    const apiCall = `/shorten/${shortcode}`;

    try {
        const response = await fetch(apiUrl+apiCall,{
            method: 'GET',
        });
        const data = await readApiResponse(response);

        if (!response.ok){
            throw new Error(getApiMessage(data, `Request failed (${response.status})`));
        }

        console.log('Success from API', data);
        localStorage.setItem("recieved_data", JSON.stringify(data));
        window.location.href = "entry_page.html";
    } catch (error) {
        console.error(error);
        document.getElementById("status_message").textContent =
            error instanceof Error ? error.message : String(error);
    }
}

async function updateEntry(){
    const shortcode = document.getElementById('update_shortcode').value;
    const url = document.getElementById('update_url').value;
    const apiCall = `/shorten/${shortcode}`;
    const urlData = {"url": url}

    try {
        const response = await fetch(apiUrl+apiCall,{
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(urlData)
        });
        const data = await response.json();

        if (!response.ok){
            throw new Error(data.message || `Request failed (${response.status})`);
        }

        console.log('Success from API', data);
        document.getElementById("status_message").textContent = String(data.message);
        clearElements();
    } catch (error) {
        console.error(error);
        document.getElementById("status_message").textContent =
            error instanceof Error ? error.message : String(error);
    }
}

async function deleteEntry(){
    const shortcode = document.getElementById('delete_shortcode').value;
    const apiCall = `/shorten/${shortcode}`;

    try {
        const response = await fetch(apiUrl+apiCall,{
            method: 'DELETE',
        });
        const data = await readApiResponse(response);

        if (!response.ok){
            throw new Error(getApiMessage(data, `Request failed (${response.status})`));
        }

        console.log('Success from API', data);
        document.getElementById("status_message").textContent =
            getApiMessage(data, "Request completed successfully.");
        clearElements();
    } catch (error) {
        console.error(error);
        document.getElementById("status_message").textContent =
            error instanceof Error ? error.message : String(error);
    }
}

async function getEntryStats(){
    const shortcode = document.getElementById('stats_shortcode').value;
    if (shortcode == ""){
        document.getElementById("status_message").textContent = "Failed to fetch"
        throw new Error("Failed to fetch");
    }
    const apiCall = `/shorten/${shortcode}/stats`;

    try {
        const response = await fetch(apiUrl+apiCall,{
            method: 'GET',
        });
        const data = await readApiResponse(response);

        if (!response.ok){
            throw new Error(getApiMessage(data, `Request failed (${response.status})`));
        }

        console.log('Success from API', data);
        localStorage.setItem("recieved_data", JSON.stringify(data));
        window.location.href = "entry_page.html";
    } catch (error) {
        console.error(error);
        document.getElementById("status_message").textContent =
            error instanceof Error ? error.message : String(error);
    }
}

async function readApiResponse(response){
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")){
        return response.json();
    }
    return response.text();
}

function getApiMessage(data, fallback){
    if (typeof data === "string" && data){
        return data;
    }
    if (data && typeof data.message === "string"){
        return data.message;
    }
    return fallback;
}

function clearElements(){
    document.getElementById("url").value = "";
    document.getElementById("retrieve_shortcode").value = "";
    document.getElementById("update_shortcode").value = "";
    document.getElementById("update_url").value = "";
    document.getElementById("delete_shortcode").value = "";
    document.getElementById("stats_shortcode").value = "";
}