document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let formData = new FormData(this);
    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(imageBlob => {
        // Create a URL for the image blob
        let imgURL = URL.createObjectURL(imageBlob);
        
        // Display the image result
        let resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<h3>Sketch Result:</h3><img id="sketchImage" src="${imgURL}" alt="Sketch Result">`;
        
        // Hide the Convert button and show the Download button
        let convertButton = document.getElementById('convertButton');
        convertButton.style.display = 'none'; // Hide convert button
        
        let downloadButton = document.getElementById('downloadButton');
        downloadButton.href = imgURL; // Set the download URL
        downloadButton.style.display = 'inline'; // Show download button
    })
    .catch(error => console.error('Error:', error));
});

// Add an event listener to detect when a new file is selected
document.getElementById('imageUpload').addEventListener('change', function() {
    // Show the Convert button again and hide the Download button
    let convertButton = document.getElementById('convertButton');
    let downloadButton = document.getElementById('downloadButton');
    
    convertButton.style.display = 'inline'; // Show Convert button
    downloadButton.style.display = 'none';  // Hide Download button
});
