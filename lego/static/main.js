// Disable checkboxes on page load.
$( document ).ready(function() {
    disableM03();
    disableM05();
});

var x,y

// Blanks out checkbox for M03.
function disableM03(){
    // Checks in place to handle page refreshing when calculating score.
    if (!document.getElementById('missions-M03 - 3D Printing-0').checked && !document.getElementById('missions-M03 - 3D Printing-1').checked){
        // Enable buttons
        document.getElementById("missions-M03 - 3D Printing-1").disabled = true;
    }
}

// Blanks out checkboxes for M05.
function disableM05(){
    // Checks in place to handle page refreshing when calculating score.
    if (!document.getElementById('missions-M05 - Extraction-0').checked && !document.getElementById('missions-M05 - Extraction-1').checked
    && !document.getElementById('missions-M05 - Extraction-2').checked && !document.getElementById('missions-M05 - Extraction-3').checked){
        // Enable buttons
        document.getElementById("missions-M05 - Extraction-1").disabled = true;
        document.getElementById("missions-M05 - Extraction-2").disabled = true;
        document.getElementById("missions-M05 - Extraction-3").disabled = true;
    }
}

// Validatating checkboxes
function validateCheckbox(){
    // If the first checkbox is checked then enable other checkboxes.
    if (document.getElementById('missions-M05 - Extraction-0').checked) {
        document.getElementById("missions-M05 - Extraction-1").disabled = false;
        document.getElementById("missions-M05 - Extraction-2").disabled = false;
        document.getElementById("missions-M05 - Extraction-3").disabled = false;
    } 
    // If the first checkbox is uchecked then disable other checkboxes.
    else if (!document.getElementById('missions-M05 - Extraction-0').checked){
        disableM05();
    }
    if (document.getElementById('missions-M03 - 3D Printing-0').checked) {
        document.getElementById("missions-M03 - 3D Printing-1").disabled = false;
    } 
    else if (!document.getElementById('missions-M03 - 3D Printing-0').checked){
        disableM03();
    }
}

// Validatation for M14
function validateSelect(dropdown) {
    // The name tag of the selection fields to validate.
    var firstName = "missions-M14 - Meteoroid Deflection-2";
    var secondName = "missions-M14 - Meteoroid Deflection-3";
    // Check we are validating the correct question.
    if (dropdown.name == firstName) {
        // Take the text from the select option and parses to an integer.
        x = parseInt(dropdown.options[dropdown.selectedIndex].text, 10);
    } else if (dropdown.name == secondName){
        y = parseInt(dropdown.options[dropdown.selectedIndex].text, 10);
    }
    // Only 2 Meteoroids allowed, alert judge and reset last option.
    if (x+y > 2){
        alert("There are a maximum of 2 Meteoroids")
        dropdown.selectedIndex = "0";
    }
}