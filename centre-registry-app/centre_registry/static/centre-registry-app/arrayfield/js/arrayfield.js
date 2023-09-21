var inputLengths = {}

function replicateFields(fieldName, inputLengths){
    let elementToReplicate = $('#input_' + fieldName + "0"),
        clonedElement = elementToReplicate.clone();
    let inputFieldID = 'input_' + fieldName + String(inputLengths[ fieldName ]);
    $(clonedElement).attr('name', inputFieldID);
    $(clonedElement).attr('id', inputFieldID)
    $(clonedElement).val('');
    let lastInputInArray = $('#input_' + fieldName + String( inputLengths[ fieldName ] - 1));
    $(lastInputInArray).after(clonedElement[0]);
    $(lastInputInArray).after("<br/>")
    inputLengths[ fieldName ] = inputLengths[ fieldName ] + 1;
}

function countInputs(fieldName){
    let arrayInputField = $('#input_' + fieldName + "0");
    let arrayLength = 0;
    while(arrayInputField.length > 0){
        arrayLength++;
        arrayInputField = $('#input_' + String(fieldName + arrayLength));
    }
    return arrayLength;
}

$(document).ready(function() {
  let addButtons = $('.addNewInput');
  $.each(addButtons, function( button ){
      button = addButtons[button]
      let bid = button.id
      inputLengths[ button.id ] = countInputs(button.id);
  });


  $(addButtons).click(function() {
      replicateFields(this.id, inputLengths);
  });
});
