#!/bin/bash

pylint plugins -E --output-format=colorized
ansible-galaxy collection build --force
ansible-galaxy collection install ridwanbejo-sentry-1.0.0.tar.gz --force
