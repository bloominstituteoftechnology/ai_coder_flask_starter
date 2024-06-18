window.onload = function() {
    document.getElementById('download-btn').setAttribute("disabled", "");
}

document.getElementById('prompt-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    document.getElementById('submit').setAttribute("disabled", "");
    const prompt = document.getElementById('prompt').value;
    const spinner = document.getElementById('spinner');
    spinner.style.display = 'block';
    const response = await fetch('/api/prompt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
    });

    const data = await response.text();
    const responseContainer = document.getElementById('response-container');
    responseContainer.innerHTML = '<pre>' + data + '</pre>';
    document.getElementById('download-btn').removeAttribute("disabled");
    spinner.style.display = 'none';
    document.getElementById('prompt').value = "";
});

document.getElementById('download-btn').addEventListener('click', function() {
    console.log("downloading...");
    window.location.href = '/api/download';
    document.getElementById('submit').removeAttribute("disabled");
    document.getElementById('download-btn').setAttribute("disabled", "");
});
