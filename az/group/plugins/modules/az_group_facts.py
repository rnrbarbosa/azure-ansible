#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: az_group_facts

short_description: AZURE facts regarding resource groups

version_added: "1.0.0"

description: AZURE facts regarding resource groups

options:
    subscription:
        description:
            - Azure subscription name
        required: true

author:
    - Roberto Barbosa (rnrbarbosa@gmail.com)
'''

EXAMPLES = r'''
- name: Return ansible_facts
  az.group.group_facts:
    subscription: 'Pay-As-You-Go'
'''

RETURN = r'''
ansible_facts:
  description: Azure Resource Group facts
  returned: always
  type: dict
  contains:
    groups:
      description: List of Resource Groups Ids
      type: str
      returned: When there are Resource Groups associated to the subscription
      sample: 'group-1'
'''

from ansible.module_utils.basic import AnsibleModule
from az.cli import az

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        subscription=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        ansible_facts=dict(),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    exit_code, result_dict, logs = az("group list --subscription " + module.params['subscription'])
    group_names = [y.split('/')[4] for y in (x['id'] for x in result_dict)]
    
    result['ansible_facts'] = {
        'groups': group_names,
    }
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()

if __name__ == '__main__':
    main()