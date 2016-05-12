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
- roles



TODO:
- define actions to do on failure of steps, stages and workflows


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
    when: "{{ variant.name == 'foo_upstream' }}"
  - enterprise:
    when: "{{ variant.name == 'foo_enterprise' }}"
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
    description: "Install {{ variant.description }} {{ variant.version }}"
    stages:
    - gather_install_hosts
    - pre_install_check
    - bootstrap_bar
    - configure
    - validate_install
    - post_install
    - validate_post_install
  upgrade:
    desription: "Upgrade {{ variant.description }} to version {{ variant.version }}"
    stages:
    - gather_upgrade_hosts
    - pre_upgrade_check
    - upgrade
    - validate_upgrade
    - post_upgrade
    - validate_post_upgrade

stages:
  - gather_install_hosts:
      description: Gather Hosts
      steps:
      - provision_hosts: # built in component to auto-provision hosts this will
                         # also add config related to the config for what providers
                         # where selected
          providers: # optional, allows for limiting or adding additional providers
          - ec2 # built-in
          - gce # built-in
          - openstack # built-in
          - existing # built-in for pre-existing hosts
          - my_custom_provider # provisioner plugin
          allow_multi_provider: yes
          # TODO: need to add ability to have a provisioning workflow,
          #       apply properties and roles to hosts, needs to be flexible
          #       enough to handle host-by-host and also hosts provisioned
          #       through templates. Should be able to take params to modify
          #       provisioning as well as apply things post-provisioning.
      - inventory: # built-in component that will invoke dynamic inventory based on
                   # config file, or generate from defined hosts, also needs to handle
                   # host/role mapping
  - pre_install_check:
      description: Pre Installation Check
      steps:
      - validate_subscription:
        when: "{{ not skip_subscription | bool }}"
      - pre_installation_tasks:
  - bootstrap_bar:
      steps:
      - bootstrap_bar
    when: "{{ 'bar' in config.deployment.roles }}"

steps:
  validate_subscription:
    ansible_playbook:
      name: playbooks/validate_subscription.yml
      vars:
        foo_product: "{{ variant.name }}" 
        foo_version: "{{ variant.version }}"
  pre_installation_tasks:

  bootstrap_bar:
    


  
        







stages:
  bootstrap_bar:
    description: Bootstraping Bar
    steps:
    - bootstrap_bar:
    when: "{{ 'bar' in config.deployment.roles }}"
  configure:
    description: Configuring Foo
    steps:
    - config_repos:
      when: "{{ not config.deployment.skip_repo_config | default(false) }}"
    - configure_foo_component_a:
    - configure_foo_component_b:


steps:

  gather_host_facts:
    ...
  generate_certificate:
    ...
  verify_ntp_configured:
    ansible_adhoc:
      task: command
      args: rpm -q ntpd
  configure_foo_component_b:
    ansible_playbook:
      name: playbooks/component_b.yml
  configure_component_a_repos:
    ansible_role:
      name: configure_repos
      params:
        repos:
        - foo_common
        - foo_component_a
  configure_component_b_repos:
    ansible_role:
      name: configure_repos
      params:
        repos:
        - foo_common
        - foo_component_b

  
  






```
