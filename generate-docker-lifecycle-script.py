#!/usr/bin/env python

import os
import stat

TEMPLATE="""
#!/usr/bin/env bash

current_container=$(docker ps | grep {container_name}  | awk '{unfortunate_awk_replacement}')
operation=$1
shift

if [ "$operation" = "start"  ]; then
  if [[ -z $current_container  ]]; then
    docker run {docker_run_args} {container_name} "$@"
  else
    echo "A(n) {container_name} container is already running with id: $current_container"
  fi
elif [ "$operation" = "stop"  ]; then
  if [[ -z $current_container  ]]; then
    echo "There is no {container_name} container running"
  else
    docker stop $current_container
    docker rm $current_container
  fi
elif [ "$operation" = "status"  ]; then
  if [[ -z $current_container  ]]; then
    echo "There is no {container_name} container running"
  else
    echo "A(n) {container_name} container is running with id: $current_container"
  fi
elif [ "$operation" = "restart" ]; then
  if [[ -z $current_container  ]]; then
    docker run {docker_run_args} {container_name} "$@"
  else
    docker stop $current_container
    docker rm $current_container
    docker run {docker_run_args} {container_name} "$@"
  fi
elif [ "$operation" = "logs" ]; then
  if [[ -z $current_container ]]; then
    echo "There is no {container_name} container running"
  else
    docker logs --tail=10 -f $current_container
  fi
fi
""".strip()

if __name__ == "__main__":
    template_data = {
        "container_name" : raw_input("please input the container name: "),
        "docker_run_args": raw_input("please input any docker run args: "),
        "unfortunate_awk_replacement": "{print $1}"
    }
    script = TEMPLATE.format(**template_data)
    script_name = template_data["container_name"].split('/')[-1] + '.sh'
    try:
        f = open(script_name, 'w')
        f.write(script)
        os.chmod(script_name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print "Your new docker lifecycle script is at: " + script_name
    except:
        raise
    finally:
        f.close()

