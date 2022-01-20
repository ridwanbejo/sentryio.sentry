#!/bin/bash

ANSIBLE_GIT_PATH=/home/ridwansense/Documents/ridwanbejo/repository/ansible

LOCAL_ANSIBLE_COLLECTIONS_PATH=/home/ridwansense/.ansible/collections/ansible_collections

. ${ANSIBLE_GIT_PATH}/venv/bin/activate

. ${ANSIBLE_GIT_PATH}/hacking/env-setup

cd ${LOCAL_ANSIBLE_COLLECTIONS_PATH}

ansible-test sanity --test pep8
