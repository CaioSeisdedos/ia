// frontend/script.js

document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            document.getElementById('response').innerHTML = 
                `<pre>${JSON.stringify(result.data, null, 2)}</pre>`;
        } else {
            document.getElementById('response').innerHTML = 
                `Erro: ${result.error}`;
        }
    } catch (error) {
        document.getElementById('response').innerHTML = 
            `Erro ao enviar o arquivo: ${error.message}`;
    }
});
