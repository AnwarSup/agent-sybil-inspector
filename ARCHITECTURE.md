# Agent Sybil Inspector Architecture

## Overview

Agent Sybil Inspector is packaged as a self-contained static web application. The page renders a product-grade AI-agent workflow without any server-side dependency.

## Runtime Model

1. Static HTML loads in the browser.
2. CSS defines the unique product metaphor and layout.
3. JavaScript drives deterministic scenario state, simulated agent reasoning, scoring, and action queues.
4. The page can be mirrored across multiple static hosts without build steps.

## Components

- Presentation layer: semantic HTML sections for hero, scenario area, metrics, evidence, and CTA.
- Interaction layer: small JavaScript handlers for tabs/buttons/state updates.
- Simulation layer: fixed datasets used to show agent output consistently during review.

## Deployment

Compatible with:

- GitHub Pages
- Surge.sh
- Vercel
- Netlify
- Cloudflare Pages
- Render Static Sites

## Security Notes

- No external secrets.
- No wallet signing.
- No tracking pixels.
- No private APIs.
- Safe to publish as a public demo repository.
