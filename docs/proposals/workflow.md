Example of generating installer from workflow configuration:
```
ftl_installer -w foo_workflow.yml -o foo_installer
```

Top level config keys:
- config
- variants
- workflows
- stages
- steps
- step_groups
- roles


Sample Workflow Definition
```
--- 
config:
  version: 2.2
  migrations:
  - migrate_v1_to_v2:
    when: "{{ config_version | version_compare('lt', 2.0) }}"
  - migrate_v2_to_v2_1:
    when: "{{ config_version | version_compare('lt', 2.1) }}"
  - migrate_v2_1_to_v2_2:
    when: "{{ config_version | version_compare('lt', 2.2) }}"
  validators:
  - upstream:
    when: "{{ variant.name == 'upstream' }}"
  - enterprise:
    when: "{{ variant.name == 'enterprise' }}"
  - containerized:
    when: "{{ config.deployment.containerized | default(false) }}"
  - valid_ha_config:
    when: "{{ config.deployment.ha | default(false) }}"

variants:
  foo_upstream:
    display_name: Foo Upstream
    description: >
      Foo Upstream is an Open Source Project that allows you to Foo
      all the things!
    default_version: 2.0
    versions:
    - 2.0
    - 1.1
    - 1.0
    workflows:
    - install
    - scale_foo
    - upgrade
    - reconfigure
    - validate_foo
  foo_enterprise:
    display_name: Foo Enterprise
    description: >
      Foo Enterprise is the premier enterprise platform to Foo all the
      things! Brought to you by Wombat, Inc.
    description: Foo Enterprise
    default_version: 1.1
    versions:
    - 1.1
    - 1.0
    workflows:
    - install
    - scale_foo
    - upgrade
    - reconfigure
    - validate_foo
    - upgrade_from_upstream

workflows:
  install:
    description: "Install {{ variant_description }} {{ variant_version }}"
    stages:
    - pre_install_check:
      when: "{{ not config.deployment.skip_pre_install_check | default(false) }}"
    - bootstrap_bar:
      when: "{{ 'bar' in config.deployment.roles }}"
    - configure:
    - validate_install:
      when: "{{ not config.deployment.skip_validation |default(false) }}"
    - post_install:
    - validate_post_install:
      when: "{{ not config.deployment.skip_validation |default(false) }}"
  upgrade:
    desription: "Upgrade {{ variant_description }} to version {{ variant_version }}"
    stages:
    - pre_upgrade_check:
      when: "{{ not config.deployment.skip_pre_install_check | default(false) }}"
    - upgrade
    - validate_upgrade
      when: "{{ not config.deployment.skip_validation |default(false) }}"
    - post_upgrade
    - validate_post_upgrade
      when: "{{ not config.deployment.skip_validation |default(false) }}"






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
