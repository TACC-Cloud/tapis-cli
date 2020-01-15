
log(){
    mesg "INFO" $@
}

die() {
    mesg "ERROR" $@
    exit 1
}

mesg() {
    lvl=$1
    shift
    message=$@
    echo "[$lvl] $(utc_date) - $message"
}

utc_date() {
    echo $(date -u +"%Y-%m-%dT%H:%M:%SZ")
}

#### BEGIN SCRIPT LOGIC
set -x

# Write shell code here to invoke the application

