#!/usr/bin/env python

import os
import stat

TEMPLATE = """
#!/usr/bin/env bash

current_container=$(docker ps | grep {container_name}  | awk '{{print $1}}')
operation=$1
shift
args=$@

NO_CONTAINER="There is no {container_name} container running"
CONTAINER_RUNNING="A(n) {container_name} container is running with id: $current_container"

start_container(){{
  echo -n "Started docker container: "
  docker run {docker_run_args} {container_name} {entry_point_args} "$@"
}}

stop_container(){{
  echo -n "Stopped docker container: "
  docker stop $current_container
}}

remove_container(){{
  echo -n "Removing docker container: "
  docker rm $current_container
}}

case "$operation" in
  start)
    if [[ -z $current_container  ]]; then
      start_container $args
    else
      echo $CONTAINER_RUNNING
    fi
    ;;
  stop)
    if [[ -z $current_container  ]]; then
      echo $NO_CONTAINER
    else
        stop_container
        remove_container
    fi
    ;;
  status)
    if [[ -z $current_container  ]]; then
      echo echo $NO_CONTAINER
    else
      echo $CONTAINER_RUNNING
    fi
    ;;
  restart)
    if [[ -z $current_container  ]]; then
      echo echo $NO_CONTAINER
      start_container $args
    else
      stop_container
      remove_container
      start_container $args
    fi
    ;;
  logs)
    if [[ -z $current_container ]]; then
      echo $NO_CONTAINER
    else
      docker logs --tail=10 -f $current_container
    fi
    ;;
  *)
    echo $"Usage: $0 {operations} <args to pass into container>"
    exit 1
    ;;
esac

""".lstrip()

OPERATIONS = [
    "start",
    "stop",
    "status",
    "restart",
    "logs"
]

if __name__ == "__main__":
    template_data = {
        "container_name": raw_input("please input the container name: ").strip(),
        "docker_run_args": raw_input("please input any docker run args (optional): ").strip(),
        "entry_point_args": raw_input("please input any args to send to the docker entry point (optional): ").strip(),
        "operations": "|".join(OPERATIONS).join(["{", "}"])
    }
    template_data["short_name"] = template_data["container_name"].split("/")[-1]
    script_name = template_data["short_name"] + ".sh"
    script = TEMPLATE.format(**template_data)
    try:
        f = open(script_name, "w")
        f.write(script)
        os.chmod(script_name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print "Your new docker lifecycle script is at: " + script_name
    except:
        raise
    finally:
        f.close()
