document.getElementById("summarization-form").addEventListener("submit",async(e) =>{
    e.preventDefault();


    //get reference to elements
    const dialogueInput = document.getElementById("dialogue-input");
    const summaryText = document.getElementById("summary-text");
    const submitButton = e.target.querySelector("button");

    const dialogue = dialogueInput.value.trim();
    if(!dialogue) return;

    //show processing message and disable button
    summaryText.innerText = "Processing...";
    submitButton.disabled = true;

    try{
        // send dialogue to backend for runtime error
        const response = await fetch("/summarize/", {
            method:"POST",
            headers: {
                "Content-Type": "application/json" },
                body: JSON.stringify({dialogue}),
            });

        if (!response.ok){
            throw new Error('Server error:${response.status}');
        }

        const data = await response.json();
        summaryText.innerText = data.summary || "No summary returned.";
    } catch (err) {
        summaryText.innerText = 'Error: ${err.message}';
    } finally{
        submitButton.disabled = false;
    }
});