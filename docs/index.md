---
title: Home
layout: home
nav_order: 1
---

<div class="sb-hero">
  <img src="{{ '/assets/readme-banner.png' | relative_url }}" alt="Space Base strategy and simulation" />
</div>

<p class="sb-lead">
  Race to <strong>40 VP</strong> across twelve sectors — blue rewards on your turn, red on theirs.
  Strategy guides for every player count, plus the <strong>spacebase2p</strong> Python simulator and live bot stats.
</p>

<div class="sb-sim-highlight">
  <span class="sb-pill"><em>spacebase2p</em> — CLI batch games</span>
  <span class="sb-pill">Bots: income · rush · random</span>
  <span class="sb-pill"><a href="{{ '/simulation.html' | relative_url }}">Plots &amp; results</a></span>
</div>

## Explore

<div class="sb-cards">
  <div class="sb-card">
    <strong>Simulation</strong>
    <a href="{{ '/simulation.html' | relative_url }}">Bot matchups &amp; charts</a> — win rates, overspend, colony timing from <code>spacebase2p</code>.
  </div>
  <div class="sb-card">
    <strong>Engine</strong>
    <a href="{{ '/engine.html' | relative_url }}">Dice, income floor, colonies</a> — shared rules for all modes.
  </div>
  <div class="sb-card">
    <strong>Two-player</strong>
    <a href="{{ '/guide/2p-normal.html' | relative_url }}">Normal start</a> — income, arrows, closing race.
  </div>
  <div class="sb-card">
    <strong>Three-player</strong>
    <a href="{{ '/guide/3p-normal.html' | relative_url }}">Normal start</a> — red stacks, earlier colonies.
  </div>
  <div class="sb-card">
    <strong>Light Speed</strong>
    <a href="{{ '/guide/light-speed.html' | relative_url }}">15-gold draft</a> — 2p and 3p LS playbooks.
  </div>
  <div class="sb-card">
    <strong>Cheat sheet</strong>
    <a href="{{ '/guide/quick-reference.html' | relative_url }}">Quick reference</a> — one table, four sentences.
  </div>
</div>

<div class="sb-callout">
  <strong>Run the sim locally:</strong>
  <code>pip install -e ".[dev]"</code> then
  <code>python3 -m spacebase2p.cli -n 500 --p0 income --p1 rush</code>.
  Regenerate site plots with <code>python3 scripts/generate_simulation_plots.py</code>.
</div>
