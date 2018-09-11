#!/usr/bin/bash
git commit -m "stable branch update" gcc-stable-branch.patch
make bump
make koji-nowait
