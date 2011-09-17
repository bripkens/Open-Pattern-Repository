// This is a manifest file that'll be compiled into including all the files listed below.
// Add new JavaScript/Coffee code in separate files in this directory and they'll automatically
// be included in the compiled file accessible from http://example.com/assets/application.js
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// the compiled file.
//
//= require jquery
//= require jquery_ujs
//= require_tree .

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
        $(this).prev().find(":input:visible:first").focus();
        return false;
    });
});