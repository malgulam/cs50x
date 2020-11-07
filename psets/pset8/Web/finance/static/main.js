var check = function(){
    if (document.getElementById('password').value == document.getElementById('cpassword').value)
    {
        document.getElementById('message').style.color = 'green';
        document.getElementById('message').innerHTML = 'Passwords matching';
        document.getElementById("registerBtn").disabled = false;
    }
    else
    {
        document.getElementById('message').style.color = 'red';
        document.getElementById('message').innerHTML = 'Passwords not matching';
        document.getElementById("registerBtn").disabled = true;
    }
}

var check_new_password = function(){
    if (document.getElementById("NPassword").value == document.getElementById("CNPassword").value)
    {
        document.getElementById('message').style.color = 'green';
        document.getElementById('message').innerHTML = 'Passwords matching';
        document.getElementById("changePSWDBtn").disabled = false;
    }
    else
    {
        document.getElementById('message').style.color = 'red';
        document.getElementById('message').innerHTML = 'Passwords not matching';
        document.getElementById("changePSWDBtn").disabled = true;
    }
}