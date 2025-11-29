// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('pdf-file');
const fileLabel = document.getElementById('file-label');
const fileNameDisplay = document.getElementById('file-name');
const roastBtn = document.getElementById('roast-btn');
const loader = document.getElementById('loader');
const loadingText = document.getElementById('loading-text');
const resultsArea = document.getElementById('results-area');

// Funny loading messages to keep user entertained while waiting
const loadingMessages = [
    "Scanning for typos...",
    "Judging your font choices...",
    "Laughing at your 'Skills' section...",
    "Consulting the Roast Master...",
    "Preparing emotional damage...",
    "Generating brutally honest feedback..."
];

// --- FILE UPLOAD HANDLING ---
dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', handleFileSelect);

// Drag and drop effects
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#ff4b4b';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#30363d';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#30363d';
    fileInput.files = e.dataTransfer.files;
    handleFileSelect();
});

function handleFileSelect() {
    if (fileInput.files.length > 0) {
        const name = fileInput.files[0].name;
        fileNameDisplay.innerText = name;
        fileLabel.innerText = "File Selected:";
        roastBtn.disabled = false;
        // Hide previous results if they upload a new file
        resultsArea.classList.add('hidden');
    }
}

// --- ROAST ACTION ---
async function startRoast() {
    if (!fileInput.files[0]) {
        alert("Please upload a PDF first!");
        return;
    }

    // UI Updates
    roastBtn.disabled = true;
    roastBtn.innerText = "ROASTING...";
    loader.style.display = 'block';
    resultsArea.classList.add('hidden');

    // Cycle through funny text
    let msgIndex = 0;
    const msgInterval = setInterval(() => {
        loadingText.innerText = loadingMessages[msgIndex];
        msgIndex = (msgIndex + 1) % loadingMessages.length;
    }, 3000);

    // Prepare Data
    const formData = new FormData();
    formData.append('file', fileInput.files[0]); // This matches 'file' in app.py

    try {
        // Send to Backend
        const response = await fetch('/roast', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        clearInterval(msgInterval); // Stop loading text

        if (data.error) {
            alert("Error: " + data.error);
        } else {
            displayResults(data);
        }

    } catch (error) {
        clearInterval(msgInterval);
        console.error("Error:", error);
        alert("Something went wrong. The Roast Master is sleeping.");
    } finally {
        // Reset UI state
        loader.style.display = 'none';
        roastBtn.innerText = "ROAST ME";
        roastBtn.disabled = false;
    }
}

function displayResults(data) {
    // 1. Set Rating Color based on score
    const scoreElement = document.getElementById('rating-score');
    scoreElement.innerText = `${data.rating}/10`;
    
    if (data.rating < 5) scoreElement.style.color = "#ff4b4b"; // Red
    else if (data.rating < 8) scoreElement.style.color = "#ffa500"; // Orange
    else scoreElement.style.color = "#2ea043"; // Green

    // 2. Set Roast Text
    document.getElementById('roast-content').innerText = `"${data.roast_critique}"`;

    // 3. Set Advice List
    const list = document.getElementById('advice-list');
    list.innerHTML = ""; // Clear old list
    
    data.professional_suggestions.forEach(tip => {
        const li = document.createElement('li');
        li.innerText = tip;
        list.appendChild(li);
    });

    // 4. Reveal Section
    resultsArea.classList.remove('hidden');
    
    // Auto scroll to results
    resultsArea.scrollIntoView({ behavior: 'smooth' });
}