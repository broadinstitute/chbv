---
layout: page
permalink: /join-us/
title: Join
title_long: Join Us
nav: true
nav_order: 8
display_categories: [Open positions]
---

<!-- pages/join_us.md -->
<div>
<p>The Center is committed to assembling a team with a variety of perspectives, while fostering a welcoming environment where all members flourish.</p>

<p>We're always looking for outstanding applicants who share our passion for understanding brain function and its dysfunction in disease. If there are no open roles that fit your talents, please send your CV and cover letter to <a href="mailto:brain@broadinstitute.org">brain@broadinstitute.org</a>. Postdoctoral applicants are especially encouraged to apply.</p>
</div>

{% assign any_open_jobs = 0 %}

{% if any_open_jobs == 1 %}

<div class="team">
  <!-- Display categorized jobs -->
  {%- for category in page.display_categories %}
  <h2 class="category">{{ category }}</h2>
  {%- assign categorized_job = site.jobs | where: "category", category -%}
  {%- assign sorted_job = categorized_job | sort: "importance" %}
  <!-- Generate cards for each job -->
  <div class="grid">
    {%- for job in sorted_job -%}
      {% include job.html %}
    {%- endfor %}
  </div>
  {% endfor %}
</div>
{% endif %}
