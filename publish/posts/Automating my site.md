---
layout: post
title: "Automating my site (Factory must grow)"
date: 20.8.2025
categories: jekyll update
---

I wanted to get more into writing about my projects and thought in general since I want to better my writing. My thesis was in English and I really felt it lacking in the fancy words and coherent writing department. I figured that one of the better ways to get better at writing was to write. I wanted to write something meaningful that would be fun and entertaining and I remembered I actually have a static Jekyll site (this one!)
![[Pasted image 20250820203255.png]]

While writing in neovim is lovely on it's own, I sometimes miss the cool features that modern internet gardens like Notion or Obsidian have, and because I am a good little software engineer I love me some self-hosting and open-source which is why I always chose Obsidian.

Now I can write my notes in Obsidian and then copy paste them to my static site, but that is rather annoying and makes me feel a little bit stupid. The idea is of course to automate this process as much as possible so straight up I grabbed everyone's favourite scripting language and got to work. First problem I encoutered is that Jekyll sited require very specific setup of directories.