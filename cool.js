console.log("JavaScript loaded");

// Strand buttons
setTimeout(function() {
    const btn1 = document.getElementById("btn1");
    const btn2 = document.getElementById("btn2");
    const btn3 = document.getElementById("btn3");
    
    console.log("btn1:", btn1);
    console.log("btn2:", btn2);
    console.log("btn3:", btn3);
    
    if (btn1) {
        btn1.onclick = function() {
            console.log("btn1 clicked");
            this.classList.toggle("active");
        };
    }
    
    if (btn2) {
        btn2.onclick = function() {
            console.log("btn2 clicked");
            this.classList.toggle("active");
        };
    }
    
    if (btn3) {
        btn3.onclick = function() {
            console.log("btn3 clicked");
            this.classList.toggle("active");
        };
    }
    
    // Learning Outcomes
    const selectedLOs = new Set();
    const loCards = document.querySelectorAll('.lo-card');
    
    console.log("Found cards:", loCards.length);
    
    loCards.forEach(function(card, index) {
        console.log("Adding listener to card", index);
        card.onclick = function() {
            console.log("Card clicked:", index);
            const loId = this.getAttribute('data-lo');
            this.classList.toggle('selected');
            
            if (selectedLOs.has(loId)) {
                selectedLOs.delete(loId);
            } else {
                selectedLOs.add(loId);
            }
            
            document.getElementById('selected-los').value = Array.from(selectedLOs).join(',');
            console.log('Selected LOs:', Array.from(selectedLOs));
        };
    });
}, 100);