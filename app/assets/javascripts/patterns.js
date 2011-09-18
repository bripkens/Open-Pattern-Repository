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
        suggestTag : "/suggest/tag/{0}",
        retrieveTemplate : "/api/json/templates/{0}"
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

    var converter1 = Markdown.getSanitizingConverter();
    var editor1 = new Markdown.Editor(converter1);
    editor1.run();

    $('.togglePreviewSize').click(function() {
        $(this).siblings('#wmd-input, .preview').toggleClass('bigger');
        return false;
    });

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
                for (var i = data.length - 1; i >= 0; i--) {
                    if (opr.managePattern.containsTag(data[i])) {
                        data.splice(i, 1);
                    }
                }

                response(data);
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
    var tagOut = $("#id_tags");
    if (tagOut.length == 0) {
        return;
    }
    var allTags = tagOut.val().trim().split(' ');

    for (var i = 0; i < allTags.length; i++) {
        if (allTags[i].trim().length != 0) {
            opr.managePattern.addTagToList(allTags[i]);
        }
    }
});

opr.managePattern.addTag = function() {
    // retrieve the value and reset the input field
    var input = $("#input_tag");
    var newTags = input.val().trim().split(" ");
    input.val("");

    var tagOut = $("#id_tags");
    var addedTags = tagOut.val().split(' ');
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

    tagOut.val(addedTags.join(' ').trim());

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
    var tagOut = $("#id_tags");
    var allTags = tagOut.val().split(' ');

    tag = tag.toLowerCase();

    for (var i = allTags.length - 1; i >= 0; i--) {
        if (allTags[i].toLowerCase() == tag) {
            allTags.splice(i, 1);
        }
    }

    tagOut.val(allTags.join(' ').trim());
}

opr.managePattern.containsTag = function(tag) {
    var tagOut = $("#id_tags");
    var allTags = tagOut.val().split(' ');

    tag = tag.toLowerCase();

    for (var i = 0; i < allTags.length; i++) {
        if (allTags[i].toLowerCase() == tag) {
            return true;
        }
    }

    return false;
}

/*#############################################################################
 ::: Manage pattern select / change template
 ############################################################################*/
$(function() {
    $("#change_template").click(opr.managePattern.changeTemplate);

    if (typeof mySettings != "undefined") {
        $(".textual-description-step textarea").markItUp(mySettings);
    }
});

opr.managePattern.changeTemplate = function() {
    var selectedValue = $("#id_template option:selected").val();

    if (selectedValue.trim().length == 0) {
        // TODO show user friendly error message
        alert("Please select something.");
        return false;
    }

    var descriptionBox = $(this).siblings(".description-box");

    var url = opr.settings.urls.retrieveTemplate.replace("{0}", selectedValue);
    opr.cachedJSONRequest(url, {}, function(data) {
        // TODO error handling (template retrieval failed)

        // remove previous text input components
        descriptionBox.find(".description").remove();

        // sort the components
        data.components.sort(function(a, b) {
            return a.sort_order - b.sort_order;
        });

        for (var i = 0; i < data.components.length; i++) {
            var component = data.components[i];

            var innerBox = document.createElement("div");
            innerBox.className = "description";

            var heading = document.createElement("h3");
            $(heading).text(component.name);
            innerBox.appendChild(heading);

            if (component.mandatory) {
                var requiredNotifier = document.createElement("span");
                requiredNotifier.textContent = " *";
                requiredNotifier.className = "required";
                requiredNotifier.title = "required";
                heading.appendChild(requiredNotifier);
            }

            var textarea = document.createElement("textarea");
            textarea.rows = 15;
            textarea.cols = 75;
            textarea.name = "description-" + component.id;
            innerBox.appendChild(textarea);

            descriptionBox.append(innerBox);

            $(textarea).markItUp(mySettings);
        }
    });

    return false;
}

/*#############################################################################
 ::: Driver / Impact slider
 ############################################################################*/
$(function() {
    var addslider = function(select) {
        var slider = $("<div></div>").insertAfter($(select).parent()).slider({
            min: 1,
            max: 10,
            range: "min",
            animate : true,
            value : select.selectedIndex + 1,
            slide: function(event, ui) {
                select.selectedIndex = ui.value -1;
            }
        });
        $(select).change(function() {
            slider.slider("value", select.selectedIndex + 1);
        });
    }

    $("div.forces_consequences > div.entries > " +
            "fieldset").each(function() {

        addslider($(this).find("label:eq(1) > select").get(0));
    });

    $("#input_add_driver").click(function() {
        var lastFieldset = $(".forces_consequences fieldset:last");
        var newFieldset = opr.cloneFormSet(lastFieldset, 'driver');

        var select = newFieldset.find("label:eq(1) > select").get(0);

        select.selectedIndex = 4;

        addslider(select);

        $(select).parent().next(".ui-slider").next(".ui-slider").remove();

        newFieldset.find(".val-show").removeClass("val-show");

        newFieldset.find(":input:visible:first").focus();

        return false;
    });
});

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