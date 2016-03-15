Proposal for config file format:
```
# top level values represent installer config
version: v1
variant: Product Variant
variant_version: Product Variant Version

# The deployment key specifies values that apply to the whole deployment
deployment:
  ansible_ssh_user: root  # this could be set on a per host basis as well
  ansible_become: no      # same as above

  # mapped_ansible_var_1 does not need to match up with the ansible variable
  # name, the installer should maintain a set of mappings for known
  # name/variable combinations
  mapped_ansible_var_1: my_value

  # unmapped variables are passed along directly to ansible at the associated
  # group level
  unmapped_ansible_var_1: my_value

  # the hosts key represents settings applied at the host level
  hosts:
    # connect_to is an optional variable that can be used to override the ansible
    # inventory connect_to value, otherwise the mapped value that is used for
    # setting the hostname in the inventory for the host will be used instead
  - connect_to: my_connect_to_string 
    mapped_host_var_1: host_val_1
    unmapped_host_var_1: host_val_2
    # roles links an individual host to appropriate role defined under
    # deployment.roles
    roles:
    - role_a
    - role_b
  roles:    
    role_a:
      mapped_role_var_1: my_role_a_val
      unmapped_role_var_2: my_role_a_val2
    role_b:
      mapped_role_var_1: my_role_b_val
      unmapped_role_var_2: my_role_b_val2
```
