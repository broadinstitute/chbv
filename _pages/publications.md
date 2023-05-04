---
layout: page
permalink: /publications/
title: Publications
title_long: Publications
description: Experimental and computational methods that make the science at the Center possible.
years: [2023, 2022]
nav: true
nav_order: 4
---
<!-- _pages/publications.md -->
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
