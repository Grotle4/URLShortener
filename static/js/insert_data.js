function loadData(){
    const recieved_data = localStorage.getItem("recieved_data");
    if (recieved_data){
        const new_data = JSON.parse(recieved_data);
        document.getElementById("id").textContent = new_data.id
        document.getElementById("url").textContent = new_data.url
        document.getElementById("shortcode").textContent = new_data.shortcode
        document.getElementById("created_at").textContent = new_data.created_at
        document.getElementById("updated_at").textContent = new_data.updated_at
        document.getElementById("access_count").textContent = new_data.access_count
    }
}

document.addEventListener("DOMContentLoaded", function(){
    loadData();
});