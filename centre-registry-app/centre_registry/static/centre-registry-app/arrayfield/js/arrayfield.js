//Initialization of array
let javascriptArray = [];
const data = document.currentScript.dataset;
const inputName = data.inputName;

//Function to replicate fields in the form
function replicateFields(){
    var elementToReplicate = $('.inputs').first(), //Only clone first group of inputs
        clonedElement = elementToReplicate.clone();//Cloned the element
    clonedElement.find('input').val(''); //Clear cloned elements value on each new addition
    clonedElement.insertBefore($('form a'));
}

//Calling function on click
$('.addRow').click(function(){
    replicateFields();
});

//Go through inputs filling up the array.
$('form').submit(function(){
    $('.inputs').each(function(){
        javascriptArray.push($(this).find('input[name='+$(inputName)+']').val());
    });
    console.log(javascriptArray);
    return false; // remove this to submit the form.
});
