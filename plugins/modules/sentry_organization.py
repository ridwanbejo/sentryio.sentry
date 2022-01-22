#!/usr/bin/python

# Copyright: (c) 2022, Ridwan Fadjar Septian <ridwanbejo@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function


__metaclass__ = type



DOCUMENTATION = r"""
module: sentry_organization
short_description: Manage organization information in Sentry. Currently supported operation is update only.
author:
    - "ridwanbejo (@ridwanbejo)"
description:
  - Based on Sentry API documentation (https://docs.sentry.io/api/), this module will help you to update your organization information
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
    - Slug of organization which need to be updated
    type: str
    default: true
    version_added: 1.0.0
  name:
    description:
    - name for the organization
    type: str
    default: false
    version_added: 1.0.0
  slug:
    description:
    - slug for the organization
    type: str
    default: false
    version_added: 1.0.0
  state:
    description:
      - Perform operation to update organization information. This state option is provided to handle another operation from Sentry API
    default: 'present'
    choices: [present']
    type: str
requirements:
    - "python >= 3.8.10"
    - "ansible >= 2.12.1"
    - "requests >= 2.26.0"
"""

EXAMPLES = r"""
# Update default name and slug to new organization name and slug
- name: Update organization in Sentry
    ridwanbejo.sentry.sentry_organization:
      sentry_host: "http://localhost:9000"
      sentry_token: "8702e9c2d5224b60b24d2f7a9fa486f0eaaee9748a0e4acda3ea8febdc790093"
      name: 'My Great Company'
      slug: 'my-great-company'
      organization_slug: 'sentry'
      state: present
"""

RETURN = r"""
msg:
  description:
  - If a change was successfully applied, it will return the updated object, otherwise returns response with status code 40x.
  returned: always
  type: complex
  contains:
     changed:
       description: If update process succeed, changed will be true otherwise false
       returned:always
       type: bool
     failed:
       description: failure status of this module execution
       returned: always
       type: bool
     message:
       description: Additional message along yield by this module
       returned: always
       type: str
       sample: Organization has been updated
     response:
       description: Response from organization related endpoints. Will vary based on the I(api_version) and I(kind). Check more response detail at https://docs.sentry.io/api/organizations/update-an-organization/
       returned: always
       type: complex
     status_code:
       description: Response status code
       returned: always
       type: int
       sample: 200
     url:
       description: requested URL from this module
       returned: always
       type: str
       sample: http://localhost:9000/api/0/organizations/my-great-company/
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
        name=dict(type='str', required=False),
        slug=dict(type='str', required=False),
        state=dict(
            default="present", 
            choices=['present'],  
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

    # a. if state is present then check the existence of organization
    if module.params['state'] == "present":

        # a.1. if the organization is not exist then create new organization
        retrieve_requests = sentry_api.retrieve_organization(
            module.params['organization_slug']
        )

        if retrieve_requests['status_code'] == 200:
            result = sentry_api.update_organization(
                module.params['organization_slug'],
                module.params['name'],
                module.params['slug'],
            )

            if result['status_code'] != 200:
                module.fail_json(msg=result)
        else:
            result = retrieve_requests
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
