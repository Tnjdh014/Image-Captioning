document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.querySelector('input[type="file"]');
    const fileNamesContainer = document.querySelector('.file-names'); // Select the container for file names
    const generatedCaptionsContainer = document.querySelector('.generated-captions'); // Select the container for generated captions

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('highlight');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('highlight');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('highlight');
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        const files = fileInput.files;
        handleFiles(files);
    });

    async function handleFiles(files) {
        const allowedTypes = ['image/jpeg', 'image/png']; // Allowed MIME types

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            if (allowedTypes.includes(file.type)) {
                // File is of an allowed type
                console.log(file.name); // Logging file names

                // Create elements for file name, remove button, and generate caption button
                const fileContainer = document.createElement('div');
                fileContainer.classList.add('file-container');

                const fileNameElement = document.createElement('p');
                fileNameElement.textContent = file.name;

                const removeButton = document.createElement('button');
                removeButton.textContent = 'Remove';
                removeButton.classList.add('remove-button');
                removeButton.addEventListener('click', () => {
                    fileContainer.remove(); // Remove file from the UI
                });

                const generateCaptionButton = document.createElement('button');
                generateCaptionButton.textContent = 'Generate Caption';
                generateCaptionButton.classList.add('generate-caption-button');
                generateCaptionButton.addEventListener('click', async () => {
                    const formData = new FormData();
                    formData.append('image', file); // Append the file to FormData

                    try {
                        const response = await fetch('/caption-image', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ image: file })
                        });
                        

                        if (response.ok) {
                            const data = await response.json();
                            console.log('Generated Caption:', data.caption);
                            const captionElement = document.createElement('p');
                            captionElement.textContent = data.caption;
                            generatedCaptionsContainer.appendChild(captionElement); // Append caption to the container
                        } else {
                            console.error('Failed to generate caption');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                    }
                });

                fileContainer.appendChild(fileNameElement);
                fileContainer.appendChild(removeButton);
                fileContainer.appendChild(generateCaptionButton); // Add the Generate Caption button
                fileNamesContainer.appendChild(fileContainer);
            } else {
                // File is not of an allowed type
                alert(`File ${file.name} is not a valid file. Please select a new file.`);
            }
        }
    }
});
