// ============================================================
// SMARTVISION AI - FRONTEND
// ============================================================

const API_BASE = "http://127.0.0.1:8000";

console.log("SmartVision frontend loaded");

// ============================================================
// DOM ELEMENTS
// ============================================================

const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const dropArea = document.getElementById("dropArea");
const dropContent = document.getElementById("dropContent");
const previewImage = document.getElementById("previewImage");
const analyzeBtn = document.getElementById("analyzeBtn");

const verdict = document.getElementById("verdict");

const sharpness = document.getElementById("sharpness");
const brightness = document.getElementById("brightness");
const contrast = document.getElementById("contrast");
const noise = document.getElementById("noise");
const saturation = document.getElementById("saturation");
const entropy = document.getElementById("entropy");
const edgeDensity = document.getElementById("edge_density");

const width = document.getElementById("width");
const height = document.getElementById("height");

const sharpnessBar = document.getElementById("sharpnessBar");
const brightnessBar = document.getElementById("brightnessBar");
const contrastBar = document.getElementById("contrastBar");
const noiseBar = document.getElementById("noiseBar");
const saturationBar = document.getElementById("saturationBar");
const entropyBar = document.getElementById("entropyBar");
const edgeBar = document.getElementById("edgeBar");

const message = document.getElementById("message");

const apiDot = document.getElementById("apiDot");
const apiStatus = document.getElementById("apiStatus");
const latency = document.getElementById("latency");

const history = document.getElementById("history");
const recordCount = document.getElementById("recordCount");
const refreshBtn = document.getElementById("refreshBtn");


// ============================================================
// SELECTED FILE
// ============================================================

let selectedFile = null;


// ============================================================
// FORMAT NUMBER
// ============================================================

function formatNumber(value) {

    if (value === null || value === undefined) {
        return "—";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
        return "—";
    }

    return number.toFixed(4);
}


// ============================================================
// SET BAR
// ============================================================

function setBar(element, value, maxValue = 100) {

    if (!element) return;

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(Number(value))
    ) {
        element.style.width = "0%";
        return;
    }

    let percent =
        (Number(value) / maxValue) * 100;

    percent = Math.max(
        0,
        Math.min(100, percent)
    );

    element.style.width = `${percent}%`;
}


// ============================================================
// RESET FEATURES
// ============================================================

function resetFeatures() {

    sharpness.textContent = "—";
    brightness.textContent = "—";
    contrast.textContent = "—";
    noise.textContent = "—";
    saturation.textContent = "—";
    entropy.textContent = "—";
    edgeDensity.textContent = "—";

    width.textContent = "—";
    height.textContent = "—";

    sharpnessBar.style.width = "0%";
    brightnessBar.style.width = "0%";
    contrastBar.style.width = "0%";
    noiseBar.style.width = "0%";
    saturationBar.style.width = "0%";
    entropyBar.style.width = "0%";
    edgeBar.style.width = "0%";
}


// ============================================================
// DISPLAY ANALYSIS RESULT
// ============================================================

function displayAnalysis(data) {

    console.log("Displaying analysis:", data);

    if (!data) {
        console.error("No analysis data received");
        return;
    }

    // --------------------------------------------------------
    // Prediction
    // --------------------------------------------------------

    if (data.prediction) {

        const predictionText =
            String(data.prediction).replace(
                /_/g,
                " "
            ).toUpperCase();

        const confidence =
            data.confidence !== undefined
                ? ` — ${(Number(data.confidence) * 100).toFixed(1)}%`
                : "";

        verdict.textContent =
            `${predictionText}${confidence}`;
    }


    // --------------------------------------------------------
    // Features
    // --------------------------------------------------------

    const features = data.features;

    console.log("FEATURES RECEIVED:", features);

    if (!features) {

        console.error(
            "No features object found in API response"
        );

        return;
    }


    // --------------------------------------------------------
    // Put values into Feature Matrix
    // --------------------------------------------------------

    sharpness.textContent =
        formatNumber(features.sharpness);

    brightness.textContent =
        formatNumber(features.brightness);

    contrast.textContent =
        formatNumber(features.contrast);

    noise.textContent =
        formatNumber(features.noise);

    saturation.textContent =
        formatNumber(features.saturation);

    entropy.textContent =
        formatNumber(features.entropy);

    edgeDensity.textContent =
        formatNumber(features.edge_density);

    width.textContent =
        features.width ?? "—";

    height.textContent =
        features.height ?? "—";


    // --------------------------------------------------------
    // Progress bars
    // --------------------------------------------------------

    // Sharpness can be very large
    setBar(
        sharpnessBar,
        features.sharpness,
        2000
    );

    // Brightness: approximately 0 - 255
    setBar(
        brightnessBar,
        features.brightness,
        255
    );

    // Contrast
    setBar(
        contrastBar,
        features.contrast,
        100
    );

    // Noise
    setBar(
        noiseBar,
        features.noise,
        20
    );

    // Saturation
    setBar(
        saturationBar,
        features.saturation,
        1
    );

    // Entropy
    setBar(
        entropyBar,
        features.entropy,
        8
    );

    // Edge density
    setBar(
        edgeBar,
        features.edge_density,
        1
    );


    console.log(
        "Feature Matrix updated successfully"
    );
}


// ============================================================
// FILE SELECT
// ============================================================

function handleFile(file) {

    if (!file) {
        return;
    }

    console.log("Selected file:", file.name);

    // Validate type

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ];

    if (!allowedTypes.includes(file.type)) {

        showMessage(
            "Please select JPEG, PNG or WEBP image.",
            true
        );

        return;
    }


    // Validate size

    const maxSize =
        10 * 1024 * 1024;

    if (file.size > maxSize) {

        showMessage(
            "Image size must be less than 10 MB.",
            true
        );

        return;
    }


    selectedFile = file;

    analyzeBtn.disabled = false;


    // Preview

    const imageURL =
        URL.createObjectURL(file);

    previewImage.src = imageURL;

    previewImage.hidden = false;

    dropContent.style.display = "none";


    verdict.textContent =
        "READY — PRESS RUN ANALYSIS";


    showMessage(
        `Selected: ${file.name}`,
        false
    );
}


// ============================================================
// BROWSE BUTTON
// ============================================================

browseBtn.addEventListener(
    "click",
    () => {

        fileInput.click();

    }
);


// ============================================================
// FILE INPUT
// ============================================================

fileInput.addEventListener(
    "change",
    (event) => {

        const file =
            event.target.files[0];

        handleFile(file);

    }
);


// ============================================================
// DROP AREA CLICK
// ============================================================

dropArea.addEventListener(
    "click",
    () => {

        fileInput.click();

    }
);


// ============================================================
// DRAG OVER
// ============================================================

dropArea.addEventListener(
    "dragover",
    (event) => {

        event.preventDefault();

        dropArea.classList.add(
            "drag-over"
        );

    }
);


// ============================================================
// DRAG LEAVE
// ============================================================

dropArea.addEventListener(
    "dragleave",
    () => {

        dropArea.classList.remove(
            "drag-over"
        );

    }
);


// ============================================================
// DROP
// ============================================================

dropArea.addEventListener(
    "drop",
    (event) => {

        event.preventDefault();

        dropArea.classList.remove(
            "drag-over"
        );

        const file =
            event.dataTransfer.files[0];

        handleFile(file);

    }
);


// ============================================================
// RUN ANALYSIS
// ============================================================

analyzeBtn.addEventListener(
    "click",
    async () => {

        if (!selectedFile) {

            showMessage(
                "Please select an image first.",
                true
            );

            return;
        }


        analyzeBtn.disabled = true;

        analyzeBtn.textContent =
            "ANALYZING...";


        verdict.textContent =
            "ANALYZING IMAGE...";


        showMessage(
            "Sending image to SmartVision AI...",
            false
        );


        const formData =
            new FormData();

        formData.append(
            "file",
            selectedFile
        );


        const startTime =
            performance.now();


        try {

            const response =
                await fetch(
                    `${API_BASE}/api/analyze`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const endTime =
                performance.now();


            const requestLatency =
                Math.round(
                    endTime - startTime
                );


            latency.textContent =
                `${requestLatency} MS`;


            if (!response.ok) {

                let errorText =
                    "Analysis failed.";

                try {

                    const errorData =
                        await response.json();

                    errorText =
                        errorData.detail ||
                        errorText;

                } catch (_) {}


                throw new Error(
                    errorText
                );
            }


            const data =
                await response.json();


            console.log(
                "ANALYSIS RESPONSE:",
                data
            );


            // IMPORTANT:
            // Immediately display returned data

            displayAnalysis(data);


            showMessage(
                "Analysis completed successfully.",
                false
            );


            // Refresh history AFTER displaying result.
            // It will NOT reset Feature Matrix.

            await loadHistory();


        } catch (error) {

            console.error(
                "Analysis error:",
                error
            );


            verdict.textContent =
                "ANALYSIS FAILED";


            showMessage(
                error.message,
                true
            );

        } finally {

            analyzeBtn.disabled = false;

            analyzeBtn.textContent =
                "RUN ANALYSIS";

        }

    }
);


// ============================================================
// LOAD HISTORY
// ============================================================

async function loadHistory() {

    console.log(
        "Loading analysis history..."
    );


    try {

        const response =
            await fetch(
                `${API_BASE}/api/analyses`
            );


        if (!response.ok) {

            throw new Error(
                `History request failed: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "History data:",
            data
        );


        // ----------------------------------------------------
        // Handle different API response formats
        // ----------------------------------------------------

        let records = [];


        if (Array.isArray(data)) {

            records = data;

        } else if (
            Array.isArray(data.items)
        ) {

            records = data.items;

        } else if (
            Array.isArray(data.results)
        ) {

            records = data.results;

        }


        recordCount.textContent =
            records.length;


        renderHistory(records);


        // IMPORTANT:
        // DO NOT reset Feature Matrix here.
        //
        // The latest analysis remains visible.


    } catch (error) {

        console.error(
            "History error:",
            error
        );


        history.innerHTML = `
            <div class="empty-history">
                FAILED TO LOAD HISTORY
            </div>
        `;
    }
}


// ============================================================
// RENDER HISTORY
// ============================================================

function renderHistory(records) {

    if (!records || records.length === 0) {

        history.innerHTML = `
            <div class="empty-history">
                NO ANALYSIS RECORDS
            </div>
        `;

        return;
    }


    history.innerHTML = "";


    records.forEach(
        (item) => {

            const row =
                document.createElement("div");

            row.className =
                "history-row";


            const confidence =
                item.confidence !== undefined
                    ? `${(
                        Number(item.confidence) * 100
                    ).toFixed(1)}%`
                    : "—";


            row.innerHTML = `

                <div class="history-id">
                    #${item.id ?? "—"}
                </div>

                <div class="history-file">
                    ${escapeHTML(
                        item.filename ?? "Unknown"
                    )}
                </div>

                <div class="history-prediction">
                    ${escapeHTML(
                        String(
                            item.prediction ?? "—"
                        ).replace(
                            /_/g,
                            " "
                        ).toUpperCase()
                    )}
                </div>

                <div class="history-confidence">
                    ${confidence}
                </div>

            `;


            // Click history record
            // and display its features

            row.addEventListener(
                "click",
                () => {

                    console.log(
                        "History record selected:",
                        item
                    );

                    displayAnalysis(item);

                }
            );


            history.appendChild(row);

        }
    );
}


// ============================================================
// REFRESH HISTORY
// ============================================================

refreshBtn.addEventListener(
    "click",
    () => {

        loadHistory();

    }
);


// ============================================================
// HEALTH CHECK
// ============================================================

async function checkHealth() {

    const start =
        performance.now();


    try {

        const response =
            await fetch(
                `${API_BASE}/api/health`
            );


        const end =
            performance.now();


        if (!response.ok) {

            throw new Error(
                "API not healthy"
            );

        }


        const data =
            await response.json();


        console.log(
            "Health:",
            data
        );


        apiDot.classList.remove(
            "offline"
        );

        apiDot.classList.add(
            "online"
        );


        apiStatus.textContent =
            "API ONLINE";


        latency.textContent =
            `${Math.round(
                end - start
            )} MS`;


    } catch (error) {

        console.error(
            "Health check failed:",
            error
        );


        apiDot.classList.remove(
            "online"
        );

        apiDot.classList.add(
            "offline"
        );


        apiStatus.textContent =
            "API OFFLINE";


        latency.textContent =
            "--";

    }
}


// ============================================================
// MESSAGE
// ============================================================

function showMessage(
    text,
    isError = false
) {

    message.textContent =
        text;

    message.className =
        isError
            ? "message error"
            : "message success";
}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(value) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


// ============================================================
// INITIALIZATION
// ============================================================

async function initialize() {

    console.log(
        "Initializing SmartVision..."
    );


    // Health

    await checkHealth();


    // History

    await loadHistory();


    console.log(
        "SmartVision initialization complete"
    );
}


// ============================================================
// START
// ============================================================

initialize();