async function analyzeText() {
    const inputText = document.getElementById('inputText').value;
    const resultDiv = document.getElementById('result');
    const paragraphDiv = document.getElementById('paragraphDisplay');

    try {
        const response = await fetch('http://127.0.0.1:3000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: inputText })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Display the input paragraph
        paragraphDiv.innerHTML = `<h2>Input Text</h2><p>${inputText}</p>`;

        // Display analysis results
        if (Array.isArray(result) && result.length > 0) {
            let htmlContent = `<h2>Analysis Results</h2>`;
            result.forEach(analysis => {
                const positiveWords = analysis.positive_words?.join(', ') || "None";
                const negativeWords = analysis.negative_words?.join(', ') || "None";
                
                htmlContent += `
                    <div class="analysis-result">
                        <p><strong>Sentence:</strong> ${analysis.sentence}</p>
                        <p><strong>Sentiment:</strong> ${analysis.sentiment}</p>
                        <p><strong>Positive Count:</strong> ${analysis.positive_count}</p>
                        <p><strong>Negative Count:</strong> ${analysis.negative_count}</p>
                        <p><strong>Positive Words:</strong> ${positiveWords}</p>
                        <p><strong>Negative Words:</strong> ${negativeWords}</p>
                    </div>
                    <hr />
                `;
            });

            resultDiv.innerHTML = htmlContent;
        } else {
            resultDiv.innerHTML = `<p>No analysis results found.</p>`;
        }

        // Clear the textarea after analysis
        document.getElementById('inputText').value = '';

    } catch (error) {
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}
