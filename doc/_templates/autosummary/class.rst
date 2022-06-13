{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

.. rubric:: Attributes

.. autosummary::
    {% for item in attributes %}
        {{ objname }}.{{ item }}
    {% endfor %}

.. rubric:: Methods

.. autosummary::
    {% for item in methods %}
    {% if item != "__init__" %}
        {{ objname }}.{{ item }}
    {% endif %}
    {% endfor %}

----

.. rubric:: Method documentation

{% for item in methods %}
{% if item != '__init__' %}
.. automethod:: {{ objname }}.{{ item }}
{% endif %}
{% endfor %}

.. raw:: html

     <div style='clear:both'></div>

