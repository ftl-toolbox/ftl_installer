Rough concept for the workflow yaml definition:
```
---
# Variants are used to limit workflows and roles available during the
# deployment.
variants:
  openshift-enterpise:
    variant_name: Atomic OpenShift Enterprise
    workflows: [install, upgrade, reconfigure, validate, manage_certificates,
add_node]
    roles: [master, node, etcd, lb, storage]
  atomic-enterprise:
    variant_name: Atomic Enterprise Platform
    workflows: [install, upgrade, reconfigure, validate, manage_certificates,
add_node]
    roles: [master, node, etcd, lb, storage]
  origin:
    variant_name: Origin
    workflows: [install, upgrade, reconfigure, validate, manage_certificates,
add_node]
    roles: [master, node, etcd, lb]

# Role configuration would be used to help with branching considerations in
# the stages
roles:
  masters:
    description: blah
    required: true
    ha: true
  nodes:
    description: blah
    required: true
    ha: false
  etcd:
    description: blah
    required: false
    ha: true
  lb:
    description: blah
    required: false
    ha: false
  storage:
    description: blah
    required: false
    ha: false

# Workflows basically tie the different high level actions (install, upgrade,
# etc) into a set of stages
workflows:
  install:
    description: blah blah blah
    stages:
    - pre_install
    - configure
    - validate
    - post_install
    - validate_post
  upgrade:
    desription: blah blah blah
    stages:
    - pre_upgrade
    - upgrade
    - validate_upgrade
    - post_upgrade
    - validate_post_upgrade
  ...


# Stages here are the workhorse of the workflow, they would have to be able to
# reference other stages (for re-use) and would be an ordered set of
# questions, actions and some type of conditionals based on other settings. In
# my head, they are able to set and interact with object attributes and
# methods.
stages:
  gather_host_info:
     description: blue green yellow
    - type: question
      prompt: Host type to use
      question_type: choice
      choices: get_host_types # python method to return an object of the
host_types below
      dest: host_type
    - type: branch
      if:
        condition: host_type in [on_demand, dynamic]
        - type: question
          prompt: Provider to use
          question_type: choice
          choices: host_type.providers
          dest: provider
        - type: question
          prompt: Provider credentials
          question_type: string
          dest: provider_creds
        - type: branch
          if:
            condition: host_types is on_demand
            - type: action
              description: blah blah blah
              action: provider.launch_instance, provider_creds
          else:
            - type: question
              question_type: string
              prompt: host tag?
              dest: host_tag
            - type: action
              action: provider.set_tag, host_tag
      else:
      ...
  pre_install:
    description: blah blah blah
    steps:
    - type: stage
      stage: gather_host_info
      

# host_types wouldn't come into play until we want to support dynamic
# inventories or provisioning of instances.
# These would need quite a bit of scaffolding around them, so I'm not sure we
# have much of a win here, except if there are provider specific questions,
# actions, etc...  
host_types:
- id: on_demand # These would be cloud envs where we would provision the hosts
  for the user
  providers:
    id: ec2
    supported_features:
    - host
    - load_balancer
    - security_groups
    - dns
- id: detected # Hosts that we gather from a dynamic inventory script
  providers:
    id: ec2
    supported_features:
    - load_balancer
    - security_groups
    id: rhev
    supported_features:
    - self_manage_ip
- id: user_entered # Hosts that the user enters
    supported_features:
    - self_manage_ip
```
