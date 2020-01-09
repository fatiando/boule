{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

.. rubric:: Attributes

.. autosummary::
    {% for item in attributes %}
        {{ objname }}.{{ item }}
    {% endfor %}

 {% if methods|length > 1 %}

.. rubric:: Methods

.. autosummary::
    {% for item in methods %}
    {% if item != '__init__' %}
        {{ objname }}.{{ item }}
    {% endif %}
    {% endfor %}

{% endif %}

----

{% for item in methods %}
{% if item != '__init__' %}
.. automethod:: {{ objname }}.{{ item }}
{% endif %}
{% endfor %}

.. include:: backreferences/{{ fullname }}.examples

.. raw:: html

     <div style='clear:both'></div>

