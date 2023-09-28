function showTab(tabId) {
    // Get all tab content elements
    var tabContents = document.getElementsByClassName('tab-content');
    
    // Hide all tab content
    for (var i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = 'none';
    }
    
    // Show the selected tab content
    document.getElementById(tabId).style.display = 'block';
}