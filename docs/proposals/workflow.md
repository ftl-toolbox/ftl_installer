#Workflow Config Design Proposal
The Workflow Config is a yaml formatted file that is used to generate a
product installer. 

Example of generating installer from workflow configuration:
```
ftl_installer -w foo_workflow.yml -o foo_installer
```

## Workflow Config Primitives
The Workflow Config defines the following Primitives:

###Providers (Provider Engine)
TODO: Better define the Provider Engine

Providers defines the configuration for the Provider Engine. This includes how host
information is gathered for use by the generated installer. The following scenarios
should be handled by provider engine:
- Gathering of host information:
  - End User provided through prompts or unattended config (static_host - _needs complete example_)
  - Dynamic Inventory through built-in inventories (aws, gce, etc)
  - Specification of custom dynamic inventories
    - This should be able to be linked to a built-in provider in addition
      to a custom provider plugin
  - Mapping of groups provided by dynamic inventories to installer groups - _needs example_
  - Setting of additional attributes on hosts - _needs example_
- Provisioning of hosts:
  - Specification of built-in provisioner plugins
  - Specification of custom provisioner plugins

Example providers definition:
```
providers:
  aws: # built-in provider
    provisioners:
    - ec2_host
    - ec2_cloud_formation
    - my_custom_ec2_provisioner
    inventory
      path: inventory/aws/my_ec2.py
      env:
        EC2_INI_PATH: inventory/aws/hosts/ec2.ini
  my_custom_provider:
    provisioners:
    - alpha_provisioner
    - beta_provisioner
  gce:
  static_host:
  
```

TODO: Describe what a provider plugin is
TODO: define and describe the built-in provider plugins
TODO: define and describe the provider plugin interface

TODO: Describe what a provisioner plugin is
TODO: define and describe the built-in provisioner plugins
TODO: define and describe the provisioner plugin interface

TODO: define how inventories interact with the provider plugins
      and/or provisioner plugins      

###Config (Config Engine)

TODO: better define the Config Engine

Config defines the configuration file for the generated installer.
The purpose of the config section is to:
- define the current configuration file version (`version`)
- define the default config file location (`default_path`). If not set, the default
  config file should be: `~/.config/<generated_installer_name>`.
- define configuration migrations for previous configuration file
  versions through `config_migration` plugins
- define configuration file validation through `config_validator` plugins

In order to allow for flexibility on when to apply migrations and particular
validations, we borrow conditional primitive `when` from ansible along with the
inline use of jinja2 templates.

The migrations section is evaluated only when reading in an existing configuration file.
If not running in unattended mode, once all migrations have been completed successfully
the resulting config file should be persisted to disk.

The validators section is evaluated after executing migrations, prior to persisting
configs to disk, or through the invocation of the `config_save` task by the workflow engine. 

TODO: Define the ftl-managed config schema.

TODO: Define explicit generated installer config schema definition.

TODO: Define implicit generated installer config schema definition
      (schema determined through items in the workflow configuration)

TODO: Provide example for user-provided config file

TODO: Provide a way to specify which version of the ftl-managed schema
      is used by each version of the generated installer config version.

TODO: Describe behavior for ftl-managed config schema migrations and validations

TODO: Describe built-in validators. This should include validation that the
      generated installer config schema does not conflict with ftl-managed config
      schema, circular reference detection, etc
      
TODO: define the interface and variables available throught the config engine execution
      lifecycle

Example config definition:
```
config:
  version: 2.2
  default_path: ~/.config/ftl_installer_config.yml
  migrations:
  - migrate_v1_to_v2:
    when: "{{ config.version | version_compare('lt', 2.0) }}"
  - migrate_v2_to_v2_1:
    when: "{{ config.version | version_compare('lt', 2.1) }}"
  - migrate_v2_1_to_v2_2:
    when: "{{ config.version | version_compare('lt', 2.2) }}"
  validators:
  - upstream:
    when: "{{ config.variant == 'foo_upstream' }}"
  - enterprise:
    when: "{{ config.variant == 'foo_enterprise' }}"
  - containerized:
    when: "{{ config.deployment.containerized | default(false) }}"
  - valid_ha_config:
    when: "{{ config.deployment.ha | default(false) }}"
```

###Variants (Variant Engine)

TODO: define the purpose of the Variant Engine and the schema of the variant 
Example variants definition:
```
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
```

###Workflows (Workflow Engine)

TODO: Describe the workflow engine and the configuration schema.

Example workflows definition:
```
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
```

###Stages

TODO: Define stages, their use and their configuration

Example stages definition:
```
stages:
  - gather_install_hosts:
      description: Gather Hosts
      steps:
      - provision: # built in step plugin to auto-provision hosts this will
                   # also add config related to the config for what providers
                   # where selected
      - inventory: 
          # built-in step plugin that will invoke dynamic inventory based on
          # config file, or generate from defined hosts, also needs to handle
          # host/role mapping
          path: 
  - pre_install_check:
      description: Pre Installation Check
      steps:
      - validate_subscription:
        when: "{{ not skip_subscription | bool }}"
      - pre_installation_tasks:
  - bootstrap_bar:
      steps:
      - install_bar
      - configure_bar
    when: "{{ 'bar' in config.deployment.roles }}"

    
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
    
```

###Steps

TODO: define steps, their use and their configuration

TODO:
- define actions to do on failure of steps, stages and workflows

Example steps definition:
```
steps:
  validate_subscription:
    ansible_playbook:
      name: playbooks/validate_subscription.yml
      vars:
        foo_product: "{{ variant.name }}" 
        foo_version: "{{ variant.version }}"
  pre_installation_tasks:
    ...
  bootstrap_bar:
    ansible_playbook:
      name: playbooks/install_bar.yml
      vars:
        ...
  configure_bar:
    ansible_role:
      name: foo_bar
      vars:
        ...



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


##Plugins


###config migration plugin
###config validator plugin
###provider plugin
###step plugins

built-in step plugins:
- inventory:
  - invoke built in dynamic inventory based on value of `cloud.providers` if
    `cloud.providers` is unset, defaults to `config.allowed_cloud_providers`
    ```
    - inventory:
    ```