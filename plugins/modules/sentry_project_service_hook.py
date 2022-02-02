#!/usr/bin/python

# Copyright: (c) 2022, Ridwan Fadjar Septian <ridwanbejo@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function


__metaclass__ = type



DOCUMENTATION = r"""
module: sentry_project_service_hook
short_description: Manage project service hook in Sentry. Currently supported operation are create, update and delete.
author:
    - "ridwanbejo (@ridwanbejo)"
description:
  - Based on Sentry API documentation (https://docs.sentry.io/api/), this module will help you to manage your project service hook
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
  hook_id:
    description:
    - new name for service hook
    type: str
    default: false
    version_added: 1.0.0
  hook_url:
    description:
    - URL for service hook target
    type: str
    default: false
    version_added: 1.0.0
  hook_events:
    description:
    - list events that trigger service hook
    type: list
    default: false
    version_added: 1.0.0
  state:
    description:
      - Perform operation to create, update and delete project service hook in Sentry
    default: 'present'
    choices: [present', 'absent']
    type: str
requirements:
    - "python >= 3.8.10"
    - "ansible >= 2.12.1"
    - "requests >= 2.26.0"
"""

EXAMPLES = r"""
# Create new project service hook in Sentry
- name: Test Sentry service hook module - create service hook
    ridwanbejo.sentry.sentry_project_service_hook:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      project_slug: 'selamat-sore'
      organization_slug: 'sentry'
      hook_url: 'https://example.com/sentry_hook/'
      hook_events: 
      - event.alert 
      - event.created
      state: present

# Update project which has slug bonjour in Sentry with new slug and name
- name: Test Sentry service hook module - update service hook
    ridwanbejo.sentry.sentry_project_service_hook:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      project_slug: 'selamat-sore'
      organization_slug: 'sentry'
      hook_id: '4451ffd8134440d9a5e0c20e7d635234'
      hook_url: 'https://example.com/sentry_hooks/'
      hook_events:
      - event.created
      state: present

# Delete project which has slug bonjour-monsieur
- name: Test Sentry 10 service hook module - delete service hook
    ridwanbejo.sentry.sentry_project_service_hook:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      project_slug: 'selamat-sore'
      organization_slug: 'sentry'
      hook_id: '4451ffd8134440d9a5e0c20e7d635234'
      state: absent
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
        hook_id=dict(type='str', required=False),
        hook_url=dict(type='str', required=False),
        hook_events=dict(type='list', required=False),
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

    # a. if state is present then check the existence of hook
    if module.params['state'] == "present":

        # a.1. if the hook_id is provided
        if (module.params['hook_id'] == "") or (module.params['hook_id'] is None):
            result = sentry_api.create_service_hook(
                module.params['organization_slug'],
                module.params['project_slug'],
                module.params['hook_url'],
                module.params['hook_events']
            )

            if result['status_code'] != 201:
                module.fail_json(msg=result)

        # a.2. if the hook_id is not provided
        else:
            result = sentry_api.update_service_hook(
                module.params['organization_slug'],
                module.params['project_slug'],
                module.params['hook_id'],
                module.params['hook_url'],
                module.params['hook_events']
            )

            if result['status_code'] != 200:
                module.fail_json(msg=result)

    # b. if state is absent then delete the client key
    elif module.params['state'] == "absent":
        result = sentry_api.delete_service_hook(
            module.params['organization_slug'],
            module.params['project_slug'],
            module.params['hook_id']
        )

        if result['status_code'] != 204:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
