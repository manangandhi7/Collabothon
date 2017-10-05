$(document).ready(function() {
    console.log('viewer.js')
    $('.country-match').each(function(index, countryMatch) {
        $countryMatch = $(countryMatch);
        console.log('Got country match:', $countryMatch.data('country-iso'), $countryMatch.data('country-name'), $countryMatch.data('found-text'));
    });
    goToIndex(0);
//    $($('.country-match')[0]).addClass('active');
    $('body').append('<div class="top overlay"></div>')
    $('body').append('<div class="left overlay"></div>')
    $('body').append('<div class="right overlay"></div>')
    $('body').append('<div class="bottom overlay"></div>')
    $('body').append('<div id="info"></div>')
    var matches = $('body').data('matches')
    var foreign_counter = matches['foreign'];
    var foreign_matches_html = ''
    $.each(foreign_counter, function(foreign_match_name, number) {
        foreign_matches_html += '<span class="match" data-match="' + foreign_match_name + '">' + foreign_match_name + ' (' + number + ')</span><br/>'
    });
    var country_counter = matches['country'];
    var country_matches_html = ''
    $.each(country_counter, function(country_name, number) {
        country_matches_html += '<span class="match" data-match="' + country_name + '">' + country_name + ' (' + number + ')</span><br/>'
    });
    var info_html = '<strong>Foreign matches:</strong><div>' +  foreign_matches_html + '</div><br/><strong>Country matches</strong><div>' + country_matches_html + '</div>'
    $('#info').html(info_html)

    function getCurrentIndex() {
        var $countryMatches = $('.country-match');
        var $foreignMatches = $('.foreign-match');
        $active = $('.foreign-match.active, .country-match.active');
        if ($foreignMatches.index($active) > -1) {
            index = $foreignMatches.index($active);
        } else if ($countryMatches.index($active) > -1) {
            index = $foreignMatches.length + $countryMatches.index($active);
        } else {
            throw $active + ' not in country matches or foreign matches';
        }
        console.log('current index:' + index);
        return index;
    }

    function getElementForIndex(index) {
        var $countryMatches = $('.country-match');
        var $foreignMatches = $('.foreign-match');
        if (index < $foreignMatches.length) {
            return $($('.foreign-match')[index])
        } else {
            return $($('.country-match')[index - $foreignMatches.length])
        }
    }

    function goToIndex(index) {
        $('.overlay').hide()
        $('.country-match.active, .foreign-match.active').removeClass('active');
        console.log('index', index)
        $newActive = getElementForIndex(index);
        $newActive.addClass('active');
        console.log('current match', $newActive.data('match'))
        $('#info .match').removeClass('active')
        $('#info .match[data-match="' + $newActive.data('match') + '"]').addClass('active')
        $body = $('html, body')
        console.log('body scrolltop', $body.scrollTop())
        console.log('newActive offset top', $newActive.offset().top)
        console.log('body offset top', $body.offset().top)
//        debugger;
//        $newActive[0].scrollIntoView()

        $body.animate({
          scrollTop: Math.max(0, $newActive.offset().top - 200) // $body.scrollTop() + ($newActive.offset().top - $body.offset().top)
        }, 150, 'swing', function() {
            console.log('animation complete')
            rect = $newActive[0].getBoundingClientRect()
            console.log('rect', rect)
            $('.overlay.top').css('bottom', '')
            $('.overlay.top').css('height', document.scrollingElement.scrollTop + rect.top + 'px')
            $('.overlay.left, .overlay.right').css('top', document.scrollingElement.scrollTop + rect.top + 'px')
            $('.overlay.right').css('left', rect['right'] + 'px')
            $('.overlay.bottom').css('top', document.scrollingElement.scrollTop + rect['bottom'] + 'px')
            $('.overlay.bottom').css('height', document.scrollingElement.scrollHeight - rect['bottom'] + 'px')
            $('.overlay.left').css('right', '')
            $('.overlay.left').css('width', rect['left'])

            $('.overlay.left, .overlay.right').css('height', rect['height'])
            $('.overlay').show()
        });
    }

    function goToPreviousMatch() {
        var $countryMatches = $('.country-match');
        var $foreignMatches = $('.foreign-match');
        index = getCurrentIndex();
        num_elements = $foreignMatches.length + $countryMatches.length
        index = (index - 1 + num_elements) % num_elements
        goToIndex(index);
    }

    function goToNextMatch() {
        var $countryMatches = $('.country-match');
        var $foreignMatches = $('.foreign-match');
        index = getCurrentIndex();
        num_elements = $foreignMatches.length + $countryMatches.length
        index = (index + 1 + num_elements) % num_elements
        goToIndex(index);
    }

    $(document).keydown(function(e) {
        switch(e.which) {
            case 37: // left
                console.log('left');
                goToPreviousMatch();
            break;

            case 38: // up
                console.log('up');
                goToPreviousMatch();
            break;

            case 39: // right
                console.log('right');
                goToNextMatch();
            break;

            case 40: // down
                console.log('down');
                goToNextMatch();
            break;

            default: return; // exit this handler for other keys
        }
        e.preventDefault(); // prevent the default action (scroll / move caret)
    });
})