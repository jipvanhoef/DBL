In this folder all our asset must be stored for the main pages this includes the css stylesheets and any picuters or icons
to link the html to a asset in this folder first include the folowing tag
{% load static %}
then write after href "{% static 'main/asset.css' %}"
the same works for other assets. 