#!/bin/bash
cd /tmp
git clone https://github.com/twardoch/mkdocs-combine.git
cd mkdocs-combine
pip install -e .
sudo apt-get install fonts-lmodern lmodern pandoc texlive-base texlive-latex-extra texlive-fonts-recommended texlive-latex-recommended texlive-xetex
pandoc --toc -f markdown+grid_tables+table_captions -o SpartanTriKringleConWriteup.pdf SpartanTriKringleConWriteup.pd
mkdocscombine -o SpartanTriKringleConWriteup.pd