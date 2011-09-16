//function remove_fields(link) {
//    $(link).prev('input[type=hidden]').value = '1';
//    $(link).parent('.fields').hide();
//};

$(function() {
    var templates = {};
    $('.fieldTemplates div').each(function() {
        templates[$(this).data('templateFor')] = $(this).html();
    });

    $('.removeFields').live('click', function() {
        $(this).prev('input[type=hidden]').val(true);
        $(this).parent().hide();
        return false;
    });

    $('.addFields').live('click', function() {
        var name = $(this).data('association');
        var template = templates[name];
        
        var new_id = new Date().getTime();
        var regexp = new RegExp('new_' + name, 'g');
        $(this).before(template.replace(regexp, new_id));
        return false;
    });
});
//function add_fields(link) {

//  $(link).parent().before(content.replace(regexp, new_id));
//};