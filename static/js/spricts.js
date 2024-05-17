function uploadImage(event) {
    event.preventDefault(); // Prevent default form submission

    const fileInput = document.getElementById('file');
    if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
        console.error('No file selected');
        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('image', file);

    fetch('/process-image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const outputBox1 = document.getElementById('info');
        const outputBox2 = document.getElementById('info2');
        
        outputBox1.innerHTML = ''; // Clear previous content in output box 1
        outputBox2.innerHTML = ''; // Clear previous content in output box 2

        // Display image in output box 1
        const image = document.createElement('img');
        image.src = URL.createObjectURL(file);
        image.style.width = '100%'; // Ensure the image fits the box width
        image.style.height = '100%'; // Ensure the image fits the box height
        image.style.objectFit = 'cover'; // Maintain aspect ratio and cover entire box
        outputBox1.appendChild(image);

        // Display information in output box 2
        const titleElement = document.createElement('h2');
        titleElement.textContent = JSON.stringify(data.info[0]);
        titleElement.style.fontSize = '1.5em'; // Adjust font size as needed
        outputBox2.appendChild(titleElement);

        const listElement = document.createElement('ul');
        listElement.style.fontSize = '1em'; // Adjust font size as needed
        for (let i = 1; i < data.info.length; i++) {
            const listItem = document.createElement('li');
            listItem.textContent = JSON.stringify(data.info[i]);
            listElement.appendChild(listItem);
        }
        outputBox2.appendChild(listElement);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
