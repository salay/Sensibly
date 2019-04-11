function viewAppointments() {
    console.log('clicked view appt')
    var appointmentsTable = document.getElementById("your-appointments");
    if (appointmentsTable.style.display != 'none') {
    appointmentsTable.style.display = 'none';
    }
    else if (appointmentsTable.style.display == 'none') {
        appointmentsTable.style.display = 'block';
    }
}

function editProfile() {
  var editProf = document.getElementById("editProfileForm");
    if (editProf.style.display != 'none') {
    editProf.style.display = 'none';
    }
    else if (editProf.style.display == 'none') {
        editProf.style.display = 'block';
    }
}