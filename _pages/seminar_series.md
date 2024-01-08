---
layout: page
permalink: /seminar-series/
title: Seminar Series
title_long: Seminar Series
nav: false
category: Center leadership
---
Our Seminar Series is a quarterly series designed to make cutting-edge neuroscience research accessible to all.  Our lineup features speakers from a variety of career stages with diverse backgrounds and expertise.  We believe in the power of diversity and inclusion, recognizing that a multitude of voices contributes to a richer scientific dialogue. 

Register for our upcoming events, read about the speakers, watch previous talks, and delve into the fascinating world of neuroscience. Join us as we connect minds, share knowledge, and pave the way for a more accessible and collaborative scientific community.
<h2>Upcoming seminars</h2>
  {%- assign sorted_seminars = site.seminars -%}

  <!-- Generate cards for each seminar -->
  <div class="grid">
    {%- for seminar in sorted_seminars -%}
      {% include seminar.html %}
    {%- endfor %}
  </div>
