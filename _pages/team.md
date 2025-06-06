---
layout: page
title: Team
title_long: Our team
permalink: /team/
nav: true
nav_order: 2
horizontal: false
display_categories: [Center leadership, Co-investigators, Project Management and Operations, Computational Analysis, Data Generation]
---

<!-- pages/team.md -->
<img src="/assets/img/team_202501.jpg" alt="Group photo of the research team." height="100%" width="100%" display="block">

<div class="category-links">
  {% for category in page.display_categories %}
    <a href="#{{ category | slugify }}" class="category-button">{{ category }}</a>
  {% endfor %}
</div>

<div class="team">
{%- if site.enable_team_categories and page.display_categories %}
  <!-- Display categorized team -->
  {%- for category in page.display_categories %}
  <h2 class="category" id="{{ category | slugify }}" >{{ category }}</h2>
  {%- assign categorized_team = site.team | where: "category", category -%}
  {%- assign sorted_team = categorized_team | sort: "importance" %}
  <!-- Generate cards for each team member -->
  {% if page.horizontal -%}
  <div class="container">
    <div class="row row-cols-2">
    {%- for team in sorted_team -%}
      {% include team_horizontal.html %}
    {%- endfor %}
    </div>
  </div>
  {%- else -%}
  <div class="grid">
    {%- for team in sorted_team -%}
      {% include team.html %}
    {%- endfor %}
  </div>
  {%- endif -%}
  {% endfor %}

{%- else -%}
<!-- Display team without categories -->
  {%- assign sorted_team = site.team | sort: "importance" -%}
  <!-- Generate cards for each team -->
  {% if page.horizontal -%}
  <div class="container">
    <div class="row row-cols-2">
    {%- for team in sorted_team -%}
      {% include team_horizontal.html %}
    {%- endfor %}
    </div>
  </div>
  {%- else -%}
  <div class="grid">
    {%- for team in sorted_team -%}
      {% include team.html %}
    {%- endfor %}
  </div>
  {%- endif -%}
{%- endif -%}
</div>

<!-- Display alumni -->
<div class="alumni">
  {%- assign category = "Alumni" %}
  <h2 class="category">{{ category }}</h2>
  {%- assign categorized_team = site.team | where: "category", category -%}
  {%- assign sorted_team = categorized_team | sort: "title" %}
  <!-- Generate list of alumni-->
  {%- for team in sorted_team -%}
    {% include alumni.html %}
  {%- endfor %}
</div>
