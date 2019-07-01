
//Scroll to the top button
$(document).ready(function(){ 
    $(window).scroll(function(){ 
        if ($(this).scrollTop() > 100) { 
            $('.scroll-to-top').fadeIn(); 
        } else { 
            $('.scroll-to-top').fadeOut(); 
        } 
    }); 
    $('.scroll-to-top').click(function(){ 
        $("html, body").animate({ scrollTop: 0 }, 600); 
        return false; 
    }); 
});

//Ip validation for ADD_SERVER form
function ValidateIPaddress(ip)
{
    var ipFormat = /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/;
    var domainFormat = /^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$/;

    if(ip.value.match(ipFormat) || ip.value.match(domainFormat))
    {
        document.add_server_form.server_ip.focus();
        return true;
    }
    else
    {
        alert("You have entered an invalid IP address!");
        document.add_server_form.server_ip.focus();return false;
    }
}