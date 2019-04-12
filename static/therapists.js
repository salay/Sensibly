function searchFunction() {
    let input = document.getElementById('myInput');
    //console.log(input.value)
    let filter = input.value.toUpperCase();
    let list = document.getElementById("all-therapists");
    let therapistbloc = list.getElementsByClassName("is-primary");
    //console.log(therapistbloc)
    let div = list.getElementsByClassName("therapist-name");
    //console.log(div)
    for (let i = 0; i < div.length; i++) {
        let name = div[i];
        //console.log(name)
        let txtValue = name.textContent || name.outerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            therapistbloc[i].style.display = "block";
        }
        else {
            therapistbloc[i].style.display = "none";
        }
    }
}