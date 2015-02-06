environment: production

domain: traffic-stops.codefordurham.com

repo:
  url: git@github.com:copelco/NC-Traffic-Stops.git
  branch: dev

postgresql_config: # from pgtune
  work_mem: 22MB
  maintenance_work_mem: 224MB
  shared_buffers: 896MB
  effective_cache_size: 2560MB
  checkpoint_segments: 16

# Addtional public environment variables to set for the project
env:
  FOO: BAR
