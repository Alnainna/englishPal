function toggleCheckboxSelection(checkStatus) {
    // used in userpage_post.html
    const checkBoxes = document.getElementsByName('marked');
    checkBoxes.forEach((checkbox) => { checkbox.checked = checkStatus;} );
}
