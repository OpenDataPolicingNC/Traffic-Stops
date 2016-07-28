import $ from 'jquery';

$(function ($) {
  var $padder = $('.affix-padder');
  var $affixEl = $('.affix-element');
  var BREAKPOINT = 770;
  var $offsetTopPos, $offsetTopNeg, $offsetBottom;

  if ($(window).width() > BREAKPOINT && $affixEl.length > 0) {
    $offsetTopPos = $('.affix-offset-top-pos');
    $offsetTopNeg = $('.affix-offset-top-neg');
    $offsetBottom = $('.affix-offset-bottom');

    $affixEl.affix({
      offset: {
        top: function () {
          var offsetTopPos = 0, offsetTopNeg = 0;

          $offsetTopPos.each(function () {
            offsetTopPos += $(this).outerHeight();
          });

          $offsetTopNeg.each(function () {
            offsetTopNeg += $(this).innerHeight();
          })

          return offsetTopPos - offsetTopNeg;
        },
        bottom: function () {
          return $offsetBottom.outerHeight(true);
        }
      }
    })
    .on('affixed.bs.affix', function () {
      $padder.height($affixEl.outerHeight());
    })
    .on('affixed-top.bs.affix', function () {
      $padder.height(0);
    });
  }
});
