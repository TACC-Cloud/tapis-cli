
container_exec() {




    # [TODO] Check for existence of docker or singularity executable
    # [TODO] Enable honoring a DEBUG global
    # [TODO] Figure out how to accept more optional arguments (env-file, etc)
    # [TODO] Better error handling and reporting
    # [TODO] Handle "urllib2.URLError: <urlopen error [Errno -3] Temporary failure in name resolution>"

    local CONTAINER_IMAGE=$1
    shift
    local COMMAND=$1
    shift
    local PARAMS=$@

    # A litte logging to help with the edge cases
    if [ ! -z "$DEBUG" ];
    then
        local _PID=$$
        echo $CONTAINER_IMAGE > .container_exec.${_PID}.log
        echo $COMMAND >> .container_exec.${_PID}.log
        echo $PARAMS >> .container_exec.${_PID}.log
        echo $PWD >> .container_exec.${_PID}.log
        echo $(ls $PWD) >> .container_exec.${_PID}.log
        env > .container_exec.${_PID}.env
    fi

    # Detect container engine
    local _CONTAINER_APP=$(which singularity)

    echo $_CONTAINER_APP

    if [ ! -z "${_CONTAINER_APP}" ]
    then
        _CONTAINER_ENGINE="singularity"
    else
        _CONTAINER_APP=$(which docker)
        if [ ! -z "${_CONTAINER_APP}" ]
        then
            echo "setting to docker"
            _CONTAINER_ENGINE="docker"
        fi
    fi

    if [ -z "$SINGULARITY_PULLFOLDER" ];
    then
        if [ ! -z "$STOCKYARD" ];
        then
            SINGULARITY_PULLFOLDER="${STOCKYARD}/.singularity"
        else
            SINGULARITY_PULLFOLDER="$HOME/.singularity"
        fi
    fi

    if [ -z "$SINGULARITY_CACHEDIR" ];
    then
        if [ ! -z "$STOCKYARD" ];
        then
            SINGULARITY_CACHEDIR="${STOCKYARD}/.singularity"
        else
            SINGULARITY_CACHEDIR="$HOME/.singularity"
        fi
    fi

    local _UID=$(id -u)
    local _GID=$(id -g)
    chmod g+rwxs .
    umask 002 .


    if [[ "$_CONTAINER_ENGINE" == "docker" ]]; then
        echo "hey, it's docker"
        #local OPTS="--network=none --cpus=1.0000 --memory=1G --device-read-iops=/dev/sda:1500 --device-read-iops=/dev/sda:1500"

        # Set group ownership on all files making them readable by archive process
        OPTS="$OPTS --rm  --user=0:${_GID} -v $PWD:/home:rw -w /home"
        if [ ! -z "$ENVFILE" ]
        then
            OPTS="$OPTS --env-file ${ENVFILE}"
        fi
        if [ ! -z "$DEBUG" ];
        then
            set -x
        fi
        echo ${PARAMS}
        docker pull ${CONTAINER_IMAGE}
        docker run $OPTS ${CONTAINER_IMAGE} ${COMMAND} ${PARAMS} &&
        docker run $OPTS bash chmod -R g+rw .
        if [ ! -z "$DEBUG" ];
        then
            set +x
        fi
    elif [[ "$_CONTAINER_ENGINE" == "singularity" ]];
    then
        # [TODO] Detect and deal if an .img has been passed it (rare)
        singularity exec docker://${CONTAINER_IMAGE} ${COMMAND} ${PARAMS}
    else
        echo "_CONTAINER_ENGINE needs to be 'docker' or 'singularity' [$_CONTAINER_ENGINE]"
    fi

}


count_logical_cores() {

    local _count_cores=4
    local _uname=$(uname)

    if [ "$_uname" == "Darwin" ]
    then
        _count_cores=$(sysctl -n hw.logicalcpu)
    elif [ "$_uname" == "Linux" ]
    then
        _count_cores=$(grep -c processor /proc/cpuinfo)
    fi

    echo $_count_cores

}

auto_maxthreads() {

    local hwcore=$(count_logical_cores)
    hwcore=$((hwcore-1))
    echo $hwcore

}