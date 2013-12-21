{% set project = pillar['project_name'] + "-" + pillar['environment'] %}
{% set root_dir = "/var/www/" + project + "/" %}

{% macro build_path(root, name) -%}
  {{ root }}{%- if not root.endswith('/') -%}/{%- endif -%}{{ name }}
{%- endmacro %}

{% macro path_from_root(name) -%}
  {{ build_path(root_dir, name) }}
{%- endmacro %}

{% set log_dir = path_from_root('log') %}
{% set run_dir = path_from_root('run') %}
{% set server_socket = build_path(root_dir, project + '.sock') %}
{% set source_dir = path_from_root('source') %}
{% set services_dir = path_from_root('services') %}
{% set venv_dir = path_from_root('env') %}
