// Disable checkboxes on page load.
$( document ).ready(function() {
    disableM03();
    disableM05();
});

var x,y

var questions = [
    // Question name given on html. M03 = questions[0][x] | M05 = questions[1][x]
    [document.getElementById('missions-M03 - 3D Printing-0'), document.getElementById('missions-M03 - 3D Printing-1')],
    [document.getElementById('missions-M05 - Extraction-0'), document.getElementById('missions-M05 - Extraction-1'),
    document.getElementById('missions-M05 - Extraction-2'), document.getElementById('missions-M05 - Extraction-3')],
  ];

// Blanks out checkbox for M03.
function disableM03(){
    // Checks in place to handle page refreshing when calculating score.
    if (!questions[0][0].checked && !questions[0][1].checked){
        // Enable buttons
        questions[0][1].disabled = true;
    }
}

// Validatating checkboxes
function validateCheckbox(){
    // If the first checkbox is checked then enable other checkboxes.
    if (questions[1][0].checked) {
        questions[1][1].disabled = false;
        questions[1][2].disabled = false;
        questions[1][3].disabled = false;
        // 2 / 3 independant from each other
        if (questions[1][1].checked){
            questions[1][2].disabled = true;
        }
        if (questions[1][2].checked){
            questions[1][1].disabled = true;
        }
    } 
    // If the first checkbox is uchecked then disable other checkboxes.
    else if (!questions[1][0].checked){
        questions[1][1].checked = false;
        questions[1][2].checked = false;
        questions[1][3].checked = false;
        disableM05();
    }
    if (questions[0][0].checked) {
        questions[0][1].disabled = false;
    } 
    else if (!questions[0][0].checked){
        questions[0][1].checked = false;
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
