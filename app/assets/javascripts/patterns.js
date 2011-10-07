/*#############################################################################
 ::: Namespace, settings, vars
 ############################################################################*/
/**
 * @namespace The namespace for the whole diagram JavaScript.
 */
var opr = opr || {};
opr.settings = {
    defaultCacheExpiration : 60000, // milli seconds
    urls : {
        suggestTag : "/suggest/tag?start={0}"
    }
}
opr.vars = {
    jsonCache : {}
};

/*#############################################################################
 ::: Manage pattern toggle accordion
 ############################################################################*/
$(function() {
    $(".accordion > div").not(":first").hide();


    $('.togglePreviewSize').click(function() {
        $(this).siblings('.markdownEditor, .preview').toggleClass('bigger');
        return false;
    });

    opr.markdown.enable();
    // click listener should execute latest
    // maybe do this in a addField hook?
    // TODO
    addFieldAddListener(opr.markdown.enable);

    var hideAll = function(except) {
        if (except == undefined) {
            $(".accordion > div").slideUp();
        } else {
            $(".accordion > div").not(except).slideUp();
        }

    }

    $(".accordion > h2").click(function() {
        $(this).next().slideToggle();
        return false;
    });

    $(".accordion > div > input.previous").click(function() {
        var target = $(this).parent().prev().prev();
        hideAll(target);

        target.slideDown();

        target.find(":input:visible:first").focus();

        return false;
    });

    $(".accordion > div > input.next").click(function() {
        var target = $(this).parent().next().next();
        hideAll(target);

        target.slideDown();

        target.find(":input:visible:first").focus();

        return false;
    });

    $(".accordion-manage-links > .open-all").click(function() {
        $(this).parent().prev(".accordion").children("div").slideDown();
        return false;
    });

    $(".accordion-manage-links > .close-all").click(function() {
        $(this).parent().prev(".accordion").children("div").slideUp();
        return false;
    });

    $(".accordion-manage-links > .with-errors").click(function() {
        $(this).parent().prev(".accordion").children("div").each(function() {
            if ($(this).find(".errors").length != 0) {
                $(this).slideDown();
            } else {
                $(this).slideUp();
            }
        });

        return false;
    });

    $(".accordion").each(function() {
        opr.accordion.openWithErrors($(this));
    });
});

opr.accordion = {
    openWithErrors : function(accordion, openAtLeastOne) {
        var anythingOpen = false;

        accordion.children("div").each(function() {
            if ($(this).find(".errors").length != 0) {
                $(this).show();
                anythingOpen = true;
            } else {
                $(this).hide();
            }
        });

        if (!anythingOpen && (openAtLeastOne === undefined || openAtLeastOne === true)) {
            accordion.children("div:first").show();
        }
    }
}
opr.markdown = {
    idCounter : 0
};
opr.markdown.enable = function() {
    var buttons = $('#page_content .markdownEditor-buttons');
    var editors = $('#page_content  .markdownEditor');
    var previews = $('#page_content .markdownEditor-preview');

    

    for (var i = 0; i < buttons.length; i++) {
        var button = $(buttons[i]);
        // check for visibility because of the field templates which are
        // located at the end of the file
        // TODO check for button visibility
        if (button.data('wmdActivated') !== true) {
            button.attr('id', 'wmd-button-bar' + opr.markdown.idCounter);
            button.data('wmdActivated', true);
            $(editors[i]).attr('id', 'wmd-input' + opr.markdown.idCounter);
            $(previews[i]).attr('id', 'wmd-preview' + opr.markdown.idCounter);

            var converter = Markdown.getSanitizingConverter();
            new Markdown.Editor(converter, opr.markdown.idCounter.toString()).run();
            opr.markdown.idCounter++;
        }
    }
}

/*#############################################################################
 ::: Manage pattern add / remove tag behaviour
 ############################################################################*/
opr.managePattern = {}

$(function() {
    $('.tag_autocomplete').autocomplete({
        minLength : 3,
        source : function(request, response) {
            var url = opr.settings.urls.suggestTag.replace("{0}",
                    request.term);

            opr.cachedJSONRequest(url, {}, function(data) {
                // remove tags that have already been added
                var tags = [];
                for (var i = data.length - 1; i >= 0; i--) {
                    var suggestedTag = data[i].name;
                    if (!opr.managePattern.containsTag(suggestedTag)) {
                        tags.push(suggestedTag);
                    }
                }

                response(tags);
            });
        }
    });

    $('#add_tag').click(opr.managePattern.addTag);

    $('#input_tag').keypress(function(event) {
        if (event.keyCode == 13) {
            $('#add_tag').click();
            return false;
        }
    });

    // reload tags after server side validation error
    var tagOut = $("#pattern_tag_list");
    if (tagOut.length == 0) {
        return;
    }
    var allTags = tagOut.val().trim().split(',');

    for (var i = 0; i < allTags.length; i++) {
        if (allTags[i].trim().length != 0) {
            opr.managePattern.addTagToList(allTags[i]);
        }
    }
});

opr.managePattern.addTag = function() {
    // retrieve the value and reset the input field
    var input = $("#input_tag");
    var newTags = input.val().trim().split(",");
    input.val("");

    var tagOut = $("#pattern_tag_list");
    var addedTags = tagOut.val().split(',');
    var tagDuplication = false;
    for (var i = 0; i < newTags.length; i++) {
        var tagComparable = newTags[i].toLowerCase();

        if (tagComparable.trim().length == 0) {
            continue;
        }

        tagDuplication = false;

        for (var j = 0; j < addedTags.length; j++) {
            if (addedTags[j].toLowerCase() == tagComparable) {
                tagDuplication = true;
                break;
            }
        }

        if (!tagDuplication) {
            addedTags.push(newTags[i]);
            opr.managePattern.addTagToList(newTags[i]);
        }
    }

    tagOut.val(addedTags.join(',').trim());

    return false;
}

opr.managePattern.addTagToList = function(tag) {
    var li = document.createElement("li");

    // jquery is good at escaping and events
    $(li).text(tag);

    var a = document.createElement("a");
    a.title = "Remove this tag";
    $(a).text("X").click(function() {
        $(this).parent().remove();
        opr.managePattern.removeTagFromInput(tag);
    });

    li.appendChild(a);

    document.getElementById("output_tag").appendChild(li);
}

opr.managePattern.removeTagFromInput = function(tag) {
    var tagOut = $("#pattern_tag_list");
    var allTags = tagOut.val().split(',');

    tag = tag.toLowerCase();

    for (var i = allTags.length - 1; i >= 0; i--) {
        if (allTags[i].toLowerCase() == tag) {
            allTags.splice(i, 1);
        }
    }

    tagOut.val(allTags.join(',').trim());
}

opr.managePattern.containsTag = function(tag) {
    var tagOut = $("#pattern_tag_list");
    var allTags = tagOut.val().split(',');

    tag = tag.toLowerCase();

    for (var i = 0; i < allTags.length; i++) {
        if (allTags[i].toLowerCase() == tag) {
            return true;
        }
    }

    return false;
}


/*#############################################################################
 ::: JSON async request caching
 ############################################################################*/
opr.cachedJSONRequest = function(url, parameter, callback, expiration) {
    if (expiration === undefined) {
        expiration = opr.settings.defaultCacheExpiration;
    }

    var urlCache = opr.vars.jsonCache[url];

    if (urlCache == undefined) {
        opr.vars.jsonCache[url] = {}
        opr.doCachedJSONRequest(url, parameter, callback)
        return;
    }

    var parameterCache = urlCache[parameter];

    var timeDelta = new Date().getTime() - parameterCache['time'].getTime();

    if (parameterCache == undefined ||
            timeDelta >= expiration) {
        opr.doCachedJSONRequest(url, parameter, callback)
    } else {
        callback(parameterCache['result']);
    }
}

opr.doCachedJSONRequest = function(url, parameter, callback) {
    var parameterCache = opr.vars.jsonCache[url][parameter] = {};

    parameterCache['time'] = new Date();
    parameterCache['xhr'] = $.getJSON(url, parameter, function(data, status, xhr) {
        parameterCache['result'] = data;
        if (xhr === parameterCache['xhr']) {
            callback(data);
        }
    });
}

/*#############################################################################
 ::: Validation
 ############################################################################*/
$(function() {
    opr.validation.init();
});

opr.validation = {};
opr.validation.init = function() {
    $("label .errors").each(function() {
        var error = $(this);
        $(this).parent().find(":input").change(function() {
            error.fadeOut();
        });
    });
};