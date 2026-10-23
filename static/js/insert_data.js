function loadData() {
    const recieved_data = localStorage.getItem("recieved_data");
    console.log("Stored data:", recieved_data);

    if (recieved_data){
        const new_data = JSON.parse(recieved_data);
        document.getElementById("id").textContent = `ID: ${new_data[0]}`
        document.getElementById("url").textContent = `URL: ${new_data[1]}`
        document.getElementById("shortcode").textContent = `Short Code: ${new_data[2]}`
        document.getElementById("created_at").textContent = `Created At: ${new_data[3]}`
        document.getElementById("updated_at").textContent = `Last Updated: ${new_data[4]}`
        if (new_data[5]){
            document.getElementById("access_count").textContent = `Total number of accesses: ${new_data[5]}`
        }
    }
}


function returnToHome(){
    console.log("Returning")
    window.location.href = "homepage.html";
}


document.addEventListener("DOMContentLoaded", function(){
    loadData();
});