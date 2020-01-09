// Disable checkboxes on page load.
$( document ).ready(function() {
    // disableM03();
    // disableM05();
    missionOneDependencies();
});

var x,y

var missionOneInputs = [
    document.getElementById('missions-M01 - Elevated Places-0'),   // (checkbox field) the following fields are dependant upon this
    document.getElementById('missions-M01 - Elevated Places-1-0'), // no flags raised
    document.getElementById('missions-M01 - Elevated Places-1-1'), // 1 flag raised
    document.getElementById('missions-M01 - Elevated Places-1-2'), // 2 flags raised
]

function missionOneDependencies() {
    // flags can only be raised if the robot is supported by the bridge
    // this function disables the radio fields if the checkbox is not active
    if (!missionOneInputs[0].checked) {
        missionOneInputs[1].disabled = true;
        missionOneInputs[2].disabled = true;
        missionOneInputs[3].disabled = true;
    }
}

// // Blanks out checkbox for M03.
// function disableM03(){
//     // Checks in place to handle page refreshing when calculating score.
//     if (!questions[0][0].checked && !questions[0][1].checked){
//         // Enable buttons
//         questions[0][1].disabled = true;
//     }
// }

// Validatating checkboxes
function validateCheckbox(){
    if (!missionOneInputs[0].checked) {
        missionOneInputs[1].disabled = true;
        missionOneInputs[2].disabled = true;
        missionOneInputs[3].disabled = true;
    }

    if (missionOneInputs[0].checked) {
        missionOneInputs[1].disabled = false;
        missionOneInputs[2].disabled = false;
        missionOneInputs[3].disabled = false;
    }
}

// Validatation for M14
// function validateSelect(dropdown) {
//     // The name tag of the selection fields to validate.
//     var firstName = "missions-M14 - Meteoroid Deflection-2";
//     var secondName = "missions-M14 - Meteoroid Deflection-3";
//     // Check we are validating the correct question.
//     if (dropdown.name == firstName) {
//         // Take the text from the select option and parses to an integer.
//         x = parseInt(dropdown.options[dropdown.selectedIndex].text, 10);
//     } else if (dropdown.name == secondName){
//         y = parseInt(dropdown.options[dropdown.selectedIndex].text, 10);
//     }
//     // Only 2 Meteoroids allowed, alert judge and reset last option.
//     if (x+y > 2){
//         alert("There are a maximum of 2 Meteoroids")
//         dropdown.selectedIndex = "0";
//     }
// }
