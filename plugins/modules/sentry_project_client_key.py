#!/usr/bin/python

# Copyright: (c) 2022, Ridwan Fadjar Septian <ridwanbejo@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function


__metaclass__ = type



DOCUMENTATION = r"""
module: sentry_project_client_key
short_description: Manage project's client keys in Sentry. Currently supported operation are create, update and delete.
author:
    - "ridwanbejo (@ridwanbejo)"
description:
  - Based on Sentry API documentation (https://docs.sentry.io/api/), this module will help you to manage your project's client keys
options:
  sentry_host:
    description:
    - Target hostname of Sentry
    type: str
    default: true
    version_added: 1.0.0
  sentry_token:
    description:
    - Token which generated in Sentry by administrator. This token is located under "Settings > Internal Integration"
    type: str
    default: true
    version_added: 1.0.0
  organization_slug:
    description:
    - Slug of the organization
    type: str
    default: true
    version_added: 1.0.0
  project_slug:
    description:
    - slug for the chosen project
    type: str
    default: false
    version_added: 1.0.0
  client_key:
    description:
    - chosen client key for update and delete operation
    type: str
    default: false
    version_added: 1.0.0
  name:
    description:
    - new name for client key
    type: str
    default: false
    version_added: 1.0.0
  is_active:
    description:
    - enable or disabled the client key
    type: bool
    default: false
    version_added: 1.0.0
  state:
    description:
      - Perform operation to create, update or delete project's client key in Sentry
    default: 'present'
    choices: [present', 'absent']
    type: str
requirements:
    - "python >= 3.8.10"
    - "ansible >= 2.12.1"
    - "requests >= 2.26.0"
"""

EXAMPLES = r"""
# Create new project client key in Sentry
- name: Test Sentry Client Key module - create client key
    ridwanbejo.sentry.sentry_project_client_key:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      project_slug: 'selamat-pagi'
      organization_slug: 'sentry'
      name: 'default_key'
      is_active: true
      state: present
    register: testout

# Update project client key which the key is 2b31e31bf52742d7a6f6b9d695c23c06 and project slug selamat-pagi in Sentry with new name
- name: Test Sentry 10 Client Key module - update client key
    ridwanbejo.sentry.sentry_project_client_key:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      project_slug: 'selamat-pagi'
      organization_slug: 'sentry'
      client_key: '2b31e31bf52742d7a6f6b9d695c23c06'
      name: 'default client key abcdef'
      is_active: true
      state: present

# Delete project client key which has project slug selamat-pagi and client key afe0b49402a9400191797b22984ff0f8
- name: Test Sentry 10 Client Key module - delete client key
    ridwanbejo.sentry.sentry_project_client_key:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      project_slug: 'selamat-pagi'
      organization_slug: 'sentry'
      client_key: 'afe0b49402a9400191797b22984ff0f8'
      state: absent
    register: testout
"""

RETURN = r"""
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ridwanbejo.sentry.plugins.module_utils.sentry_api import SentryApi

import requests
import json


def run_module():
    module_args = dict(
        sentry_host=dict(type='str', require=True),
        sentry_token=dict(type='str', require=True),
        organization_slug=dict(type='str', required=True),
        project_slug=dict(type='str', required=False),
        client_key=dict(type='str', required=False),
        name=dict(type='str', required=False),
        is_active=dict(type='bool', required=False),
        state=dict(
            default="present", 
            choices=['present', 'absent'],  
            type='str')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(dict(
            changed=False,
            message='Check mode success!'
        ))

    result = dict(
    )

    sentry_api = SentryApi(module, module.params['sentry_host'], module.params['sentry_token'])

    # a. if state is present then check the existence of client key
    if module.params['state'] == "present":

        # a.1. if the client key is provided
        if (module.params['client_key'] == "") or (module.params['client_key'] is None):
            result = sentry_api.create_client_key(
                module.params['organization_slug'],
                module.params['project_slug'],
                module.params['name']
            )

            if result['status_code'] != 201:
                module.fail_json(msg=result)

        # a.2. if the client key is not provided
        else:
            result = sentry_api.update_client_key(
                module.params['organization_slug'],
                module.params['project_slug'],
                module.params['client_key'],
                module.params['name'],
                module.params['is_active']
            )

            if result['status_code'] != 200:
                module.fail_json(msg=result)
            
    # b. if state is absent then delete the client key
    elif module.params['state'] == "absent":
        result = sentry_api.delete_client_key(
            module.params['organization_slug'],
            module.params['project_slug'],
            module.params['client_key']
        )

        if result['status_code'] != 204:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
