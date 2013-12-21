# salt's locale.system only sets LANG but we want to set LC_ALL as well
# This is done in margarita, but by using sed to change LANG and LC_ALL from their defaults to
# en_US.UTF-8. The problem is if LANG or LC_ALL aren't there at all, then they won't be changed.
# So, instead, we just make the file look the way we want it to.

/etc/default/locale:
  file.managed:
    - source: salt://locale/locale
    - user: root
    - mode: 644
