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






```
