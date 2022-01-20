#!/usr/bin/python

# Copyright: (c) 2022, Ridwan Fadjar Septian <ridwanbejo@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function


__metaclass__ = type



DOCUMENTATION = r"""
module: sentry_project
short_description: Manage projects in Sentry. Currently supported operation are create, update and delete.
author:
    - "ridwanbejo (@ridwanbejo)"
description:
  - Based on Sentry API documentation (https://docs.sentry.io/api/), this module will help you to manage your projects
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
  team_slug:
    description:
    - slug of the team
    type: str
    default: false
    version_added: 1.0.0
  project_slug:
    description:
    - slug for the chosen project
    type: str
    default: false
    version_added: 1.0.0
  name:
    description:
    - new name for the project
    type: str
    default: false
    version_added: 1.0.0
  slug:
    description:
    - new slug for the project
    type: str
    default: false
    version_added: 1.0.0
  platform:
    description:
    - Platform for the chosen project
    type: str
    default: false
    version_added: 1.0.0
  is_bookmarked:
    description:
    - Bookmark the project
    type: bool
    default: false
    version_added: 1.0.0
  state:
    description:
      - Perform operation to create, update and delete project in Sentry
    default: 'present'
    choices: [present', 'absent']
    type: str
requirements:
    - "python >= 3.8.10"
    - "ansible >= 2.12.1"
    - "requests >= 2.26.0"
"""

EXAMPLES = r"""
# Create new project in Sentry
- name: Test Sentry Project module - create project
    ridwanbejo.sentry.sentry_project:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      name: 'Bonjour'
      slug: 'bonjour'
      organization_slug: 'sentry'
      team_slug: 'sentry'
      state: present

# Update project which has slug bonjour in Sentry with new slug and name
- name: Test Sentry Project module - update project
    ridwanbejo.sentry.sentry_project:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      organization_slug: 'sentry'
      project_slug: 'bonjour'
      name: 'Buongiorno'
      slug: 'bonjour-monsieur'
      platform: "python"
      is_bookmarked: true
      state: present

# Delete project which has slug bonjour-monsieur
- name: Test Sentry Project module - delete project
    ridwanbejo.sentry.sentry_project:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      organization_slug: 'sentry'
      project_slug: 'bonjour-monsieur'
      state: absent
"""

RETURN = r"""
"""

import requests
import json

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ridwanbejo.sentry.plugins.module_utils.sentry_api import SentryApi


def run_module():
    module_args = dict(
        sentry_host=dict(type='str', require=True),
        sentry_token=dict(type='str', require=True),
        organization_slug=dict(type='str', required=True),
        team_slug=dict(type='str', required=False),
        project_slug=dict(type='str', required=False),
        name=dict(type='str', required=False),
        slug=dict(type='str', required=False),
        platform=dict(type='str', required=False),
        is_bookmarked=dict(type='bool', required=False),
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

    # a. if state is present then check the existence of project
    if module.params['state'] == "present":

        # a.1. if the project is not exist then create new project
        retrieve_requests = sentry_api.retrieve_project(
            module.params['organization_slug'],
            module.params['project_slug']
        )

        if retrieve_requests['status_code'] == 200:
            result = sentry_api.update_project(
                module.params['organization_slug'],
                module.params['project_slug'],
                module.params['team_slug'],
                module.params['name'],
                module.params['slug'],
                module.params['platform'],
                module.params['is_bookmarked']
            )

            if result['status_code'] != 200:
                module.fail_json(dict(message="Failed update operation", status_code=result['status_code'], response=result['response']))

        # a.2. if the project is exist before then update the project
        elif retrieve_requests['status_code'] == 404:

            result = sentry_api.create_project(
                module.params['organization_slug'],
                module.params['team_slug'],
                module.params['name'],
                module.params['slug']
            )

            if result['status_code'] != 201:
                module.fail_json(dict(message="Failed create operation", status_code=result['status_code'], detail=result['response']))

    # b. if state is absent then delete the project
    elif module.params['state'] == "absent":
        result = sentry_api.delete_project(
            module.params['organization_slug'],
            module.params['project_slug']
        )

        if result['status_code'] != 204:
            module.fail_json(dict(message="Failed delete operation", status_code=result['status_code'], detail=result['response']))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
