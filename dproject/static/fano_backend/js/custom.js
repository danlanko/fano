

$(document).on('click', '.confirm-delete', function(){
    return confirm('This action cannot be called back, Are you sure you want to proceed?');
});



$(document).on('click', '.confirm-deactivate', function(){
    return confirm('You are about to block a member, Are you sure you want to proceed?');
});


$(document).on('click', '.confirm-activate', function(){
    return confirm('You are about to restore a member, Are you sure you want to proceed?');
});
