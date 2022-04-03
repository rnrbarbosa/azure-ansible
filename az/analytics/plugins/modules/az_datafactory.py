#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: az_datafactory

short_description: Azure Data Factory

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str

extends_documentation_fragment:
    - az.analytics.az_datafactory

author:
    - Roberto Barbosa (@rnrbarbosa)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  az.analytics.az_datafactory:
    name: my_adf


# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'


    df_resource = Factory(location='westeurope')
    df = adf_client.factories.create_or_update(rg_name, df_name, df_resource)
    print_item(df)
'''

from ansible.module_utils.basic import AnsibleModule
from az.cli import az

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(
            type='str', 
            required=True),
        group=dict(
            type='str', 
            required=True),
        state=dict(
            type='str', 
            choices=['present','absent'], 
            default='present'
        )
    )


    result = dict(
        changed=False,
    )

    module = AnsibleModule(argument_spec=module_args)
    ########################################################################
    # MAIN
    ########################################################################
    # This program creates this resource group. If it's an existing resource group, comment out the code that creates the resource group
    rg_name = module.params['group']

    # The data factory name. It must be globally unique.
    df_name = module.params['name']

    exit_code=0
    changed=False

    az_command=f"datafactory show -n {df_name} -g {rg_name} -o json"
    exit_code, response, logs = az(az_command)

#    # ADF exists, do nothing
#     if not exit_code and module.params['state'] == 'present':
#         changed = False
#     # ADF exists but we don't want it to
#     elif exists and module.params['state'] == 'absent':
#         changed = True
#     # ADF doesn't exist but we want it to
#     else:
#         if module.params['state'] == 'present':
#             changed = True

    # only perform changes when a required change has been detected and if check mode is off
    if exit_code: 
        if module.params['state'] == 'present':
            # Create Data Factory
            az_command =  f"datafactory create -g {rg_name}  --factory-name {df_name} -o json"
            exit_code, result_dict , logs = az(az_command)
            if exit_code:
                module.fail_json(msg="Failed Creating Data Factory", meta=module.params)
            else:
                changed=True
    else:
        if module.params['state'] == 'absent':
            az_command =  f"datafactory delete -y -g {rg_name}  --factory-name {df_name} -o json"
            exit_code, result_dict , logs = az(az_command)
            if exit_code:
                module.fail_json(msg="Failed Deleting Data Factory", meta=module.params)
            else:
                changed=True

    module.exit_json(changed=changed,meta=module.params)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    if exit_code:
        module.fail_json(msg='Data Factory Failed to be created', **result)
 #
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()