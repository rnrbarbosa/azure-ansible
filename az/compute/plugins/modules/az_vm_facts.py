#!/usr/bin/python

# Copyright: (c) 2022, Roberto Barbosa <rnrbarbosa@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: az_vm_facts

short_description: AZURE facts regarding resource groups

version_added: "1.0.0"

description: AZURE facts regarding Virtual Machine

options:
    subscription:
        description:
            - Azure subscription name
        required: true
    group:
        description:
            - Name of resource group. 
        required: true
    vm:
        description:
            - The name of the Virtual Machine


author:
    - Roberto Barbosa (rnrbarbosa@gmail.com)
'''

EXAMPLES = r'''
- name: Return ansible_facts
  az.group.vm_facts:
    subscription: 'Pay-As-You-Go'
    vm: 'host1'
'''

RETURN = r'''
ansible_facts:
  description: Azure Resource Group facts
  returned: always
  type: dict
  contains:
    os_disk:
      description: VM OS Disk
      type: str
      returned: VM OS Disk
    data_disk:
      description: VM List of Data Disks
      type: str
      returned: VM List of Data Disks
'''

from ansible.module_utils.basic import AnsibleModule
from az.cli import az

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        vm=dict(type='str', required=True),
        group=dict(type='str', required=True),
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

    vm =  module.params['vm']
    group = module.params['group']

    vm_facts = []
    vm_os_disk = ""
    vm_data_disks = []
    vm_nics = []


    az_command =  f"vm show --name {vm} -g {group} -o json"
    exit_code, result_dict , logs = az(az_command)
    vm_facts = result_dict

    az_command =  f"vm show --name {vm} -g {group} --query 'storageProfile.osDisk' -o json"
    exit_code, result_dict , logs = az(az_command)
    if result_dict:
        vm_os_disk = result_dict['name']

    az_command =  f"vm show --name {vm} -g {group} --query 'storageProfile.dataDisks' -o json"
    exit_code, result_dict , logs = az(az_command)
    if result_dict:
        vm_data_disks = [x['name'] for x in result_dict]
    
    az_command =  f"vm show --name {vm} -g {group} --query 'networkProfile.networkInterfaces' -o json"
    exit_code, result_dict , logs = az(az_command)
    if result_dict:
        vm_nics = [x['id'] for x in result_dict]

    result['ansible_facts'] = {
        'vm': vm_facts,
        'os_disk': vm_os_disk,
        'data_disks': vm_data_disks,
        'nics': vm_nics,
    }

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()