function handleSubmit(event) {
    event.preventDefault();

    const overlay = document.getElementById('loading-overlay');
    const factContainer = document.getElementById('loading-fact');

    // Set the random fact
    const fitnessFacts = [
        "Drinking water before meals can help with weight loss.",
        "Walking for 30 minutes a day improves heart health.",
        "Strength training increases your metabolism.",
        "Sleep is just as important as exercise for fitness.",
        "Stretching reduces injury risk and improves flexibility."
    ];

    if (factContainer) {
        const randomIndex = Math.floor(Math.random() * fitnessFacts.length);
        factContainer.textContent = fitnessFacts[randomIndex];
    }

    // Show overlay immediately
    overlay.style.display = 'flex';

    // Use double requestAnimationFrame to force repaint
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            // After paint is complete, delay briefly, then submit form
            setTimeout(() => {
                event.target.submit(); // Now it will render everything first
            }, 1000); // 1 second is enough now
        });
    });

    return false;
}
